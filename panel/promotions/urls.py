from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views

urlpatterns = [
   
    path(r'search/<int:pk>/', views.PromotionDetailView.as_view()),
    url(r'', views.PromottionCreateView.as_view()), 
  
]
