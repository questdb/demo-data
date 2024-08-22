#
# This product based on cryptofeed https://github.com/bmoscon/cryptofeed software developed by Bryant Moscon (http://www.bryantmoscon.com/) Copyright (C) 2017-2022 Bryant Moscon - bmoscon@gmail.com
#
import argparse
import os

from cryptofeed import FeedHandler
from cryptofeed.backends.backend import BackendCallback
from cryptofeed.backends.socket import SocketCallback
from cryptofeed.defines import TRADES
from cryptofeed.exchanges import OKX


QUEST_HOST = '127.0.0.1'
QUEST_PORT = 9009


class QuestCallback(SocketCallback):
    def __init__(self, host='127.0.0.1', port=9009, **kwargs):
        super().__init__(f"tcp://{host}", port=port, **kwargs)
        self.numeric_type = float
        self.none_to = None

    async def writer(self):
        while True:
            try:
                await self.connect()
            except:
                exit(-1)
            async with self.read_queue() as update:
                update = "\n".join(update) + "\n"
                try:
                    self.conn.write(update.encode())
                except:
                    exit(-2)

class TradeQuest(QuestCallback, BackendCallback):
    default_key = 'trades'

    async def write(self, data):
        update = f'{self.key},symbol={data["symbol"]},side={data["side"]} price={data["price"]},amount={data["amount"]} {int(data["timestamp"] * 1_000_000_000)}'
        await self.queue.put(update)


def main():
    host = os.getenv("QUEST_HOST", default=QUEST_HOST)
    port = os.getenv("QUEST_PORT", default=QUEST_PORT)

    parser = argparse.ArgumentParser()
    parser.add_argument('symbols', nargs='+', help='')

    hanlder = FeedHandler()
    hanlder.add_feed(OKX(channels=[TRADES], symbols=[
        'ADA-USDC'
        'ADA-USDT',
        'ADA-USDT',
        'AVAX-USDT',
        'BTC-USDC',
        'BTC-USDT',
        'BTC-USDT',
        'DAI-USDT',
        'DOGE-USDT',
        'DOT-USDT',
        'ETH-DAI',
        'ETH-USDC',
        'ETH-USDT',
        'ETH-USDT',
        'LTC-USDT',
        'MATIC-USDT',
        'SHIB-USDT',
        'SOL-BTC',
        'SOL-ETH',
        'SOL-USDT',
        'UNI-USDT',
        'USDT-USDC',
        'XLM-USDT',
        #'ADA-BTC',
        #'AVAX-BTC',
        #'DOGE-BTC',
        #'DOT-BTC',
        #'ETH-BTC',
        #'LTC-BTC',
        #'MATIC-BTC',
        #'UNI-BTC',
        #'XLM-BTC',
        ],
        callbacks={TRADES: TradeQuest(host=host,
        port=port)}))
    hanlder.run()


if __name__ == '__main__':
    main()
