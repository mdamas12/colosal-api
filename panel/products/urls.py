from django.conf.urls import url
from django.urls import path
from django.urls import include
from rest_framework import routers

from . import views

base_router = routers.SimpleRouter()
base_router.register(r'', views.ProductViewSet)
base_router.register(r'detail', views.ProductDetailViewSet)
base_router.register(r'gallery', views.ProductGalleryViewSet)

urlpatterns = [
   
    path(r'search/<int:pk>/', views.ProductSearchView.as_view()),
    path(r'product-detail/<int:pk>/', views.ProductDetailView.as_view()),
    url(r'', views.ProductCreateView.as_view()), 
    #url(r'', include(base_router.urls)),
    #url(r'list', ProductsListView.as_view()),
]
