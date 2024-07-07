from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from jwt_auth.models import *
import json



class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        try:
            user_info = UserInfo.objects.create(name='yoshidadaisuke', invest_amount = '',invest_period = '', phone='080-1234-5678')
            m_user = User.objects.create(user_info=user_info, email='yoshidadaisuke0420@gmail.com', password=make_password('password'), permission='super', is_active=True, is_superuser=True, is_staff=True)
        except Exception as e:
            print(str(e))
            raise CommandError('Failed to create super user')
