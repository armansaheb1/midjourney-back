from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('imagine-result/<ids>', views.ImagineResult.as_view(), name="ImagineResult"),
    path('imagine', views.Imagine.as_view(), name="imagine"),
    path('user', views.GetUser.as_view(), name="user"),
    path('my-imagines', views.MyImagine.as_view(), name="user"),
    path('charge', views.Charge.as_view(), name="user"),
    path('request', views.send_request.as_view(), name="user"),
    path('verify', views.verify, name="user"),
    path('image', views.Images.as_view(), name="user"),
    path('button', views.Button.as_view(), name="user"),
]
