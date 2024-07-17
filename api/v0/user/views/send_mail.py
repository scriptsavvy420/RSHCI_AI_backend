# api/v0/user/views/send_mail.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import json


class ContactMailAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data)
            name = data.get("contactName")
            email = data.get("contactEmail")
            phone = data.get("contactPhone")
            disires = data.get("contactDisires")
            description = data.get("contactText")
            company_email = "liweichen798@gmail.com"

            mail_subject = f"Arrived message from {name}"
            message = render_to_string(
                "contact_mail.html",
                {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "disires": disires,
                    "description": description,
                },
            )

            email_obj = EmailMessage(mail_subject, message, to=[company_email])
            email_obj.content_subtype = "html"
            email_obj.send()
            return Response(
                {
                    "data": True,
                    "msg": "Message has been sent.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as error:
            print(error)
            return Response({"error": str(error)}, status=400)
