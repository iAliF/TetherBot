import logging

from rich.logging import RichHandler
from telegram.ext import Updater, Dispatcher

import config

logging.basicConfig(
    level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    updater = Updater(config.BOT_TOKEN)
    dp: Dispatcher = updater.dispatcher
