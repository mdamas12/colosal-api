
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.pagination import PageNumberPagination

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

"""
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

"""

class PurchaseCreateView(APIView):

    def post(self,request,format=None):
        data = request.data
        #print(data)

        #if "purchase" in data and "products" in data:
        if "purchase" in data and "products" in data:

            data_purchase = data["purchase"]

            try:
                provider = Provider.objects.get(id=(data_purchase["provider"]))
            except provider.DoesNotExist:
                return Response("El proveedor no existe", status=status.HTTP_400_BAD_REQUEST)

            serializer_purchase = PurchaseMixinSerializer(data=data_purchase)
   
            if serializer_purchase.is_valid():

                purchase = Purchase()
                purchase.date = data_purchase["date"]
                purchase.description = data_purchase["description"]
                purchase.provider = provider
                purchase.invoice = data_purchase["invoice"]
                purchase.coin = data_purchase["coin"]
                purchase.amount = data_purchase["amount"]
                purchase.save()

                #registro de detalle de compra
                data_products = data["products"]
                purchases_detail_array = []
                for item_product in data_products:

                    serializer_product = PurshaseDetailCreateSerializer(data=item_product)
                    if serializer_product.is_valid():
                        try:
                            Product.objects.get(id=item_product["product"])
                        except Product.DoesNotExist:
                            return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST)
                       
                        #actualizacion de la cantidad en producto
                        product = Product.objects.get(id=item_product["product"])
                        product.quantity = product.quantity + item_product['purchase_Received']
                        product.save()
                        
                        # Registro de detalle de la compra
                        purchase_detail = PurchaseDetail()
                        purchase_detail.purchase = purchase
                        purchase_detail.product = product
                        purchase_detail.purchase_price = item_product['purchase_price']
                        purchase_detail.purchase_quantity = item_product['purchase_quantity']
                        purchase_detail.purchase_Received = item_product['purchase_Received']
                        purchase_detail.status = item_product['status']
                        purchase_detail.save()

                        purchases_detail_array.append(PurshaseDetailCreateSendSerializer(purchase_detail).data)
                       
                    else:
                        return Response(serializer_product.errors, status=status.HTTP_400_BAD_REQUEST)
                
                data_end = {
                    "purchase": serializer_purchase.data,
                    "detail": purchases_detail_array
                }

                return Response(data_end)
            else:
                
                return Response(serializer_purchase.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe enviar purchase y data", status=status.HTTP_400_BAD_REQUEST)
    
        #return Response(data["purchase"])

"""
class changesPurshaseDetail(APIView):
    
     1-) Get: busca un producto segun su id
     2-) put: Actualiza/edita el producto de una compra
     3-) delete: elimina el producto de una compra 
     

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
            product = Product.objects.get(id=request.data['product'])
            product.quantity = product.quantity - before_quantity + request.data['purchase_Received']
            #product.quantity = 
            product.save()
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

    
    def delete(self, request, pk, format=None):
        Products = PurchaseDetail.objects.get(id=pk)
        Products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""  
class PurchaseListView(ListAPIView):

    queryset = Purchase.objects.all()
    serializer_class = PurchaseMixinSerializer
    pagination_class = PageNumberPagination



    
