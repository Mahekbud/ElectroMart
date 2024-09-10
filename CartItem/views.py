from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import CartItem
from .serializers import CartItemSerializer
from .models import CartItem
from UserAuth.models import User
from Product.models import Product



#-------------------------------create_cartitem--------------------------

@api_view(['POST'])
def create_cartitem(request):
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    
    if not product_id or not quantity:
        return Response({"error": "Product ID and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
   
    discounted_price = product.discount_price
    
    if discounted_price is None:
        return Response({"error": "Discount price not available for this product."}, status=status.HTTP_400_BAD_REQUEST)

    total_price = discounted_price * int(quantity)

    data = request.data.copy()
    data['total_price'] = total_price
   
    serializer = CartItemSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------get_cartitem_by_id------------------------------


@api_view(['GET'])
def get_cartitem_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cartitem = CartItem.objects.get(pk=id, is_active=True, is_deleted=False)
    except CartItem.DoesNotExist:
        return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartItemSerializer(cartitem)
    return Response(serializer.data)


#-----------------------------update_cartitem_by_id-----------------------------------

@api_view(['PUT'])
def update_cartitem_by_id(request):
    cartitem_id = request.query_params.get('id')
    
    if not cartitem_id:
        return Response({"error": "CartItem ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cartitem = CartItem.objects.get(pk=cartitem_id, is_active=True, is_deleted=False)
    except CartItem.DoesNotExist:
        return Response({"error": "CartItem not found."}, status=status.HTTP_404_NOT_FOUND)

    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')

    if not product_id or not quantity:
        return Response({"error": "Product ID and quantity are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

    discounted_price = product.discount_price
    
    if discounted_price is None:
        return Response({"error": "Discount price not available for this product."}, status=status.HTTP_400_BAD_REQUEST)

    total_price = discounted_price * int(quantity)

    data = {
        'product_id': product_id,
        'quantity': quantity,
        'total_price': total_price
    }

    serializer = CartItemSerializer(cartitem, data=data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------------delete_cartitem_by_id-----------------------------

@api_view(['DELETE'])
def delete_cartitem_by_id(request):
    cartitem_id = request.query_params.get('id')

    if not cartitem_id:
        return Response({"error": "CartItem ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cartitem = CartItem.objects.get(pk=cartitem_id, is_active=True, is_deleted=False)
    except CartItem.DoesNotExist:
        return Response({"error": "CartItem not found."}, status=status.HTTP_404_NOT_FOUND)

    cartitem.is_deleted = True
    cartitem.save()
    
    return Response({"message": "CartItem deleted successfully."}, status=status.HTTP_200_OK)

#-----------------------------get_all_cartitems----------------------------------

@api_view(['GET'])
def get_all_cartitems(request):
    cartitems = CartItem.objects.filter(is_active=True, is_deleted=False)

    serializer = CartItemSerializer(cartitems, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)