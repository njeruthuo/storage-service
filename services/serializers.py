from rest_framework import serializers
from .models import DateStorage


class DateStorageSerializer(serializers.ModelSerializer):
    # Optional: Format the output strings for easier frontend consumption
    start_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=True)
    end_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", required=True)

    class Meta:
        model = DateStorage
        fields = ['id', 'start_date', 'end_date']

    def validate(self, data):
        start = data.get('start_date') or (
            self.instance.start_date if self.instance else None)
        end = data.get('end_date') or (
            self.instance.end_date if self.instance else None)

        if start and end and start >= end:
            raise serializers.ValidationError({
                "end_date": "The competition end date must be after the start date."
            })
        return data
