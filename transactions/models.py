from django.db import models
from django.conf import settings

class PaymentTransaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Points', 'Points'),
        ('Dummy Virtual Account', 'Dummy Virtual Account'),
        ('Dummy Credit Card', 'Dummy Credit Card'),
    ]
    STATUS_CHOICES = [
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    points_used = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    failure_reason = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Simulate writing transaction details to the data warehouse.
        try:
            from django.db import connections
            with connections['warehouse'].cursor() as cursor:
                cursor.execute(
                    "INSERT INTO payment_transaction (id, user_id, timestamp, amount, points_used, points_earned, payment_method, status, failure_reason) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [self.id, self.user.id, self.timestamp, self.amount, self.points_used, self.points_earned, self.payment_method, self.status, self.failure_reason]
                )
        except Exception as e:
            # Log the error but don't stop the transaction from being saved
            print(f"Warehouse write error: {e}")
