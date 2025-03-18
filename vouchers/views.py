from rest_framework import viewsets, permissions
from .models import Voucher
from .serializers import VoucherSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class VoucherViewSet(viewsets.ModelViewSet):
    queryset = Voucher.objects.all()
    serializer_class = VoucherSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def redeem(self, request, pk=None):
        voucher = self.get_object()
        user = request.user
        
        # Log initial state
        print(f"[VOUCHER DEBUG] User: {user.username}, Voucher: {voucher.name}")
        print(f"[VOUCHER DEBUG] Points required: {voucher.points_required}, User balance: {user.points_balance}")
        
        if user.points_balance < voucher.points_required:
            print(f"[VOUCHER DEBUG] Redemption failed: Insufficient points")
            return Response({"detail": "Insufficient points."}, status=400)
        
        # Deduct points
        old_balance = user.points_balance
        user.points_balance -= voucher.points_required
        user.save()
        
        print(f"[VOUCHER DEBUG] Redemption successful: Balance {old_balance} -> {user.points_balance}")
        return Response({"detail": f"Voucher '{voucher.name}' redeemed successfully."})