from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    url(r'^products/', include('panel.products.urls')),
    url(r'^brands/', include('panel.brands.urls')),
]
