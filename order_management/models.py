from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    ORDER_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_filled', 'Partially Filled'),
        ('filled', 'Filled'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    instrument = models.CharField(max_length=10)  # e.g., EUR_USD
    price = models.DecimalField(max_digits=10, decimal_places=5)
    quantity = models.BigIntegerField()
    filled_quantity = models.BigIntegerField(default=0)  # Quantity that has been filled
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.order_type.capitalize()} {self.quantity} of {self.instrument} at {self.price}"


    def remaining_quantity(self):
        return self.quantity - self.filled_quantity