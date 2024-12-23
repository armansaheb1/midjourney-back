from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('imagine-result/<ids>', views.ImagineResult.as_view(), name="ImagineResult"),
    path('imagine-result2/<ids>', views.ImagineResult2.as_view(), name="ImagineResult"),
    path('faceswap-result/<ids>', views.FaceSwapResult.as_view(), name="faceswapResult"),
    path('imagine', views.Imagine.as_view(), name="imagine"),
    path('imagine2', views.Imagine2.as_view(), name="imagine2"),
    path('gpt', views.Gpt.as_view(), name="imagine"),
    path('gpt/<ids>', views.Gpt.as_view(), name="imagine"),
    path('my-gpt', views.MyGPT.as_view(), name="user"),
    path('faceswap', views.FaceSwap.as_view(), name="faceswap"),
    path('faceswap/<ids>', views.FaceSwap.as_view(), name="faceswap"),
    path('user', views.GetUser.as_view(), name="user"),
    path('my-imagines/<page>', views.MyImagine.as_view(), name="user"),
    path('my-faceswap', views.MyFaceSwap.as_view(), name="user"),
    path('charge', views.Charge.as_view(), name="user"),
    path('request', views.send_request.as_view(), name="user"),
    path('verify', views.verify.as_view(), name="user"),
    path('image', views.Images.as_view(), name="user"),
    path('button', views.Button.as_view(), name="user"),
    path('button2', views.Button2.as_view(), name="user"),
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
    path('sms-verify/<phone>', views.SMSVerify.as_view(), name="user"),
    path('sms-verify/<phone>', views.SMSVerifyUser.as_view(), name="user"),
    path('check-verify', views.CheckVerify.as_view(), name="user"),
    path('workout', views.Workout.as_view(), name="user"),
    # path('workout2', views.Workout2.as_view(), name="user"),
    path('links', views.Links.as_view(), name="user"),
]
