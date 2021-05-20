import base64
from django.core.files.base import ContentFile
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import *
from .serializers import *

from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny


class SliderCreateView(APIView):

        
    def get(self, request, format=None):

        """listar una imagenes"""
        
        images = Slide.objects.all()
        serializer = SlideDetailSerializer(images, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        """Subir imagen un Producto"""
        
        data = request.data

        slide = {
                "image" : data["image"],
                "status" : data["status"],
                "title" : data["title"],
                "span" : data["span"],
                "action_title" : data["action_title"],
                "action_link" : data["action_link"],
             }
        Slide_serializer = SlideSerializer(data=slide)
        if Slide_serializer.is_valid():
            Slide_serializer.save()   
            return Response("¡Imagen registrada con exito!",status=status.HTTP_201_CREATED)           
        else:
            return Response("la imagen no ha sido registrada", status=status.HTTP_400_BAD_REQUEST)

class HeaderDetailView(APIView):
    """Detalle de Imegen para header"""
    
    def get(self, request, pk, format=None):

        """Buscar una imagen"""
        try:
            Slide.objects.get(id=pk)
        except Slide.DoesNotExist:
            return Response("Imagen no existe")
        
        slide = Slide.objects.get(id=pk)
        serializer = SlideDetailSerializer(slide, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):

        data = request.data
    
        
        try:
            Slide.objects.get(id=pk)
        except Slide.DoesNotExist:
            return Response("Imagen no existe")

        slide = Slide.objects.get(id=pk)
        if data["status"] == "true":
            status_image = True
        else:
            status_image = False

        slide.image = data["image"]
        slide.status = status_image
        slide.title = data["title"]
        slide.span = data["span"]
        slide.action_title = data["action_title"]
        slide.action_link = data["action_link"]

        slide.save()

        return Response("¡Imagen Actualizada con exito!",status=status.HTTP_200_OK) 
    
    def delete(self, request, pk, format=None):


        """Eliminar un imagen"""
        image = Slide.objects.get(id=pk)
        image.delete()
        
        return Response("se ha eliminado la imagen",status=status.HTTP_204_NO_CONTENT)


class SliderWebView(APIView):
   
    def get(self, request, format=None):

        """listar una imagenes para la web"""
        images = Slide.objects.filter(status=True)
        serializer = SlideDetailSerializer(images, many=True)
        return Response(serializer.data)  
