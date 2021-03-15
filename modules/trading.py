import pandas as pd
import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go  
from plotly.subplots import make_subplots

import streamlit as st
import financial_data as fd

def crossover_ma(close, budget=10000, ma_type="Exponential Moving Average (EMA)"):
    """
    :param close: closing prices
    :return df_signal: new dataframe that contains "close" and the "ma(s)"
    :return balance: final balance after trading
    :return profit: list with all the profits
    """

    st.markdown("<br /><br />",unsafe_allow_html=True)
    len_short_ma = st.slider("Select the window of the short Moving Average: ",5, 200, 15, 1)
    len_long_ma = st.slider("Select the window of the long Moving Average: ",5, 200, 100, 1)
    st.markdown("<br /><br />",unsafe_allow_html=True)

    # to do : validation

    if ma_type == "Exponential Moving Average (EMA)":
        ma_short = fd.get_EMA(close,length=len_short_ma)
        ma_long = fd.get_EMA(close,length=len_long_ma)
    elif ma_type == "Simple Moving Average (SMA)":
        ma_short = fd.get_SMA(close,length=len_short_ma)
        ma_long = fd.get_SMA(close,length=len_long_ma)

    df_signal = pd.DataFrame({'ma_short' : ma_short, 
                              'ma_long' : ma_long,
                              'close' : close},
                              index=list(close.index)).dropna()
    
    buy = []
    sell = []
    
    # trade at most 30% of the total balance
    balance = budget 
    traded = 0
    traded_price = 0
    
    # pos = 0 : we do not have any position -> we can buy but we cannot sell
    # pos = 1 : we have a position -> we can sell and we cannot buy 
    
    # I am not considering trading fees
    # I suppose to trade the entire balance 
    pos = 0
    
    # update the profit every time I sell
    # I use another sell_list because I want to know also the final balance If it 
    # is still holding the last position
    sell_dates = []
    profit_values = []
    
    for i in range(len(df_signal)-1):
        
        if df_signal.ma_short.iloc[i-1] < df_signal.ma_long.iloc[i] \
        and df_signal.ma_short.iloc[i+1] > df_signal.ma_long.iloc[i] \
        and pos == 0:
            buy.append(i)
            pos = 1
            
            # update balance
            traded_price = df_signal.close[i]
            traded = balance
            balance = 0
            
        
        if df_signal.ma_short.iloc[i-1] > df_signal.ma_long.iloc[i] \
        and df_signal.ma_short.iloc[i+1] < df_signal.ma_long.iloc[i] \
        and pos == 1:
            sell.append(i)
            pos = 0
            
            # update balance
            balance += traded * (df_signal.close[i]/traded_price)
            
            # update profit
            sell_dates.append(i)
            profit_values.append(balance-budget)
        
    # final price
    if pos == 1:
        balance += traded * (df_signal.close[len(df_signal)-1]/traded_price)
        
        # update profit
        sell_dates.append(len(df_signal)-1)
        profit_values.append(balance-budget)

    # plot the signals
    fig_ma = go.Figure()
    
    fig_ma.add_trace(go.Scatter(x=df_signal.index, y=df_signal['close'], name='Close'))
    fig_ma.add_trace(go.Scatter(x=df_signal.index, y=df_signal['ma_short'], name='MA_short'))
    fig_ma.add_trace(go.Scatter(x=df_signal.index, y=df_signal['ma_long'], name='MA_long'))

    fig_ma.add_trace(go.Scatter(x=df_signal.iloc[buy].index, y=df_signal.iloc[buy]['close'], name='Buy',
                          mode='markers', marker=dict(color='green', size=10, symbol='triangle-up'))
                     )
    fig_ma.add_trace(go.Scatter(x=df_signal.iloc[sell].index, y=df_signal.iloc[sell]['close'], name='Sell',
                            mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'))
                     )
    fig_ma.update_layout(title="Crossover with two Moving Averages")
    st.plotly_chart(fig_ma,use_container_width=True)

    return df_signal, balance, sell_dates, profit_values


