import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

@pytest.mark.django_db(databases=['default', 'warehouse'])
class TestUserModel:
    def test_create_user(self):
        """Test creating a new user."""
        user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='testpass123'
        )
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_admin is False
        assert user.points_balance == Decimal('0.00')
        assert user.membership_status == 'Bronze'
        assert user.check_password('testpass123')

    def test_create_superuser(self):
        """Test creating a new superuser."""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        assert admin.username == 'admin'
        assert admin.email == 'admin@example.com'
        assert admin.is_active is True
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.points_balance == Decimal('0.00')
        assert admin.membership_status == 'Bronze'

    def test_update_membership_status_bronze(self):
        """Test updating membership status to Bronze."""
        user = User.objects.create_user(
            username='bronze',
            email='bronze@example.com',
            password='testpass123',
            points_balance=Decimal('10000.00')
        )
        user.update_membership_status()
        assert user.membership_status == 'Bronze'

    def test_update_membership_status_silver(self):
        """Test updating membership status to Silver."""
        user = User.objects.create_user(
            username='silver',
            email='silver@example.com',
            password='testpass123',
            points_balance=Decimal('50000.00')
        )
        user.update_membership_status()
        assert user.membership_status == 'Silver'

    def test_update_membership_status_gold(self):
        """Test updating membership status to Gold."""
        user = User.objects.create_user(
            username='gold',
            email='gold@example.com',
            password='testpass123',
            points_balance=Decimal('100000.00')
        )
        user.update_membership_status()
        assert user.membership_status == 'Gold'

    def test_email_unique(self, user):
        """Test that email must be unique."""
        with pytest.raises(Exception):
            User.objects.create_user(
                username='anotheruser',
                email='test@example.com',  # Same email as fixture user
                password='testpass123'
            )
