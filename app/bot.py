from django.conf import settings
from requests import post
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
from logging.handlers import RotatingFileHandler

BACKUP_COUNT = 5
MAX_LOG_WEIGHT = 52428800

logging.basicConfig(
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    filename="bot_log.log",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    "bot_log.log",
    maxBytes=MAX_LOG_WEIGHT, backupCount=BACKUP_COUNT
)
logger.addHandler(handler)


BOT_TOKEN = settings.BOT_TOKEN

yes = InlineKeyboardButton("Да", callback_data='choice_yes')
no = InlineKeyboardButton("Нет", callback_data='choice_no')
keyboard = InlineKeyboardMarkup([[yes, no]])

async def wake_up(update, context):
    name = update.message.from_user.first_name
    await update.message.reply_text(
        text='Приветствую, {}!'.format(name),
        reply_markup=keyboard,
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'choice_yes':
        post("url/choice_yes", data=...)
    elif query.data == 'choice_no':
        post("url/choice_no", data=...)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', wake_up))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == '__main__':
    main()
