from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views


urlpatterns = [
   
    path(r'detail/<int:pk>/', views.HeaderDetailView.as_view()),
    path(r'list-web/', views.SliderWebView.as_view()),
    url(r'', views.SliderCreateView.as_view()), 
    
   
    
]

