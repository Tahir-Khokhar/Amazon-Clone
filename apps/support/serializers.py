from rest_framework import serializers
from .models import FAQ, SupportTicket, TicketMessage


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = '__all__'
        read_only_fields = ['id', 'created_at']
