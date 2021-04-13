from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.conf import settings

from .serializers import *
from panel.payments.models import *

#from .repositories import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

# Create your views here.

class PaymentCreateView(APIView):
    
    def get(self, request, format=None):
        """listar formas de pago """

        banks = Bank.objects.all()
        serializer = listpaymentsSerializer(banks, many=True)
        return Response(serializer.data)


    def post(self,request,format=None):
        """Guardar una opcion de pago"""
        data = request.data
        #print(data)

        #if "purchase" in data and "products" in data:
        if "bank" in data and "method" in data:

            data_bank = data["bank"]

            serializer_bank = BankSerializer(data=data_bank)
   
            if serializer_bank.is_valid():

                bank = Bank()
                bank.name = data_bank["name"]
                bank.account_owner = data_bank["account_owner"]
                bank.account_number = data_bank["account_number"]
                bank.owner_id = data_bank["owner_id"]
                bank.email = data_bank["email"]
                bank.phone = data_bank["phone"]
                bank.currency = data_bank["currency"]
                bank.save()

                #registro de metodos de pago para el banco registrado
                data_method = data["method"]
                method_array = []
                for item_method in data_method:

                    serializer_method = MethodSerializer(data=item_method)
                    if serializer_method.is_valid():

                        method = Method()
                        method.bank = bank
                        method.payment_type = item_method['payment_type']
                        method.save()

                        method_array.append(serializer_method.data)
                       
                    else:
                        return Response(serializer_method.errors, status=status.HTTP_400_BAD_REQUEST)
                
                data_end = {
                    "Bank": serializer_bank.data,
                    "Methods": method_array
                }

                return Response(data_end)
            else:
                
                return Response(serializer_bank.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response("Debes enviar informacion del banco y metodos de pago", status=status.HTTP_400_BAD_REQUEST)
    
     
class PaymentBanksView(APIView):
    
    def get(self, request, type, format=None):
        """listar por tipo de pago """

        paymentbank = Method.objects.filter(payment_type = type)
        serializer = MethodWebSerializer(paymentbank, many=True)
        return Response(serializer.data)
