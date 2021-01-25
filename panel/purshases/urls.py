from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from panel.purshases.views import *
from . import views

base_router = routers.SimpleRouter()

base_router.register(r'', views.PurshaselViewSet)


urlpatterns = [
       
    path('detail/<int:pk>/', views.ListPurshaseDetail.as_view()),
    path('detail/', views.PurshaseDetailCreate.as_view()),  
    path('detail-change/<int:pk>/', views.changesPurshaseDetail.as_view()),
    url(r'', include(base_router.urls)), 
     
]
urlpatterns = format_suffix_patterns(urlpatterns)
