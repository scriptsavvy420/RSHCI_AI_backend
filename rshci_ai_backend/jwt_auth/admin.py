from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Role)
admin.site.register(Wallet)
admin.site.register(UserInfo)
admin.site.register(User)
admin.site.register(ResetToken)
admin.site.register(RegisterToken)
admin.site.register(Email)


