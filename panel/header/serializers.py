from rest_framework import serializers
from  SistemaGestion.settings import *
from .models import *

class SlideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slide
        fields = ('__all__')

class SlideDetailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Slide
        fields = ('__all__')

    def to_representation(self,instance):
        representation = super(SlideDetailSerializer,self).to_representation(instance)
        if representation['image'] is not None:
            domain_name = SERVER_URL
            if instance.image:
                full_path = domain_name + instance.image.url
                representation['image'] = full_path
        return representation