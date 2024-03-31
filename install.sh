#!/bin/bash

# Install Python 3.10
echo "Installing Python 3.10..."
sudo apt-get update
sudo apt-get install python3.10 -y

# Install pip for Python 3.10
echo "Installing pip for Python 3.10..."
sudo apt-get install python3-pip -y

# Use pip3 for installing Python packages
PIP=pip3

# Install tkinter
echo "Installing tkinter..."
sudo apt-get install python3-tk -y

# Install tkcalendar
echo "Installing tkcalendar..."
$PIP install tkcalendar

# Install mplfinance
echo "Installing mplfinance..."
$PIP install mplfinance

# Install matplotlib
echo "Installing matplotlib..."
$PIP install matplotlib

# Install pandas
echo "Installing pandas..."
$PIP install pandas

# Install yfinance
echo "Installing yfinance..."
$PIP install yfinance

echo "Installation completed successfully."
