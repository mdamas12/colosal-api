from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.
class Product(TimeStampedModel):

    name = models.CharField(unique=True,max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.FileField()

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self): return self.name