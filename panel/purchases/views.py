
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound as NotFoundError
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

class CustomPaginator(PageNumberPagination):
    page_size = 25 # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)

class PurchaseCreateView(APIView):
    

    def post(self,request,format=None):
        """Guardar una compra"""
        data = request.data
        
        

        #if "purchase" in data and "products" in data:
        if "purchase" in data and "products" in data:

            data_purchase = data["purchase"]
          
      
            try:
                Provider.objects.get(id=data_purchase["provider"]["id"])
            except Provider.DoesNotExist:
                return Response("El proveedor no existe", status=status.HTTP_400_BAD_REQUEST)
            
            provider = Provider.objects.get(id=data_purchase["provider"]["id"])
            
            purchase = {
          
                "date" : data_purchase["date"],
                "description" : data_purchase["description"],
                "provider" : provider.id,
                "invoice" : data_purchase["invoice"],
                "coin" : data_purchase["coin"],
                "amount" : data_purchase["amount"],
               
            }

            serializer_purchase = PurchaseMixinSerializer(data=purchase)
   
            if serializer_purchase.is_valid():
                serializer_purchase.save()
                
                #registro de detalle de compra
                data_products = data["products"]
                purchases_detail_array = []
                new_purchase = Purchase.objects.latest('created')
               
                for item_product in data_products:

                    try:
                        Product.objects.get(id=item_product["product"]["id"])
                    except Product.DoesNotExist:
                        return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST)
                          
                    product = Product.objects.get(id=item_product["product"]["id"])
                    purchase_detail = {
                       "purchase" : new_purchase.id,
                       "product" : product.id,
                       "purchase_price" : item_product['purchase_price'],
                       "purchase_quantity" : item_product['purchase_quantity'],
                       "purchase_Received" : item_product['purchase_Received'],
                       "status" : item_product['status']
                    }


                    serializer_product = PurshaseDetailCreateSerializer(data=purchase_detail)
                    if serializer_product.is_valid():
                      
                        #actualizacion de la cantidad en producto
                        product = Product.objects.get(id=item_product["product"]["id"])
                        product.quantity = product.quantity + item_product['purchase_Received']
                        product.save()
                        
                        # Registro de detalle de la compra
                        serializer_product.save()

                        purchases_detail_array.append(serializer_product.data)
                       
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
     
        """
        for item in data["products"]:
            print(item)
            print("ok")
        return Response("probando ok")
        """
        #if "purchase" in data and "products" in data:
        if "purchase" in data and "products" in data:

            data_purchase = data["purchase"]

            try:
                Purchase.objects.get(id=pk)
            except Purchase.DoesNotExist:
                return Response("el id de Compra no existe", status=status.HTTP_400_BAD_REQUEST)

            purchase = Purchase.objects.get(id=pk)
            
            try:
                Provider.objects.get(id=(data_purchase["provider"]["id"]))
            except provider.DoesNotExist:
                return Response("El proveedor no existe", status=status.HTTP_400_BAD_REQUEST)
            provider = Provider.objects.get(id=(data_purchase["provider"]["id"]))

            purchase_data = {
          
                "date" : data_purchase["date"],
                "description" : data_purchase["description"],
                "provider" : provider.id,
                "invoice" : data_purchase["invoice"],
                "coin" : data_purchase["coin"],
                "amount" : data_purchase["amount"],  
            }

            serializer_purchase = PurchaseMixinSerializer(data=purchase_data)
   
            if serializer_purchase.is_valid():

                purchase = serializer_purchase.data
                purchase.save()
                return Response("todo ok")

                #registro de detalle de compra
                data_products = data["products"]
                purchases_detail_array = []
                for item_product in data_products:

                    purchase_detail = PurchaseDetail.objects.get(id=item_product["id"])
                    serializer_product = PurshaseDetailCreateSerializer(purchase_detail, data=item_product)   
                    if serializer_product.is_valid():
                        #print(item_product)
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

    def get(self, request, format=None):

        """Listar Todas Las Compras"""

        purshases = Purchase.objects.all()
        paginator = CustomPaginator()
        serializer = paginator.generate_response(purshases, ListPurshaseSerializer, request)
        return serializer  
    
    

    
