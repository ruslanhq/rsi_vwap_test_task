from binance_websocket.binance_candlesticks import BinanceCandlestickWebSocket


def main():
    binance_ws = BinanceCandlestickWebSocket("BTCUSDT", "5m", 14)
    binance_ws.connect()


if __name__ == '__main__':
    main()
