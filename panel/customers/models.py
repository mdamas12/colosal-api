from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class Customer(TimeStampedModel):
    
    fullname = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True, max_length=254)
    phone = models.CharField(max_length=255,null=True,blank=True)
    password = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self): return self.fullname