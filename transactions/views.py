from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import PaymentTransactionSerializer
from .models import PaymentTransaction
from django.contrib.auth import get_user_model
from decimal import Decimal
from points.models import PointsConfig

User = get_user_model()

class PaymentTransactionCreateView(generics.CreateAPIView):
    serializer_class = PaymentTransactionSerializer

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        # Log initial state for debugging
        print(f"[POINTS DEBUG] Initial points balance: {user.points_balance}")
        print(f"[POINTS DEBUG] Transaction: {data['payment_method']}, Amount: {data['amount']}")

        # If payment is using points
        if data['payment_method'] == 'Points':
            # Use points_used from request if provided, otherwise use amount
            points_to_use = data.get('points_used') if data.get('points_used') else data['amount']
            print(f"[POINTS DEBUG] Points to use: {points_to_use}, Current balance: {user.points_balance}")
            
            if user.points_balance < points_to_use:
                print(f"[POINTS DEBUG] Insufficient points!")
                serializer.save(user=user, status='Failed', failure_reason='Insufficient points')
                return
                
            # Deduct points from user balance
            user.points_balance -= points_to_use
            print(f"[POINTS DEBUG] New balance after deduction: {user.points_balance}")
            user.save()
            
            # Save transaction with points_used field updated
            transaction = serializer.save(user=user, points_used=points_to_use, status='Success')
            return

        # For non-points payments, calculate points earned using the admin-configured rules
        try:
            # Get points configuration based on user's membership level
            config = PointsConfig.objects.get(membership_level=user.membership_status.lower())
            
            # Calculate points earned using the threshold and multiplier from config
            # Formula: (Amount / Threshold) * Multiplier
            points_earned = (data['amount'] / config.threshold) * config.multiplier
            print(f"[POINTS DEBUG] Points earned: {points_earned}")
            
        except PointsConfig.DoesNotExist:
            # Fallback to default if no configuration exists
            points_earned = data['amount'] / 10000  # Default threshold of 10,000
            print(f"[POINTS DEBUG] Using default calculation: {points_earned}")
        
        # Save transaction with earned points
        transaction = serializer.save(user=user, points_earned=points_earned, status='Success')
        
        # Update user's points balance and membership status
        old_balance = user.points_balance
        user.points_balance += Decimal(str(points_earned))
        print(f"[POINTS DEBUG] Points balance updated: {old_balance} -> {user.points_balance}")
        user.update_membership_status()


class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)