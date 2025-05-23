from django.urls import path
from . import views

urlpatterns = [
    path('updates/', views.news_updates_list, name='news_updates_list')
]