import streamlit as st
import numpy as np
import pandas as pd
import ccxt
import datetime
import plotly.graph_objects as go
from pprint import pprint
import base64

binance = ccxt.binance()
okex = ccxt.okex5()

all_symbols = tuple(sorted(list(binance.load_markets().keys())))
st.title('Crypto Monitoring Dashboard')

@st.cache
def fetch_data(symbol,interval,exchange,limit=None):
	if(exchange=="Binance"):
		data = binance.fetch_ohlcv(symbol, interval,limit=limit)
	elif(exchange=="Okex"):
		data = okex.fetch_ohlcv(symbol, interval,limit=limit)
	df = pd.DataFrame.from_records(data,columns=["Time","Open","High","Low","Close","Volume"])	
	df['Time'] = pd.to_datetime(df['Time'],unit='ms')
	return df

def plot_data(df):
	data=[go.Candlestick(x=df['Time'],open=df['Open'], high=df['High'],low=df['Low'], close=df['Close'])]
	return data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href

symbol = st.sidebar.selectbox(label="Select your symbol", options=tuple([x for x in all_symbols if x[-4:]=="USDT"]))
interval = st.sidebar.selectbox(label="Select inteval", options=("1m","5m","15m","1h"))
exchange = st.sidebar.selectbox(label="Select exchange", options=("Binance","Okex"))

if(exchange=="Okex"):
	limit = st.sidebar.slider(label="Number of bars",min_value=1,max_value=100)
else:
	limit = st.sidebar.slider(label="Number of bars",min_value=1,max_value=1000)

st.write(f"The last {limit} candlesticks of {symbol} on {exchange} are:")

data = fetch_data(symbol,interval,exchange,limit)
st.dataframe(data)

st.markdown(get_table_download_link(data), unsafe_allow_html=True)

st.plotly_chart(plot_data(data),use_container_width=True)