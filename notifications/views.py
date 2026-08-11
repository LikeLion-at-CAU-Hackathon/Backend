from rest_framework.generics import ListAPIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.all()