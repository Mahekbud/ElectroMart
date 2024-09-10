from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Category
from .serializers import CategorySerializer



#-------------------------create_category------------------------------

@api_view(['POST'])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------get_category_by_id---------------------------------

@api_view(['GET'])
def get_category_by_id(request):
    id = request.query_params.get('id')
    
    if not id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = Category.objects.get(pk=id, is_active=True, is_deleted=False)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category)
    return Response(serializer.data)

#--------------------------get_all_categories----------------------------


@api_view(['GET'])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

#-------------------------update_category_by_id--------------------

@api_view(['PUT'])
def update_category_by_id(request):
    category_id = request.query_params.get('id')
    
    if not category_id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = Category.objects.get(pk=category_id, is_active=True, is_deleted=False)
 
    
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
   
    serializer = CategorySerializer(category, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#----------------------------delete_category_by_id-----------------------------

@api_view(['DELETE'])
def delete_category_by_id(request):
    category_id = request.query_params.get('id')
    
    if not category_id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = Category.objects.get(pk=category_id, is_active=True, is_deleted=False)
 
        category.is_deleted = True
        category.save()
        
        return Response({"message": "Category successfully marked as deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)