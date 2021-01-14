from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'$',views.ProductsListView.as_view(), name='products'),
]
