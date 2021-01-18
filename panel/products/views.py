from rest_framework.generics import ListAPIView
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
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProductMixinSerializer
