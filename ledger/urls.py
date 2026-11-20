from django.urls import path
from .views import dashboard_view, add_transaction,add_contact,contact_detail,contact_report

urlpatterns = [
    path('dashboard/', dashboard_view, name='ledger_dashboard'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('add-contact/', add_contact, name='add_contact'),
    path('contact/<int:id>/', contact_detail, name='contact_detail'),
    path('contact/<int:id>/report/', contact_report, name='contact_report'),
]
