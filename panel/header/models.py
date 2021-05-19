from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.

class Slide(TimeStampedModel):

    image = models.FileField(upload_to='header', null=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "header"
        verbose_name_plural = "header"
