from django.db import models

class Voucher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
