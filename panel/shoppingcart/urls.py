from django.conf.urls import url
from django.urls import path
from django.urls import include
from .views import *
from rest_framework import routers

base_router = routers.SimpleRouter()
base_router.register(r'', ShoppingcartViewSet)

urlpatterns = [
    url(r'customer/', ShoppingcartCustomerView.as_view()),
    url(r'add-product/', AddProductShoppingcartView.as_view()),
    url(r'add-promotion/', AddPromotionShoppingcartView.as_view()),
    url(r'verify-product/', CustomerSearchView.as_view()), 
    url(r'verify-promotion/', SearchPromotionShoppView.as_view()),
    path(r'change/<int:pk>/', ChangeShoppingcartView.as_view()), 
    url(r'list', ShoppingcartListall.as_view()),
    url(r'', include(base_router.urls)),
]
