from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

from .views import *

base_router = routers.SimpleRouter()

#base_router.register(r'', views.PurshaselViewSet)


urlpatterns = [
    #path('category-search/<int:pk>/', views.CategoryDetailView.as_view()),
    path(r'products-search/<str:search>/', ProductSearch.as_view()),
    url(r'categories-featured/', categoriesFeaturedView.as_view()),
    url(r'products-featured/', ProductsFeaturedView.as_view()),
    url(r'promotions-featured/', PromotionsFeaturedView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
