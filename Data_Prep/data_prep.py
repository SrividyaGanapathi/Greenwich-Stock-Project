import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Fill in datapaths default with the paths in our directory once we know them
def prep_data(datapaths):
  return()
  # Load all of the data files and combine them
  # Clean the data
  # Create new features
  # Save the data
  
  
#   master = pd.read_csv('greenwich_master_backtestsamplepublic.csv',encoding='latin-1')
#   stock_df=pd.read_csv('greenwich_stock_data.csv')


#   # In[50]:

#   stock_df.head()


#   # In[51]:

#   post_count=master.groupby('ticker').agg({'job_id':'count'}).sort_values(by=['ticker'],ascending=True).reset_index()
#   #post_count.describe()

#   sig_tickers=post_count[post_count['job_id']>post_count['job_id'].mean()] 
#   #these are companies in the 4th quartile by count of job_postings --- ^isn't this actually just where job_id > its mean?
#   #sig_tickers.head()
#   # In[52]:

#   post_stock=pd.merge(sig_tickers,stock_df,how='inner',left_on='ticker',right_on='Ticker')
#   #post_stock.info()


#   # In[55]:

#   #len(post_stock.ticker.unique())==len(post_stock.Ticker.unique()) #none of the companies with significant number of job postings have been delisted.


#   # In[ ]:
#   return(post_stock)
