


from rest_framework import mixins, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound as NotFoundError
from .models import Category
from .serializers import CategorySerializer, CategoriesDetailSerializer


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all().order_by('-modified')
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer

class CategoryDetailView(APIView):
      
    def get(self, request, pk, format=None):
          
        """detalle de categoria"""
    
        category = Category.objects.get(id=pk)
        serializer = CategoriesDetailSerializer(category, many=False)
        return Response(serializer.data)


class CategoryCreateView(APIView):

   
    def post(self,request,format=None):
        """Crear Categoria"""
        
        data = request.data
        print(data)
        #return Response(data)
        if data["image"] == 'null':
            category = {
                'name' : data["name"]         
            }
           
        else:

            category = {
                'name' : data["name"],
                'image' :  data["image"]
            }
         
        serializer_categories = CategorySerializer(data=category)
   
        if serializer_categories.is_valid():   
            serializer_categories.save()
            new_category = Category.objects.latest('created')
            serializer = CategoriesDetailSerializer(new_category, many=False)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        else:
            return Response("erro al validar informacion", status=status.HTTP_400_BAD_REQUEST)

            


class listAllCategories(APIView):
      
    def get(self, request, format=None):
        """Listar categorias sin paginacion"""
        categories = Category.objects.all()
        serializer = CategoriesDetailSerializer(categories, many=True)
        return Response(serializer.data)

class pruebaLogin(APIView):
      
    def post(self,request,format=None):

        print(request.data)
        return Response(request.data)