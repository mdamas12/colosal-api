from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Customer
from django.db.models import Q
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


class CustomerSearch(APIView):
      
    def get(self, request, search, format=None):
        """busqueda de clientes"""
        customer = Customer.objects.filter(Q(name__icontains = search))
        serializer = CustomerDetailSerializer(customer, many=True)
        return Response(serializer.data)