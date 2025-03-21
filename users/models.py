from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    email = models.EmailField(unique=True)
    points_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    membership_status = models.CharField(max_length=20, default='Bronze')
    is_admin = models.BooleanField(default=False)

    def update_membership_status(self):
        if self.points_balance >= 100000:
            self.membership_status = 'Gold'
        elif self.points_balance >= 50000:
            self.membership_status = 'Silver'
        else:
            self.membership_status = 'Bronze'
        self.save()

    def calculate_points_earned(self, transaction_amount):
        """Calculate points earned based on transaction amount and membership level."""
        # Dummy implementation for now, will be updated later
        return transaction_amount * Decimal('1.0')

    def redeem_points(self, points_to_redeem):
        """Redeem points, reducing the points balance."""
        # Dummy implementation for now, will be updated later
        if self.points_balance >= points_to_redeem:
            self.points_balance -= points_to_redeem
            self.save()
        else:
            raise ValueError("Insufficient points to redeem.")
