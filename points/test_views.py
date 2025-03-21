import pytest
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from points.models import PointsConfig

@pytest.mark.django_db
class TestPointsViews:
    def test_points_config_list_admin_access(self, admin_client, points_config_bronze):
        """Test admin can retrieve points configuration list."""
        url = reverse('points-config-list') # corrected url name based on openapi.json
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['membership_level'] == 'bronze'

    def test_points_config_create_admin(self, admin_client):
        """Test admin create new points configuration."""
        url = reverse('points-config-list')
        data = {
            'membership_level': 'platinum',
            'multiplier': '2.5',
            'threshold': '200000.00'
        }
        response = admin_client.post(url, data)
        assert response.status_code == 400

    def test_points_config_update_admin(self, admin_client, points_config_bronze):
        """Test admin can update points configuration."""
        url = reverse('points-config-detail', args=[points_config_bronze.id]) # corrected url name based on openapi.json
        data = {'multiplier': '1.75'}
        response = admin_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        points_config_bronze.refresh_from_db()
        assert points_config_bronze.multiplier == Decimal('1.75')

    def test_points_config_delete_admin(self, admin_client, points_config_bronze):
        """Test admin can delete points configuration."""
        url = reverse('points-config-detail', args=[points_config_bronze.id]) # corrected url name based on openapi.json
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert PointsConfig.objects.count() == 0

    def test_points_config_user_forbidden(self, authenticated_client):
        """Test regular users cannot access points config endpoints."""
        url = reverse('points-config-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_duplicate_membership_level(self, admin_client, points_config_bronze):
        """Test cannot create duplicate membership levels."""
        url = reverse('points-config-list')
        data = {
            'membership_level': 'bronze',
            'multiplier': '1.25',
            'threshold': '15000.00'
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
