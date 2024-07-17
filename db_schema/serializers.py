from rest_framework import serializers
from django_mailbox.models import Message, Mailbox, MessageAttachment
from django.db.models import *
import re
from .models import *
from jwt_auth.serializers import *

from rest_framework import serializers
from .models import *

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'price']
