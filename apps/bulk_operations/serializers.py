from rest_framework import serializers
from .models import ImportJob


class ImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        fields = ['id', 'user', 'file', 'file_type', 'status', 'file_name', 'total_rows', 'processed_rows', 'success_count', 'error_count', 'errors', 'created_at', 'completed_at']
        read_only_fields = ['id', 'created_at', 'completed_at']


class ImportCreateSerializer(serializers.Serializer):
    file = serializers.FileField()
    file_type = serializers.ChoiceField(choices=ImportJob.FILE_TYPE_CHOICES)
