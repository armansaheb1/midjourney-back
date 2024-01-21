from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('imagine-result/<ids>', views.ImagineResult.as_view(), name="ImagineResult"),
    path('imagine', views.Imagine.as_view(), name="imagine"),
    path('gpt', views.Gpt.as_view(), name="imagine"),
    path('gpt/<ids>', views.Gpt.as_view(), name="imagine"),
    path('my-gpt', views.MyGPT.as_view(), name="user"),
    path('faceswap', views.FaceSwap.as_view(), name="faceswap"),
    path('faceswap/<ids>', views.FaceSwap.as_view(), name="faceswap"),
    path('user', views.GetUser.as_view(), name="user"),
    path('my-imagines', views.MyImagine.as_view(), name="user"),
    path('my-faceswap', views.MyFaceSwap.as_view(), name="user"),
    path('charge', views.Charge.as_view(), name="user"),
    path('request', views.send_request.as_view(), name="user"),
    path('verify', views.verify.as_view(), name="user"),
    path('image', views.Images.as_view(), name="user"),
    path('button', views.Button.as_view(), name="user"),
    path('plans', views.Plans.as_view(), name="Plans"),
    path('check-bonus/<token>', views.CheckBonus.as_view(), name="CheckBonus"),
    path('get-bonus', views.GetBonus.as_view(), name="get-bonus"),
    path('dj-rest-auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('image-details', views.ImageDetails.as_view(), name="user"),
    path('add-details', views.AddDetails.as_view(), name="user"),
    path('mimic', views.Mimics.as_view(), name="user"),
    path('parameters', views.Parameters.as_view(), name="user"),
    path('sizes', views.Sizes.as_view(), name="user"),
    path('posts', views.Posts.as_view(), name="user"),
    path('posts/<id>', views.Posts.as_view(), name="user"),
    path('support', views.Support.as_view(), name="user"),
]
