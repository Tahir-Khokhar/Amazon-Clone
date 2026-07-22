from rest_framework import serializers


class UtilitySerializer(serializers.Serializer):
    message = serializers.CharField()
