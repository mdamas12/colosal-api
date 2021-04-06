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
        shoppingcart = Shoppingcart.objects.filter(customer = request.user)
        paginator = CustomPaginator()
        serializer = paginator.generate_response(shoppingcart, ShoppingcartDetailSerializer, request)
        return serializer

    def post(self,request,format=None):

        """Guardar un producto en carrito de compra"""
        
        data = request.data
        #print(data)
        
        user = UserSerializer(User.objects.get(username = request.user), many = False)
        try:
            Product.objects.get(id=data["product"])
        except Product.DoesNotExist:
            return Response("producto no existe", status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(id=data["product"])
        
        
        shopping = Shoppingcart()
        shopping.customer = user.data["id"]
        shopping.product = data["product"]
        shopping.quantity =  data["quantity"]
        shopping.amount = product.data["price"] * data["quantity"]
        shopping.save()
        
        new_shopping = Shoppingcart.objects.latest('created')
        serializer = ShcCustomerSerializer(new_shopping, many=False)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
       

class ShoppingcartListall(ListAPIView):
    
    """Listar Todo el carro de compra"""

    queryset = Shoppingcart.objects.all()
    serializer_class = ShoppingcartDetailSerializer
    pagination_class = PageNumberPagination
    