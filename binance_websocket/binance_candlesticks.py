from typing import List, Dict

import json
import websocket
import pandas as pd
import pandas_ta as ta


class BinanceCandlestickWebSocket:
    """
    Class for connecting to Binance websocket and calculate RSI based on candlestick data.
    """

    def __init__(self, symbol: str, timeframe: str, rsi_length: int = 14):
        """
        :param symbol: Trading symbol (e.g., "BTCUSDT").
        :param timeframe: Timeframe for candlesticks (e.g. "5m").
        :param rsi_length: Length of RSI calculation period.
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.rsi_length = rsi_length
        self.close_prices: List[float] = []
        self._ws_url = f'wss://stream.binance.com:9443' \
                       f'/ws/{self.symbol.lower()}@kline_{self.timeframe}'

    def connect(self):
        """
        Start WebSocket connection and calculate RSI.
        """
        ws = websocket.WebSocketApp(
            self._ws_url,
            on_message=self._on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            on_open=self.on_open
        )
        ws.run_forever()

    def on_open(self, ws):
        print("WebSocket connection opened")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket connection closed with code {close_status_code}: {close_msg}")

    def on_error(self, ws, error):
        print(f"Error encountered: {error}")

    def _calculate_rsi(self, close_prices: List[float]) -> List[float]:
        """
        Calculate the Relative Strength Index (RSI) based on a list of closing prices.

        :param close_prices: A list of closing prices for RSI.
        :return: The RSI value.
        """
        if len(close_prices) >= self.rsi_length + 1:
            close_series = pd.Series(close_prices)
            return ta.rsi(close_series, length=self.rsi_length).iloc[-1]

    def _process_candlestick_data(self, kline_data: Dict):
        if kline_data["x"]:
            close_price = float(kline_data["c"])
            self.close_prices.append(close_price)
            rsi = self._calculate_rsi(self.close_prices)
            return close_price, rsi
        return None, None

    def _on_message(self, ws, message):
        """
        Process candlestick data from a WebSocket message
        and calculate RSI when a closed candlestick is received.

        :param message: Candlestick data from the WebSocket message.
        """
        data = json.loads(message)
        if "k" in data:
            kline_data = data["k"]
            close_price, rsi = self._process_candlestick_data(kline_data)
            if rsi is not None:
                print('-' * 23)
                print("Binance:")
                print(f"Close Price: {close_price}")
                print(f"RSI: {rsi}")

                self.close_prices = []
