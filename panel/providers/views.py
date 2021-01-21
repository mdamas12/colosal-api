from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import *
from .serializers import *

#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class ProviderViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Provider.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = ProviderMixinSerializer

