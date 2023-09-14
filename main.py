import asyncio

from binance_websocket.binance_candlesticks import BinanceCandlestickWebSocket
from bitfinex_websocket.bitfinex_candles import BitfinexWebSocketClient


async def main():
    binance_ws = BinanceCandlestickWebSocket("BTCUSDT", "1m", 14)
    bitfinex_ws = BitfinexWebSocketClient(
        currency_pair="tBTCUSD", timeframe="1m"
    )

    await asyncio.gather(
        binance_ws.connect(),
        bitfinex_ws.connect()
    )


if __name__ == '__main__':
    asyncio.run(main())
