from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Transaction
from .form import CustomerForm, TransactionForm
from accounts.decorators import subscription_required, shop_required
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Transaction, Customer
from django.db.models import Q
from notifications.utils import shop_transaction_message, whatsapp_link, email_link

# ---------------- DASHBOARD ----------------


@login_required
@subscription_required
@shop_required
def dashboard(request):

    search = request.GET.get('search')

    customers = Customer.objects.filter(shop=request.user)

    # SEARCH FILTER
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search)
        )

    total_receive = Decimal('0.00')
    total_pay = Decimal('0.00')

    customer_data = []

    for customer in customers:
        transactions = customer.transactions.all()

        gave = Decimal('0.00')
        got = Decimal('0.00')

        for t in transactions:
            if t.transaction_type == 'gave':
                gave += t.amount
            else:
                got += t.amount

        balance = gave - got

        if balance > 0:
            total_receive += balance
        else:
            total_pay += abs(balance)

        customer_data.append({
            'customer': customer,
            'balance': balance,
            'abs_balance': abs(balance)
        })

    context = {
        'customer_data': customer_data,
        'total_customers': customers.count(),
        'total_receive': total_receive,
        'total_pay': total_pay,
        'net_balance': total_receive - total_pay,
    }

    return render(request, 'shop/dashboard.html', context)
# ---------------- ADD CUSTOMER ----------------

@login_required
def add_customer(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.shop = request.user
            customer.save()
            return redirect('shop_dashboard')
    else:
        form = CustomerForm()

    return render(request, 'shop/add_customer.html', {'form': form})


# ---------------- VIEW CUSTOMERS ----------------

@login_required
def view_customers(request):
    customers = Customer.objects.filter(shop=request.user)

    return render(request, 'shop/view_customers.html', {
        'customers': customers
    })


# ---------------- CUSTOMER LEDGER ----------------

@login_required
def customer_ledger(request, pk):

    customer = get_object_or_404(Customer, pk=pk, shop=request.user)

    transactions = customer.transactions.all()

    total_gave = Decimal('0.00')
    total_got = Decimal('0.00')

    for t in transactions:
        if t.transaction_type == 'gave':
            total_gave += t.amount
        else:
            total_got += t.amount

    balance = total_gave - total_got
    abs_balance = abs(balance)

    # Get last transaction for notification message
    last_transaction = transactions.last()

    wa_link = None
    mail_link = None

    if last_transaction:

        message = shop_transaction_message(
            request.user,
            customer,
            last_transaction.amount,
            last_transaction.transaction_type
        )

        wa_link = whatsapp_link(customer.phone, message)
        mail_link = None

    context = {
        'customer': customer,
        'transactions': transactions,
        'total_gave': total_gave,
        'total_got': total_got,
        'balance': balance,
        'abs_balance': abs_balance,
        'wa_link': wa_link,
        'mail_link': mail_link
    }

    return render(request, 'shop/customer_ledger.html', context)

# ---------------- ADD TRANSACTION ----------------

@login_required
def add_transaction(request, pk):

    customer = get_object_or_404(Customer, pk=pk, shop=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.customer = customer
            transaction.save()
            return redirect('customer_ledger', pk=customer.id)
    else:
        form = TransactionForm()

    return render(request, 'shop/add_transaction.html', {
        'form': form,
        'customer': customer
    })




@login_required
def customer_report(request, id):

    customer = Customer.objects.get(id=id, shop=request.user)

    transactions = Transaction.objects.filter(
        customer=customer
    ).order_by('-date')

    template = get_template('reports/customer_pdf.html')

    context = {
        'customer': customer,
        'transactions': transactions,
        'user': request.user
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{customer.name}_ledger.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response