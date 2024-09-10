from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shipping
from .serializers import ShippingSerializer
from Order.models import Order



#-------------------------create_shipping-------------------------------


@api_view(['POST'])
def create_shipping(request):
    order_id = request.data.get('order_id')

    try:
        order = Order.objects.get(id=order_id, is_deleted=False)
    except Order.DoesNotExist:
        return Response({'error': 'Order with the given ID does not exist or has been deleted.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ShippingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#----------------------------get_shipping_by_id-----------------------------

@api_view(['GET'])
def get_shipping_by_id(request):
    shipping_id = request.query_params.get('id')  
    
    if not shipping_id:
        return Response({'error': 'ID query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        shipping = Shipping.objects.get(id=shipping_id,is_active=True, is_deleted=False)
    except Shipping.DoesNotExist:
        return Response({'error': 'Shipping record not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ShippingSerializer(shipping)
    return Response(serializer.data, status=status.HTTP_200_OK)

#---------------------------get_all_shipping------------------------------

@api_view(['GET'])
def get_all_shipping(request):
    shipping_records = Shipping.objects.filter(is_active=True, is_deleted=False)
    serializer = ShippingSerializer(shipping_records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

#-----------------------------update_shipping_by_id----------------------------

@api_view(['PUT'])
def update_shipping_by_id(request):
    shipping_id = request.query_params.get('id')
    
    if not shipping_id:
        return Response({'error': 'ID query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        shipping = Shipping.objects.get(id=shipping_id, is_active=True, is_deleted=False)
    except Shipping.DoesNotExist:
        return Response({'error': 'Shipping record not found or has been deleted.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ShippingSerializer(shipping, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#--------------------------delete_shipping_by_id----------------------------

@api_view(['DELETE'])
def delete_shipping_by_id(request):
    shipping_id = request.query_params.get('id')
    
    if not shipping_id:
        return Response({'error': 'ID query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        shipping = Shipping.objects.get(id=shipping_id, is_active=True, is_deleted=False)
    except Shipping.DoesNotExist:
        return Response({'error': 'Shipping record not found or has been deleted.'}, status=status.HTTP_404_NOT_FOUND)

    shipping.is_deleted = True
    shipping.save()
    
    return Response({'message': 'Shipping record marked as deleted.'}, status=status.HTTP_204_NO_CONTENT)

#---------------------------get_shipping_by_status----------------------------------

@api_view(['GET'])
def get_shipping_by_status(request):
    status_filter = request.query_params.get('status')
    
    if not status_filter:
        return Response({'error': 'Status query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    shipping_records = Shipping.objects.filter(status=status_filter, is_active=True, is_deleted=False)
    serializer = ShippingSerializer(shipping_records, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
