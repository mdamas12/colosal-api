from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.conf import settings
import random

from  panel.categories.models import *
from  panel.products.models import *
from  panel.promotions.models import *
from .models import *

from panel.categories.serializers import CategoriesDetailSerializer 
from panel.products.serializers import ProductListSearchSerializer
from panel.promotions.serializers import PromotionFullSerializer

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

class CustomPaginator(PageNumberPagination):
    page_size = 25 # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)

class categoriesFeaturedView(APIView):
      
    def get(self, request, format=None):
        """Listar Catagorias destacadas"""
         
        categories = Category.objects.all().order_by('?')[:10]
        paginator = CustomPaginator()
        serializer = paginator.generate_response(categories, CategoriesDetailSerializer, request)       
        return serializer
        
class ProductsFeaturedView(APIView):
      
    def get(self, request, format=None):
        """Listar Productos destacados"""
         
        products = Product.objects.all().order_by('?')[:10]
        paginator = CustomPaginator()
        serializer = paginator.generate_response(products, ProductListSearchSerializer, request)       
        return serializer

class PromotionsFeaturedView(APIView):
      
    def get(self, request, format=None):
        """Listar Productos destacados"""
         
        promotions = Promotion.objects.all().order_by('?')[:10]
        paginator = CustomPaginator()
        serializer = paginator.generate_response(promotions, PromotionFullSerializer, request)       
        return serializer
   
class CategoryDetailView(APIView):
      
    def get(self, request, pk, format=None):
          
        """Buscar venta y detalle"""
        category = Category.objects.get(id=pk)
        serializer = CategoriesDetailSerializer(category, many=False)
        return Response(serializer.data)
    

