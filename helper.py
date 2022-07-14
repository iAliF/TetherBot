from datetime import datetime

import pytz
from tether import SourceManager
from tether.sources import *

import config


class PriceHelper:
    SOURCES = (ArzPaya, Bitbarg, Hamtapay, Wallex)

    last_time: int = None
    last_text: str = None

    def __init__(self) -> None:
        mngr = SourceManager()
        for source in self.SOURCES:
            mngr.add(source())

        self._manager = mngr

    def generate_text(self) -> str:
        now = datetime.now(pytz.timezone(config.TIMEZONE))
        if self.last_time is not None and now.minute == self.last_time:
            return self.last_text

        p_list = self._manager.get_prices_list()
        prices = ''

        for price in p_list.prices:
            prices += config.PRICE_FORMAT.format(
                source=price.source,
                buy=price.buy,
                sell=price.sell
            )

        self.last_time = now.minute
        self.last_text = config.PRICE_TEXT.format(
            date=now.strftime('%Y/%m/%d'),
            time=now.strftime('%H:%M'),
            prices=prices
        )

        return self.last_text
