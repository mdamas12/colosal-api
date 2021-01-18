from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from panel.categories.models import Category
from panel.products.models import Product


class Combo(TimeStampedModel):

    COINS = Choices('USD', 'BS')

    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='uploads')
    price = models.DecimalField(max_digits=19, decimal_places=2)
    coin = models.CharField(max_length=20,choices=COINS,default="USD")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Combo"
        verbose_name_plural = "Combos"

    def __str__(self): return self.name


class ComboDetail(TimeStampedModel):

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    combo = models.ForeignKey(Combo, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Detalle de combo"
        verbose_name_plural = "Detalles de Combos"

    def __str__(self): return self.name