import base64

from django.core.files.base import ContentFile
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .repositories import *

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

class ProductViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProductMixinSerializer


class ProductDetailViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = ProductDetail.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProductDetailMixinSerializer

class ProductGalleryViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = ProductGallery.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProductGalleryMixinSerializer

class ProductCreateView(APIView):

    def get(self, request, format=None):
        """Listar Todos Los Productos"""

        products = Product.objects.all()
        paginator = CustomPaginator()
        serializer = paginator.generate_response(products, ProductListSearchSerializer, request)
        #serializer = ShoppingcartDetailSerializer(shoppingcart, many=True)
        return serializer    
    

    def post(self,request,format=None):
        """Guardar un Producto"""
        
        data = request.data
        features_array = []
        gallery_array = []
        #print(data)

        #if "purchase" in data and "products" in data:
        if "product" in data:
            
            data_product = data["product"]
            
            try:
                category = Category.objects.get(id=data_product["category"])
            except category.DoesNotExist:
                return Response("La categoria no existe", status=status.HTTP_400_BAD_REQUEST)

            try:
                brand = Brand.objects.get(id=data_product["brand"])
            except brand.DoesNotExist:
                return Response("La Marca no existe", status=status.HTTP_400_BAD_REQUEST)

            serializer_product = ProductSerializer(data=data_product)
   
            if serializer_product.is_valid():

                product = Product()
                product.name = data_product["name"]
                product.description = data_product["description"]
                """
                if ';base64,' in data_product["image"]:
                    format, imgstr = data_product["image"].split(';base64,')
                    ext = format.split('/')[-1]
                    product.image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                """
                product.coin = data_product["coin"]
                product.price = data_product["price"]
                product.category = category
                product.brand = brand
                product.quantity = data_product["quantity"]
                product.save()

                #registro de detalle de compra
                if "features" in data:
                    
                    data_features = data["features"]                   
                    
                    for item_features in data_features:
                        #print(item_features)
                        try:    
                            characteristic = Characteristic.objects.get(id=item_features['feature'])
                        except characteristic.DoesNotExist:
                            return Response("La Caracteristica no existe", status=status.HTTP_400_BAD_REQUEST)
                        
                        serializer_feature = ProductDetailSerializer(data=item_features)
                        if serializer_feature.is_valid():
                                                    
                            feature = ProductDetail()
                            feature.product = product
                            feature.characteristic = characteristic
                            feature.description = item_features['description']
                            feature.save()
                            features_array.append(serializer_feature.data)
                            features_array.append(ProductDetailViewSerializer(feature).data)
                        else:
                            return Response(serializer_feature.errors, status=status.HTTP_400_BAD_REQUEST)
                

                if "gallery" in data:
                    
                    data_gallery = data["gallery"]
                    

                    for item_gallery in data_gallery:
                        
                        serializer_gallery = ProductGalleryMixinSerializer(data=item_gallery)
                        if serializer_gallery.is_valid():
                                                    
                            gallery = ProductGallery()
                            gallery.product = product
                            gallery.image = item_gallery['image']
                            gallery.save()
                            gallery_array.append(serializer_gallery.data)
                        else:
                            return Response(serializer_gallery.errors, status=status.HTTP_400_BAD_REQUEST)
                
                data_end = {
                    "Product": serializer_product.data,
                    "Detail": features_array,
                    "Gallery": gallery_array,
                }

                return Response(data_end)
            else:
                
                return Response(serializer_product.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe suministrar informacion de producto", status=status.HTTP_400_BAD_REQUEST)
    
class ProductSearchView(APIView):
    
    def get(self, request, pk, format=None):

        """Buscar un producto"""
        try:
            Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("EL Id de producto no existe")
        
        product = Product.objects.get(id=pk)
        serializer = ProductListSearchSerializer(product, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """Actualizar un Producto"""
        
        data = request.data
        features_array = []
        gallery_array = []
        #print(data)
        
        try:
            Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST)
        
        
        #if "purchase" in data and "products" in data:
        if "product" in data:
            
            data_product = data["product"]
            
            try:
                Category.objects.get(id=data_product["category"])
            except Category.DoesNotExist:
                return Response("La categoria no existe", status=status.HTTP_400_BAD_REQUEST)

            category = Category.objects.get(id=data_product["category"])

            try:
                 Brand.objects.get(id=data_product["brand"])
            except Brand.DoesNotExist:
                return Response("La Marca no existe", status=status.HTTP_400_BAD_REQUEST)
            
            brand = Brand.objects.get(id=data_product["brand"])

            serializer_product = ProductSerializer(data=data_product)
   
            if serializer_product.is_valid():
                product = Product.objects.get(id=pk)
                product.name = data_product["name"]
                product.description = data_product["description"]
                """
                if data_product["image"] and ';base64,' in data_product["image"]:
                    format, imgstr = data_product["image"].split(';base64,')
                    ext = format.split('/')[-1]
                    product.image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                """
                product.coin = data_product["coin"]
                product.price = data_product["price"]
                product.category = category
                product.brand = brand
                product.quantity = data_product["quantity"]
                product.save()

                #registro de detalle de compra
                if "features" in data:
                    
                    
                    data_features = data["features"]                   
                    
                    for item_features in data_features:

                        try:    
                            detail_product = ProductDetail.objects.get(id=item_features['id'])
                        except detail_product.DoesNotExist:
                            return Response("el ID de Detalle no existe", status=status.HTTP_400_BAD_REQUEST)
                        
                        try:    
                            characteristic = Characteristic.objects.get(id=item_features['feature'])
                        except characteristic.DoesNotExist:
                            return Response("La Caracteristica no existe", status=status.HTTP_400_BAD_REQUEST)
                        
                        serializer_detail = ProductDetailSerializer(data=item_features)
                        if serializer_detail.is_valid():
                                                    
                            detail_product.characteristic = characteristic
                            detail_product.description = item_features['description']
                            detail_product.save()
                            #features_array.append(serializer_feature.data)
                            features_array.append(ProductDetailViewSerializer(detail_product).data)
                        else:
                            return Response(serializer_detail.errors, status=status.HTTP_400_BAD_REQUEST)
                

                if "gallery" in data:
                    
                    data_gallery = data["gallery"]
                    

                    for item_gallery in data_gallery:
                        
                        serializer_gallery = ProductGalleryMixinSerializer(data=item_gallery)
                        if serializer_gallery.is_valid():
                                                    
                            gallery = ProductGallery()
                            gallery.product = product
                            gallery.image = item_gallery['image']
                            gallery.save()
                            gallery_array.append(serializer_gallery.data)
                        else:
                            return Response(serializer_gallery.errors, status=status.HTTP_400_BAD_REQUEST)

                #registro de detalle de compra
                if "news_features" in data:
                    
                    data_news_features = data["news_features"]                   
                    
                    for item_features in data_news_features:
                        try:    
                            characteristic = Characteristic.objects.get(id=item_features['feature'])
                        except characteristic.DoesNotExist:
                            return Response("La Caracteristica no existe", status=status.HTTP_400_BAD_REQUEST)
                        
                        serializer_feature = ProductDetailSerializer(data=item_features)
                        if serializer_feature.is_valid():
                                                    
                            feature = ProductDetail()
                            feature.product = product
                            feature.characteristic = characteristic
                            feature.description = item_features['description']
                            feature.save()
                            #features_array.append(serializer_feature.data)
                            features_array.append(ProductDetailViewSerializer(feature).data)
                        else:
                            return Response(serializer_feature.errors, status=status.HTTP_400_BAD_REQUEST)



                data_end = {
                    "Product": serializer_product.data,
                    "Detail": features_array,
                    "Gallery": gallery_array,
                }

                return Response(data_end)
            else:
                
                return Response(serializer_product.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debe suministrar informacion de producto", status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request, pk, format=None):


        """Eliminar un producto"""
        product= Product.objects.get(id=pk)
        product_detail= ProductDetail.objects.filter(product=product)
        serializer = ProductDetailMixinSerializer(product_detail, many=True)
    
        for item_detail in serializer.data:
            detail = ProductDetail.objects.get(id=item_detail["id"])
            detail.delete()
        
        product.delete()
        
        return Response("se ha eliminado El producto",status=status.HTTP_204_NO_CONTENT)

            
class ProductDetailView(APIView):
      
    def get(self, request, pk, format=None):
          
        """Buscar detalle de producto"""
        detail = ProductDetail.objects.get(id=pk)
        #detail = ProductDetail.objects.all()
        serializer = ProductDetailMixinSerializer(detail, many=False)
        return Response(serializer.data)
       
    
    def delete(self, request, pk, format=None):

        """Eliminar detalle de un producto"""
  
        detail_product = ProductDetail.objects.get(id=pk)
        detail_product.delete()
        return Response("se ha eliminado el detalle para este producto",status=status.HTTP_204_NO_CONTENT)

            