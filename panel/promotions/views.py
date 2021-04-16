from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from .models import Promotion, PromotionDetail
from rest_framework.decorators import parser_classes
from  panel.products.models import *
from .serializers import PromotionSerializer, PromotionDetailSerializer, PromotionDetailViewSerializer, PromotionFullSerializer



class CustomPaginator(PageNumberPagination):
    page_size = 25 # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)


class PromottionCreateView(APIView):

    def get(self, request, format=None):
        """Listar Todos Los Promociones"""

        promotions = Promotion.objects.all()
        paginator = CustomPaginator()
        serializer = paginator.generate_response(promotions, PromotionFullSerializer, request)
        #serializer = ShoppingcartDetailSerializer(shoppingcart, many=True)
        return serializer    
    

    def post(self,request,format=None):
        """Guardar una Promocion"""
        
        data = request.data
        #print(data)
        """
        print(data["name"])
        print(data["description"])
        print(data["quantity"])
        print(data["image"])
        print(data["coin"])
        print(data["category"])
        return Response("todo ok")
        """
        try:
            Category.objects.get(id=data["category"])
        except Category.DoesNotExist:
            #return Response("La categoria no existe", status=status.HTTP_400_BAD_REQUEST)
            return Response("categoria no es")   

        category = Category.objects.get(id=data["category"])
        serializer_promotion = PromotionSerializer(data=data)
   
        if serializer_promotion.is_valid():

            promotion = Promotion()
            promotion.name = data["name"]
            promotion.description = data["description"]
            promotion.image = data["image"]
            promotion.coin = data["coin"]
            promotion.price = data["price"]
            promotion.category = category
            promotion.quantity = data["quantity"]
            promotion.save()
            
            new_promotion = Promotion.objects.latest('created')
            serializer = PromotionSerializer(new_promotion, many=False)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:           
            #return Response(serializer_promotion.errors, status=status.HTTP_400_BAD_REQUEST) 
            return Response("serializer de promocion no valido")   

class PromotionDetailCreateView(APIView): 

    def post(self,request,format=None):

        """Guardar una productos de la promocion""" 
        data = request.data
        #print(data)

        for item in data["products_detail"]:
            product = {
                "promotion" : data["promotion"],
                "product" : item["product"],
                "quantity" : item["quantity"],
             }
            Product_serializer = PromotionDetailSerializer(data=product)
            if Product_serializer.is_valid():
                Product_serializer.save()              
            else:
                return Response("products list doesn't exist", status=status.HTTP_400_BAD_REQUEST)
        return Response("¡Promocion Creada con exito!",status=status.HTTP_201_CREATED)

class PromotionDetailView(APIView):
    """ Funcion para Mostrar los detalles de una promocion y sus productos agregados"""
    
    def get(self, request, pk, format=None):

        """Buscar una promocion"""
        try:
            Promotion.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("EL Id de promocion no existe")
        
        promotion = Promotion.objects.get(id=pk)
        serializer = PromotionFullSerializer(promotion, many=False)
        return Response(serializer.data)


class PromotionModificationView(APIView):

    def put(self, request, pk, format=None):
        data = request.data

        try:
            Promotion.objects.get(id=pk)
        except Promotion.DoesNotExist:
            return Response("La Promomcion no existe", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            Category.objects.get(id=data["category"])
        except Category.DoesNotExist:
            #return Response("La categoria no existe", status=status.HTTP_400_BAD_REQUEST)
            return Response("categoria no es")   

        category = Category.objects.get(id=data["category"])
        promotion = Promotion.objects.get(id=pk)
    
        promotion.name = data["name"]
        promotion.description = data["description"]
        promotion.image = data["image"]
        promotion.coin = data["coin"]
        promotion.price = data["price"]
        promotion.category = category
        promotion.quantity = data["quantity"]
        promotion.save()
        return Response("Promocion Actualizada", status=status.HTTP_200_OK)
        

    
          
    def delete(self, request, pk, format=None):

        """Eliminar detalle de una promocion"""
        try:
            Promotion.objects.get(id=pk)
        except Promotion.DoesNotExist:
            return Response("La Promomcion no existe", status=status.HTTP_400_BAD_REQUEST)
        
        promotion = Promotion.objects.get(id=pk)
        products = PromotionDetail.objects.filter(promotion=pk)
        for item in products:
            item.delete()

        products = PromotionDetail.objects.filter(promotion=pk)
        if products:
            return Response("La Promocion no pudo ser eliminada, aun tiene productos", status=status.HTTP_204_NO_CONTENT)
        else:
            promotion.delete()
            return Response("La Promocion Ha sido Eliminada con Exito", status=status.HTTP_200_OK)

      

class PromotionDetailModificationView(APIView):

    def put(self, request, pk, format=None):
        data = request.data

        try:
            Promotion.objects.get(id=pk)
        except Promotion.DoesNotExist:
            return Response("La Promomcion no existe", status=status.HTTP_400_BAD_REQUEST)
           
        promotion = Promotion.objects.get(id=pk)
        
        products_in = data["products_detail"]

        for item in products_in:
            product_d = Product.objects.get(id=item["product"])

            detail = PromotionDetail.objects.get(id=item["id"])
            detail.product = product_d
            detail.quantity = item["quantity"]
            detail.save()
        
        products_news = data["products_news"]

        for item in products_news:
   
            detail_new = {
                "promotion" : promotion.id,
                "product" : item["product"],
                "quantity" : item["quantity"]
             }
            detail_serializer = PromotionDetailSerializer(data=detail_new)
            if detail_serializer.is_valid():
                detail_serializer.save() 
            else:
                print(detail_serializer.errors)
        return Response("Promocion Actualizada", status=status.HTTP_200_OK)
        

            
class DeleteDetailPromotion(APIView):   

    def delete(self, request, pk, format=None):
        
        try:

            PromotionDetail.objects.get(id=pk)
        except PromotionDetail.DoesNotExist:
            return Response("El Producto no existe en esta promocion", status=status.HTTP_400_BAD_REQUEST)
           
        product = PromotionDetail.objects.get(id=pk)
        product.delete()
        return Response("Producto Eliminado de esta promociom",status=status.HTTP_200_OK)

                  