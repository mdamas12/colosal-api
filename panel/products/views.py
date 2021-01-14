from rest_framework.generics import RetrieveAPIView, ListAPIView
from .serializers import *
from .repositories import *

# Create your views here.
class ProductsListView(ListAPIView):

    serializer_class = ProductSerializer

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