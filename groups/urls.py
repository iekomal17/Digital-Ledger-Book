from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_group, name='create_group'),
    path('list/', views.group_list, name='group_list'),
    path('<int:group_id>/', views.group_detail, name='group_detail'),
    path('<int:group_id>/split/', views.split_bill, name='split_bill'),
    path('bill/received/<int:bill_id>/', views.mark_received, name='mark_received')
]