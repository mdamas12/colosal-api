from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from panel.purchases.views import *
from . import views

base_router = routers.SimpleRouter()

#base_router.register(r'', views.PurshaselViewSet)


urlpatterns = [
    #url(r'^$', include(base_router.urls)),
    url(r'list', views.PurchaseListView.as_view()),
    url(r'', views.PurchaseCreateView.as_view()),
    #url(r'^detail/$', views.PurshaseDetailCreate.as_view()),
    #url(r'^detail/<int:pk>/$', views.ListPurshaseDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
