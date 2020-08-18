from load_market_data import load_market_data
from get_stock_data import get_stock_data
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from multiprocessing import  Pool

# STEPS
#   1) Pull the data from Greenwich HR about the companies and their job postings
#   2) Get the stock data corresponding to the Greenwich HR companies
#   3) Create vector of 90 day rolling pct changes for each company
#   4) Pull the market data (load_market_data(start_date, end_date))
#   5) Create vector of 90 day rolling pct changes in the market data
#   6) Compute the values of x for the 90 days before and after each job posting (for stock + market)
#      For each job posting we have some m = f(X). Group by ticker and find mean(m) by ticker
#   7) Sort tickers from greatest mean(m) to least mean(m)

print('Preparing to read the job posting data')

# Hard-coded constants
greenwich_datapath = './greenwich_master_backtestsamplepublic.csv'
usecols = ['post_date', 'salary', 'city', 'state', 'ticker']
tau = 20 # Minimum number of unique job postings (need to figure out how to set this)

########### (1) Pull Greenwich HR data ##############
# 1st, actually get the data
dat = pd.read_csv(greenwich_datapath, encoding='latin-1', usecols=usecols)
print('Job posting data read successfully')
print('Cleaning and preparing job posting data')
dat = dat.drop_duplicates() # For some reason job postings appears with the same timestamp and info...
dat = dat[dat.post_date>='2018'] # Let's just start by subsetting from all data 2018 or later. Old stuff is less relevant anyway

dat['post_date'] = dat.post_date.apply(lambda x: x.split(' ')[0]) # Strips the time of day
dat['post_date'] = pd.to_datetime(dat.post_date) # Converts column to datetime
####### dat = dat.drop_duplicates() # Removes duplicates again

x = dat.groupby('ticker')[['post_date']]
x = x.max().reset_index().merge(x.min().reset_index(), on='ticker') # Gets the latest and earliest posting by ticker
x['date_range'] = (x.post_date_x - x.post_date_y).dt.days # Determines date range from earliest to latest posting by ticker

dat = x[x.date_range>365][['ticker']].merge(dat, how='left') # Removes all tickers that have less than a year's worth of data between Jan 1, 2018 and latest appearance
dat['post_date'] = dat.post_date.apply(lambda x: datetime.strftime(x, '%Y-%m-%d')) # Convert back to string for consistency with later code

# Create n_jobs column and compute the weight column, and shrink the data
dat = dat[['ticker','state']].groupby('ticker').count()\
    .rename({'state':'njobs'}, axis=1).reset_index().merge(dat)
dat = dat.groupby(['ticker','post_date']).count()[['njobs']]\
    .rename({'njobs':'weight'}, axis=1).reset_index()\
    .merge(dat, on=['ticker','post_date'], how='left')[['ticker','post_date','njobs', 'weight']]\
    .drop_duplicates()

# 2nd, subset based on tau
dat = dat[dat['njobs']>=tau] # dat[(dat.njobs>1000) & (dat.njobs<1100)] #

print('Job posting data successfully prepared')
######### (2) Pull Greenwich HR stock data ############
print('Pulling relevant stock ticker data')
# Just get the data, based on start date corresponding with earliest job posting by each company minus 180 days
greenwich_stock_data = get_stock_data(dat, offset=90*2)

####### (3) 90 day rolling pct change for Greenwich data #######
greenwich_stock_data['pct_change_90_stock'] = greenwich_stock_data.groupby('ticker').Close.pct_change(90)

############### (4) Pull market data ##################
print('Pulling relevant market data')
## start_date is the earliest date in greenwich_stock_data
## end_date is today
greenwich_stock_data = greenwich_stock_data.reset_index().rename({'index':'date'}, axis=1)
start_date = greenwich_stock_data.date.min()
end_date = datetime.today().strftime("%Y-%m-%d")
s_and_p, nasdaq = load_market_data(start_date, end_date)

####### (5) 90 day pct change for market data #######
sp_ninety_day_roll_pct_chg = s_and_p[["Close"]].pct_change(periods=90).dropna().rename({'Close':'s_and_p'}, axis=1)
nasdaq_ninety_day_roll_pct_chg = nasdaq[["Close"]].pct_change(periods=90).dropna().rename({'Close':'nasdaq'}, axis=1)
market_data = pd.concat([sp_ninety_day_roll_pct_chg, nasdaq_ninety_day_roll_pct_chg], axis=1)
market_data['pct_change_90_market'] = market_data.mean(axis=1)
market_data = market_data.reset_index() #.rename({'index':'date'}, axis=1)

####### (6) Compute the 4 values of x for each ticker #######
# x_star_s
# x_star_m
# x_0_s
# x_0_m

# This means define a function and then apply the function
def compute_m(row):
    row_date_as_datetime = datetime.strptime(row.post_date.split(' ')[0], '%Y-%m-%d')
    ninety_days_before = datetime.strftime(row_date_as_datetime - timedelta(days=90), '%Y-%m-%d') # string date
    ninety_days_after = datetime.strftime(row_date_as_datetime + timedelta(days=90), '%Y-%m-%d') # string date

    stock_relevant_subset = greenwich_stock_data[(greenwich_stock_data.ticker==row.ticker) & (ninety_days_before <= greenwich_stock_data.date) & (greenwich_stock_data.date <= ninety_days_after)]
    x_star_s = stock_relevant_subset[stock_relevant_subset.date >= row.post_date].pct_change_90_stock.mean()
    x_0_s = stock_relevant_subset[stock_relevant_subset.date <= row.post_date].pct_change_90_stock.mean()

    market_relevant_subset = market_data[(ninety_days_before <= market_data.Date) & (market_data.Date <= ninety_days_after)]
    x_star_m = market_relevant_subset[market_relevant_subset.Date >= row.post_date].pct_change_90_market.mean()
    x_0_m = market_relevant_subset[market_relevant_subset.Date <= row.post_date].pct_change_90_market.mean()

    m = (x_star_s - x_star_m) - (x_0_s - x_0_m)
    return(m)

def apply_compute_m(df):
    df['individual_metric'] = df.apply(compute_m, axis=1)
    return(df)

def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return(df)

print('Parallelizing apply to all rows of data')
dat = parallelize_dataframe(dat, apply_compute_m)
#dat['metric'] = dat.apply(compute_m, axis=1)
dat = dat.dropna(subset=['individual_metric'])
dat['weighted_metric'] = dat.weight * dat.individual_metric
#dat[dat.ticker=='PCG'].to_csv('./examine_PCG.csv', header=True, index=False)
dat_mid = dat.groupby('ticker').sum().reset_index() # weighted_metric is now weighted sums, njobs is now count(ticker)
dat_mid['metric'] = dat_mid.weighted_metric / dat_mid.weight
final_result = dat_mid[['ticker', 'metric']].sort_values(by='metric',ascending=False)

final_result.to_csv('./output_data_corr_final.csv', header=True, index=False)
## NOW TAKE THE TOP N COMPANIES FROM FINAL_RESULT AND THOSE ARE THE BEST ONES!
