# python 3.10

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime


def fetch_stock_data(symbol, start_date, end_date):
    """
    Function to fetch stock data using yfinance.
    """
    try:
        data = yf.download(symbol, start=start_date, end=end_date)
        data.index = pd.to_datetime(data.index)  # Convert index to DatetimeIndex
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

def plot_candlestick_macd_rsi(data, macd, signal, rsi, symbol):
    """
    Function to plot candlestick chart with MACD and RSI indicators.
    """
    apds = [
        mpf.make_addplot(macd, panel=1, color='r', secondary_y=False),
        mpf.make_addplot(signal, panel=1, color='g', secondary_y=False),
        mpf.make_addplot(rsi, panel=2, color='b', secondary_y=False)
    ]

    title = f'{symbol} Stock Analysis'

    # Plotting the candlestick chart with MACD and RSI
    mpf.plot(data, type='candle', addplot=apds, volume=True, style='charles', title=title, ylabel='PRICE',
             ylabel_lower='RSI                MACD', figsize=(12, 8))  # Larger width

def fetch_data_and_plot(symbol, start_date, end_date):
    """
    Function to fetch data and plot the graph.
    """
    # Fetch stock data
    data = fetch_stock_data(symbol, start_date, end_date)

    if data is not None:
        # Calculate MACD and signal line
        macd, signal = calculate_macd(data)

        # Calculate RSI
        rsi = calculate_rsi(data)

        # Plot candlestick chart with MACD and RSI
        plot_candlestick_macd_rsi(data, macd, signal, rsi, symbol)
        plt.show()

def on_submit():
    """
    Function to handle submission of form.
    """
    symbol = symbol_entry.get()
    start_date_str = start_cal.get_date()  # Get date as string
    end_date_str = end_cal.get_date()  # Get date as string
    # Convert string dates to datetime objects
    start_date = datetime.datetime.strptime(start_date_str, "%m/%d/%y")  # Adjust format string
    end_date = datetime.datetime.strptime(end_date_str, "%m/%d/%y")  # Adjust format string
    # Format dates as yyyy-mm-dd strings
    start_date_formatted = start_date.strftime("%Y-%m-%d")
    end_date_formatted = end_date.strftime("%Y-%m-%d")
    fetch_data_and_plot(symbol, start_date_formatted, end_date_formatted)


# Create Tkinter window
root = tk.Tk()
root.title("Stock Chart View Tool by CodeProSpecialist")

# Larger width and height for the window
root.geometry("530x425")  # Larger width and height

# Create form labels and input widgets
symbol_label = ttk.Label(root, text="Stock Symbol:")
symbol_label.grid(row=0, column=0, padx=5, pady=5)
symbol_entry = ttk.Entry(root)
symbol_entry.grid(row=0, column=1, padx=5, pady=5)

start_label = ttk.Label(root, text="Start Date:")
start_label.grid(row=1, column=0, padx=5, pady=5)
start_cal = Calendar(root, selectmode='day', year=2024, month=3, day=1)
start_cal.grid(row=1, column=1, padx=5, pady=5)

end_label = ttk.Label(root, text="End Date:")
end_label.grid(row=2, column=0, padx=5, pady=5)
end_cal = Calendar(root, selectmode='day', year=2024, month=3, day=1)
end_cal.grid(row=2, column=1, padx=5, pady=5)

submit_button = ttk.Button(root, text="View Chart", command=on_submit)
submit_button.grid(row=3, columnspan=2, padx=5, pady=5)

root.mainloop()
