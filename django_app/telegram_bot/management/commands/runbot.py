from django.core.management.base import BaseCommand
from telegram_bot.handlers import app as polling_app


class Command(BaseCommand):
    help = "Start the Telegram bot in polling mode."

    def handle(self, *args, **options):
        self.stdout.write("🔄 Starting polling…")
        polling_app.run_polling()
