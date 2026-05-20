from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DateStorageViewSet

router = DefaultRouter()
router.register(r'datestorage', DateStorageViewSet, basename='datestorage')

urlpatterns = [
    path('', include(router.urls)),
]
