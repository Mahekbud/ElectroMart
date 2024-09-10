# Generated by Django 5.1 on 2024-08-30 10:05

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Cart', '0002_alter_cart_user_id'),
        ('UserAuth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('delivery_address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Cart.cart')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='UserAuth.user')),
            ],
        ),
    ]