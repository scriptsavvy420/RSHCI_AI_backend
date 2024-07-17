from django.contrib.auth.models import AbstractUser as BaseUser
from django.db import models
from decimal import Decimal

class Email(models.Model):

    when = models.DateTimeField(null=False, auto_now_add=True)
    to = models.EmailField(null=False, blank=False,)
    subject = models.CharField(null=False, max_length=128,)
    body = models.TextField(null=False, max_length=1024,)
    ok = models.BooleanField(null=False, default=True,)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"    
