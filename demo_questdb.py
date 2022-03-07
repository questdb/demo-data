from cryptofeed import FeedHandler
from cryptofeed.backends.backend import BackendCallback
from cryptofeed.backends.socket import SocketCallback
from cryptofeed.defines import TRADES
from cryptofeed.exchanges import Coinbase

QUEST_HOST = '127.0.0.1'
QUEST_PORT = 9009


class QuestCallback(SocketCallback):
    def __init__(self, host='127.0.0.1', port=9009, **kwargs):
        super().__init__(f"tcp://{host}", port=port, **kwargs)
        self.numeric_type = float
        self.none_to = None

    async def writer(self):
        while True:
            await self.connect()
            count = self.queue.qsize()
            if count == 0:
                count = 1

            async with self.read_many_queue(count) as update:
                update = "\n".join(update) + "\n"
                self.conn.write(update.encode())

    async def write(self, data):
        d = self.format(data)
        timestamp = data["timestamp"]
        timestamp_str = f',timestamp={int(timestamp * 1_000_000_000)}i' if timestamp is not None else ''
        update = f'{self.key},symbol={data["symbol"]} {d}{timestamp_str}'
        await self.queue.put(update)

    def format(self, data):
        ret = []
        for key, value in data.items():
            if key in {'timestamp', 'exchange', 'symbol', 'receipt_timestamp'}:
                continue
            if isinstance(value, str):
                ret.append(f'{key}="{value}"')
            else:
                ret.append(f'{key}={value}')
        return ','.join(ret)


class TradeQuest(QuestCallback, BackendCallback):
    default_key = 'trades'

    def format(self, data):
        return f'side="{data["side"]}",price={data["price"]},amount={data["amount"]}'


def main():
    hanlder = FeedHandler()
    hanlder.add_feed(Coinbase(channels=[TRADES], symbols=['BTC-USD', 'ETH-USD'],
                              callbacks={TRADES: TradeQuest(host=QUEST_HOST, port=QUEST_PORT)}))
    hanlder.run()


if __name__ == '__main__':
    main()
