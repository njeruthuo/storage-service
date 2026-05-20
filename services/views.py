from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import DateStorage
from .serializers import DateStorageSerializer


class DateStorageViewSet(viewsets.ModelViewSet):
    queryset = DateStorage.objects.all().order_by('-start_date')
    serializer_class = DateStorageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            from rest_framework.exceptions import ValidationError as DRFValidationError
            raise DRFValidationError({"detail": e.message})
