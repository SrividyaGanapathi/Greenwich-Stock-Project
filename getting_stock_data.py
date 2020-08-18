# coding: utf-8

# In[1]:


import pandas as pd
import yfinance as yf # Need to install yfinance first before import will work
import datetime
import numpy as np


# In[2]:


datapath = "path_redacted/greenwich_master_backtestsamplepublic.csv"
dat = pd.read_csv(datapath, encoding='latin-1') 


# In[3]:


first_job_posting_time_by_ticker = dat.groupby('ticker')[['post_date']].first()
first_job_posting_time_by_ticker.head()


# In[4]:


"""
This cell shows how to access a single stock's information from yfinance:

# Get the data for the stock Apple by specifying the stock ticker, start date, and end date (in the form YYYY-MM-DD)
data = yf.download('AAPL','2016-01-01','2018-01-01')
"""
yf.download('AAPL','2016-01-01','2018-01-01')


# In[25]:


full_ticker_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Ticker'])
for ticker, date in first_job_posting_time_by_ticker.iterrows():
    start_date = date.post_date.split()[0] 
    end_date = datetime.date.today().strftime("%Y-%m-%d")
    try:
        ticker_data = yf.download(ticker, start_date, end_date)
    except:
        ticker_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        for col in ticker_data.columns:
            ticker_data[col].values[:] = 'No Data Available'
    ticker_data['Ticker'] = ticker
    full_ticker_data = pd.concat([full_ticker_data, ticker_data])


# In[41]:


# Remove date as the index, and rename the column that corresponds to date to 'date'
full_ticker_data = full_ticker_data.reset_index().rename({'index':'date'}, axis=1)


# In[60]:


mismatching_tickers = []
for ticker in first_job_posting_time_by_ticker.index:
    if ticker not in full_ticker_data.Ticker.unique():
        mismatching_tickers.append(ticker)
tickers_with_no_data = pd.DataFrame(np.nan, columns=full_ticker_data.columns, index=mismatching_tickers)
tickers_with_no_data.Ticker = mismatching_tickers
tickers_with_no_data = tickers_with_no_data.reset_index(drop=True)
tickers_with_no_data['data_unavailable'] = 1

full_ticker_data['data_unavailable'] = 0


# In[61]:


all_tickers_data = pd.concat([full_ticker_data,tickers_with_no_data])


# In[63]:


all_tickers_data.to_csv("path_redacted/greenwich_stock_data.csv")


# In[64]:


all_tickers_data

