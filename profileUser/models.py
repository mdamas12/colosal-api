from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='user_profile', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
