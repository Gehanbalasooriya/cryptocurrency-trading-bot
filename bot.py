import os
from binance.client import Client
from binance.enums import *
import pyttsx3

# API keys
api_key = ''
api_secret = ''

# Binance client
client = Client(api_key, api_secret)

# Define your trading parameters
symbol = 'BTCUSDT'    # Trading pair

# Voice alert configuration
engine = pyttsx3.init()

# Trading bot logic
def trading_bot():
    # Fetch historical price data
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "100 hours ago UTC")
    closing_prices = [float(entry[4]) for entry in klines]

    # Calculate MACD manually
    macd_fast_period = 12
    macd_slow_period = 26
    macd_signal_period = 9

    macd_line = []
    signal_line = []

    for i in range(len(closing_prices)):
        if i >= macd_slow_period:
            macd_fast = sum(closing_prices[i - macd_fast_period + 1 : i + 1]) / macd_fast_period
            macd_slow = sum(closing_prices[i - macd_slow_period + 1 : i + 1]) / macd_slow_period
            macd = macd_fast - macd_slow
            macd_line.append(macd)

            if i >= macd_slow_period + macd_signal_period - 1:
                signal = sum(macd_line[i - macd_signal_period + 1 : i + 1]) / macd_signal_period
                signal_line.append(signal)

    current_macd = macd_line[-1]
    current_macd_signal = signal_line[-1]

    # Check MACD signal condition
    if current_macd > current_macd_signal:
        alert_message = f"MACD Signal: Buy {symbol}"
    else:
        alert_message = f"MACD Signal: No action on {symbol}"

    # Voice alert
    engine.say(alert_message)
    engine.runAndWait()

# Run the trading bot
trading_bot()

