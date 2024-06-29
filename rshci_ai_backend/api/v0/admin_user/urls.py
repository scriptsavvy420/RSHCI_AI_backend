from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter


from .views import *

router = DefaultRouter()

urlpatterns = [
    re_path(r'^',include(router.urls)),
    re_path(r'^users/$', GetUsersAPI.as_view(), name='get_users'),
    re_path(r'^users/create$', CreateUserAPI.as_view(), name='create_user'),
    re_path(r'^users/(?P<user_id>[0-9]+)$', UpdateUserAPI.as_view(), name='update_user'),
]