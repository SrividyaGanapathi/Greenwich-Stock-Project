import pandas as pd
import numpy as np
import pickle
#from scikitlearn ...

def cross_validate(data, models, params, n_folds, model_path):
  # Save the model at model_path
  return()

def model_metrics():
  return()

def train_test_model(data, models, params, cv='False', n_folds=None, model_path=None):
  """
  model is a a list of models
  params is a list of lists of params, one for each model
  
  
  """
  if cv == True:
    cross_validate(data=data, models=models, params=params, n_folds=n_folds, model_path=model_path)
  
  # load the best cv model using model_path
  # test the model
