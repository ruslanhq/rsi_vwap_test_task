from typing import List

import json
import websocket
import pandas_ta as ta
import pandas as pd


class BitfinexWebSocketClient:
    """
    Class for connecting to Bitfinex websocket and calculating VWAP.
    """

    def __init__(self, currency_pair: str, timeframe: str):
        """
        :param currency_pair: Trading pair symbol (e.g., "tBTCUSD")
        :param timeframe: Timeframe for candlesticks (e.g. "1m").
        """
        self.currency_pair = currency_pair
        self.timeframe = timeframe

    def process_candle_data(self, candle_data: List):
        """
        Process candle data and calculate VWAP.
        """
        df = pd.DataFrame(
            [candle_data],
            columns=["mts", "open", "close", "high", "low", "volume"],
        )
        df.set_index(pd.DatetimeIndex(df["mts"]), inplace=True)
        df["vwap"] = ta.vwap(low=df.low, close=df.close, volume=df.volume, high=df.high)
        vwap = df["vwap"].iloc[-1]
        return df["close"].iloc[-1], vwap

    def on_message(self, ws, message):
        """
        Callback function for handling received messages.
        """
        data = json.loads(message)
        candle_data = data[1]
        if isinstance(candle_data, list):
            close_price, vwap = self.process_candle_data(candle_data)
            print('-' * 23)
            print("Bitfinex:")
            print(f'Close price: {close_price}')
            print(f"VWAP: {vwap}")

    def on_open(self, ws):
        """
        Callback function for handling WebSocket open event.
        """
        print("WebSocket connection opened")

        subscription_message = {
            "event": "subscribe",
            "channel": "candles",
            "key": f"trade:{self.timeframe}:{self.currency_pair}",
        }
        ws.send(json.dumps(subscription_message))

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback function for handling WebSocket close event.
        """
        print(
            f"WebSocket connection closed with"
            f" status code {close_status_code}: {close_msg}"
        )

    def on_error(self, ws, error):
        """
        Callback function for handling WebSocket error event.
        """
        print(f"WebSocket error: {error}")

    def connect(self):
        """
        Connect to Bitfinex websocket API and subscribe to the specified currency pair and timeframe.
        """
        url = f"wss://api-pub.bitfinex.com/ws/2"

        ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_error
        )
        ws.run_forever()
