from django.conf.urls import url
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from . import views

base_router = routers.SimpleRouter()

base_router.register(r'', views.UserViewSet)

urlpatterns = [
    url(r'^find/', views.UserFindView.as_view()),
    url(r'^me/', views.UserRetrieveView.as_view()),
    url(r'^', include(base_router.urls)),
]
urlpatterns = format_suffix_patterns(urlpatterns)
