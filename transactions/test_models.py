import pytest
from decimal import Decimal
from transactions.models import PaymentTransaction
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db(databases=['default', 'warehouse'])
User = get_user_model()

@pytest.mark.django_db(databases=['default', 'warehouse'])
class TestPaymentTransactionModel:
    def test_create_transaction(self, user, mock_warehouse_connection):
        """Test creating a payment transaction."""
        transaction = PaymentTransaction.objects.create(
            user=user,
            amount=Decimal('100.00'),
            points_earned=Decimal('100.00'),
            payment_method='Dummy Credit Card',
            status='Success'
        )
        assert transaction.amount == Decimal('100.00')
        assert transaction.points_earned == Decimal('100.00')
        assert transaction.payment_method == 'Dummy Credit Card'
        assert transaction.status == 'Success'
        assert transaction.user == user

    def test_transaction_warehouse_write(self, user, mock_warehouse_connection):
        """Test warehouse write operation on transaction save."""
        transaction = PaymentTransaction(
            user=user,
            amount=Decimal('50.00'),
            points_earned=Decimal('50.00'),
            payment_method='Points',
            status='Success'
        )
        transaction.save()
        mock_warehouse_connection.__getitem__.assert_called_with('warehouse')
        mock_warehouse_connection.__getitem__('warehouse').cursor.assert_called_once()
