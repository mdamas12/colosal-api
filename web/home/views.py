from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.conf import settings
from django.db.models import Q
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
         
        categories = Category.objects.all().order_by('?')[:12] 
        serializer = CategoriesDetailSerializer(categories, many=True)    
        return Response(serializer.data)
        
class ProductsFeaturedView(APIView):
      
    def get(self, request, format=None):
        """Listar Productos destacados"""
         
        products = Product.objects.all().order_by('?')[:12]
        serializer = ProductListSearchSerializer(products, many=True)      
        return Response(serializer.data)

class ProductSearch(APIView):
      
    def get(self, request, search, format=None):
        """busqueda de productos"""
        products = Product.objects.filter(Q(name__icontains = search))
        paginator = CustomPaginator()
        serializer = paginator.generate_response(products, ProductListSearchSerializer, request)       
        return serializer

class PromotionsFeaturedView(APIView):
      
    def get(self, request, format=None):
        """Listar Productos destacados"""
         
        promotions = Promotion.objects.all().order_by('?')[:12]
        serializer = PromotionFullSerializer(promotions, many=True)      
        return Response(serializer.data)
   
class CategoryDetailView(APIView):
      
    def get(self, request, pk, format=None):
          
        """Buscar venta y detalle"""
        category = Category.objects.get(id=pk)
        serializer = CategoriesDetailSerializer(category, many=False)
        return Response(serializer.data)
    

class ProductsOrderbyView(APIView):
      
    def get(self, request, pk, format=None):
        """Listar Productos ordenados por"""
        if pk==1:     
            products = Product.objects.all().order_by('name')
            paginator = CustomPaginator()
            serializer = paginator.generate_response(products, ProductListSearchSerializer, request)       
            return serializer
        elif pk==2:
            products = Product.objects.all().order_by('category')
            paginator = CustomPaginator()
            serializer = paginator.generate_response(products, ProductListSearchSerializer, request)       
            return serializer
        else:
            return Response({"error": "el orden ingresado no es valido"}, status=status.HTTP_400_BAD_REQUEST)

