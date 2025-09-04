from telegram import Bot
from django.conf import settings
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

from .start_handler import start
from .subscribe_handler import subscribe
from .noop_handler import noop

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

app = (
    ApplicationBuilder()
    .token(settings.TELEGRAM_BOT_TOKEN)
    .build()
)

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(subscribe, pattern="subscribe_toggle"))
app.add_handler(CallbackQueryHandler(noop, pattern="noop"))
