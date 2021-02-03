from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from .models import Customer
from .serializers import CustomerSerializer, CustomerDetailSerializer


class CustomerViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Customer.objects.all().order_by('-fullname')
    permission_classes = (AllowAny,)
    serializer_class = CustomerSerializer
