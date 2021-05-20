from django.db import models
from model_utils.models import TimeStampedModel

# Create your models here.

class Slide(TimeStampedModel):

    image = models.FileField(upload_to='header', null=True)
    title = models.CharField( max_length=255, blank=True)
    span = models.CharField( max_length=255, blank=True)
    action_title = models.CharField( max_length=255, blank=True)
    action_link = models.CharField( max_length=255, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "header"
        verbose_name_plural = "header"
