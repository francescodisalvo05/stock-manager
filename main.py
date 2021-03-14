import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go  
from plotly.subplots import make_subplots

import datetime

container_1 = st.beta_container()
container_2 = st.beta_container()
container_3 = st.beta_container()


def get_data(ticker,start):
    """
    :param ticker: ticker that we want to track
    :param start: start date of the analysis (1 year ago, by default)
    :return: historical data
    """
    return yf.download(ticker,start=start)

def get_EMA(close,length=20):
    """
    :param close: closing prices
    :param length: moving average length
    :return: stock's exponential moving average (EMA)
    """
    return close.ewm(span=length, adjust=False).mean()

def trade_ema(close, len_short_ma=20, len_long_ma=100, budget=10000):
    """
    :param close: closing prices
    :param len_moving_average: moving average length
    :return buy: list with buy's signals (indexes)
    :return sell: list with sell's signals (indexes)
    :return df_signal: new dataframe that contains "close" and "ema(s)"
    :return balance: final balance after trading
    """
    ma_short = get_EMA(close,length=len_short_ma)
    ma_long = get_EMA(close,length=len_long_ma)


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
    
    return buy, sell, df_signal, balance, sell_dates, profit_values

with container_1:
    st.title('STOCK MANAGER')

    label_obj = st.empty()
    slider_obj = st.empty()

    ticker_input = label_obj.text_input("Select ticker", 'AAPL')
    value = slider_obj.slider("Select the number of months: ",4, 60, 24, 1)

    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=value*30)
    history = get_data(ticker_input,start_date)

    fig = go.Figure(data=[go.Candlestick(x=history.index, open=history.Open,
                                        high=history.High, low=history.Low,
                                        close=history.Close)])
    
    # responsive layout
    st.plotly_chart(fig,use_container_width=True)


with container_2:

    indicators = {
        1 : "Relative Strength Index (RSI)",
        2 : "Bollinger Bands",
        3 : "Simple Moving Average (SMA)",
        4 : "Exponential Moving Average (EMA)"
    }

    descriptions = {
        1 : "The relative strength index (RSI) is a momentum indicator used in \
             technical analysis that measures the magnitude of recent price changes \
             to evaluate overbought or oversold conditions in the price of a stock or \
             other asset.",
        2 : "BBBBBBBBBBBBBBB",
        3 : "CCCCCCCCCCCCCCC",
        4 : "The **exponential moving average ** (EMA) is a type of moving average (MA) that \
            places a greater weight and significance on the most recent data points. \
            An exponentially weighted moving average reacts more \
            significantly to recent price changes than a simple moving average (SMA), \
            which applies an equal weight to all observations in the period. "
    }

    custom_indicator = st.selectbox("Technical analysis indicator", list(indicators.items()), 3 , format_func=lambda o: o[1])
    st.markdown(descriptions[custom_indicator[0]])

    trade_input = st.number_input("Select the initial amount $$", 1000,step=100)

    history_close = history['Adj Close']

    string_info = " The following trading **strategy** uses two moving averages to a chart: one **longer** and one **shorter**. When the shorter-term MA crosses above the longer-term MA, \
                    it's a buy signal, as it indicates that the trend is shifting up. This is known as a **'golden cross'**\
                    Meanwhile, when the shorter-term MA crosses below the longer-term MA, it's a sell signal, as it \
                    indicates that the trend is shifting down. This is known as a **'dead/death cross'**."
    
    st.markdown(string_info)

    short_ema_input = st.slider("Select the window of the short EMA: ",5, 200, 15, 1)
    long_ema_input = st.slider("Select the window of the long EMA: ",5, 200, 100, 1)

    # to do : validation

    buy, sell, df_signal, balance, sell_dates, profit_values = trade_ema(history_close, short_ema_input, long_ema_input, trade_input)

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Crossover with two EMAs", "Profit"))
    
    fig.add_trace(go.Scatter(x=df_signal.index, y=df_signal['close'], name='Close'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_signal.index, y=df_signal['ma_short'], name='EMA_short'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_signal.index, y=df_signal['ma_long'], name='EMA_long'), row=1, col=1)

    fig.add_trace(go.Scatter(x=df_signal.iloc[buy].index, y=df_signal.iloc[buy]['close'], name='Buy',
                          mode='markers', marker=dict(color='green', size=10, symbol='triangle-up')),
              row=1, col=1)
    fig.add_trace(go.Scatter(x=df_signal.iloc[sell].index, y=df_signal.iloc[sell]['close'], name='Sell',
                            mode='markers', marker=dict(color='red', size=10, symbol='triangle-down')),
                row=1, col=1)

    fig.add_trace(go.Scatter(x=df_signal.iloc[sell_dates].index, y=profit_values, name='profit'),row=2, col=1)

    fig.update_layout(height=700)
    st.plotly_chart(fig,use_container_width=True)

    if balance > 0:
        final_comment = "Congratulations, you would have earned \t $ " + str(round(balance,2))
        st.info(final_comment)
    elif balance < 0:
        final_comment = "I am sorry, you would have lost   $ " + str(round(balance,2))
    else :
        st.info("It could have been worse, your final balance would be the same")

#with container_3: