from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from . import views

base_router = routers.SimpleRouter()

# base_router.register(r'', views.PurshaselViewSet)


urlpatterns = [
    path('find/', views.SalesDetailView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
