indicators = {
        0 : "Relative Strength Index (RSI)",
        1 : "Moving Average Convergence/Divergence (MACD)",
        2 : "Simple Moving Average (SMA)",
        3 : "Exponential Moving Average (EMA)"
}

descriptions = {
    0 : "The **relative strength index** (RSI) is a momentum indicator used in \
            technical analysis that measures the magnitude of recent price changes \
            to evaluate overbought or oversold conditions in the price of a stock or \
            other asset.",

    1 : "The **moving average convergence divergence** (MACD) is a trend-following momentum \
        indicator that shows the relationship between two moving averages of a security’s price. \
        The MACD is calculated by subtracting the 26-period exponential moving average (EMA) from \
        the 12-period EMA. The result of that calculation is the MACD line. A nine-day EMA of \
        the MACD called the signal line, is then plotted on top of the MACD line, which can \
        function as a trigger for buy and sell signals.",

    2 : "The **simple moving average** (SMA) is an arithmetic moving average calculated \
        by adding recent prices and then dividing that figure by the number of time periods in the calculation average.",
    3 : "The **exponential moving average ** (EMA) is a type of moving average (MA) that \
        places a greater weight and significance on the most recent data points. \
        An exponentially weighted moving average reacts more \
        significantly to recent price changes than a simple moving average (SMA), \
        which applies an equal weight to all observations in the period. "
}

strategies = {

    0 : "",

    1 : "The following trading **strategy** simply buy the when the MACD crosses above its signal line \
        and sell when the MACD crosses below the signal line. ",

    2 : "The following trading **strategy** uses two moving averages to a chart: one **longer** and one **shorter**. When the shorter-term MA crosses above the longer-term MA, \
        it's a buy signal, as it indicates that the trend is shifting up. This is known as a **'golden cross'**\
        Meanwhile, when the shorter-term MA crosses below the longer-term MA, it's a sell signal, as it \
        indicates that the trend is shifting down. This is known as a **'dead/death cross'**.",
    3 : "The following trading **strategy** uses two moving averages to a chart: one **longer** and one **shorter**. When the shorter-term MA crosses above the longer-term MA, \
        it's a buy signal, as it indicates that the trend is shifting up. This is known as a **'golden cross'**\
        Meanwhile, when the shorter-term MA crosses below the longer-term MA, it's a sell signal, as it \
        indicates that the trend is shifting down. This is known as a **'dead/death cross'**."


}