from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class Brand(TimeStampedModel):
    
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self): return self.name
