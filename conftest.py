import pytest
from pytest_mock import MockerFixture
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from points.models import PointsConfig
from vouchers.models import Voucher
from transactions.models import PaymentTransaction
from decimal import Decimal

User = get_user_model()

@pytest.fixture
def api_client():
    """Return an authenticated API client."""
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an admin-authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def user():
    """Create and return a regular user in both databases."""
    user = User.objects.create_user(
        id=2,
        username='testuser',
        email='test@example.com',
        password='password123',
        points_balance=Decimal('1000.00'),
        membership_status='Bronze'
    )
    # Ensure user exists in the warehouse database as well
    User.objects.using('warehouse').create(
        id=2,  # Use the same ID
        username='testuser',
        email='test@example.com',
        password='password123',
        points_balance=Decimal('1000.00'),
        membership_status='Bronze'
    )
    return user

@pytest.fixture
def admin_user():
    """Create and return an admin user."""
    return User.objects.create_user(
        id=1,
        username='adminuser',
        email='admin@example.com',
        password='password123',
        is_staff=True,
        is_admin=True,
        points_balance=Decimal('5000.00'),
        membership_status='Gold'
    )

@pytest.fixture
def points_config_bronze():
    """Create and return a Bronze points configuration."""
    return PointsConfig.objects.create(
        membership_level='bronze',
        multiplier=Decimal('1.00'),
        threshold=Decimal('10000.00')
    )

@pytest.fixture
def points_config_silver():
    """Create and return a Silver points configuration."""
    return PointsConfig.objects.create(
        membership_level='silver',
        multiplier=Decimal('1.50'),
        threshold=Decimal('50000.00')
    )

@pytest.fixture
def points_config_gold():
    """Create and return a Gold points configuration."""
    return PointsConfig.objects.create(
        membership_level='gold',
        multiplier=Decimal('2.00'),
        threshold=Decimal('100000.00')
    )

@pytest.fixture
def voucher():
    """Create and return a voucher."""
    return Voucher.objects.create(
        name='Test Voucher',
        description='A test voucher for testing',
        points_required=Decimal('500.00')
    )

@pytest.fixture
def transaction(user):
    """Create and return a payment transaction."""
    return PaymentTransaction.objects.using('warehouse').create(
        user=user,
        amount=Decimal('100.00'),
        points_earned=Decimal('100.00'),
        payment_method='Dummy Credit Card',
        status='Success'
    )

@pytest.fixture
def mock_warehouse_connection(mocker: MockerFixture):
    """Mock warehouse connection for tests."""
    mock = mocker.patch('django.db.connections')
    return mock
