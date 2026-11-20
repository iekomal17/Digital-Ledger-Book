from django.shortcuts import render, redirect


def home_view(request):
    if request.user.is_authenticated:

        if request.user.role == 'individual':
            return redirect('ledger_dashboard')

        elif request.user.role == 'shop':
            return redirect('shop_dashboard')

    return render(request, 'home.html')