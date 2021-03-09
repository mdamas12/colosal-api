from django.conf.urls import url
from django.urls import path
from django.urls import include
from .views import *
from rest_framework import routers

base_router = routers.SimpleRouter()
base_router.register(r'', CategoryViewSet)

urlpatterns = [
    path('detail/<int:pk>/', CategoryDetailView.as_view()),
    url(r'', include(base_router.urls)),
]
