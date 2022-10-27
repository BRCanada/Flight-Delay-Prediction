# MODELING MODULE
# This module will contain all of the functions needed for predictions and model building

#---------RANDOM SEARCH--------------
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from scipy.stats import uniform as sp_randFloat
from scipy.stats import randint as sp_randInt


def random_search(X, y, model, parameters):
    
    """
    Randomly apply parameters to models and return the parameters that returned the best results:
    
    X = dataframe or array
    y = target Series
    model = model variable (defined outside of function)
    parameters = parameters to search through (dictionary)
    
    """
    
    #Split data into train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
    
    #Scale the data
    scaler = StandardScaler()
    X_scaled_train = scaler.fit_transform(X_train)
    X_scaled_test = scaler.transform(X_test)   
    
    randm_src = RandomizedSearchCV(estimator=model, param_distributions = parameters,
                               cv = 5, n_iter = 10, n_jobs=-1)
    randm_src.fit(X_scaled_train, y_train)

    print(" Results from Random Search " )
    print("\n The best estimator across ALL searched params:\n", randm_src.best_estimator_)
    print("\n The best score across ALL searched params:\n", randm_src.best_score_)
    print("\n The best parameters across ALL searched params:\n", randm_src.best_params_)

