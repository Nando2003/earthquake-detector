from telegram import Update
from telegram.ext import ContextTypes


async def noop(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()  # type: ignore
    noop_message = (
        "<b>Você já realizou esta ação.</b>"
        " Para alterar sua inscrição, utilize o comando /start novamente."
    )
    
    query = update.callback_query
    await query.message.reply_text(noop_message, parse_mode='HTML')  # type: ignore
