from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from panel.products.views import ProductsListView
from . import views

base_router = routers.SimpleRouter()
base_router.register(r'', views.ProductViewSet)

urlpatterns = [
    url(r'', include(base_router.urls)),
    url(r'list', ProductsListView.as_view()),
]
