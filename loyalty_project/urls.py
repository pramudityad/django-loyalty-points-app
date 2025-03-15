from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from loyalty_project.views import CeleryStatusView
from django.http import HttpResponse

schema_view = get_schema_view(
   openapi.Info(
      title="Loyalty Points and Digital Payment API",
      default_version='v1',
      description="API documentation for the loyalty points system",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def home(request):
    return HttpResponse("<h1>Welcome to the Loyalty Points System</h1>")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('transactions.urls')),
    path('api/', include('vouchers.urls')),
    path('api/', include('points.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/celery-status/', CeleryStatusView.as_view(), name='celery-status'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
