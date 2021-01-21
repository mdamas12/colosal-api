from django.conf.urls import url
from django.conf.urls import include

urlpatterns = [
    url(r'^brands/', include('panel.brands.urls')),
    url(r'^categories/', include('panel.categories.urls')),
    url(r'^features/', include('panel.characteristics.urls')),
   
]
