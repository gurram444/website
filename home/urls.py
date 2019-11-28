from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('home/',views.Home, name='home'),
    path('register',views.register, name='register'),
    path('login', views.login, name='login'),
    path('search/',views.search, name='search'),
]
