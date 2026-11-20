from django.http import HttpResponse
from functools import wraps
from django.shortcuts import redirect
from django.utils import timezone


def subscription_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        user = request.user
        today = timezone.now().date()

        # If subscription expired
        if user.subscription_end and today > user.subscription_end:
            user.subscription_active = False
            user.save()

        # If inactive redirect
        if not user.subscription_active:
            return redirect('subscribe')

        return view_func(request, *args, **kwargs)

    return wrapper

def individual_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'individual':
            return HttpResponse("Unauthorized - Individual access only")
        return view_func(request, *args, **kwargs)

    return wrapper


def shop_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'shop':
            return HttpResponse("Unauthorized - Shop access only")
        return view_func(request, *args, **kwargs)

    return wrapper
