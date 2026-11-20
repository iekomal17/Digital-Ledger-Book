from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='shop_dashboard'),

    # Customer
    path('add-customer/', views.add_customer, name='add_customer'),
    path('view-customers/', views.view_customers, name='view_customers'),

    # Retailer

    path('customer/<int:pk>/', views.customer_ledger, name='customer_ledger'),
    path('customer/<int:pk>/add/', views.add_transaction, name='add_transaction'),
    path('customer/<int:id>/report/', views.customer_report, name='customer_report'),
]
