from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointsConfigViewSet

router = DefaultRouter()
router.register(r'points-config', PointsConfigViewSet, basename='points-config')

urlpatterns = [
    path('', include(router.urls)),
]
