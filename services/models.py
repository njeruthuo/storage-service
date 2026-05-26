from django.db import models


class DateStorage(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    backup_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.start_date.year} competition"

    def save(self, *args, **kwargs):  # type: ignore
        # Force start time to exactly 07:30:00
        if self.start_date:
            self.start_date = self.start_date.replace(
                second=0, microsecond=0
            )

        # Force end time to exactly 17:30:00 (5:30 PM)
        if self.end_date:
            self.end_date = self.end_date.replace(
                hour=17, minute=30, second=0, microsecond=0
            )

        # Enforce Singleton pattern: block creation if a record already exists
        if not self.pk and DateStorage.objects.exists():
            from django.core.exceptions import ValidationError
            raise ValidationError(
                "Only one DateStorage instance can exist at any time.")

        super().save(*args, **kwargs)  # type: ignore
