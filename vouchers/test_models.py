import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError
from vouchers.models import Voucher

@pytest.mark.django_db
class TestVoucherModel:
    def test_create_voucher(self):
        """Test creating a new voucher."""
        voucher = Voucher.objects.create(
            name='Test Voucher',
            description='Test Description',
            points_required=500.00
        )
        assert voucher.name == 'Test Voucher'
        assert voucher.points_required == Decimal('500.00')
        assert str(voucher) == 'Test Voucher'

    def test_points_required_positive(self):
        """Test voucher requires positive points."""
        voucher = Voucher(
            name='Invalid Voucher',
            description='Test',
            points_required=-100.00
        )
        with pytest.raises(ValidationError):
            voucher.full_clean()
