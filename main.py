import threading

from binance_websocket.binance_candlesticks import BinanceCandlestickWebSocket
from bitfinex_websocket.bitfinex_candles import BitfinexWebSocketClient


def main():
    binance_ws = BinanceCandlestickWebSocket("BTCUSDT", "5m", 14)
    bitfinex_ws = BitfinexWebSocketClient(currency_pair="tBTCUSD", timeframe="1m")

    binance_thread = threading.Thread(target=binance_ws.connect)
    bitfinex_thread = threading.Thread(target=bitfinex_ws.connect)
    binance_thread.start()
    bitfinex_thread.start()


if __name__ == '__main__':
    main()
