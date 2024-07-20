from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from db_schema.models import Wallet, User
from db_schema.serializers import WalletSerializer, UserInfoSerializer
from utils.generate import generate_address, generate_secretcode


# Create your views here.
class WalletAPI(APIView):
    def get(self, request):
        keyword = request.GET.get("keyword", "")
        page = int(request.GET.get("page", 1))
        pageSize = int(request.GET.get("pageSize", 10))

        try:
            m_data = User.objects.filter().order_by("id")
            serializer = UserInfoSerializer(
                m_data[pageSize * (page - 1) : pageSize * page], many=True
            )
            print(serializer)
            return Response({"data": serializer.data, "total": m_data.count()})
        except Exception as e:
            print(str(e))
            return Response(str(e), status=500)

    def post(self, request):
        try:
            data = request.data
            user_id = data.get("user_id")

            # Ensure user exists
            user = User.objects.get(id=user_id)

            address = generate_address()
            secretcode = generate_secretcode()

            with transaction.atomic():
                wallet = Wallet.objects.create(
                    owner=user, secretcode=secretcode, address=address, coin_amount=Decimal('0')
                )

                # Update the user_info with the created wallet
                user_info = user.user_info
                user_info.wallet_info = wallet
                user.permission = "customer"
                user.save()
                user_info.save()
            company_email = "RHCI AI LLC"
            wallet_serializer = WalletSerializer(wallet)
            
            mail_subject = f"Arrived message from {company_email}"
            message = render_to_string(
                "wallet_mail.html",
                {
                    "walletaddress": address,
                    "secretcode": secretcode,
                },
            )

            email_obj = EmailMessage(mail_subject, message, to=[user.email])
            email_obj.content_subtype = "html"
            email_obj.send()

            return Response(
                {
                    "data": wallet_serializer.data,
                    "msg": "Wallet has been created and user_info updated.",
                },
                status=200,
            )
        except User.DoesNotExist:
            return Response({"msg": "User not found."}, status=404)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)


