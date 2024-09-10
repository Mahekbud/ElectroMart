from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart
from .serializers import CartSerializer



#--------------------------create_Cart--------------------------------

@api_view(['POST'])
def create_cart(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#----------------------------get_cart_by_id--------------------------------

@api_view(['GET'])
def get_cart_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        cart = Cart.objects.get(pk=id, is_active=True, is_deleted=False)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart)

    return Response(serializer.data)

#--------------------------update_cart_by_id----------------------------

@api_view(['PUT'])
def update_cart_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cart = Cart.objects.get(pk=id, is_active=True, is_deleted=False)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------delete_cart_by_id--------------------------

@api_view(['DELETE'])
def delete_cart_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cart = Cart.objects.get(pk=id, is_active=True, is_deleted=False)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    cart.is_deleted = True
    cart.save()

    return Response({"message": "Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)