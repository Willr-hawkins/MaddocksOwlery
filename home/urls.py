from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('live_feed/', views.live_feed, name='live_feed'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
]