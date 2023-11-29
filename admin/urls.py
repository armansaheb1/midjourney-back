from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('users', views.Users.as_view(), name="user"),
    path('transactions', views.Transactions.as_view(), name="user"),
    path('imagines', views.Imagines.as_view(), name="user"),
    path('charge', views.Charge.as_view(), name="user"),
    path('plans', views.Plans.as_view(), name="user"),
    path('plans/<ids>', views.Plans.as_view(), name="Plans"),
    path('bonus', views.Bonuss.as_view(), name="user"),
    path('bonus/<ids>', views.Bonuss.as_view(), name="bonus"),
    path('faceswap', views.FaceSwap.as_view(), name="user"),
]
