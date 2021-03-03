<<<<<<< HEAD
=======
from django.contrib.auth.models import User
>>>>>>> master
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response

<<<<<<< HEAD
from panel.customers.models import * 
=======
>>>>>>> master
from panel.products.models import * 


class Shoppingcart(TimeStampedModel):

<<<<<<< HEAD

    customer = models.ForeignKey(Customer, related_name='shoppingcart', on_delete=models.PROTECT)
=======
    customer = models.ForeignKey(User, related_name='shoppingcart', on_delete=models.PROTECT)
>>>>>>> master
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    status = models.CharField(max_length=15)
    

    class Meta:
        verbose_name = "Carrito de Compra"
        verbose_name_plural = "Carrito de Compras"

    def __str__(self): return self.custumer