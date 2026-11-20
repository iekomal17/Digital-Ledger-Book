from django.contrib import admin
from .models import Customer, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'address', 'customer_type', 'created_at')
    list_filter = ('shop',)
    search_fields = ('name', 'phone')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'transaction_type', 'date')
    list_filter = ('transaction_type', 'date')