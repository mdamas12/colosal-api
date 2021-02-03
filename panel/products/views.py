from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import *
from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.
class ProductsListView(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return self.repository.get_product_list()

    @property
    def repository(self):
        return ProductRepositories()

    """def get_object(self):
        repository = ProductRepositories()
        usecase = ProductsList(
            repository
        )
        return usecase.execute()"""


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

"""
class SearchsPrdoctslView(APIView):
    
    def get(self, request, pk, format=None):
        

        product = Product.objects.filter(name__contains=pk)
        serializer = ProductMixinSerializer(product, many=True)
        return Response(serializer.data)
"""