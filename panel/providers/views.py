from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.db.models import Q
from .models import *
from .serializers import *

#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class ProviderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Provider.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProviderMixinSerializer

class SupplierSearch(APIView):
      
    def get(self, request, search, format=None):
        """busqueda de productos"""
        supplier = Provider.objects.filter(Q(name__icontains = search))
        serializer = ProviderDetailSerializer(supplier, many=True)
        return Response(serializer.data)