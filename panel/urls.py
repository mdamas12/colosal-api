from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    url(r'^products/', include('panel.products.urls')),
    url(r'^brands/', include('panel.brands.urls')),
    url(r'^categories/', include('panel.categories.urls')),
    url(r'^features/', include('panel.characteristics.urls')),
    url(r'^promotions/', include('panel.combos.urls')),
    url(r'^stock/', include('panel.stocktaking.urls')),
]
