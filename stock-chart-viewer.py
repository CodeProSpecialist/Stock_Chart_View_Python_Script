#using python 3.10 in Linux

import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

def fetch_stock_data(symbol, start_date, end_date):
    """
    Function to fetch stock data using yfinance.
    """
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        return data
    except Exception as e:
        print("Error fetching data:", e)
        return None

def calculate_macd(data):
    """
    Function to calculate MACD and signal line.
    """
    data['12_EMA'] = data['Close'].ewm(span=12).mean()
    data['26_EMA'] = data['Close'].ewm(span=26).mean()
    data['MACD'] = data['12_EMA'] - data['26_EMA']
    data['Signal'] = data['MACD'].ewm(span=9).mean()
    return data['MACD'], data['Signal']

def calculate_rsi(data, window=14):
    """
    Function to calculate RSI.
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_candlestick_macd_rsi(data, macd, signal, rsi):
    """
    Function to plot candlestick chart with MACD and RSI indicators.
    """
    apds = [
        mpf.make_addplot(macd, panel=1, color='r', secondary_y=False),
        mpf.make_addplot(signal, panel=1, color='g', secondary_y=False),
        mpf.make_addplot(rsi, panel=2, color='b', secondary_y=False)
    ]

    mpf.plot(data, type='candle', addplot=apds, volume=True, style='charles')

def main():
    symbol = input("Enter stock or ETF symbol: ")
    start_date = input("Enter start date (yyyy-mm-dd): ")
    end_date = input("Enter end date (yyyy-mm-dd): ")

    # Fetch stock data
    data = fetch_stock_data(symbol, start_date, end_date)

    if data is not None:
        # Calculate MACD and signal line
        macd, signal = calculate_macd(data)

        # Calculate RSI
        rsi = calculate_rsi(data)

        # Plot candlestick chart with MACD and RSI
        plot_candlestick_macd_rsi(data, macd, signal, rsi)
        plt.show()

if __name__ == "__main__":
    main()
