import atexit
import asyncio
from django.apps import AppConfig
from django.conf import settings
from telegram.ext import Application

class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self) -> None:
        from telegram_bot.handlers import app
        
        if not settings.TELEGRAM_WEBHOOK_URL:
            return # Caso a URL do webhook não esteja definida, não faz nada
        
        asyncio.create_task(self.setup_bot(
            app=app,
            url=settings.TELEGRAM_WEBHOOK_URL, 
            max_conn=settings.TELEGRAM_MAX_CONNECTIONS,
        ))

        async def shutdown_hook():
            try:
                await app.bot.deleteWebhook()
            except Exception:
                pass
        
        atexit.register(lambda: asyncio.run(shutdown_hook()))

    async def setup_bot(self, app: Application, url: str, max_conn: int) -> None:
        await asyncio.gather(
            app.bot.setWebhook(url=url, max_connections=max_conn),
            app.initialize(),
            app.bot.initialize(),
        )
