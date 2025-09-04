from django.urls import path
from alerts.views import AlertWebhookView

urlpatterns = [
    path('webhook/', AlertWebhookView.as_view(), name='alert_webhook'),
]
