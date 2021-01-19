from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import *
#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class ProviderViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Provider.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProviderMixinSerializer


class PurshaselViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Purchase.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = PurchaseMixinSerializer


class PurshaseDetailCreate(APIView):
    serializer_class = PurshaseDetailSerializer

    def post(self, request, format=None):
        serializer = PurshaseDetailSerializer(data=request.data)
        if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       

class PurshaseDetailist(APIView):
    serializer_class = PurshaseDetailSerializer

    def get(self, request, pk):
        Products = PurchaseDetail.objects.all(purshase=pk)
        serializer = PurshaseDetailSerializer(Products, many=True)
        return Response(serializer.data)


 


   
    
