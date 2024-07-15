from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import *
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password

from db_schema.models import *
from db_schema.serializers import *
from utils.permissions import *
from validations.auth.user import *
from utils.generate import *


# Create your views here.
class WalletDetailAPI(APIView):
    def get(self, request, wallet_id):
        try:
            wallet = Wallet.objects.get(id=wallet_id)
            wallet_serializer = WalletSerializer(wallet)
            return Response({"data": wallet_serializer.data}, status=200)
        except Wallet.DoesNotExist:
            return Response({"msg": "Wallet not found."}, status=404)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)

    def post(self, request, wallet_id):
        try:
            data = request.data
            coin_amount = data.get("coin_amount")

            # Ensure wallet exists
            wallet = Wallet.objects.get(id=wallet_id)

            with transaction.atomic():
                wallet.coin_amount = coin_amount
                wallet.save()

            wallet_serializer = WalletSerializer(wallet)

            return Response(
                {
                    "data": wallet_serializer.data,
                    "msg": "Wallet coin amount has been updated.",
                },
                status=200,
            )
        except Wallet.DoesNotExist:
            return Response({"msg": "Wallet not found."}, status=404)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
