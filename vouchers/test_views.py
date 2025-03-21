import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal

@pytest.mark.django_db
class TestVoucherViews:
    def test_voucher_list(self, authenticated_client, voucher):
        """Test retrieving available vouchers."""
        url = reverse('vouchers_list') # corrected url name based on openapi.json
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Voucher'

    def test_create_voucher_admin(self, admin_client):
        """Test admin creating a new voucher."""
        url = reverse('vouchers_list') # corrected url name based on openapi.json
        data = {
            'name': 'New Voucher',
            'description': 'New Test Voucher',
            'points_required': '1000.00'
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['points_required'] == '1000.00'

    def test_redeem_voucher(self, authenticated_client, user, voucher):
        """Test voucher redemption process."""
        url = reverse('vouchers_redeem', args=[voucher.id]) # corrected url name based on openapi.json
        user.points_balance = voucher.points_required
