


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
        print(request.data)
        #return Response(data)
        serializer_categories = CategorySerializer(data=request.data)
   
        if serializer_categories.is_valid():
           
            category = Category()
            category.name = data["name"]
            category.image =  data["image"]
            """
            if ';base64,' in data_product["image"]:
                format, imgstr = data_product["image"].split(';base64,')
                ext = format.split('/')[-1]
                product.image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            """
            category.save()
            new_category = Category.objects.latest('created')
            serializer = CategoriesDetailSerializer(new_category, many=False)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        else:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    
class listAllCategories(APIView):
      
    def get(self, request, format=None):
        """Listar categorias sin paginacion"""
        categories = Category.objects.all()
        serializer = CategoriesDetailSerializer(categories, many=True)
        return Response(serializer.data)