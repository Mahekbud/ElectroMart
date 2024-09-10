# from rest_framework import serializers
# from .models import Order


# class OrderSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = Order
#         fields = '__all__'
        
        
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user_id', 'cart_id', 'delivery_address', 'phone_number', 'total_amount']
