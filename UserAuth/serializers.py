from rest_framework import serializers
from .models import User,Otp


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'
        
        
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'
        

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

