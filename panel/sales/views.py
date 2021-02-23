from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.conf import settings

from panel.customers.models import *
from panel.payments.models import *
from panel.products.models import *
from .models import *

from .serializers import *
from  panel.shoppingcart.serializers import *
#from .repositories import *


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

class SaleCreateView(APIView):
     
    
    def get(self, request, format=None):
        """Listar Todas las ventas"""
        
        sales = Sale.objects.all()
        paginator = CustomPaginator()
        serializer = paginator.generate_response(sales, SaleViewchSerializer, request)
        return serializer    
        

    def post(self,request,format=None):
        """Guardar un Producto"""
        
        data = request.data
        sale_detail_array = []
        parcial_amount = 0
        #if "purchase" in data and "products" in data:
        if "sale" in data:
            
            data_sale = data["sale"]
            
            try:
                 Customer.objects.get(id=data_sale["customer"])
            except Customer.DoesNotExist:
                return Response("El cliente no existe", status=status.HTTP_400_BAD_REQUEST)
            
            customer = Customer.objects.get(id=data_sale["customer"])

            try:
                 Bank.objects.get(id=data_sale["bank"])
            except Bank.DoesNotExist:
                return Response("los datos de pago no existen", status=status.HTTP_400_BAD_REQUEST)
            
            bank = Bank.objects.get(id=data_sale["bank"])

            serializer_sale = SaleSerializer(data=data_sale)
   
            if serializer_sale.is_valid():

                sale = Sale()
                sale.description = data_sale["description"]
                sale.customer = customer
                sale.payment_type = data_sale["payment_type"]
                sale.bank = bank
                sale.coin = data_sale["coin"]
                sale.status = "POR VALIDAR"
                sale.save()

     

                #registro de detalle de venta 
    
                if "sale_detail" in data:
                    
                    data_sale_detail = data["sale_detail"]                   
                    #data_saledetail = []
                    for item_detail in data_sale_detail:
                        
                        try:    
                             Shoppingcart.objects.get(id=item_detail["shoppingcart"])
                        except Shoppingcart.DoesNotExist:
                            return Response("el producto no esta en carrito de compra", status=status.HTTP_400_BAD_REQUEST)
                        
                        shoppingcart = Shoppingcart.objects.get(id=item_detail["shoppingcart"])     
                        product = Product.objects.get(id = shoppingcart.product.id)
                
                            
                        sale_detail = SaleDetail()
                        sale_detail.sale = sale
                        sale_detail.product = product
                        sale_detail.sale_price = product.price
                        sale_detail.quantity_sold = shoppingcart.quantity
                        sale_detail.amount = shoppingcart.quantity * product.price
                        sale_detail.status = "POR ENTREGAR"
                        sale_detail.save()
                        
                        sale_detail_array.append(SaleDetailViewSerializer(sale_detail).data) 
                        #sale_detail_array.append(sale_detail)                           
                        parcial_amount = parcial_amount +  (shoppingcart.quantity * product.price)
                        product.quantity = product.quantity - shoppingcart.quantity
                        product.save()

                        shoppingcart.status = "PROCESADO"
                        shoppingcart.save()
                        #shoppingcart.delete()
 
                    sale.amount = parcial_amount
                    sale.save()
                    
                data_end = {
                    "Sale": SaleViewchSerializer(sale).data,
                    "Detail": sale_detail_array
                }

                return Response(data_end)
            else:
                
                return Response(serializer_sale.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe suministrar informacion", status=status.HTTP_400_BAD_REQUEST)

class SalesDetailView(APIView):
      
    def get(self, request, pk, format=None):
          
        """Buscar venta y detalle"""
        sale = Sale.objects.get(id=pk)
        serializer = SaleViewchSerializer(sale, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):

        data = request.data

        if "sale" in data: 
            data_sale = data["sale"]
            
            try:
                 Sale.objects.get(id=pk)
            except Sale.DoesNotExist:
                return Response("La venta no existe", status=status.HTTP_400_BAD_REQUEST)
            
            sale = Sale.objects.get(id=pk)
            sale.status = data_sale["status"]
            sale.save()
            return Response(SaleViewchSerializer(sale).data)

    def delete(self, request, pk, format=None):

        
        try:
            Sale.objects.get(id=pk)
        except Sale.DoesNotExist:
            return Response("La venta no existe", status=status.HTTP_400_BAD_REQUEST)
            
        sale = Sale.objects.get(id=pk)
        sale.delete()
        return Response("La venta ha sido eliminada")

class ProductSale(APIView):
      
    
    def put(self, request, pk, format=None):

        data = request.data

        if "sale_detail" in data: 
            data_sale_detail = data["sale_detail"]
            
            try:
                 SaleDetail.objects.get(id=pk)
            except SaleDetail.DoesNotExist:
                return Response("el producto no existe", status=status.HTTP_400_BAD_REQUEST)
            
            Prdoduct_sale = SaleDetail.objects.get(id=pk)
            Prdoduct_sale.status = data_sale_detail["status"]
            Prdoduct_sale.save()
            return Response("Status del Producto actualizado")


class SalespanelView(APIView):

      def post(self,request,format=None):
        """Guardar un Producto"""
        
        data = request.data
        sale_detail_array = []
        parcial_amount = 0
        #if "purchase" in data and "products" in data:
        if "sale" in data:
            
            data_sale = data["sale"]
            
            try:
                 Customer.objects.get(id=data_sale["customer"])
            except Customer.DoesNotExist:
                return Response("El cliente no existe", status=status.HTTP_400_BAD_REQUEST)
            
            customer = Customer.objects.get(id=data_sale["customer"])

            try:
                 Bank.objects.get(id=data_sale["bank"])
            except Bank.DoesNotExist:
                return Response("los datos de pago no existen", status=status.HTTP_400_BAD_REQUEST)
            
            bank = Bank.objects.get(id=data_sale["bank"])

            serializer_sale = SaleSerializer(data=data_sale)
   
            if serializer_sale.is_valid():

                sale = Sale()
                sale.description = data_sale["description"]
                sale.customer = customer
                sale.payment_type = data_sale["payment_type"]
                sale.bank = bank
                sale.coin = data_sale["coin"]
                sale.status = "POR VALIDAR"
                sale.save()

     

                #registro de detalle de venta 
    
                if "sale_detail" in data:
                    
                    data_sale_detail = data["sale_detail"]                   
                    #data_saledetail = []
                    for item_detail in data_sale_detail:
                        
                        try:    
                             Product.objects.get(id=item_detail["product"])
                        except Product.DoesNotExist:
                            return Response("el producto no existe", status=status.HTTP_400_BAD_REQUEST)    
                  
                        product = Product.objects.get(id = item_detail["product"])
                
                            
                        sale_detail = SaleDetail()
                        sale_detail.sale = sale
                        sale_detail.product = product
                        sale_detail.sale_price = item_detail["price"]
                        sale_detail.quantity_sold = item_detail["quantity"]
                        sale_detail.amount = item_detail["quantity"] * item_detail["price"]
                        sale_detail.status = "POR ENTREGAR"
                        sale_detail.save()
                        
                        sale_detail_array.append(SaleDetailViewSerializer(sale_detail).data) 
                        #sale_detail_array.append(sale_detail)                           
                        parcial_amount = parcial_amount +  (item_detail["quantity"]  * item_detail["price"])
                        product.quantity = product.quantity - item_detail["quantity"]
                        product.save()
 
                    sale.amount = parcial_amount
                    sale.save()
                    
                data_end = {
                    "Sale": SaleViewchSerializer(sale).data,
                    "Detail": sale_detail_array
                }

                return Response(data_end)
            else:
                
                return Response(serializer_sale.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe suministrar informacion", status=status.HTTP_400_BAD_REQUEST)


