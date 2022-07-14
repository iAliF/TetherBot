from datetime import datetime

import pytz
from tether import SourceManager
from tether.sources import *

import config


class PriceHelper:
    SOURCES = (ArzPaya, Bitbarg, Hamtapay, Wallex)

    def __init__(self) -> None:
        mngr = SourceManager()
        for source in self.SOURCES:
            mngr.add(source())

        self._manager = mngr

    def generate_text(self) -> str:
        p_list = self._manager.get_prices_list()
        prices = ''

        for price in p_list.prices:
            prices += config.PRICE_FORMAT.format(
                source=price.source,
                buy=price.buy,
                sell=price.sell
            )

        now = datetime.now(pytz.timezone(config.TIMEZONE))
        return config.PRICE_TEXT.format(
            date=now.strftime('%Y/%m/%d'),
            time=now.strftime('%H:%M'),
            prices=prices
        )
