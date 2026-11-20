from django.urls import path
from . import views

urlpatterns = [
    path('ledger/report/', views.ledger_report_view, name='ledger_report_view'),
    path('ledger/pdf/', views.ledger_pdf, name='ledger_pdf'),

    path('shop/report/', views.shop_report_view, name='shop_report_view'),
    path('shop/pdf/', views.shop_pdf, name='shop_pdf'),

    path('group/pdf/', views.group_pdf, name='group_pdf'),
]