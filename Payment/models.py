from django.db import models
from django.utils import timezone
import uuid




class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('UserAuth.User', on_delete=models.CASCADE, null=True, blank=True)  # Foreign key to User model
    order_id = models.ForeignKey('Order.Order', on_delete=models.CASCADE, null=True, blank=True)
    shipping_id = models.ForeignKey('Shipping.Shipping', on_delete=models.SET_NULL, null=True, blank=True) # Foreign key to Order model
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in your currency
    currency = models.CharField(max_length=10, default='USD')  # Default currency
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, default='pending')  # e.g., 'pending', 'completed', 'failed'
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)  # ID from payment gateway
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount} {self.currency}"

