from django.urls import path, re_path
from . import views

urlpatterns = [
    path("Accounts/user_signup",views.User_SignUp.as_view(),name='SignUp'),
    path("Accounts/user_login",views.User_Login.as_view(),name='Login'),
]