from django.db import models
from django.conf import settings
from ledger.models import Contact


class Group(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    members = models.ManyToManyField(Contact)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BillSpliting(models.Model):

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    bill_name = models.CharField(max_length=100)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    member = models.ForeignKey(Contact, on_delete=models.CASCADE)

    split_amount = models.DecimalField(max_digits=10, decimal_places=2)

    paid_by = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name="paid_bills",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('received', 'Received')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)