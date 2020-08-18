import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from get_stock_data import get_stock_data
from load_market_data import load_market_data
from scipy.stats import pearsonr as cor

greenwich_datapath = '../../MSiA400-Bryce-Canyon/greenwich_master_backtestsamplepublic.csv'
usecols = ['post_date', 'salary', 'city', 'state', 'ticker']
tau = 20 # Minimum number of unique job postings (need to figure out how to set this)

# 1st, actually get the data
dat = pd.read_csv(greenwich_datapath, encoding='latin-1', usecols=usecols)
dat = dat.drop_duplicates() # For some reason job postings appears with the same timestamp and info...
dat = dat[dat.post_date>='2018'] # Let's just start by subsetting from all data 2018 or later. Old stuff is less relevant anyway

dat['post_date'] = dat.post_date.apply(lambda x: x.split(' ')[0]) # Strips the time of day
dat['post_date'] = pd.to_datetime(dat.post_date) # Converts column to datetime

x = dat.groupby('ticker')[['post_date']]
x = x.max().reset_index().merge(x.min().reset_index(), on='ticker') # Gets the latest and earliest posting by ticker
x['date_range'] = (x.post_date_x - x.post_date_y).dt.days # Determines date range from earliest to latest posting by ticker

dat = x[x.date_range>365][['ticker']].merge(dat, how='left') # Removes all tickers that have less than a year's worth of data between Jan 1, 2018 and latest appearance
dat['post_date'] = dat.post_date.apply(lambda x: datetime.strftime(x, '%Y-%m-%d')) # Convert back to string for consistency with later code

dat = dat[['ticker','state']].groupby('ticker').count()\
    .rename({'state':'njobs'}, axis=1).reset_index().merge(dat)
    
dat2 = dat.groupby(['ticker','post_date'])[['njobs']].count().rename({'njobs':'njobs_on_date'}, axis=1)\
    .reset_index().merge(dat)[['ticker','post_date','njobs_on_date','njobs']].drop_duplicates()

greenwich_stock_data = get_stock_data(dat, offset=90*2)
greenwich_stock_data['pct_change_90_stock'] = greenwich_stock_data.groupby('ticker').Close.pct_change(90)

# Pull market data
print('Pulling relevant market data')
## start_date is the earliest date in greenwich_stock_data
## end_date is today
greenwich_stock_data = greenwich_stock_data.reset_index().rename({'index':'date'}, axis=1)
start_date = greenwich_stock_data.date.min()
end_date = datetime.today().strftime("%Y-%m-%d")
s_and_p, nasdaq = load_market_data(start_date, end_date)

# 90 day pct change for market data
sp_ninety_day_roll_pct_chg = s_and_p[["Close"]].pct_change(periods=90).dropna().rename({'Close':'s_and_p'}, axis=1)
nasdaq_ninety_day_roll_pct_chg = nasdaq[["Close"]].pct_change(periods=90).dropna().rename({'Close':'nasdaq'}, axis=1)
market_data = pd.concat([sp_ninety_day_roll_pct_chg, nasdaq_ninety_day_roll_pct_chg], axis=1)
market_data['pct_change_90_market'] = market_data.mean(axis=1)
market_data = market_data.reset_index()    

ticker_cor_p = {}
for ticker in np.unique(greenwich_stock_data.ticker):
    x = greenwich_stock_data[greenwich_stock_data.ticker=='ZUMZ'].merge(market_data, how='right',left_on='date', right_on='Date')
    x = x.dropna(subset=['pct_change_90_stock'])
    x['adj_pct_chg'] = x.pct_change_90_stock - x.pct_change_90_market # THIS COLUMN IS L2
    x['date_minus_90'] = pd.to_datetime(x.date) - timedelta(90)
    
    subset = dat2[dat2.ticker == ticker]
    date_range = [subset.post_date.min(), subset.post_date.max()]
    idx = pd.date_range(date_range[0], date_range[1]) ####


    subset.index = pd.DatetimeIndex(subset.post_date)
    subset_jobs_posted = subset.reindex(idx, fill_value=0).njobs_on_date # THIS IS almost L1
    
    z = subset_jobs_posted.reset_index().rename({'index':'date'}, axis=1).merge(x, left_on='date', right_on='date_minus_90')
    ticker_cor_p[ticker] = cor(z.njobs_on_date, z.adj_pct_chg)
    
pd.DataFrame(ticker_cor_p).T.rename({0:'correlation',1:'p_value'}, axis=1).sort_values(by='correlation',ascending=False).to_csv('./validation_correlations.csv')
