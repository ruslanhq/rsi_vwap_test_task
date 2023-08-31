import json
from typing import List

import websocket
import pandas as pd
import pandas_ta as ta


class BinanceCandlestickWebSocket:
    """
    Class for connecting to Binance websocket and calculate RSI based on candlestick data.
    """

    def __init__(self, symbol: str, timeframe: str, length: int = 14):
        """
        :param symbol: Trading symbol (e.g. "BTCUSDT").
        :param timeframe: Timeframe for candlesticks (e.g. "5m").
        :param length: Length of RSI calculation period.
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.length = length
        self.close_prices: List[float] = []
        self._ws_url = f'wss://stream.binance.com:9443' \
                       f'/ws/{self.symbol.lower()}@kline_{self.timeframe}'

    def connect(self):
        """
        Start WebSocket connection and calculate RSI.
        """
        ws = websocket.WebSocketApp(
            self._ws_url, on_message=self.on_message, on_close=self.on_close,
            on_error=self.on_error, on_open=self.on_open
        )
        ws.run_forever()

    def on_open(self, ws):
        print("WebSocket connection opened")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket connection closed with code {close_status_code}: {close_msg}")

    def on_error(self, ws, error):
        print(f"Error encountered: {error}")

    def calculate_rsi(self, close_prices: List[float]) -> List[float]:
        close_series = pd.Series(close_prices)
        return ta.rsi(close_series, length=self.length).iloc[-1]

    def on_message(self, ws, message):
        """
        Callback function for processing received data.
        :param ws: WebSocket instance
        :param message: Received message
        """
        data = json.loads(message)
        kline_data = data["k"]

        if kline_data["x"]:
            close_price = float(kline_data["c"])
            self.close_prices.append(close_price)

            if len(self.close_prices) >= self.length + 1:
                rsi = self.calculate_rsi(self.close_prices)
                if rsi is not None:
                    print("Binance:")
                    print(f"Close Price: {close_price}")
                    print(f"RSI: {rsi}")

                    self.close_prices = []
