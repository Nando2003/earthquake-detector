from datetime import timedelta
from django.utils import timezone

from asgiref.sync import async_to_sync
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from subscribers.models import Subscriber
from telegram_bot.handlers import bot

from alerts.models import Alert
from alerts.serializers import AlertWebhookSerializer


@method_decorator(csrf_exempt, name='dispatch')
class AlertWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = AlertWebhookSerializer(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data

                if isinstance(validated_data, dict):
                    level = validated_data['level']
                    detected_at = validated_data['detected_at']
                    cutoff = timezone.now() - timedelta(minutes=3)

                    if detected_at < cutoff:
                        return Response({'error': 'Alert is too old'}, status=status.HTTP_400_BAD_REQUEST)

                    alert = Alert.objects.create(
                        level_of_severity=level,
                        detected_at=detected_at
                    )

                    subscribers = Subscriber.objects.filter(show_alerts=True).all()

                    message_contact_type_mapper = {

                        Subscriber.ContactTypes.TELEGRAM.value: {
                            Alert.LevelOfSeverity.LOW.value: (
                                "<b>⚠️ ALERTA DE SISMO FRACO ⚠️</b>\n\n"
                                "Um tremor leve foi detectado na região.\n"
                                "➡️ <i>Mantenha a calma</i> e siga as orientações da equipe de segurança.\n\n"
                                "➡️ Evite elevadores e fique atento a novas instruções.\n\n"
                            ),

                            Alert.LevelOfSeverity.HIGH.value: (
                                "<b>🚨 SISMO FORTE DETECTADO 🚨</b>\n\n"
                                "Um forte tremor foi registrado na sua região.\n\n"
                                "➡️ <b>EVACUE IMEDIATAMENTE O PRÉDIO!</b>\n\n"
                                "➡️ Utilize as rotas de fuga sinalizadas.\n\n"
                                "➡️ Ajude pessoas com dificuldade de locomoção.\n\n"
                                "➡️ Dirija-se a um local aberto e seguro.\n\n"
                            ),
                        },

                    }

                    for subscriber in subscribers:
                        message = message_contact_type_mapper[subscriber.contact_type][alert.level_of_severity]

                        if subscriber.contact_type == Subscriber.ContactTypes.TELEGRAM:
                            async_to_sync(bot.send_message)(subscriber.contact, message, parse_mode='HTML')
                        
                    return Response({'status': 'success', 'alert_id': alert.id}, status=status.HTTP_201_CREATED) # type: ignore

            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, _):
        return Response({'error': 'Only POST method is allowed'}, status=status.HTTP_400_BAD_REQUEST)
