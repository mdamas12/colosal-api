from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel

# Models
from panel.categories.models import Category
from panel.products.models import Product


class Promotion(TimeStampedModel):

    COINS = Choices('USD', 'BS')

    name = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='promotions', null=True)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    coin = models.CharField(max_length=20,choices=COINS,default="USD")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='%(class)s_category')
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20,default="ACTIVE")

    class Meta:
        verbose_name = "Promocion"
        verbose_name_plural = "Promociones"

    def __str__(self): return self.name


class PromotionDetail(TimeStampedModel):

    promotion = models.ForeignKey(Promotion, related_name='promotion_detail', on_delete=models.PROTECT, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='%(class)s_product')
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Detalle de promocion"
        verbose_name_plural = "Detalles de promociones"

    def __str__(self): return self.product