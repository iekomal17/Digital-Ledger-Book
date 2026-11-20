from django.urls import path
from .views import register_view,subscribe_view,logout_view,profile_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

]
