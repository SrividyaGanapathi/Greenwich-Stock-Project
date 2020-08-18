import pandas as pd 
import numpy as np 
import yfinance as yf
from datetime import datetime, timedelta

def get_stock_data(dat, offset):
    first_job_posting_time_by_ticker = dat.sort_values(by='post_date').groupby('ticker')[['post_date']].first()
    full_ticker_data = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Ticker'])
    
    for ticker, date in first_job_posting_time_by_ticker.iterrows():
        start_date = datetime.strftime(datetime.strptime(date.post_date.split()[0], '%Y-%m-%d') - timedelta(days=offset), '%Y-%m-%d')
        end_date = datetime.today().strftime("%Y-%m-%d")
        try:
            ticker_data = yf.download(ticker, start_date, end_date)
            ticker_data['ticker'] = ticker
        except:
            pass # Stock not listed 
        full_ticker_data = pd.concat([full_ticker_data, ticker_data])
    
    return(full_ticker_data)