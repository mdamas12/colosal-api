from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from .models import Promotion, PromotionDetail
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
        detail_array = []

        #if "purchase" in data and "products" in data:
        if "promotion" in data:
            
            data_promotion = data["promotion"]
            
            try:
                Category.objects.get(id=data_promotion["category"])
            except Category.DoesNotExist:
                return Response("La categoria no existe", status=status.HTTP_400_BAD_REQUEST)

            category = Category.objects.get(id=data_promotion["category"])
            serializer_promotion = PromotionSerializer(data=data_promotion)
   
            if serializer_promotion.is_valid():

                promotion = Promotion()
                promotion.name = data_promotion["name"]
                promotion.description = data_promotion["description"]
                """
                if ';base64,' in data_promotion["image"]:
                    format, imgstr = data_promotion["image"].split(';base64,')
                    ext = format.split('/')[-1]
                    promotion.image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                """
                promotion.coin = data_promotion["coin"]
                promotion.price = data_promotion["price"]
                promotion.category = category
                promotion.quantity = data_promotion["quantity"]
                promotion.save()

                #registro de detalle de compra
                
                if "Detail" in data:
                    
                    data_promDetail = data["Detail"]                   
                    
                    for item_detail in data_promDetail:
                        #print(item_features)
                        try:    
                            Product.objects.get(id=item_detail['product'])
                        except Product.DoesNotExist:
                            return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST)
                        
                        product = Product.objects.get(id=item_detail['product'])
                        serializer_detail = PromotionDetailSerializer(data=item_detail)
                        if serializer_detail.is_valid():
                                                    
                            detail = PromotionDetail()
                            detail.promotion = promotion
                            detail.product = product
                            detail.quantity = item_detail['quantity']
                            detail.save()

                            #detail_array.append(serializer_feature.data)
                            detail_array.append(PromotionDetailViewSerializer(detail).data)
                        else:
                            return Response(serializer_detail.errors, status=status.HTTP_400_BAD_REQUEST)
                
                
                
                data_end = {
                    "Promotion": serializer_promotion.data,
                     "Detail": detail_array,
                }

                return Response(data_end)
            else:
                
                return Response(serializer_promotion.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe suministrar informacion de la promocion", status=status.HTTP_400_BAD_REQUEST)


class PromotionDetailView(APIView):
    
    def get(self, request, pk, format=None):

        """Buscar una promocion"""
        try:
            Promotion.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("EL Id de promocion no existe")
        
        promocion = Promotion.objects.get(id=pk)
        serializer = PromotionFullSerializer(promocion, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        data = request.data
        detail_array = []

        if "promotion" in data:
            
            data_promotion = data["promotion"]

            try:
                Promotion.objects.get(id=pk)
            except Promotion.DoesNotExist:
                return Response("el Id de promocion no existe", status=status.HTTP_400_BAD_REQUEST)
            promotion = Promotion.objects.get(id=pk)
            
            try:
                Category.objects.get(id=data_promotion["category"])
            except Category.DoesNotExist:
                return Response("La categoria no existe", status=status.HTTP_400_BAD_REQUEST)
            category = Category.objects.get(id=data_promotion["category"])

            serializer_promotion = PromotionSerializer(data=data_promotion)
   
            if serializer_promotion.is_valid():
                 
                promotion.name = data_promotion["name"]
                promotion.description = data_promotion["description"]
                """
                if ';base64,' in data_promotion["image"]:
                    format, imgstr = data_promotion["image"].split(';base64,')
                    ext = format.split('/')[-1]
                    promotion.image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                """
                promotion.coin = data_promotion["coin"]
                promotion.price = data_promotion["price"]
                promotion.category = category
                promotion.quantity = data_promotion["quantity"]
                promotion.save()

                if "Detail" in data:

                    data_promDetail = data["Detail"]                   
                    
                    for item_detail in data_promDetail:
                        #print(item_features)

                        try:    
                            PromotionDetail.objects.get(id=item_detail['id'])
                        except PromotionDetail.DoesNotExist:
                            return Response("detalle de promocion no existe", status=status.HTTP_400_BAD_REQUEST)                      
                        detail =  PromotionDetail.objects.get(id=item_detail['id'])

                        try:    
                            Product.objects.get(id=item_detail['product'])
                        except Product.DoesNotExist:
                            return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST) 
                        product = Product.objects.get(id=item_detail['product'])
                        
                        serializer_detail = PromotionDetailSerializer(data=item_detail)
                        if serializer_detail.is_valid():
                                                    
                            detail.promotion = promotion
                            detail.product = product
                            detail.quantity = item_detail['quantity']
                            detail.save()

                            detail_array.append(PromotionDetailViewSerializer(detail).data)
                        else:
                            return Response(serializer_detail.errors, status=status.HTTP_400_BAD_REQUEST)
                
                if "newDetail" in data:
                    
                    data_newDetail = data["newDetail"]                   
                    
                    for item_detail in data_newDetail:
                       
                        try:    
                            Product.objects.get(id=item_detail['product'])
                        except Product.DoesNotExist:
                            return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST)
                        
                        product = Product.objects.get(id=item_detail['product'])
                        serializer_detail = PromotionDetailSerializer(data=item_detail)
                        if serializer_detail.is_valid():
                                                    
                            detail = PromotionDetail()
                            detail.promotion = promotion
                            detail.product = product
                            detail.quantity = item_detail['quantity']
                            detail.save()

                            detail_array.append(PromotionDetailViewSerializer(detail).data)
                        else:
                            return Response(serializer_detail.errors, status=status.HTTP_400_BAD_REQUEST)
                
                data_end = {
                    "Promotion": serializer_promotion.data,
                     "Detail": detail_array,
                }

                return Response(data_end)
            else:
                
                return Response(serializer_promotion.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe suministrar informacion de la promocion", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):


        """Eliminar una Promocion"""

        promotion = Promotion.objects.get(id=pk)
        prom_detail= PromotionDetail.objects.filter(promotion=promotion)
        detail_serializer = PromotionDetailSerializer(prom_detail, many=True)
    
        for item_detail in detail_serializer.data:
            detail = PromotionDetail.objects.get(id=item_detail["id"])
            detail.delete()
        
        promotion.delete()
        
        return Response("se ha eliminado la promocion",status=status.HTTP_204_NO_CONTENT)


class PromocionDetailDeleteView(APIView):
          
    def delete(self, request, pk, format=None):

        """Eliminar detalle de una promocion"""
  
        detail_promotion = PromotionDetail.objects.get(id=pk)
        detail_promotion.delete()
        return Response("se ha eliminado el detalle de esta promociom",status=status.HTTP_204_NO_CONTENT)

            