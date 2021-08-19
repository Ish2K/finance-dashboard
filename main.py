import streamlit as st
import numpy as np
import pandas as pd
import ccxt
import datetime

binance = ccxt.binance()
okex = ccxt.okex5()


st.title('Crypto Monitoring Dashboard')

@st.cache
def fetch_data(symbol,interval,exchange,limit=None):
	if(exchange=="Binance"):
		data = binance.fetch_ohlcv(symbol, interval,limit=limit)
	else:
		data = okex.fetch_ohlcv(symbol, interval,limit=limit)
	df = pd.DataFrame.from_records(data,columns=["Time","Open","High","Low","Close","Volume"])	
	return df


symbol = st.sidebar.selectbox(label="Select your symbol", options=("BTC/USDT","ETH/USDT","1INCH/USDT"))
interval = st.sidebar.selectbox(label="Select inteval", options=("1m","5m","15m","1h"))
exchange = st.sidebar.selectbox(label="Select exchange", options=("Binance","Okex"))

if(exchange=="Okex"):
	limit = st.sidebar.slider(label="Number of bars",min_value=1,max_value=100)
else:
	limit = st.sidebar.slider(label="Number of bars",min_value=1,max_value=1000)

st.write(f"The last {limit} candlesticks of {symbol} on {exchange} are:")


st.write(fetch_data(symbol,interval,exchange,limit))