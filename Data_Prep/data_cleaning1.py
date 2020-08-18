
# coding: utf-8

# In[48]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[49]:

master = pd.read_csv('greenwich_master_backtestsamplepublic.csv',encoding='latin-1')
stock_df=pd.read_csv('greenwich_stock_data.csv')


# In[50]:

stock_df.head()


# In[51]:

post_count=master.groupby('ticker').agg({'job_id':'count'}).sort_values(by=['ticker'],ascending=True).reset_index()
post_count.describe()

sig_tickers=post_count[post_count['job_id']>post_count['job_id'].mean()] 
#these are companies in the 4th quartile by count of job_postings
sig_tickers.head()
# In[52]:

post_stock=pd.merge(sig_tickers,stock_df,how='inner',left_on='ticker',right_on='Ticker')
post_stock.info()


# In[55]:

len(post_stock.ticker.unique())==len(post_stock.Ticker.unique()) #none of the companies with significant number of job postings have been delisted.


# In[ ]:
