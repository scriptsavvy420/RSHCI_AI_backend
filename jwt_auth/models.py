from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

class Role(models.Model):
    role_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Role Management"

class Wallet(models.Model):
    address = models.CharField(max_length=150,unique=True)
    secretcode = models.CharField(max_length=150,default='password')
    owner = models.CharField(max_length=100,default='')
    coin_amount = models.DecimalField(max_digits=7,decimal_places=2,default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.address
    
    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallet Management"

class UserInfo(models.Model):
    name = models.CharField(max_length=50,blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)

    invest_amount = models.CharField(max_length=50,blank=True,null=True)
    invest_period = models.CharField(max_length=50,blank=True,null=True)
    wallet_info = models.ForeignKey(Wallet, on_delete=models.CASCADE, blank=True, null=True )

    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "UserInfo"
        verbose_name_plural = "UserInfo Management"


class User(AbstractUser):
    user_id = models.CharField(max_length=50, null=True, blank=True)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, blank=True, null=True)

    
    email = models.EmailField(_('email address'), unique=True)

    REQUIRED_FIELDS=[]
    USERNAME_FIELD = 'email'

    PERMISSION_CHOICES = [
        ("customer", 'Customer'),
        ("owner", 'Owner'),
        ("super", 'Super'),
    ]

    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES, default="customer")
    is_allowed = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User Management"

class RegisterToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    expire_at = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    expire_at = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
        verbose_name_plural = "Email Management"
