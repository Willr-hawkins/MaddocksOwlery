from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_updates_list, name='news_updates_list'),
    path('create_news_update/', views.create_news_update, name='create_news_update'),
]