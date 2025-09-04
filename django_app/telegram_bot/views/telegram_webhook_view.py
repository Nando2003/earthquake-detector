import json

from asgiref.sync import async_to_sync

from telegram import Update
from telegram_bot.handlers import app

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.TELEGRAM_WEBHOOK_URL:
            return Response({'error': 'TELEGRAM_WEBHOOK_URL is not set'}, status.HTTP_503_SERVICE_UNAVAILABLE)
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(data, app.bot)
            async_to_sync(app.process_update)(update)
            return Response({'status': 'ok'})
        
        except Exception as e:
            return Response({'error': str(e)}, status.HTTP_400_BAD_REQUEST)

    def get(self, _):
        return Response({'error': 'Only POST method is allowed'}, status.HTTP_400_BAD_REQUEST)
    