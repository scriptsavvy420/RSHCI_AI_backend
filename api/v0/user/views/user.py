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



# Create your views here.
class GetUserAPI(APIView):
 def get(self, request):
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        pageSize = int(request.GET.get('pageSize', 10))

        try:
            m_data = User.objects.filter(Q(user_info__name__contains=keyword) | Q(email__contains=keyword), Q(is_active=True)).order_by('id')
            serializer = UserSerializer(m_data[pageSize * (page - 1):pageSize * page], many=True)
            print(serializer)
            return Response({
                "data": serializer.data,
                "total": m_data.count()
            })
        except Exception as e:
            print(str(e))
            return Response(str(e), status=500)