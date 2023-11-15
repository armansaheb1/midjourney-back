from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('users', views.Users.as_view(), name="user"),
    path('transactions', views.Transactions.as_view(), name="user"),
    path('imagines', views.Imagines.as_view(), name="user"),
    path('charge', views.Charge.as_view(), name="user"),
]
