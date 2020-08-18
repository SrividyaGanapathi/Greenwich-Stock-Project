import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


data = pd.read_csv('final_dataset.csv')


#drop the date, Date, date 90 after record_date columns, and an "Unnamed: 0" column included [unnecessary]
if 'Unnamed: 0' in data.columns:
    data.drop(columns = 'Unnamed: 0', inplace = True)
if 'date_90_after_record_date' in data.columns:
    data.drop(columns = 'Unnamed: 0', inplace = True)
if 'date' in data.columns:
    data.drop(columns = 'Unnamed: 0', inplace = True)
if 'Date' in data.columns:
    data.drop(columns = 'Unnamed: 0', inplace = True)

#drop all null records
data = data[(data['city'] != '\\N') & (data['state'] != '\\N') & (data['ticker'] != '\\N')]
#map null values in salary column to None type to enable median imputation
data['salary'] = data['salary'].apply(lambda x: None if x == '\\N' else x)


#10% of observations contain NULL salary values. We can delete them or impute median salary. Let's impute median salary.
median_salary = data['salary'].dropna().median()
data['salary'] = data['salary'].fillna(median_salary)
data.head()



#date is in format month, day, year (American style)
data['post_date'] = pd.to_datetime(data['post_date'])


#split post_date column into separate month, day, year columns
data['year'] = data['post_date'].dt.year
data['month'] = data['post_date'].dt.month
data['day'] = data['post_date'].dt.day
#now drop the post_date column as we have parsed out all its data if you'd like
#data = data.drop(columns = ['post_date'])

#remove the companies who have posted less than 500 jobs
ticker_value_count = data['ticker'].value_counts()
grped_data  = data.groupby('ticker').count()
selected_tickers = grped_data[grped_data['post_date'] > 500].index.values
selected_data = data[data['ticker'].isin(selected_tickers)]

#get dummy variables for state, city. Must do separately as dataset is large and will cause a memory error if done all at once.
with_state_encoded = pd.get_dummies(selected_data,columns = ['state'], prefix = ['state'], drop_first = True)

with_ticker_encoded = pd.get_dummies(with_state_encoded, columns = ['ticker'], prefix = ['ticker'], drop_first = True)


#attempt to write to csv 
with_ticker_encoded.to_csv()

#carry out train/test split
X = data.drop(columns = 'pct_change_90_stock')
y = data['pct_change_90_stock'] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 108)



#removing null values one last time
jobs = jobs.loc[~jobs['pct_change_90_stock'].isna()]
jobs = jobs.loc[~jobs['Close'].isna()]
jobs = jobs.loc[~jobs['prev_90_day_pct_change'].isna()]



