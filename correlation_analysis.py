# coding: utf-8

# In[1]:


import pandas as pd


# In[4]:


stockdata = pd.read_csv("path_redacted/greenwich_stock_data.csv")
masterdata = pd.read_csv("path_redacted/greenwich_master_backtestsamplepublic.csv", encoding="latin-1")
stockdata = stockdata.drop(stockdata.columns[0], axis=1)


# In[74]:


masterdata[masterdata.ticker=='AA']


# In[58]:


from datetime import datetime, timedelta
import os

pct_changes = {}
for ticker in stockdata.Ticker[stockdata.data_unavailable == 0].unique():
    # check stock price movement across stock opens at no lag, over next 30 days
        # 1st we probably want to get info like the mean, median, and variance of that stock movement over the 30 days
        relevant_subset = stockdata[stockdata.Ticker==ticker]
        first_date = min(relevant_subset.date)
        first_date_as_datetime = datetime.strptime(first_date, '%Y-%m-%d')
        relevant_subset = relevant_subset[relevant_subset.date &lt;= datetime.strftime(first_date_as_datetime+timedelta(days=30), '%Y-%m-%d')]
        final_close = relevant_subset.Close[relevant_subset.date==max(relevant_subset.date)].values[0]
        original_close = relevant_subset.Close[relevant_subset.date==first_date].values[0]
        pct_changes[ticker] = (final_close - original_close) / original_close
        
        
    # check stock price movement across tock opens at no lag, over next 90 days
    


# In[75]:


pct_changes

