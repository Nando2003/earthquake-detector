from rest_framework import serializers
from alerts.models import Alert as AlertModel


class AlertWebhookSerializer(serializers.Serializer):
    level = serializers.ChoiceField(choices=[
        (AlertModel.LevelOfSeverity.LOW, "Low"),
        (AlertModel.LevelOfSeverity.HIGH, "High"),
    ], required=True)
    
    detected_at = serializers.DateTimeField(required=True)
