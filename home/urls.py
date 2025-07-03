from django.contrib import admin
from django.urls import path
from . import views
from django.shortcuts import render
urlpatterns = [
    path('', views.index, name='home'),
    path('test-static/', views.test_static_view, name='test_static'),
]


