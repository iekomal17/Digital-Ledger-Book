from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Contact, Transaction
from .services import calculate_balance
from django.shortcuts import render
from .services import get_user_summary
from .form import ContactForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import subscription_required, individual_required
from .form import TransactionForm
from django.db.models import Q
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from notifications.utils import individual_transaction_message, whatsapp_link, email_link


@login_required
def add_transaction(request):
    if request.method == "POST":
        contact_id = request.POST.get("contact")
        amount = request.POST.get("amount")
        transaction_type = request.POST.get("transaction_type")
        date = request.POST.get("date")

        # 🔐 SECURITY CHECK HERE
        contact = get_object_or_404(Contact, id=contact_id)

        if contact.user != request.user:
            return HttpResponse("Unauthorized")

        Transaction.objects.create(
            user=request.user,
            contact=contact,
            amount=amount,
            transaction_type=transaction_type,
            date=date
        )

        return redirect('home_view')

    contacts = Contact.objects.filter(user=request.user)

    return render(request, 'ledger/add_transaction.html', {
        'contacts': contacts
    })


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)

    return render(request, 'ledger/transaction_list.html', {
        'transactions': transactions
    })


# @login_required
# def dashboard_view(request):
#     print("Logged in user:", request.user)
#
#     summary = get_user_summary(request.user)
#     return render(request, 'ledger/dashboard.html', summary)


@login_required
@subscription_required
@individual_required
def dashboard_view(request):

    summary = get_user_summary(request.user)

    search = request.GET.get('search')

    contacts = Contact.objects.filter(user=request.user)

    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search)
        )

    summary['contacts'] = contacts

    return render(request, 'ledger/dashboard.html', summary)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('ledger_dashboard')

    else:
        form = TransactionForm(user=request.user)

    return render(request, 'ledger/add_transaction.html', {'form': form})


@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('ledger_dashboard')

    else:
        form = ContactForm()

    return render(request, 'ledger/add_contact.html', {'form': form})


@login_required
def contact_detail(request, id):

    contact = Contact.objects.get(id=id, user=request.user)

    transactions = Transaction.objects.filter(
        user=request.user,
        contact=contact
    ).order_by('-date')

    # last transaction for message
    last_transaction = transactions.first()

    wa_link = None
    mail_link = None

    if last_transaction:
        message = individual_transaction_message(
            request.user,
            contact,
            last_transaction.amount,
            last_transaction.transaction_type
        )

        wa_link = whatsapp_link(contact.phone, message)
        mail_link = email_link(contact.email, message)

    return render(request, 'ledger/contact_detail.html', {
        'contact': contact,
        'transactions': transactions,
        'wa_link': wa_link,
        'mail_link': mail_link
    })

@login_required
def contact_report(request, id):

    contact = Contact.objects.get(id=id, user=request.user)

    transactions = Transaction.objects.filter(
        user=request.user,
        contact=contact
    ).order_by('-date')

    template = get_template('reports/contact_pdf.html')

    context = {
        'contact': contact,
        'transactions': transactions,
        'user': request.user
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{contact.name}_report.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response