from django.db import models

class PointsConfig(models.Model):
    MEMBERSHIP_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]
    membership_level = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, unique=True)
    multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    threshold = models.DecimalField(max_digits=10, decimal_places=2, default=10000)

    def __str__(self):
        return self.membership_level
