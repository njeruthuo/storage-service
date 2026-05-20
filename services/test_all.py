import pytest
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient
from .models import DateStorage


@pytest.mark.django_db
class TestDateStorageSingleton:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()

        # Hardcoded default DRF router path structures.
        # Adjust /api/ if your base endpoints are nested inside an API prefix.
        self.list_url = "/datestorage/"

        # Base setup dates
        self.start = timezone.now().replace(year=2026, month=5, day=20, hour=10, minute=0)
        self.end = timezone.now().replace(year=2026, month=5, day=20, hour=16, minute=0)

    def test_model_normalization_on_save(self):
        """Verify times force to 07:30 and 17:30 respectively on save."""
        instance = DateStorage.objects.create(
            start_date=self.start, end_date=self.end)

        assert instance.start_date.hour == 7
        assert instance.start_date.minute == 30
        assert instance.end_date.hour == 17
        assert instance.end_date.minute == 30

    def test_model_prevents_multiple_rows_via_orm(self):
        """Verify the database layer actively blocks a second row creation."""
        DateStorage.objects.create(start_date=self.start, end_date=self.end)

        with pytest.raises(ValidationError):
            DateStorage.objects.create(
                start_date=self.start, end_date=self.end)

    def test_api_can_create_first_row(self):
        """Verify the API successfully creates the item when the table is empty."""
        assert DateStorage.objects.count() == 0

        data = {
            "start_date": self.start.isoformat(),
            "end_date": self.end.isoformat()
        }
        response = self.client.post(self.list_url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert DateStorage.objects.count() == 1

    def test_api_rejects_second_row_creation(self):
        """Verify API blocks POST request if a row already exists."""
        DateStorage.objects.create(start_date=self.start, end_date=self.end)

        data = {
            "start_date": self.start.isoformat(),
            "end_date": self.end.isoformat()
        }
        response = self.client.post(self.list_url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert DateStorage.objects.count() == 1

    def test_api_can_read_and_update_existing_row(self):
        """Verify that the single existing row can be read and updated successfully."""
        existing = DateStorage.objects.create(
            start_date=self.start, end_date=self.end)
        detail_url = f"{self.list_url}{existing.pk}/"

        # Test READ (GET)
        get_response = self.client.get(detail_url)
        assert get_response.status_code == status.HTTP_200_OK

        # Test UPDATE (PATCH)
        new_end = self.end.replace(hour=12, minute=0)
        patch_data = {"end_date": new_end.isoformat()}

        patch_response = self.client.patch(detail_url, patch_data)
        assert patch_response.status_code == status.HTTP_200_OK

        existing.refresh_from_db()
        assert existing.end_date.hour == 17

    def test_api_can_delete_existing_row(self):
        """Verify that the single row can be deleted, leaving the table empty."""
        existing = DateStorage.objects.create(
            start_date=self.start, end_date=self.end)
        detail_url = f"{self.list_url}{existing.pk}/"

        assert DateStorage.objects.count() == 1

        delete_response = self.client.delete(detail_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        assert DateStorage.objects.count() == 0
