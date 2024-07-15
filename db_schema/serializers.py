from rest_framework import serializers
from django_mailbox.models import Message, Mailbox, MessageAttachment
from django.db.models import *
import re
from .models import *
from jwt_auth.serializers import *
