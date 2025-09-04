from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from subscribers.models import Subscriber


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]: # type: ignore
        return # Evita responder em grupos
    
    user_telegram_id = update.effective_user.id # type: ignore

    is_user_subscribed = await sync_to_async(Subscriber.objects.filter(
        contact=user_telegram_id, 
        show_alerts=True
    ).exists)()

    subscribe_message_mapper = {
        True: (
            "Caso não esteja mais <b>interessado</b> em receber alertas"
            " sugiro que se <b>desinscreva</b> clicando no botão abaixo:"
        ),
        False: (
            "Caso esteja <b>interessado</b> em receber alertas sempre que um tremor for detectado"
            " sugiro que se <b>inscreva</b> clicando no botão abaixo:"
        ),
    }

    subscribe_button_text_mapper = {
        True: "Desinscrever-se",
        False: "Inscrever-se",
    }

    subscribe_message = subscribe_message_mapper[is_user_subscribed]
    subscribe_button_text = subscribe_button_text_mapper[is_user_subscribed]

    greeting_message = (
        "Olá! Eu sou o <b>Earthquake Detector Bot</b> 🤖.\n\n"
        "Eu forneço alertas sobre tremores de terra.\n\n"
    ) + subscribe_message

    subscribe_button = InlineKeyboardButton(
        text=subscribe_button_text,
        callback_data="subscribe_toggle"
    )

    with open("static/bot_logo.jpeg", "rb") as photo_file:
        await update.message.reply_photo(  # type: ignore
            photo=photo_file,
            caption=greeting_message,
            reply_markup=InlineKeyboardMarkup([[subscribe_button]]),
            parse_mode='HTML',
        )
