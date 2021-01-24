from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from .models import Characteristic
from .serializers import CharacteristicSerializer


class CharacteristicViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Characteristic.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = CharacteristicSerializer
