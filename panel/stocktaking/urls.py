from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from panel.stocktaking.views import ProviderViewSet,PurshaselViewSet,PurshaseDetailCreate,PurshaseDetailist
from . import views

base_router = routers.SimpleRouter()
base_router.register(r'providers', views.ProviderViewSet)
base_router.register(r'purchases', views.PurshaselViewSet)


urlpatterns = [
    url(r'', include(base_router.urls)),
    url(r'purshase-detail/', views.PurshaseDetailCreate.as_view()),
    url(r'purshase-detail/<int:pk>/', views.PurshaseDetailist.as_view()),
]
