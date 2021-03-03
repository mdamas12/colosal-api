from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from .models import *
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

    def get(self, request, pk, format=None):
        """Carrito de Compra Por cliente"""

        shoppingcart = Shoppingcart.objects.filter(customer=pk)
        paginator = CustomPaginator()
        serializer = paginator.generate_response(shoppingcart, ShoppingcartDetailSerializer, request)
        #serializer = ShoppingcartDetailSerializer(shoppingcart, many=True)
        return serializer


class ShoppingcartListall(ListAPIView):
    
    """Listar Todo el carro de compra"""

    queryset = Shoppingcart.objects.all()
    serializer_class = ShoppingcartDetailSerializer
    pagination_class = PageNumberPagination
    