from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from . import views

base_router = routers.SimpleRouter()

#base_router.register(r'', views.PurshaselViewSet)


urlpatterns = [
    path('detail/<int:pk>/', views.SalesDetailView.as_view()),
    path('list-status/<int:pk>/', views.SaleListStatusView.as_view()),
    path('product-sale/<int:pk>/', views.ProductSale.as_view()),
    path(r'customer/<str:search>/', views.CustomerSearch.as_view()),
    path('sale-panel/', views.SalespanelView.as_view()),
    url(r'', views.SaleCreateView.as_view()),
   
    #url(r'^detail/$', views.PurshaseDetailCreate.as_view()),
    
]
urlpatterns = format_suffix_patterns(urlpatterns)
