from django.db import models


class Subscriber(models.Model):

    class ContactTypes(models.TextChoices):
        SMS = 'sms', 'SMS'
        TELEGRAM = 'telegram', 'Telegram'
        WHATSAPP = 'whatsapp', 'WhatsApp'

    contact = models.TextField(null=False, blank=False, unique=True)
    contact_type = models.CharField(max_length=50, choices=ContactTypes.choices)
    show_alerts = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'subscriber'
        verbose_name_plural = 'subscribers'
    
    def __str__(self):
        return f"Subscriber<contact='{self.contact}', contact_type='{self.contact_type}'>"
    