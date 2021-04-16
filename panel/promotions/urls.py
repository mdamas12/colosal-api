from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views


urlpatterns = [
   
    path(r'search/<int:pk>/', views.PromotionDetailView.as_view()),
    path(r'modification/<int:pk>/', views.PromotionModificationView.as_view()), 
    path(r'products-modification/<int:pk>/', views.PromotionDetailModificationView.as_view()),
    path(r'delete-detail/<int:pk>/', views.DeleteDetailPromotion.as_view()),
    path(r'products/', views.PromotionDetailCreateView.as_view()),
    url(r'', views.PromottionCreateView.as_view()), 
   
    
]

