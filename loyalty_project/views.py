from rest_framework.views import APIView
from rest_framework.response import Response
from celery import current_app

class CeleryStatusView(APIView):
    def get(self, request, *args, **kwargs):
        inspector = current_app.control.inspect()
        active = inspector.active() or {}
        scheduled = inspector.scheduled() or {}
        reserved = inspector.reserved() or {}
        return Response({
            "active": active,
            "scheduled": scheduled,
            "reserved": reserved,
        })
