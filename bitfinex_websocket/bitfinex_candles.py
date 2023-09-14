import json
from typing import List

import pandas_ta as ta
import pandas as pd
import websockets


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

    def _process_candle_data(self, candle_data: List):
        """
        Process candle data and calculate VWAP.
        """
        df = pd.DataFrame(
            [candle_data],
            columns=["mts", "open", "close", "high", "low", "volume"],
        )
        df.set_index(pd.DatetimeIndex(df["mts"]), inplace=True)
        df["vwap"] = ta.vwap(
            low=df.low, close=df.close, volume=df.volume, high=df.high
        )
        vwap = df["vwap"].iloc[-1]
        return df["close"].iloc[-1], vwap

    async def _on_message(self, ws, message):
        """
        Callback function for handling received messages.
        """
        data = json.loads(message)
        print(data)

        if isinstance(data, dict):
            if "event" in data and data["event"] == "subscribed":
                print(f"Subscribed to {data['key']}")

        if isinstance(data, list):
            if data[1] == "hb":
                return

            candle_data = data[1]
            close_price, vwap = self._process_candle_data(candle_data)
            print('-' * 23)
            print("Bitfinex:")
            print(f'Close price: {close_price}')
            print(f"VWAP: {vwap}")

    async def connect(self):
        """
        Connect to Bitfinex websocket API and subscribe to the specified currency pair and timeframe.
        """
        url = f"wss://api-pub.bitfinex.com/ws/2"

        async with websockets.connect(url) as ws:
            print("WebSocket connection opened")

            subscription_message = {
                "event": "subscribe",
                "channel": "candles",
                "key": f"trade:{self.timeframe}:{self.currency_pair}",
            }
            await ws.send(json.dumps(subscription_message))

            while True:
                message = await ws.recv()
                await self._on_message(ws, message)
