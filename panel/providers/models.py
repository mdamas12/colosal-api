from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from rest_framework import status
from rest_framework.response import Response


class Provider(TimeStampedModel):

    name = models.CharField(max_length=255)
    address = models.TextField(null=True,blank=True)
    email = models.TextField(null=True,blank=True)
    number = models.TextField(null=True,blank=True)
  
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self): return self.name

