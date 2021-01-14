from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from .models import Brand
from .serializers import BrandSerializer


class BrandViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Brand.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = BrandSerializer
