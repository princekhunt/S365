from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('auth/check', views.check, name='check'),
    path('auth/check_login', views.check_login, name='check_login'),
    path('auth/check_token', views.check_token, name='check_token'),
    path('auth/logout', views.logout, name='logout'),

]
