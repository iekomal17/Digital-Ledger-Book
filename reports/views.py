from django.shortcuts import render
from ledger.models import Transaction
from ledger.models import Transaction as LedgerTransaction
from shop.models import Transaction as ShopTransaction
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from groups.models import BillSpliting
from django.contrib.auth.decorators import login_required


@login_required
def ledger_pdf(request):
    customer = request.GET.get('customer')
    start = request.GET.get('start')
    end = request.GET.get('end')
    transactions = LedgerTransaction.objects.filter(user=request.user)

    if customer:
        transactions = transactions.filter(
            contact__name__icontains=customer
        )

    if start:
        transactions = transactions.filter(date__gte=start)

    if end:
        transactions = transactions.filter(date__lte=end)

    template = get_template('reports/ledger_pdf.html')
    context = {
        'transactions': transactions,
        'user': request.user
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ledger_report.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response


@login_required
def shop_pdf(request):
    customer = request.GET.get('customer')
    start = request.GET.get('start')
    end = request.GET.get('end')

    transactions = ShopTransaction.objects.filter(
        customer__shop=request.user
    )

    # Same filter as report view
    if customer:
        transactions = transactions.filter(
            customer__name__icontains=customer
        )

    if start:
        transactions = transactions.filter(date__gte=start)

    if end:
        transactions = transactions.filter(date__lte=end)

    template = get_template('reports/shop_pdf.html')
    context = {
        'transactions': transactions,
        'user': request.user
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shop_report.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response



@login_required
def group_pdf(request):

    group_id = request.GET.get('group')

    bills = BillSpliting.objects.filter(
        group_id=group_id,
        group__created_by=request.user
    )

    template = get_template('reports/group_pdf.html')

    context = {
        'bills': bills,
        'user': request.user
    }

    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="group_report.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

@login_required
def ledger_report_view(request):
    customer = request.GET.get('customer')
    start = request.GET.get('start')
    end = request.GET.get('end')

    transactions = LedgerTransaction.objects.filter(user=request.user)

    if customer:
        transactions = transactions.filter(contact__name=customer)

    if start:
        transactions = transactions.filter(date__gte=start)

    if end:
        transactions = transactions.filter(date__lte=end)

    return render(request, 'reports/ledger_report.html', {
        'transactions': transactions
    })


@login_required
def shop_report_view(request):
    customer = request.GET.get('customer')
    start = request.GET.get('start')
    end = request.GET.get('end')

    transactions = ShopTransaction.objects.filter(
        customer__shop=request.user
    )

    if customer:
        transactions = transactions.filter(
            customer__name__icontains=customer
        )

    if start:
        transactions = transactions.filter(date__gte=start)

    if end:
        transactions = transactions.filter(date__lte=end)

    return render(request, 'reports/shop_report.html', {
        'transactions': transactions
    })
