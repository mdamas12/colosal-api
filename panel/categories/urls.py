from django.conf.urls import url
from django.urls import path
from django.urls import include
from .views import *
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

base_router = routers.SimpleRouter()
base_router.register(r'', CategoryViewSet)

urlpatterns = [
    path('detail/<int:pk>/', CategoryDetailView.as_view()),
    url('save', CategoryCreateView.as_view()),
    url('list-all', listAllCategories.as_view()),
    url('prueba-login', pruebaLogin.as_view()),
    url(r'', include(base_router.urls)),
]
