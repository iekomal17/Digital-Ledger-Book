from django.db import models
from django.conf import settings


# -------------------- CUSTOMER MODEL --------------------

from django.db import models
from django.conf import settings


class Customer(models.Model):

    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('retailer', 'Retailer'),
    )

    shop = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    customer_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='customer'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# -------------------- TRANSACTION MODEL --------------------

class Transaction(models.Model):

    TRANSACTION_CHOICES = [
        ('gave', 'You Gave'),
        ('got', 'You Got'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']   # newest entry first

    def __str__(self):
        return f"{self.customer.name} - ₹{self.amount} ({self.transaction_type})"