from django.contrib.auth.models import AbstractUser
from django.db import models

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
