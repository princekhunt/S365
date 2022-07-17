from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.verify_me, name='verify-me'),
    path('auth/redirect', views.router, name='router'),
    path('auth/callback', views.callback, name='callback'),
    path('auth/callback_token', views.callback_token, name='callback_token'),
    path('auth/logout', views.logout, name='logout')
]
