from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    url(r'^products/', include('panel.products.urls')),
    url(r'^brands/', include('panel.brands.urls')),
    url(r'^categories/', include('panel.categories.urls')),
    url(r'^features/', include('panel.characteristics.urls')),
    url(r'^promotions/', include('panel.promotions.urls')),
    url(r'^providers/', include('panel.providers.urls')),
    url(r'^purchases/', include('panel.purchases.urls')),
<<<<<<< HEAD
    url(r'^customers/', include('panel.customers.urls')),
=======
>>>>>>> master
    url(r'^payments/', include('panel.payments.urls')),
    url(r'^shoppingcart/', include('panel.shoppingcart.urls')),
    url(r'^sales/', include('panel.sales.urls')),
]
