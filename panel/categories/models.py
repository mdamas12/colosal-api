from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class Category(TimeStampedModel):
    
    name = models.CharField(unique=True, max_length=255)
    image = models.FileField(upload_to='categories', null=True)
  


    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self): return self.name