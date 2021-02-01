
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

class PurchaseCreateView(APIView):
    

    def post(self,request,format=None):
        """Guardar una compra"""
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


class PurshaseDetailView(APIView):
    
    def get(self, request, pk, format=None):
        """Buscar una compra"""

        purchase = Purchase.objects.get(id=pk)
        serializer = ListPurshaseSerializer(purchase, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Actualizar una compra"""

        #purchase = Purchase.objects.get(id=pk)
        #serializer = ListPurshaseSerializer(purchase, many=False)
        #return Response("holaaaa")

        data = request.data
     

        #if "purchase" in data and "products" in data:
        if "purchase" in data and "products" in data:

            data_purchase = data["purchase"]
            try:
                purchase = Purchase.objects.get(id=pk)
            except Purchase.DoesNotExist:
                return Response("el id de Compra no existe", status=status.HTTP_400_BAD_REQUEST)
            
            try:
                provider = Provider.objects.get(id=(data_purchase["provider"]))
            except provider.DoesNotExist:
                return Response("El proveedor no existe", status=status.HTTP_400_BAD_REQUEST)

            serializer_purchase = PurchaseMixinSerializer(data=data_purchase)
   
            if serializer_purchase.is_valid():

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

                    purchase_detail = PurchaseDetail.objects.get(id=item_product["id"])
                    serializer_product = PurshaseDetailCreateSerializer(purchase_detail, data=item_product)   
                    if serializer_product.is_valid():
                        print(item_product)
                        #actualizacion de la cantidad en producto
                        product = Product.objects.get(id=item_product["product"])
                        product.quantity = product.quantity - purchase_detail.purchase_Received
                        product.quantity = product.quantity + item_product['purchase_Received']
                        product.save()
                        
                        # Registro de detalle de la compra
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

 
 
class PurchaseListView(ListAPIView):
    
    """Listar Todas Las Compras"""

    queryset = Purchase.objects.all()
    serializer_class = ListPurshaseSerializer
    pagination_class = PageNumberPagination
    
    

    
