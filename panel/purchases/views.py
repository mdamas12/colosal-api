
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from .serializers import *
from panel.products.serializers import ProductMixinSerializer
from .models import *
from panel.products.models import *

#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class PurshaselViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Purchase.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = PurchaseMixinSerializer


class ListPurshaseDetail(APIView):
    serializer_class = PurshaseDetailSerializer

    def get(self, request, pk):
        
        Products = PurchaseDetail.objects.all(purshase=pk)
        serializer = PurshaseDetailSerializer(Products, many=True)
        return Response("serializer.data")


class PurshaseDetailCreate(APIView):
    serializer_class = PurshaseDetailSerializer
    serializer_product = ProductMixinSerializer

    def get(self,request,format=None):
        Products = PurchaseDetail.objects.all()
        serializer = PurshaseDetailSerializer(Products, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
       # print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            id = request.data['product']
            product = Product()
            product = Product.objects.get(id=id)
            product.quantity = product.quantity + request.data['purchase_Received']
            #product.save()
           
            #serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            #return Response(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseCreateView(APIView):

    def post(self,request,format=None):
        data = request.data

        if "purchase" in data and "products" in data:
            data_purchase = data["purchase"]

            serializer_purchase = PurchaseMixinSerializer(data=data_purchase)

            data_products = data["products"]

            for item_product in data_products:
                serializer_product = PurshaseDetailCreateSerializer(data=item_product)
                if serializer_product.is_valid():
                    try:
                        Product.objects.get(id=item_product["id"])
                    except Product.DoesNotExist:
                        return Response("El producto no existe", status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer_product.errors, status=status.HTTP_400_BAD_REQUEST)

            if serializer_purchase.is_valid():
                purchase = Purchase()
                purchase.date = data_purchase["date"]
                purchase.description = data_purchase["description"]

                try:
                    provider = Provider.objects.get(id=data_purchase["provider"])
                except Product.DoesNotExist:
                    return Response("El proveedor no existe", status=status.HTTP_400_BAD_REQUEST)

                purchase.porvider = provider
                purchase.invoice = data_purchase["invoice"]
                purchase.coin = data_purchase["coin"]
                purchase.amount = data_purchase["amount"]
                purchase.save()

                purchases_detail_array = []

                for item_product in data_products:
                    product = Product.objects.get(id=item_product["id"])
                    product.quantity = product.quantity + item_product['purchase_quantity']
                    product.save()

                    purchase_detail = PurchaseDetail()

                    purchase_detail.purchase = purchase
                    purchase_detail.product = product
                    purchase_detail.purchase_price = item_product['purchase_price']
                    purchase_detail.purchase_quantity = item_product['purchase_quantity']
                    purchase_detail.purchase_Received = item_product['purchase_Received']
                    purchase_detail.status = item_product['status']
                    purchase_detail.save()

                    purchases_detail_array.append(PurshaseDetailSerializer(purchase_detail).data)

                data_end = {
                    "purchase": PurchaseMixinSerializer(purchase).data,
                    "detail": purchases_detail_array
                }

                return Response(data_end)
            else:
                return Response(serializer_purchase.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Debe enviar purchase y data", status=status.HTTP_400_BAD_REQUEST)



    
