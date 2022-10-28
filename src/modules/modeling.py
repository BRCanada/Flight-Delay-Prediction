# MODELING MODULE
# This module will contain all of the functions needed for predictions and model building

from sklearn.preprocessing import StandardScaler

#-----Models-------
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR

# Run an if/__main__ block

#---------RANDOM SEARCH--------------
def random_search(X_train, X_test, y_train, y_test, model, parameters, scale=False):
    """
    Randomly apply parameters to models and return the parameters that returned the best results:
    
    X = dataframe or array
    y = target Series
    model = model variable (defined outside of function)
    parameters = parameters to search through (dictionary)

    
    """

    # #Split data into train/test
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testsize)
    
    #Scale the data
    if scale == True:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
    else:
        pass
        
    
    randm_src = RandomizedSearchCV(estimator=model, param_distributions = parameters,
                               cv = 5, n_iter = 10, random_state=42, n_jobs=-1)
    randm_src.fit(X_train, y_train)

    print(" Results from Random Search " )
    print("\n The best estimator across ALL searched params:\n", randm_src.best_estimator_)
    print("\n The best score across ALL searched params:\n", randm_src.best_score_)
    print("\n The best parameters across ALL searched params:\n", randm_src.best_params_)

#-------------------------------------
#---------Regression------------------
def regression(X, y, regressor_list=None):
    """
    produce regression and result for a list of regressors
    X = data
    y = target series
    regressor_list = list by regressor module    
    """
    #split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    
    #scale
    scalar = StandardScaler()
    X_scaled = scalar.fit_transform(X_train)       #fit has a memory, don't use on test
    X_scaled_test = scalar.transform(X_test)           #scalar is an instance that has the memory
    
    #model
    for reg in regressor_list:
        model = reg()                                        # instantiate the regressor
        model.fit(X_scaled, y_train)                            # fit the model
        y_pred = model.predict(X_scaled_test)                   # Predict the Test set results
        MSE = mean_squared_error(y_test, y_pred)
        R2 = r2_score(y_test, y_pred)
        print(f'Regressor: {reg} \n MSE = {MSE} \n R2 = {R2} \n ----------------------------')

#-------------------------------------
if __name__ == '__main__':
    from sklearn.ensemble import RandomForestRegressor

    import numpy as np
    
    import pandas as pd
    
    
    flights = pd.read_csv('data/flights_10000.csv')
    flights.dropna(axis=0, inplace=True)
    X = flights.select_dtypes(include='number')
    y = flights['arr_delay']
    

    model = RandomForestRegressor()
    parameters = {'n_estimators' : [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)],
              'max_features' : ['auto', 'sqrt'],
              'criterion' : ['squared_error', 'absolute_error', 'poisson'], 
              'max_depth' : [int(x) for x in np.linspace(10, 110, num = 11)], 
              'min_samples_split' : [2, 5, 10], 
              'min_samples_leaf' : [1, 2, 4],
               }
    random_search(X, y, model, parameters)