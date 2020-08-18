from data_access import pull_data
from data_prep import prep_data
from create_train_test_sets import create_train_test_sets
from train_test_model import train_test_model

import pandas as pd
import numpy as np

# Define model constants up here
ready_data_filename = None
train_pct = 0.8
cv = True # True or False
n_folds = 5
models = [] # List of models to test
params = [] # List of lists of parameters, one for each model
datapaths = []

def main(pulldata=False, prepdata=True):
  if pulldata:
    pull_data()
    return()
  if prepdata:
    prep_data(datapaths)
    return()
  data = pd.read_csv('./' + ready_data_filename)
  train, test = create_train_test_sets(data, train_pct)  
  train_test_model(data, models, params, cv=cv, n_folds=n_folds) # Might want to make a model class
  
  # Need to then analyze the model. See model_metrics() in train_test_model.py
  return()

if __name__ == '__main__':
  np.random.seed()
  main(pulldata=True)
