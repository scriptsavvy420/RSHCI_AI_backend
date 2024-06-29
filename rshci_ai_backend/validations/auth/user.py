
from django.db.models import *
from jwt_auth.models import *
import re


def validate_create_user(request):
    data = dict(request.data)
    email = data.get("email", "")
    name = data.get("name","")
    phone = data.get("phone", "")
    password = data.get("password","")
    role = data.get("role", 0)
    is_allowed = data.get("is_allowed", False)

    try:
        errors = {}

        if email == "":
            errors["email"] = "Please enter your email."

        if email != "" and User.objects.filter(email=email).exists():
            errors["email"] = "This email has already been registered."

        if name == "":
            errors["name"] = "Please enter your name."

        if password == "":
            errors["password"] = "Please enter your password."

        if Role.objects.filter(id=role).exists() == False:
            errors["role"] = "This permission does not exist."


        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "email": email,
            "name":name,
            "phone": phone,
            "password":password,
            "role": role,
            "is_allowed": is_allowed
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    
def validate_update_user(request, user_id):
    data = dict(request.data)
    email = data.get("email", "")
    name = data.get("name","")
    password = data.get("password","")
    phone = data.get("phone", "")
    role = data.get("role", "")
    is_allowed = data.get("is_allowed", False)

    try:
        errors = {}

        if email == "":
            errors["email"] = "Please enter your email."

        if email != "" and User.objects.filter(Q(email=email), ~Q(id=user_id)).exists():
            errors["email"] = "This email has already been registered."

        if name == "":
            errors["name"] = "Please enter your name."

        if password == "":
            errors["password"] = "Please enter your password."

        if Role.objects.filter(id=role).exists() == False:
            errors["role"] = "This permission does not exist."


        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "email": email,
            "name":name,
            "phone": phone,
            "role": role,
            "is_allowed": is_allowed
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    