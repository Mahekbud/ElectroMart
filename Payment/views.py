# from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .models import Payment, Order


#-=--------------------------------------------------------------------------------------

# @api_view(['POST'])
# def create_payment(request):
#     data = request.data
#     order = get_object_or_404(Order, id=data.get('order_id'))
#     user = request.user

#     payment = Payment.objects.create(
#         user_id=user,
#         order=order,
#         amount=data.get('amount'),
#         currency=data.get('currency', 'USD'),
#         payment_method=data.get('payment_method'),
#         payment_status=data.get('payment_status', 'pending'),
#         transaction_id=data.get('transaction_id')
#     )

#     return Response({'payment_id': payment.id}, status=status.HTTP_201_CREATED)



#-----------------------------------------------------------
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from Order.models import Order
from Shipping.models import Shipping

@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def create_payment(request):
    required_fields = ['shipping_id', 'order_id', 'amount', 'currency', 'payment_method', 'payment_status']
    missing_fields = [field for field in required_fields if field not in request.data]

    if missing_fields:
        return Response({"detail": f"Missing fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if request.user.is_anonymous:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        order = Order.objects.get(id=request.data.get('order_id'))
        shipping = Shipping.objects.get(id=request.data.get('shipping_id'))

        payment = Payment.objects.create(
            user_id=request.user,  
            shipping_id=shipping, 
            order_id=order,  
            amount=request.data.get('amount'),
            currency=request.data.get('currency'),
            payment_method=request.data.get('payment_method'),
            payment_status=request.data.get('payment_status'),
            transaction_id=request.data.get('transaction_id', "")
        )

        return Response({"detail": "Payment created successfully"}, status=status.HTTP_201_CREATED)

    except Order.DoesNotExist:
        return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    except Shipping.DoesNotExist:
        return Response({"detail": "Shipping not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)



