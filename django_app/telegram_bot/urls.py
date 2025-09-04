from django.urls import path
from telegram_bot.views import TelegramWebhookView

urlpatterns = [
    path('webhook/', TelegramWebhookView.as_view(), name='telegram_webhook'),
]
