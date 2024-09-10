from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from Cart.models import Cart
from CartItem.models import CartItem
from .serializers import OrderSerializer



#---------------------------create_order---------------------------------

@api_view(['POST'])
def create_order(request):
    user_id = request.data.get('user_id')
    cart_id = request.data.get('cart_id')
    delivery_address = request.data.get('delivery_address')
    phone_number = request.data.get('phone_number')

    if not user_id or not cart_id or not delivery_address or not phone_number:
        return Response({"error": "User, cart, delivery address, and phone number are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the cart and validate its existence and association
        cart = Cart.objects.get(id=cart_id, is_active=True, is_deleted=False)
    except Cart.DoesNotExist:
        return Response({"error": "Cart does not belong to the user or is not active."}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate total amount from active cart items
    cart_items = CartItem.objects.filter(cart_id=cart_id, is_active=True, is_deleted=False)
    if not cart_items.exists():
        return Response({"error": "No active cart items found for this cart."}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(float(item.total_price) for item in cart_items)

    # Print the calculated total amount
    print(f"Calculated Total Amount: {total_amount}")

    # Prepare data for serializer
    data = {
        'user_id': user_id,
        'cart_id': cart_id,
        'delivery_address': delivery_address,
        'phone_number': phone_number,
        'total_amount': total_amount
    }

    # Serialize and save the order
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#---------------------------get_order_by_id---------------------------------

@api_view(['GET'])
def get_order_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        order = Order.objects.get(id=id, is_active=True, is_deleted=False)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order)
    return Response(serializer.data)


#----------------------------get_all_orders---------------------------------


@api_view(['GET'])
def get_all_orders(request):
    orders = Order.objects.filter(is_active=True, is_deleted=False)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


#------------------------------update_order_by_id-------------------------------
from decimal import Decimal
@api_view(['PUT'])
def update_order_by_id(request):
    order_id = request.query_params.get('id')
    
    if not order_id:
        return Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        order = Order.objects.get(id=order_id, is_active=True, is_deleted=False)
    except Order.DoesNotExist:
        return Response({"error": "Order not found or is inactive."}, status=status.HTTP_404_NOT_FOUND)

    user_id = request.data.get('user_id', order.user_id.id)  
    cart_id = request.data.get('cart_id', order.cart_id.id)
    delivery_address = request.data.get('delivery_address', order.delivery_address)
    phone_number = request.data.get('phone_number', order.phone_number)

    if not user_id or not cart_id or not delivery_address or not phone_number:
        return Response({"error": "User, cart, delivery address, and phone number are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart = Cart.objects.get(id=cart_id, is_active=True, is_deleted=False)
    except Cart.DoesNotExist:
        return Response({"error": "Cart does not belong to the user or is not active."}, status=status.HTTP_400_BAD_REQUEST)

    cart_items = CartItem.objects.filter(cart_id=cart_id, is_active=True, is_deleted=False)
    if not cart_items.exists():
        return Response({"error": "No active cart items found for this cart."}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = Decimal('0.00')
    for item in cart_items:
        total_amount += Decimal(item.total_price)

    data = {
        'user_id': user_id,
        'cart_id': cart_id,
        'delivery_address': delivery_address,
        'phone_number': phone_number,
        'total_amount': total_amount
    }

    serializer = OrderSerializer(order, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#---------------------------delete_order_by_id----------------------------

@api_view(['DELETE'])
def delete_order_by_id(request):
    id = request.query_params.get('id')

    if not id:
        return Response({"error": "ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(id=id, is_active=True, is_deleted=False)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    order.is_deleted = True
    order.save()
    return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


#---------------------------get_orders_by_user-----------------------------

@api_view(['GET'])
def get_orders_by_user(request):
    user_id = request.query_params.get('id')

    if not user_id:
        return Response({"error": "User ID query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    orders = Order.objects.filter(user_id=user_id, is_active=True, is_deleted=False)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

#-------------------------get_order_statistics---------------------------

from django.db.models import Sum

@api_view(['GET'])
def get_order_statistics(request):
    total_orders = Order.objects.filter(is_active=True, is_deleted=False).count()
    total_revenue = Order.objects.filter(is_active=True, is_deleted=False).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    stats = {
        'total_orders': total_orders,
        'total_revenue': str(total_revenue)
    }
    return Response(stats)

