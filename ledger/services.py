from django.db.models import Sum
from .models import Transaction


def calculate_balance(user):
    transactions = Transaction.objects.filter(user=user)

    total_given = transactions.filter(
        transaction_type='give'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_taken = transactions.filter(
        transaction_type='take'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return total_given, total_taken, total_given - total_taken


def get_user_summary(user):
    transactions = Transaction.objects.filter(user=user)

    total_given = transactions.filter(
        transaction_type='give'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_taken = transactions.filter(
        transaction_type='take'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    balance = total_given - total_taken

    recent_transactions = transactions.order_by('-date')[:5]

    return {
        'total_given': total_given,
        'total_taken': total_taken,
        'balance': balance,
        'recent_transactions': recent_transactions
    }
