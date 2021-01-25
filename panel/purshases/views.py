
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view

from .serializers import *
from panel.products.serializers import ProductMixinSerializer

from .models import *
from panel.products.models import *

#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class PurshaselViewSet(
    mixins.ListModelMixin,
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
    serializer_product = ProductMixinSerializer

    def get(self,request,format=None):
        Products = PurchaseDetail.objects.all()
        serializer = PurshaseDetailSerializer(Products, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
       # print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = request.data['product']
            product = Product()
            product = Product.objects.get(id=id)
            product.quantity = product.quantity + request.data['purchase_Received']
            product.save()
           
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
class ListPurshaseDetail(APIView):
    serializer_class = PurshaseDetailSerializer

    def get(self, request, pk, format=None):

        Products = PurchaseDetail.objects.filter(purchase=pk)
        serializer = PurshaseDetailSerializer(Products, many=True)
        return Response(serializer.data)

class changesPurshaseDetail(APIView):
    """ 
     1-) Get: busca un producto segun su id
     2-) put: Actualiza/edita el producto de una compra
     3-) delete: elimina el producto de una compra 
     """

    serializer_class = PurshaseDetailSerializer

    def get(self, request, pk, format=None):

        Products = PurchaseDetail.objects.filter(id=pk)
        serializer = PurshaseDetailSerializer(Products, many=True)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Products = PurchaseDetail.objects.get(id=pk)
        print(Products.purchase_Received)
        before_quantity = Products.purchase_Received
        serializer = PurshaseDetailSerializer(Products, data=request.data)
        if serializer.is_valid():
            product = Product()
            product = Product.objects.get(id=request.data['product'])
            product.quantity = product.quantity - before_quantity + request.data['purchase_Received'
            #product.quantity = 
            product.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
    def delete(self, request, pk, format=None):
        Products = PurchaseDetail.objects.get(id=pk)
        Products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)