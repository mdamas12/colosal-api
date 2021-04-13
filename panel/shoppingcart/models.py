from django.contrib.auth.models import User
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response

from panel.products.models import * 

from panel.promotions.models import * 


class Shoppingcart(TimeStampedModel):

    customer = models.ForeignKey(User, related_name='shoppingcart', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    promotion = models.ForeignKey(Promotion, on_delete=models.DO_NOTHING, null=True)
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=15)
    
  

    class Meta:
        verbose_name = "Carrito de Compra"
        verbose_name_plural = "Carrito de Compras"

    def __str__(self): return self.customer