from django.db import models
from django.utils import timezone
import uuid



class Shipping(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey('Order.Order', on_delete=models.CASCADE, related_name='shipping')
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=255)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    tracking_number = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20,default='PENDING')
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)



    def __str__(self):
        return f"Shipping for Order {self.order.id} - {self.status}"
