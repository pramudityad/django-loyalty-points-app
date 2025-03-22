import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

@pytest.mark.django_db(databases=['default', 'warehouse'])
class TestUserViews:
    def test_user_detail_admin_access(self, admin_client, user):
        """Test that admin users can access user details (profile)."""
        url = reverse('profile')  
        response = admin_client.get(url, args=[user.id])
        assert response.status_code == status.HTTP_200_OK

    def test_user_detail_own_profile(self, authenticated_client, user):
        """Test that users can access their own profile."""
        url = reverse('profile')
        response = authenticated_client.get(url, args=[user.id])
        assert response.status_code == status.HTTP_200_OK

    def test_create_user_admin(self, admin_client):
        """Test that admin users can create new users."""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'points_balance': '0.00',
            'membership_status': 'Bronze'
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='newuser').exists()

    # def test_update_user_admin(self, admin_client, user):
    #     """Test that admin users can update users (profile)."""
    #     url = reverse('profile')
    #     data = {
    #         'username': user.username + "new",
    #         'email': user.email,
    #     }
    #     response = admin_client.patch(url, data)
    #     assert response.status_code == status.HTTP_200_OK
    #     user.refresh_from_db()
    #     assert user.points_balance == Decimal('2000.00')
    #     assert user.membership_status == 'Silver'

    #     response = admin_client.delete(url)
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #     assert not User.objects.filter(username='todelete').exists()
