from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

class Voucher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return self.name
