"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import re_path,include


from jwt_auth.urls import urlpatterns as auth_urls
from api.v0.user.urls import urlpatterns as v0_user_urls

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(auth_urls)),
    re_path(r'^api/v0/', include(v0_user_urls)),
]

