from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from db_schema.models import * 
from db_schema.serializers import PriceSerializer

class PriceAPI(APIView):
    def get(self, request):
        try:
            price = Price.objects.first()
            if not price:
                return Response({"msg": "Price not set."}, status=status.HTTP_200_OK)
            price_serializer = PriceSerializer(price)
            return Response({"data": price_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            price_value = data.get("price")

            if not price_value:
                return Response({"msg": "Price value is required."}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                price, created = Price.objects.update_or_create(
                    id=1,  # Assuming there's only one price record to manage
                    defaults={"price": price_value}
                )

            price_serializer = PriceSerializer(price)
            return Response(
                {
                    "data": price_serializer.data,
                    "msg": "Price has been set." if created else "Price has been updated.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
