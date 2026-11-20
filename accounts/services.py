from datetime import date, timedelta


def activate_subscription(user):
    user.subscription_active = True
    user.subscription_start = date.today()
    user.subscription_end = date.today() + timedelta(days=365)
    user.save()
