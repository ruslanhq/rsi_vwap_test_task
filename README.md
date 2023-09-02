# Binance and Bitfinex WebSocket Client

A Python project for connecting to Binance and Bitfinex WebSocket APIs, calculating VWAP and RSI for specified trading pairs and timeframes.

## Overview

This project provides a Python-based WebSocket client for monitoring real-time market data from Binance and Bitfinex cryptocurrency exchanges. It calculates and displays the VWAP (Volume-Weighted Average Price) and RSI (Relative Strength Index) for specified trading pairs and timeframes.

## Features

- Connects to Binance and Bitfinex WebSocket APIs.
- Calculates and displays VWAP and RSI for specified trading pairs.
- Supports customizable timeframes for candlestick data.
- Provides clean and modular code structure.

## Requirements

- Python 3.10 or higher
- Required Python packages: `websocket`, `json`, `pandas`, `pandas_ta`

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/ruslanhq/rsi_vwap_test_task.git
    cd your-repo
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the WebSocket client:

    ```bash
    python main.py
    ```

4. The client will connect to both Binance and Bitfinex WebSocket APIs and display VWAP and RSI data for specified trading pairs and timeframes.

## Configuration

You can customize the following parameters in the `main.py` file:

- `symbol`: Trading pair symbol (e.g., "tBTCUSD" for Bitfinex, "btcusdt" for Binance).
- `interval`: Timeframe for candlesticks (e.g., "1m" for 1 minute, "5m" for 5 minutes).
- `rsi_length`: Length of the RSI calculation (default is 14).
