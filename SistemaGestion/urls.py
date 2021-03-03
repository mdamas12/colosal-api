"""SistemaGestion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
<<<<<<< HEAD
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Sistema-bodegon')

urlpatterns = [
=======
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from users.views import UserViewSet

schema_view = get_swagger_view(title='API Sistema-bodegon')


base_router = routers.SimpleRouter()
base_router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(base_router.urls)),
    url(r'^auth/', include('rest_auth.urls')),
    url(r'^auth/registration/', include('rest_auth.registration.urls')),
>>>>>>> 175aeecf54c5ecc9e477fa458cf712a4d870df30
    url(r'^docs/', schema_view),
    url(r'^panel/', include('panel.urls')),
    path('admin/', admin.site.urls),
]
