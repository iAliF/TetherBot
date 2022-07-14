import logging
from datetime import datetime

import pytz
from rich.logging import RichHandler
from telegram import ParseMode, TelegramError, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, Dispatcher, JobQueue, CallbackContext, CommandHandler, MessageHandler, Filters, \
    InlineQueryHandler

import config
from helper import PriceHelper

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)
helper = PriceHelper()

PRICE_BUTTON = '💲 Price 💲'


def start_handler(update: Update, _):
    update.message.reply_text(
        config.START_MESSAGE,
        reply_markup=ReplyKeyboardMarkup([
            [
                PRICE_BUTTON
            ]
        ], True))


def price_handler(update: Update, _):
    update.message.reply_text(helper.generate_text(), parse_mode=ParseMode.MARKDOWN)


def send_job(context: CallbackContext) -> None:
    try:
        context.bot.send_message(config.CHAT_ID, helper.generate_text(), parse_mode=ParseMode.MARKDOWN)
    except TelegramError as err:
        logging.error('Something went wrong ...', exc_info=err)


if __name__ == '__main__':
    updater = Updater(config.BOT_TOKEN)
    dp: Dispatcher = updater.dispatcher
    job_q: JobQueue = updater.job_queue

    # Handlers
    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(MessageHandler(Filters.text(PRICE_BUTTON), price_handler, run_async=True))

    # Jobs
    first = config.INTERVAL - (datetime.now(pytz.timezone(config.TIMEZONE)).minute % config.INTERVAL)
    job_q.run_repeating(
        send_job,
        config.INTERVAL * 60,
        first * 60
    )

    logger.debug('Starting polling (@%s)', updater.bot.get_me().username)
    updater.start_polling()
    updater.idle()
