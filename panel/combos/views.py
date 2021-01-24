from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from .models import Promotion, PromotionDetail
from .serializers import PromotionSerializer, PromotionDetailSerializer


class PromotionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Promotion.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = PromotionSerializer


class PromotionDetailViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = PromotionDetail.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = PromotionDetailSerializer
