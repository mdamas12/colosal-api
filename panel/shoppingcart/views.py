from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from .models import *
from  users.models import *
from  users.serializers import UserSerializer

from .serializers import *

#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from panel.products.models import *

# Create your views here.

class ShoppingcartViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Shoppingcart.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ShoppingcartSerializer

class CustomPaginator(PageNumberPagination):
   
    page_size = 10 # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response({"error": "No results found for the requested page"}, status=status.HTTP_400_BAD_REQUEST)

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)


class ShoppingcartCustomerView(APIView):
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        
        user = UserSerializer(User.objects.get(email = request.user), many = False)
        shoppingcart = Shoppingcart.objects.filter(customer = user.data["id"])
        paginator = CustomPaginator()
        serializer = paginator.generate_response(shoppingcart, ShoppingcartDetailSerializer, request)
        return serializer

    def post(self,request,format=None):

        """Guardar un producto en carrito de compra"""
        
        data = request.data
        user = UserSerializer(User.objects.get(email = request.user), many = False)        
        try:
            Product.objects.get(id=data["product"])
        except Product.DoesNotExist:
            return Response("producto no existe", status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=data["product"])

        if data["quantity"] > product.quantity:
            return Response("La Cantidad solicitada ya no se encuenta en stock para:  "+product.name, status=status.HTTP_200_OK)

        try: 
            Shoppingcart.objects.get(product=data["product"],customer = user.data["id"])
        except Shoppingcart.DoesNotExist:
            
            cart = {
            "customer" : user.data["id"],
            "product" : product.id,
            "quantity" :  data["quantity"],
            "amount" : product.price * data["quantity"],
            "status" : "in"
            }

            serializer_shopp = ShoppingcartSerializer(data=cart)
    
            if serializer_shopp.is_valid():
                serializer_shopp.save()
                new_shopping = Shoppingcart.objects.latest('created')
                serializer = ShoppingcartSerializer(new_shopping, many=False)
                return Response("Producto Agregado a carrito de compra",status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)
        
        cart = Shoppingcart.objects.get(product=data["product"],customer = user.data["id"])
        cart.quantity = data["quantity"]
        cart.amount = product.price * data["quantity"]
        cart.save()
        return Response("Producto Actualizado en carrito de compra",status=status.HTTP_201_CREATED)
  

class CustomerSearchView(APIView):
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

       
        data = request.data
        print(data["product"])
        user = UserSerializer(User.objects.get(email = request.user), many = False) 
        try: 
            Shoppingcart.objects.get(product=data["product"],customer = user.data["id"])
        except Shoppingcart.DoesNotExist:
            return Response("producto no existe en carrito de compra", status=status.HTTP_400_BAD_REQUEST)

        cart = Shoppingcart.objects.get(product=data["product"],customer = user.data["id"])
        return Response(cart.quantity,status=status.HTTP_201_CREATED)
        

class ChangeShoppingcartView(APIView):
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        
            
        try:
            Shoppingcart.objects.get(id=pk)
        except Shoppingcart.DoesNotExist:
            return Response("El item  no existe", status=status.HTTP_400_BAD_REQUEST)
            
        item = Shoppingcart.objects.get(id=pk)
        item.delete()
        return Response("Item ha sido eliminado")

    def put(self, request, pk, format=None):
        data = request.data
    
        product = Product.objects.get(id=data["product"])
        product_inshopp = Shoppingcart.objects.get(id=pk)
        
        
        if data["quantity"] > product.quantity:
            return Response("La Cantidad solicitada ya no se encuenta en stock para:  "+product.name, status=status.HTTP_200_OK)
        else:
            product_inshopp.quantity = data["quantity"]
            product_inshopp.amount = product.price * data["quantity"]
            product_inshopp.save()
            return Response("producto Actualizado con exito", status=status.HTTP_202_ACCEPTED)
        
        

class ShoppingcartListall(ListAPIView):
    
    """Listar Todo el carro de compra"""

    queryset = Shoppingcart.objects.all()
    serializer_class = ShoppingcartDetailSerializer
    pagination_class = PageNumberPagination
    