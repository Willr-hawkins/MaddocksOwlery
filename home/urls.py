from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
]