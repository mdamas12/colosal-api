from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer, CategoriesDetailSerializer


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

class CategoryDetailView(APIView):
      
    def get(self, request, pk, format=None):
          
        """detalle de categoria"""
    
        category = Category.objects.get(id=pk)
        serializer = CategoriesDetailSerializer(category, many=False)
        return Response(serializer.data)