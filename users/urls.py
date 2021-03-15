from django.conf.urls import url
from django.urls import include, path
from .views import *
from rest_framework import routers
from .views import *

base_router = routers.SimpleRouter()
base_router.register(r'', UserViewSet)

urlpatterns = [
    url(r'^$', include(base_router.urls)),
    path(r'register/', UserRegisterView.as_view()),
]
