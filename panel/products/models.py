from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response

from panel.brands.models import Brand
from panel.categories.models import Category


class Product(TimeStampedModel):

    COINS = Choices('USD', 'BS')

    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='uploads')
    price = models.DecimalField(max_digits=19, decimal_places=2)
    coin = models.CharField(max_length=20,choices=COINS,default="USD")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self): return self.name