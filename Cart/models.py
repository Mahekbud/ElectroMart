from django.db import models
import uuid
from django.utils import timezone

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey('UserAuth.User', on_delete=models.CASCADE,related_name='Cart')
    create_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart for user ID {self.user_id.id}"





