from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response

from panel.brands.models import Brand
from panel.categories.models import Category
from panel.characteristics.models import Characteristic


class Product(TimeStampedModel):

    COINS = Choices('USD', 'BS')

    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='products', null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    coin = models.CharField(max_length=20,choices=COINS,default="USD")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self): return self

class ProductDetail(TimeStampedModel):

    product = models.ForeignKey(Product,  related_name='detail_product',  on_delete=models.PROTECT)
    characteristic = models.ForeignKey(Characteristic, related_name='feature', on_delete=models.PROTECT)
    description = models.CharField(null=True,blank=True,max_length=255)

    class Meta:
        verbose_name = "Detalle de producto"
        verbose_name_plural = "Detalles de productos"

    def __str__(self): return self.product

class ProductGallery(TimeStampedModel):

    product = models.ForeignKey(Product, related_name='picture', on_delete=models.PROTECT)
    image = models.FileField(upload_to='products', null=True)

    class Meta:
        verbose_name = "Galeria de producto"
        verbose_name_plural = "Galerias de productos"

    def __str__(self): return self.name