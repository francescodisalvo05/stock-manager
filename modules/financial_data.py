import pandas as pd
import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go  
from plotly.subplots import make_subplots

import streamlit as st

def get_data(ticker,start):
    """
    :param ticker: ticker that we want to track
    :param start: start date of the analysis (1 year ago, by default)
    :return: historical data
    """
    return yf.download(ticker,start=start)

def get_SMA(close,length=20):
    """
    :param close: closing prices
    :param length: moving average length
    :return: stock's simple moving average (SMA)
    """
    return close.rolling(window=length).mean()

def get_EMA(close,length=20):
    """
    :param close: closing prices
    :param length: moving average length
    :return: stock's exponential moving average (EMA)
    """
    return close.ewm(span=length, adjust=False).mean()

def get_RSI(close,length=20):
    """
    :param close: closing prices
    :param length: moving average length
    """
    # check if the difference is positive or negative
    delta = close.diff(1).dropna()
    
    positive = delta.copy()
    negative = delta.copy()
    
    positive[positive < 0] = 0
    negative[negative > 0] = 0
    
    avg_gain = positive.rolling(window=length).mean()
    avg_loss = abs(negative.rolling(window=length).mean())
    
    rsi = 100 - (100/(1 + avg_gain/avg_loss))
    
    return rsi

