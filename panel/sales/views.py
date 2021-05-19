from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.db.models import Q
from django.conf import settings

from  users.serializers import UserSerializer

from panel.payments.models import *
from panel.products.models import *
from panel.customers.models import *
from panel.shoppingcart.models import *
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
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
     
    
    def get(self, request, format=None):
        """Listar Todas las ventas"""
        user = UserSerializer(User.objects.get(email = request.user), many = False)   
        sales = Sale.objects.filter(customer = user.data["id"])
        sales = Sale.objects.all()
        paginator = CustomPaginator()
        serializer = paginator.generate_response(sales, SaleViewchSerializer, request)
        return serializer    
        

    def post(self,request,format=None):
        """Guardar Una Compra"""
        
        data = request.data
        user = UserSerializer(User.objects.get(email = request.user), many = False) 
        bank = data["bank"]

        #validar stock de cada producto a comprar:

        data_products = data["products"]
        for item in data_products:
            if item["product"]:
                product = Product.objects.get(id = item["product"]["id"])
                if item["quantity"] > product.quantity :
                    return Response("La Cantidad solicitada ya no se encuenta Disponible: "+product.name,  status=status.HTTP_400_BAD_REQUEST)
            else:
                promotion = Promotion.objects.get(id = item["promotion"]["id"])
                if item["quantity"] > promotion.quantity :
                    return Response("La Cantidad solicitada ya no se encuenta Disponible: "+promotion.name,  status=status.HTTP_400_BAD_REQUEST)
                
                promotionDetail = PromotionDetail.objects.filter(promotion = promotion.id)                            
                for detail_promotion in  promotionDetail: 
                    
                    product_det =  Product.objects.get(id = detail_promotion.product.id) 
                    if detail_promotion.quantity > product_det.quantity:
                        return Response("La cantidad de "+product_det.name+" es menor a la necesaria para la promocion", status=status.HTTP_400_BAD_REQUEST)
                    

        if len(bank) == 0:
            sale = {
                "customer" : user.data["id"],
                "payment_type" : data["payment_type"],
                "amount" : data["amount"],
                "reference" : data["reference"],
                "status" : "POR VALIDAR"
            }
        else:
            sale = {
            "customer" : user.data["id"],
            "bank" : bank["bank"]["id"],
            "payment_type" : data["payment_type"],
            "amount" : data["amount"],
            "reference" : data["reference"],
            "status" : "POR VALIDAR"
           }
  
        sale_serializer = SaleSerializer(data=sale)
    
        if sale_serializer.is_valid():
            
            sale_serializer.save()
            new_sale = SaleSerializer(Sale.objects.latest('created'),many = False).data
        
            if "products" in data:
                
                data_products = data["products"]

                for item in data_products:
                    if item["product"]:
                        
                        SaleDetail = {
                            "sale" : new_sale["id"],
                            "product" : item["product"]["id"],
                            "sale_price" : item["product"]["price"],
                            "quantity_sold" : item["quantity"],
                            "amount" : item["amount"],
                            "status" : "POR ENTREGAR",
                        }
                    else:
                        SaleDetail = {
                            "sale" : new_sale["id"],
                            "promotion" : item["promotion"]["id"],
                            "sale_price" : item["promotion"]["price"],
                            "quantity_sold" : item["quantity"],
                            "amount" : item["amount"],
                            "status" : "POR ENTREGAR",
                        }

                    SaleDetail_serializer = SaleDetailSerializer(data=SaleDetail)
                    if SaleDetail_serializer.is_valid():
                        SaleDetail_serializer.save()
                        #SaleDetail = SaleSerializer(Sale.objects.latest('created'),many = False).data

                        #Actualizar Stock en productos:
                        if item["product"]:
                            product = Product.objects.get(id = item["product"]["id"])
                            product.quantity = product.quantity - item["quantity"]
                            product.save()
                            #limpiar carrito de compra (shoppingcart): dd
                            shoppingcart = Shoppingcart.objects.get(product=item["product"]["id"],customer = user.data["id"])
                            shoppingcart.delete()
                        else:
                            
                            promotion = Promotion.objects.get(id = item["promotion"]["id"])
                            promotion.quantity = promotion.quantity - item["quantity"]
                            promotion.save()

                            promotionDetail = PromotionDetail.objects.filter(promotion = item["promotion"]["id"])
                            
                            for detail_promotion in  promotionDetail:
                                
                                product_detail =  Product.objects.get(id = detail_promotion.product.id)   
                                product_detail.quantity = product_detail.quantity - detail_promotion.quantity
                                product_detail.save()
                            #limpiar carrito de compra (shoppingcart): 
                            shoppingcart = Shoppingcart.objects.get(promotion=item["promotion"]["id"],customer = user.data["id"])
                            shoppingcart.delete()           
                    else:
                        return Response("Error al intentar Guardar productos", status=status.HTTP_400_BAD_REQUEST)
                
                return Response("Se ha registrado Tu Compra",status=status.HTTP_201_CREATED)
            else:
                return Response("No hay Productos seleccionados", status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response("Error al intentar Guardar la Compra", status=status.HTTP_400_BAD_REQUEST)
    
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
        SaleDetail.objects.filter(sale=sale).delete()
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
                 User.objects.get(id=data_sale["customer"])
            except User.DoesNotExist:
                return Response("El cliente no existe", status=status.HTTP_400_BAD_REQUEST)
            
            customer = User.objects.get(id=data_sale["customer"])

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


class CustomerSearch(APIView):
      
    def get(self, request, search, format=None):
        """busqueda de clientes"""
        customers = User.objects.filter(Q(email__icontains = search))
        serializer = UserSerializer(customers, many=True)
        return Response(serializer.data)

class SaleListStatusView(APIView):
      
    def get(self, request, pk, format=None):
          
        """Listar venta por status"""
        if pk==1:            
            sale = Sale.objects.filter(status="POR VALIDAR")
            serializer = SaleViewchSerializer(sale, many=True)
            return Response(serializer.data)
        elif pk==2:
            sale = Sale.objects.filter(status="POR ENTREGAR")
            serializer = SaleViewchSerializer(sale, many=True)
            return Response(serializer.data)
        elif pk==3:
            sale = Sale.objects.filter(status="PROCESADA")
            serializer = SaleViewchSerializer(sale, many=True)
            return Response(serializer.data)
        else:
            return Response("el Status de venta no existe", status=status.HTTP_400_BAD_REQUEST)

class SaleListStatusWeb(APIView):
    """ Listar Compras de un cliente - servicio para la web """  

    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
          
        """Listar Compras por status"""
        user = UserSerializer(User.objects.get(email = request.user), many = False)   
       
        if pk==1:            
            sale = Sale.objects.filter(status="POR VALIDAR", customer = user.data["id"])
            serializer = SaleViewchSerializer(sale, many=True)
            return Response(serializer.data)
        elif pk==2:
            sale = Sale.objects.filter(status="POR ENTREGAR",customer = user.data["id"])
            serializer = SaleViewchSerializer(sale, many=True)
            return Response(serializer.data)
        elif pk==3:
            sale = Sale.objects.filter(status="PROCESADA", customer = user.data["id"])
            serializer = SaleViewchSerializer(sale, many=True)
            return Response(serializer.data)
        else:
            return Response("el Status de venta no existe", status=status.HTTP_400_BAD_REQUEST)

class PurchaseUdateReference(APIView):
    """ Actualizar Referencia - servicio para la web """  

    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk, format=None):
        data = request.data
        print(data["reference"])
        user = UserSerializer(User.objects.get(email = request.user), many = False)
        sale = Sale.objects.get(id=pk)
        sale.reference = data["reference"]
        sale.save()
        return Response("Update successful",status=status.HTTP_201_CREATED)


    


