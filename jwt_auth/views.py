from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.db import transaction
from utils.permissions import *


# Generate token and generate reset url
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator


from validations.auth.password import *
from validations.auth.user import *
# from mail.auth.password import *
import datetime



# Create your views here.


class AccountActivateAPI(APIView):

    def get(self, request):
        token = request.query_params.get('token', "")

        try:
            if RegisterToken.objects.filter(token=token).exists() == False:
                return Response("invalid token", status=404)
            
            m_item = RegisterToken.objects.get(token=token)
            m_user = User.objects.get(id=m_item.user_id)
            rslt = default_token_generator.check_token(m_user, token)
            
            if rslt:
                if m_item.expire_at > datetime.datetime.now():
                    return Response("success", status=200)
                else:
                    return Response("token has expired", status=400)
            else:
                return Response("invalid token", status=404)
            
        except Exception as e:
            print(str(e))
            return Response("invalid token", status=404)
        
    def post(self, request):
        data = dict(request.data)
        token = data.get("token", "")

        try:
            if RegisterToken.objects.filter(token=token).exists() == False:
                return Response({"msg": "Invalid token."}, status=400)
            
            m_item = RegisterToken.objects.get(token=token)
            m_user = User.objects.get(id=m_item.user.id)

            if default_token_generator.check_token(m_user, token) == False or m_item.expire_at < datetime.datetime.now():
                return Response({"msg": "Invalid token."}, status=400)

            errors, status, clean_data = validate_reset_password(request)
            if status != 200:
                return Response({"errors": errors}, status=status)

            with transaction.atomic():
                m_user.password = make_password(clean_data["new_password"])
                m_user.is_active = True
                m_user.save()
                m_item.delete()

            return Response({"msg": "Account activated."}, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
        

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            errors, status, clean_data = validate_password_change(request)
            if status != 200:
                return Response({"errors": errors}, status=status)
            
            with transaction.atomic():
                request.user.password = make_password(clean_data["new_password"])
                request.user.save()

            return Response({"msg": "Password has been changed."}, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)


class PasswordForgotView(APIView):
    
    def post(self, request):
        
        try:
            errors, status, clean_data = validate_forgot_password(request)
            if status != 200:
                return Response({"errors": errors}, status=status)    
            
            # with transaction.atomic():
                
                # send_mail(request, clean_data["email"])


            return Response({"msg": "Password reset email has been sent."}, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
        


class PasswordResetView(APIView):

    def get(self, request):
        token = request.query_params.get('token', "")

        try:
            if ResetToken.objects.filter(token=token).exists() == False:
                return Response("invalid token", status=404)
            
            m_item = ResetToken.objects.get(token=token)
            m_user = User.objects.get(id=m_item.user_id)
            rslt = default_token_generator.check_token(m_user, token)
            
            if rslt:
                if m_item.expire_at > datetime.datetime.now():
                    return Response("success", status=200)
                else:
                    return Response("token has expired", status=400)
            else:
                return Response("invalid token", status=404)
            
        except Exception as e:
            print(str(e))
            return Response("invalid token", status=404)
        
    def post(self, request):
        data = dict(request.data)
        token = data.get("token", "")

        try:
            if ResetToken.objects.filter(token=token).exists() == False:
                return Response({"msg": "Invalid token."}, status=400)
            
            m_item = ResetToken.objects.get(token=token)
            m_user = User.objects.get(id=m_item.user.id)

            if default_token_generator.check_token(m_user, token) == False or m_item.expire_at < datetime.datetime.now():
                return Response({"msg": "Invalid token."}, status=400)

            errors, status, clean_data = validate_reset_password(request)
            if status != 200:
                return Response({"errors": errors}, status=status)

            with transaction.atomic():
                m_user.password = make_password(clean_data["new_password"])
                m_user.save()
                m_item.delete()

            return Response({"msg": "Password has been changed."}, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)

class GetMyAccountInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"me": serializer.data})
    

class GetUsersAPI(APIView):
    permission_classes = []
    
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        pageSize = int(request.GET.get('pageSize', 10))

        try:
            m_data = User.objects.filter(Q(user_info__name__contains=keyword) | Q(email__contains=keyword), Q(permission="customer"), Q(is_active=True)).order_by('id')
            serializer = UserSerializer(m_data[pageSize * (page - 1):pageSize * page], many=True)

            return Response({
                "data": serializer.data,
                "total": m_data.count()
            })
        except Exception as e:
            print(str(e))
            return Response(str(e), status=500)
        

class CreateUserAPI(APIView):
    
    def post(self, request):
        
        try:
            errors, status, clean_data = validate_create_user(request)
            print(clean_data)
            
            if status != 200:
                return Response({"errors": errors}, status=status)
            
            with transaction.atomic():
                user_info = UserInfo.objects.create(
                    name = clean_data["name"],
                    phone=clean_data["phone"],
                    
                )
                print(user_info)
                print(True)
                user = User.objects.create(
                    email=clean_data["email"],
                    username = clean_data['email'],
                    password=make_password(clean_data["password"]),
                    user_info=user_info,
                    permission="member",
                    is_active=True,
                    is_allowed=clean_data['is_allowed']
                )

                # ※登録後、担当にメールが送信されます。メール内のURLからアカウントの有効化を行ってください。
                # send_mail(request, clean_data["email"])
                
                serializer = UserSerializer(user)

                return Response({
                    "data": serializer.data,
                    "msg": "Has registered."
                }, status=200)
        except Exception as e:
            print(str(e))
            return Response(str(e), status=500)
        

class UpdateUserAPI(APIView):
    permission_classes = []
    
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            serializer = UserFlatSerializer(user.user_info)

            return Response(serializer.data, status=200)

        except Exception as e:
            print(str(e))
            return Response("Can't find", status=404)
        
    def patch(self, request, user_id):
        try:
            errors, status, clean_data = validate_update_user(request, user_id)
            
            if status != 200:
                return Response({"errors": errors}, status=status)
            
            with transaction.atomic():
                user = User.objects.get(id=user_id)
                user.email = clean_data["email"]
                user.is_allowed = clean_data["is_allowed"]
                user.user_info.name = clean_data["name"]
                
                user.user_info.phone = clean_data["phone"]
                user.user_info.role = Role.objects.get(id=clean_data["role"])
                user.save()
                user.user_info.save()
                
                serializer = UserSerializer(user)

                return Response({
                    "data": serializer.data,
                    "msg": "Has been updated."
                }, status=200)

        except Exception as e:
            print(str(e))
            return Response(str(e), status=500)
        
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()

            return Response({
                "msg": "削除しました。"
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response(str(e), status=500)