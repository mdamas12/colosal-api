from .models import *

class ProductRepositories(object):

    def get_product_list(self):
        return Product.objects.all()


