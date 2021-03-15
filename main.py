import streamlit as st
import pandas as pd
import numpy as np


import plotly.express as px
import plotly.graph_objects as go  
from plotly.subplots import make_subplots

import datetime
import sys

sys.path.append('modules/')

import financial_data as fd
import trading as td
import descriptions as desc

##########################################################################

container_1 = st.beta_container()
container_2 = st.beta_container()
container_3 = st.beta_container()


with container_1:
    st.title('STOCK MANAGER')

    label_obj = st.empty()
    slider_obj = st.empty()

    ticker_input = label_obj.text_input("Select ticker", 'AAPL')
    value = slider_obj.slider("Select the number of months: ",4, 60, 24, 1)

    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=value*30)
    history = fd.get_data(ticker_input,start_date)
    history_close = history['Adj Close']

    fig = go.Figure(data=[go.Candlestick(x=history.index, open=history.Open,
                                        high=history.High, low=history.Low,
                                        close=history.Close)])
    
    # responsive layout
    st.plotly_chart(fig,use_container_width=True)

    initial_price = round(history_close[0],2)
    final_price = round(history_close[len(history_close)-1],2)
    gain_loss = round(100 * (final_price - initial_price) / initial_price,2)
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.markdown("Start price [$]")
        st.info(initial_price)
    with col2:
        st.markdown("Final price [$]")
        st.info(final_price)
    with col3:
        st.markdown("Gain/Loss [%]")
        st.info(gain_loss)


with container_2:

    indicators = desc.indicators
    descriptions = desc.descriptions
    strategies = desc.strategies
    
    st.markdown("<br /><br />",unsafe_allow_html=True)
    custom_indicator = st.selectbox("Technical analysis indicator", list(indicators.items()), 3 , format_func=lambda o: o[1])
    st.markdown(descriptions[custom_indicator[0]])

    trade_input = st.number_input("Select the initial amount $$", 1000,step=100)

    with st.beta_expander("See explanation"):
        st.markdown(strategies[custom_indicator[0]])

    # values taken from the dictionary
    if custom_indicator[0] == 2 or custom_indicator[0] == 3:
        df_signal, balance, sell_dates, profit_values = td.crossover_ma(history_close, trade_input, custom_indicator[1])
    elif custom_indicator[0] == 0:
        df_signal, balance, sell_dates, profit_values = td.trade_RSI(history_close, trade_input)

    # plot the profit
    fig_profit = go.Figure()
    fig_profit.add_trace(go.Scatter(x=df_signal.iloc[sell_dates].index, y=profit_values, name='profit'))
    fig_profit.update_layout(title="Profit")

    st.plotly_chart(fig_profit,use_container_width=True)

    net = balance - trade_input
    if net > 0:
        final_comment = "Congratulations, you would have earned \t $ " + str(round(net,2))
        st.info(final_comment)
    elif net < 0:
        final_comment = "I am sorry, you would have lost   $ " + str(abs(round(net,2)))
        st.info(final_comment)
    else :
        st.info("It could have been worse, your final balance would be the same")

    

#with container_3: