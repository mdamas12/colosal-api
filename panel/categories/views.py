from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
