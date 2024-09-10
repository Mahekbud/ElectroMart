from django.db import models
from django.utils import timezone
import uuid

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('UserAuth.User', on_delete=models.CASCADE, related_name='orders')
    cart_id = models.ForeignKey('Cart.Cart', on_delete=models.CASCADE, related_name='orders')
    delivery_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),], default='Pending')
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    

    def __str__(self):
        return f"Order {self.id} for User {self.user.id}"
