from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('create_channel/', views.create_channel, name='upload_video'),
    path('delete_channel/', views.delete_channel, name='delete_channel'),
]
