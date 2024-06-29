from django.contrib.auth.hashers import check_password, make_password
from jwt_auth.models import *
import re

def validate_password_change(request):
    data = dict(request.data)
    password = data.get("password", "")
    new_password = data.get("new_password", "")
    confirm_password = data.get("confirm_password", "")
    
    try:
        errors = {}

        if password == "":
            errors["password"] = "This field is required."

        if password != "" and check_password(password, request.user.password) == False:
            errors["password"] = "Passwords do not match."

        if new_password == "":
            errors["new_password"] = "This field is required."

        if confirm_password == "":
            errors["confirm_password"] = "This field is required."

        if password != "" and new_password != "" and new_password != confirm_password:
            errors["confirm_password"] = "New passwords do not match."

        # check contains 8 characters, 1 uppercase, 1 lowercase, 1 number
        if not re.search("[0-9]", new_password):
            errors["new_password"] = "Passwords must contain numbers."

        if not re.search("[a-zA-Z]", new_password):
            errors["new_password"] = "Passwords must contain letters."

        if not re.search("[!@#$%^&*()_+-=]", new_password):
            errors["new_password"] = "Passwords must contain symbols."

        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "password": password,
            "new_password": new_password,
            "confirm_password": confirm_password
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    

def validate_forgot_password(request):
    data = dict(request.data)
    email = data.get("email", "")
    
    try:
        errors = {}

        if email == "":
            errors["email"] = "This field is required."

        if email != "" and User.objects.filter(email=email).count() == 0:
            errors["email"] = "The email address you entered is not registered."
        
        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "email": email
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    

def validate_reset_password(request):
    data = dict(request.data)
    token = data.get("token", "")
    new_password = data.get("new_password", "")
    confirm_password = data.get("confirm_password", "")
    
    try:
        errors = {}

        if token == "":
            errors["token"] = "This field is required."

        if new_password == "":
            errors["new_password"] = "This field is required."

        if confirm_password == "":
            errors["confirm_password"] = "This field is required."

        if new_password != "" and new_password != confirm_password:
            errors["confirm_password"] = "New passwords do not match."

        # check contains 8 characters, 1 uppercase, 1 lowercase, 1 number
        if new_password != "" and (len(new_password) < 8 or new_password.isalpha() or new_password.isnumeric()):
            errors["new_password"] = "Password must contain 8 or more alphanumeric characters."

        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "token": token,
            "new_password": new_password,
            "confirm_password": confirm_password
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    
def validate_register_user(request):
    data = dict(request.data)
    name = data.get("name","")
    email = data.get("email","")
    phone = data.get("phone","")
    password = data.get("password","")
    confirm_password = data.get("confirm_password","")

    try:
        errors = {}

        if name == "":
            errors["name"] = "This field is required."

        if email == "":
            errors["email"] = "This field is required."
        
        if phone == "":
            errors["phone"] = "This field is required"

        if password == "":
            errors["password"] = "This field is required."

        if confirm_password == "":
            errors["confirm_password"] = "This field is required."

        if password != "" and password != confirm_password:
            errors["confirm_password"] = "New passwords do not match."

        
        status = 422 if len(errors) > 0 else 200
        
        clean_data = {
            "name":name,
            "email":email,
            "phone":phone,
            "password":password
        }

        return status, errors, clean_data

    except Exception as e:
        print(str(e))

        return {}, 500, {}