from django.urls import re_path, path
from rest_framework_simplejwt import views
from rest_framework.routers import DefaultRouter

from .views.user import *
from .views.wallet import WalletAPI
from .views.wallet_detail import *
from .views.price import *
from .views.transfer_coin import *
from .views.send_mail import *

router = DefaultRouter()

urlpatterns = [
    re_path(r"users$", GetUserAPI.as_view()),
    re_path(r"wallets$", WalletAPI.as_view()),
    re_path(r"wallet/send_coin$", CoinTransferAPI.as_view()),
    path("wallets/<int:wallet_id>/", WalletDetailAPI.as_view()),
    path("wallets/update/<int:wallet_id>", WalletDetailAPI.as_view()),
    path("price/", PriceAPI.as_view(), name="price-api"),
    path("send_mail", ContactMailAPI.as_view(), name="send-mail-api"),
]
