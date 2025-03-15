from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import PaymentTransactionSerializer
from .models import PaymentTransaction
from django.contrib.auth import get_user_model

User = get_user_model()

class PaymentTransactionCreateView(generics.CreateAPIView):
    serializer_class = PaymentTransactionSerializer

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        # If payment is using points, verify sufficient balance.
        if data['payment_method'] == 'Points':
            if user.points_balance < data['amount']:
                serializer.save(user=user, status='Failed', failure_reason='Insufficient points')
                return
            user.points_balance -= data['amount']
            user.save()

        # Award points based on membership level
        multiplier = 1
        if user.membership_status == 'Silver':
            multiplier = 1.5
        elif user.membership_status == 'Gold':
            multiplier = 2
        points_earned = (data['amount'] / 10000) * multiplier

        serializer.save(user=user, points_earned=points_earned, status='Success')
        # Update user's points balance and membership status
        user.points_balance += points_earned
        user.update_membership_status()

class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)
