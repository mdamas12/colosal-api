from rest_framework import serializers
from  SistemaGestion.settings import *
from panel.brands.serializers import BrandSerializer, BrandDetailSerializer
from panel.categories.serializers import CategorySerializer, CategoriesDetailSerializer
from panel.characteristics.serializers import CharacteristicViewSerializer
from .models import *

# serializador para guardar producto
class ProductSerializer(serializers.ModelSerializer):
    #category = serializers.IntegerField(read_only=True)
    #brand = serializers.IntegerField(read_only=True)
    #image = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = ('__all__')

class ProductDetailSerializer(serializers.ModelSerializer):
    #product = serializers.IntegerField(read_only=True)
    #characteristic = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProductDetail
        fields = ('__all__')



class ProductMixinSerializer(serializers.ModelSerializer):
    category = CategoriesDetailSerializer(many=False)
    brand = BrandDetailSerializer(many=False)

    class Meta:
        model = Product
        fields = ('__all__')


class ProductDetailMixinSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetail
        fields = ('__all__')



class ProductGalleryMixinSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ProductGallery
        fields = ('__all__')


class ProductDetailViewSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicViewSerializer()
    #product = serializers.IntegerField(read_only=True)

    class Meta:
        model = ProductDetail
        fields = ('__all__')

class ProductListSearchSerializer(serializers.ModelSerializer):
    #purchase = PurchaseMixinSerializer()
    #purchase = serializers.IntegerField()
    category = CategoriesDetailSerializer(many=False)
    brand = BrandDetailSerializer(many=False)
    detail_product = ProductDetailViewSerializer(many=True)
    picture = ProductGalleryMixinSerializer(many=True)
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'coin',
            'price',
            'quantity',
            'image',
            'category',
            'brand',
            'detail_product',
            'picture'
            
        )

    def to_representation(self,instance):
        representation = super(ProductListSearchSerializer,self).to_representation(instance)
        if representation['image'] is not None:
            print("antes")
            print(representation['image'])
            domain_name = SERVER_URL
            if instance.image:
                full_path = domain_name + instance.image.url
                representation['image'] = full_path
                print("despues")
                print(representation['image'])
        return representation
    

    
