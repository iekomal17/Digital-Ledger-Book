from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .services import activate_subscription
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from .forms import ProfileUpdateForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def subscribe_view(request):
    if request.GET.get('success') == 'true':
        activate_subscription(request.user)

        if request.user.role == 'individual':
            return redirect('ledger_dashboard')
        elif request.user.role == 'shop':
            return redirect('shop_dashboard')

    return render(request, 'accounts/subscribe.html')


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})
