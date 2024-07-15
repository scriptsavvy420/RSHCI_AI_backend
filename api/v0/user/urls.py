from django.urls import re_path, path
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter

from .views.user import *
from .views.wallet import *
from .views.wallet_detail import *

router = DefaultRouter()

urlpatterns = [
    re_path(r'users$', GetUserAPI.as_view()),
    re_path(r'wallets$', WalletAPI.as_view()),
    path('wallets/<int:wallet_id>/', WalletDetailAPI.as_view()),
    path('wallets/update/<int:wallet_id>', WalletDetailAPI.as_view()),
]