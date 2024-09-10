from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from Category.models import Category
from .serializers import ProductSerializer
from decimal import Decimal



#--------------------------create_product-----------------------------



@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

        category_id = request.data.get('category_id')
        if not category_id:
            return Response({'error': 'Category ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        discount_percentage = 0
        if category.name == 'Laptops':
            discount_percentage = 5
        elif category.name == 'Smartphones':
            discount_percentage = 10
        elif category.name == 'Home Appliances':
            discount_percentage = 7

        price = Decimal(data.get('price', 0))
        discount_price = price - (price * Decimal(discount_percentage) / Decimal(100))

        product = Product(
            name=data['name'],
            price=price,
            category_id=category,  
            quantity=data['quantity'],
            discount_price=discount_price 
        )
        product.save()

        serialized_product = ProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------get_product_by_id------------------------------

@api_view(['GET'])
def get_product_by_id(request):
    product_id = request.query_params.get('id')

    if not product_id:
        return Response({'error': 'ID query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)

#-----------------------------get_all_products-------------------------

@api_view(['GET'])
def get_all_products(request):
    Products = Product.objects.all()
    serializer = ProductSerializer(Products, many=True)
    return Response(serializer.data)

#--------------------------update_product_by_id--------------------------------

@api_view(['PUT'])
def update_product_by_id(request):

    id = request.query_params.get('id')
    if not id:
        return Response({'error': 'ID parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        data = serializer.validated_data

        category_id = request.data.get('category_id')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response({'error': 'Category does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            discount_percentage = 0
            if category.name == 'Laptops':
                discount_percentage = 5
            elif category.name == 'Smartphones':
                discount_percentage = 10
            elif category.name == 'Home Appliances':
                discount_percentage = 7
            
            price = Decimal(data.get('price', product.price))
            discount_price = price - (price * Decimal(discount_percentage) / Decimal(100))
        else:
            category = product.category
            price = Decimal(data.get('price', product.price))
            discount_price = product.discount_price

        product.name = data.get('name', product.name)
        product.price = price
        product.category = category
        product.quantity = data.get('quantity', product.quantity)
        product.discount_price = discount_price
        product.save()

        serialized_product = ProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------------delete_product_by_id------------------------------

@api_view(['DELETE'])
def delete_product_by_id(request):
    
    product_id = request.query_params.get('id')
    
    if not product_id:
        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#-----------------------------search_product_by_product_name-----------------------------------

@api_view(['GET'])
def search_product_by_product_name(request):
    product_name = request.query_params.get('product')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if not product_name or min_price is None or max_price is None:
        return Response({'error': 'Product name, min_price, and max_price are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        min_price = float(min_price)
        max_price = float(max_price)
    except ValueError:
        return Response({'error': 'Invalid price values'}, status=status.HTTP_400_BAD_REQUEST)

    products = Product.objects.filter(
        name__icontains=product_name,
        is_active=True,
        is_deleted=False,
        price__gte=min_price,
        price__lte=max_price
    )

    if not products.exists():
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    result = []
    for product in products:
        result.append({
            "product_name": product.name,
            "product_price": product.price
        })

    return Response({"Products": result}, status=status.HTTP_200_OK)