from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_updates_list, name='news_updates_list'),
    path('create_news_update/', views.create_news_update, name='create_news_update'),
    path('delete_news_update/<int:pk>/', views.delete_news_update, name='delete_news_update'),
    path('update_details/<int:pk>/', views.news_update_details, name='news_update_details'),
]