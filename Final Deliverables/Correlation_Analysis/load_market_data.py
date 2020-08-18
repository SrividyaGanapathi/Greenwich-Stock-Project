import yfinance as yf
import pandas as pd
import numpy as np

def load_market_data(start_date, end_date):
    """
    Loads market data for the S&P 500 and the NASDAQ Composite from start_date to end_date
    
    params:
        start_date: String of the form 'yyyy-mm-dd'
        end_date: String of the form 'yyyy-mm-dd'
        
    returns:
        s_and_p: Pandas DataFrame of daily S&P 500 information, detailed with a Date index, the 
                 Open, High, Low, Close, Adj Close, and Volume
        nasdaq:  Pandas DataFrame of daily NASDAQ Composite information, detailed with a Date index, the 
                 Open, High, Low, Close, Adj Close, and Volume
        
    """
    s_and_p = yf.download('^GSPC',start_date, end_date)
    nasdaq = yf.download('^IXIC',start_date, end_date)
    
    return(s_and_p, nasdaq)
