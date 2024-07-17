from django.db import models
import json
# Create your models here.
from jwt_auth.models import *
from django.db import models

class Price(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.price}"