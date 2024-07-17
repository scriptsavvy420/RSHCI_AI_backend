from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction

from db_schema.models import Wallet
from db_schema.serializers import WalletSerializer


class CoinTransferAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            sender_wallet_id = data.get("sender_wallet_id")
            receiver_address = data.get("receiver_address")
            amount = Decimal(data.get("amount"))
            secret_code = data.get("secret_code")

            sender_wallet = Wallet.objects.get(id=sender_wallet_id)

            # Uncomment and adjust the secret code check as necessary
            # if not check_password(secret_code, sender_wallet.secretcode):
            #     return Response({"msg": "Invalid secret code."}, status=403)

            if sender_wallet.coin_amount < amount:
                return Response({"msg": "Insufficient balance."}, status=400)

            receiver_wallet = Wallet.objects.get(address=receiver_address)

            with transaction.atomic():
                sender_wallet.coin_amount -= amount
                receiver_wallet.coin_amount += amount

                sender_wallet.save()
                receiver_wallet.save()

            # Serialize the updated sender wallet info
            sender_wallet_serializer = WalletSerializer(sender_wallet)

            return Response({
                "msg": "Transfer successful.",
                "sender_wallet": sender_wallet_serializer.data
            }, status=200)
        except Wallet.DoesNotExist:
            return Response({"msg": "Wallet not found."}, status=404)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
