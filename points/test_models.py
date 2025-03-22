import pytest
from decimal import Decimal
from points.models import PointsConfig

@pytest.mark.django_db
class TestPointsConfigModel:
    def test_create_points_config(self):
        """Test creating a new points configuration."""
        config = PointsConfig.objects.create(
            membership_level='bronze',
            multiplier=1.5,
            threshold=10000.00
        )
        assert config.membership_level == 'bronze'
        assert config.multiplier == Decimal('1.5')
        assert config.threshold == Decimal('10000.00')
        assert str(config) == 'bronze'

    def test_unique_membership_level(self):
        """Test membership level uniqueness constraint."""
        PointsConfig.objects.create(
            membership_level='silver',
            multiplier=1.5,
            threshold=50000.00
        )
        with pytest.raises(Exception):
            PointsConfig.objects.create(
                membership_level='silver',
                multiplier=2.0,
                threshold=60000.00
            )

@pytest.mark.django_db(databases=['default', 'warehouse'])
class TestPointsCalculations:
    from decimal import Decimal
    def test_points_earned_calculation(self, user, points_config_bronze):
        """Test points earned calculation based on membership level."""
        transaction_amount = Decimal('1000.00')
        expected_points = transaction_amount * Decimal(str(points_config_bronze.multiplier))
        assert user.calculate_points_earned(transaction_amount) == expected_points

    def test_points_redemption(self, user, voucher):
        """Test successful points redemption."""
        initial_balance = user.points_balance
        user.redeem_points(voucher.points_required)
        user.refresh_from_db()
        assert user.points_balance == initial_balance - voucher.points_required

    def test_insufficient_points_redemption(self, user, voucher):
        """Test redemption with insufficient points."""
        user.points_balance = Decimal('100.00')
        user.save()
        with pytest.raises(ValueError):
            user.redeem_points(voucher.points_required)
