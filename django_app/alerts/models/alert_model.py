from django.db import models


class Alert(models.Model):

    class LevelOfSeverity(models.TextChoices):
        LOW = "Low", "Low"
        HIGH = "High", "High"

    level_of_severity = models.CharField(
        max_length=10,
        choices=LevelOfSeverity.choices,
        default=LevelOfSeverity.LOW,
    )

    detected_at = models.DateTimeField()

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

    def __str__(self):
        return f"Alert=<detected_at='{self.detected_at}', level_of_severity='{self.level_of_severity}'>"
