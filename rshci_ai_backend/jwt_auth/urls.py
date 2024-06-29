from django.urls import re_path
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

urlpatterns = [
    re_path(r'auth/login$', views.TokenObtainPairView.as_view()),
    re_path(r'auth/refresh$', views.TokenRefreshView.as_view()),
    
    re_path(r'auth/password/forgot$', PasswordForgotView.as_view()),
    re_path(r'auth/password/reset$', PasswordResetView.as_view()),
    re_path(r'account/password$', PasswordChangeView.as_view()),
    re_path(r'account/activate$', AccountActivateAPI.as_view()),
    re_path(r'users/$', GetUsersAPI.as_view(), name='get_users'),
    re_path(r'users/create$', CreateUserAPI.as_view(), name='create_user'),
    re_path(r'users/(?P<user_id>[0-9]+)$', UpdateUserAPI.as_view(), name='update_user'),
    re_path(r'account/activate$', AccountActivateAPI.as_view()),

    re_path(r"me$", GetMyAccountInfoView.as_view()),
]