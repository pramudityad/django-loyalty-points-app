from rest_framework import viewsets, permissions
from .models import PointsConfig
from .serializers import PointsConfigSerializer

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class PointsConfigViewSet(viewsets.ModelViewSet):
    queryset = PointsConfig.objects.all()
    serializer_class = PointsConfigSerializer
    permission_classes = [IsAdmin]
