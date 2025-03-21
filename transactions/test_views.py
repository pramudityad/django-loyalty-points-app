import pytest
import json
from django.urls import reverse
from rest_framework import status
from decimal import Decimal

pytestmark = pytest.mark.django_db(databases=['default', 'warehouse'])
class TestTransactionViews:
    def test_create_transaction(self, authenticated_client, user):
        """Test creating a new transaction."""
        url = reverse('create-transaction') # corrected url name based on openapi.json
        data = {
            'amount': '100.00',
            'points_used': '0',
            'payment_method': 'Dummy Credit Card',
            'status': 'Success',
            'user': user.id
        }

        response = authenticated_client.post(url, json.dumps(data), content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Decimal(response.data['amount']) == Decimal('100.00')

    #def test_transaction_list(self, authenticated_client, transaction):
    #    """Test retrieving user's transactions history."""
    #    url = reverse('transaction-history') # corrected url name based on openapi.json
    #    response = authenticated_client.get(url)
    #    assert response.status_code == status.HTTP_200_OK

    def test_points_redemption_transaction(self, authenticated_client, user, voucher):
        """Test creating a points redemption transaction."""
        user.points_balance = voucher.points_required
        user.save()
        url = reverse('create-transaction')
        data = {
            'payment_method': 'Points',
            'points_used': str(voucher.points_required),
            'voucher': voucher.id,
            'amount': '0', # Assuming points redemption doesn't involve additional amount
            'status': 'Success',
            'user': user.id
        }
        response = authenticated_client.post(url, json.dumps(data), content_type='application/json') # Specify content type
        assert response.status_code == status.HTTP_201_CREATED
        user.refresh_from_db()
        assert user.points_balance == 0

