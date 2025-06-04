from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('upload/', views.upload_gallery_image, name='upload_gallery'),
]