#instantiate linear regression model
reg = LinearRegression()
#fit model
reg.fit(X_train, y_train)
#predict values
pred_values = reg.predict(X_test)


#now compute mse on test set
metrics.mean_squared_error(y_test, pred_values)


#r-squared on test set
reg.score(X_test, y_test)

#r-squared on train set
reg.score(X_train, y_train)

