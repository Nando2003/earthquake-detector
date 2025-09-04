from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from django.db import transaction
from subscribers.models import Subscriber
from asgiref.sync import sync_to_async


async def subscribe(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer() # type: ignore

    user_telegram_id = str(update.effective_user.id) # type: ignore

    def db_action(telegram_id: str):
        with transaction.atomic():
            subscriber, created = Subscriber.objects.get_or_create(
                contact=telegram_id,
                contact_type=Subscriber.ContactTypes.TELEGRAM,
                defaults={'show_alerts': True}
            )
            if not created:
                subscriber.show_alerts = not subscriber.show_alerts
                subscriber.contact_type = Subscriber.ContactTypes.TELEGRAM
                subscriber.save()

            return subscriber

    subscriber = await sync_to_async(db_action)(user_telegram_id)
    query = update.callback_query

    message_mapper = {
        True: 'Inscrito ✅',
        False: 'Desinscrito ❌',
    }

    disabled_btn = InlineKeyboardButton(text=message_mapper[subscriber.show_alerts], callback_data="noop")
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[disabled_btn]])) # type: ignore
