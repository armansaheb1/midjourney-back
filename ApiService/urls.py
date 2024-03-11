from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('support',  views.Gpt.as_view()),
    path('support/<ids>/<page>',  views.Gpt.as_view()),
    path('support/<ids>',  views.Gpt.as_view()),
    path('like',  views.Like.as_view()),
    path('admin/my-supports',  views.MyGPT.as_view()),
]