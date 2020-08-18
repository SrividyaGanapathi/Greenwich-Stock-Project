
import pandas as pd


#LASSO WITH CV
from sklearn.linear_model import LassoCV
import numpy as np
reg = LassoCV(cv=5, alphas = [.01, .001, .0001]).fit(X, y)


reg.alpha_


from sklearn import linear_model
lasso1 = linear_model.Lasso(alpha = 0.0001)



lasso1.fit(X_train, y_train)



lasso1.score(X_train, y_train)


pred_lasso = lasso1.predict(X_test)


from sklearn import metrics
metrics.mean_squared_error(y_test, pred_lasso)


from sklearn.linear_model import LinearRegression
linreg1 = LinearRegression()
linreg1.fit(X_train, y_train)
linreg1.score(X_train, y_train)


pred_linreg = linreg1.predict(X_test)
metrics.mean_squared_error(y_test, pred_linreg)


from sklearn.linear_model import RidgeCV

reg2 = RidgeCV(cv=5, alphas = [.01, .001, .0001]).fit(X, y)


reg2.alpha_


ridge1 = linear_model.Ridge(alpha = 0.01)
ridge_reg = ridge1.fit(X_train, y_train)
ridge_reg.score(X_train, y_train)

ridge_preds = ridge1.predict(X_test)


metrics.mean_squared_error(y_test, ridge_preds)

