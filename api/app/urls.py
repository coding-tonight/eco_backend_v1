from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view()),
    path('register/', views.Register.as_view()),
    path('forget/password/', views.ForgetPassword.as_view()),
    path('verify/otp/', views.VerifyOTP.as_view()),
    path('verify/change/password/', views.ChangePassword.as_view())
]