from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response


class Bank(TimeStampedModel):

    name = models.CharField(max_length=255)
    account_owner = models.CharField(max_length=25, null=True, blank=True)
    account_number = models.CharField( max_length=25, null=True, blank=True)
    owner_id = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True,blank=True)
  
    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self): return self.name

class Method(TimeStampedModel):
    PaymentType = Choices('ZELLE', 'TRANSFERENCIA $', 'TRANSFERENCIA BS', 'PAGO MOVIL', 'EFECTIVO')

    bank = models.ForeignKey(Bank, related_name='methods', on_delete=models.PROTECT)
    payment_type = models.CharField(max_length=20, choices=PaymentType, default="TRANSFERENCIA $")
  
    class Meta:
        verbose_name = "Metodo de Pago"
        verbose_name_plural = "Metodos de Pago"

    def __str__(self): return self.payment_type

