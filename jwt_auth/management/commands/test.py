from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.conf import settings
from django.db import *

class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        management.call_command(f"dbrestore", f"-itemp_cms_wavemaster_db_backup_2024-04-10.sql --noinput")