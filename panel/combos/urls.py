from django.conf.urls import url
from django.urls import include
from .views import *
from rest_framework import routers

base_router = routers.SimpleRouter()
base_router.register(r'', PromotionViewSet)
base_router.register(r'details', PromotionDetailViewSet)

urlpatterns = [
    url(r'', include(base_router.urls)),
]
