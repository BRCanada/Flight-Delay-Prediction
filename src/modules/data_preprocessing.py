# DATA PREPROCESSING MODULE
# This module includes all functions that will be used in the feature selection and feature engineering process
# As well as any functions needed for EDA

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import requests
import time

#-------Time of Day--------------------
def time_of_day(df, method='dep'):  
    """
    Creates time of day column based on dataframe values for actual departure time and actual arrival time using mapping.  
   
    500 - 1200: Morning
    1200 - 1700: Afternoon
    1700 - 2100: Evening
    2100 - 2399 OR 0 - 499: Nite
    
    Input: df = Dataframe
           method = 'dep' - departures
                    'arr' - arrivals
           
    """
    if method == 'dep':
        if (df['crs_dep_time'] >=500 and df['crs_dep_time'] < 1200):
            return 'Morning'
        elif (df['crs_dep_time'] >=1200 and df['crs_dep_time'] < 1700):
            return 'Afternoon'        
        elif (df['crs_dep_time'] >= 1700 and df['crs_dep_time'] < 2100): 
            return 'Evening'
        return 'Night'
    
    elif method == 'arr':
        if (df['crs_arr_time'] >=500 and df['crs_arr_time'] < 1200):
            return 'Morning'
        elif (df['crs_arr_time'] >=1200 and df['crs_arr_time'] < 1700):
            return 'Afternoon'        
        elif (df['crs_arr_time'] >= 1700 and df['crs_arr_time'] < 2100) :
            return 'Evening'
#-------------------------------------
#-------Feature Categorizer-----------

def feature_categorizer(dfslice, df):
    """
    This function will call other functions within data_preprocessing.py and write their outputs to a new csv file with the 
    additional features created by the other functions. 
    
    dfslice = DataFrame (Of sliced features)
    df = Main dataframe you want to update
    """
    
    temp_df = dfslice.select_dtypes(include='object')
    
    for column in temp_df.columns:
        map_dict = {}
        for key, value in enumerate(temp_df[column].unique()):
            map_dict[value] = key
        
        df[column] = df[column].map(map_dict)
#-------------------------------------
#-------Make Regions------------------
def make_regions(df, feature):
    """
    Function to take state codes of a dataframe and assign them
    to a new feature using inverse dictionary mapping
    
    df = dataframe
    feature = feature label (string)
    
    *NOTE: state code feature MUST be named state_id*
    """
    #----Dictionary Map (DO NOT ALTER)-----
    state_codes = {'Pacific' : ['AK', 'CA', 'HI', 'OR', 'WA'],
               'North-West': ['MT', 'ID', 'WY'],
               'South-West': ['AZ', 'NM', 'CO', 'NV', 'UT'],
               'East-North Central' : ['IL', 'IN', 'MI', 'OH', 'WI'],
               'West-North Central' : ['IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'],
               'New England' : ['MA', 'ME', 'NH', 'VT', 'RI', 'CT'],
               'Mid-Atlantic' : ['DE', 'MD', 'NJ', 'PA', 'NY', 'VA', 'WV'],
               'South-Atlantic' : ['FL', 'GA', 'NC', 'SC'],
               'East-South Central' : ['AL', 'KY', 'MS', 'TN'],
               'West-South Central' : ['AR', 'LA', 'OK', 'TX']
}
    
    for index in states[feature].index:
        for region, state in state_codes.items():
            if states[feature][index] in state:
                states['region'][index] = str(region)
#-------------------------------------
#-------Call Weather API------------------
def open_weather_api(lat, long, date, timezone = "America%2FChicago"):
    """
    Function returns individual api calls by location and date using the open weather api
    PARAMS:
    lat = latitude
    long = longitude
    date = YYYY-MM-DD as a string
    timezone = Continent/city
    """
    
    url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={long}&start_date={date}&end_date={date}&hourly=precipitation,rain,snowfall,cloudcover&daily=precipitation_sum,rain_sum,snowfall_sum,precipitation_hours&timezone={timezone}"
    response = requests.get(url)
    return response.json()
#-------------------------------------
#-------City Scrubber------------------
def city_scrubber(city_str):
    """
    City name will be scrubbed to remove alternate names
    Dallas/Fort Something, TX -----> Dallas, TX
    PARAMS: 
    city_str = City/City/City, State code as string
    """
    try:
        state = city_str.split(',')       #split city(s) and state
        cities = state[0].split('/')      #split the list of cities by /
        return cities[0] + ',' + state[1]
    except: 
        return "no state in your city string"
#-------------------------------------
#-------Weather Condition------------------    
def weather_condition(city, date, lat_long_df):
    """
    Function returns the weather condition for a single date/city. 
    PARAMS: 
    city = City, State code as string
    date = 2020-01-01 as string
    """
    #scrub city
    #print(city)
    city_scrub = city_scrubber(city)
    if city_scrub == 'no state in your city string':
        return city_scrub, city
    
    #pull the lat and long for city
    lat = None
    long = None
    try:
        lat = float(lat_long_df['lat'][lat_long_df['city_state'] == city_scrub])
        long = float(lat_long_df['lng'][lat_long_df['city_state'] == city_scrub])
    except:
        print(lat, long, city)
        pass
    
    #call the weather api
    if lat and long:         #none is False
        json_result = open_weather_api(lat, long, date)
        #print(json_result)
        try:
            total_rain = int(json_result['daily']['rain_sum'][0])                  # mm
        except: 
            total_rain = None
        try:
            total_snow = int(json_result['daily']['snowfall_sum'][0])              # cm        
        except:
            total_snow = None
        try:
            cloudcover_mean = round(sum(json_result['hourly']['cloudcover'])/len(json_result['hourly']['cloudcover']))     # %
        except:
            cloudcover_mean = None

        if total_rain is None and total_snow is None and cloudcover_mean is None:
            result = "no weather data"    
        elif total_rain == 0 and total_snow == 0 and cloudcover_mean < 40:
            result = "sunny"
        elif total_rain == 0 and total_snow == 0 and cloudcover_mean >= 40:
            result = "cloudy"
        elif total_rain > 0 and total_snow == 0:
            result = "rain"
        elif total_rain == 0 and total_snow > 0:
            result = "snow"
        elif total_rain > 0 and total_snow > 0:
            result = "snow & rain"
        else:
            result = f"Error, total rain: {total_rain}, total snow: {total_snow}, mean cloud: {cloudcover_mean}"

        return result 
#-------------------------------------
#-------Regression------------------ 
def regression(X_train, X_test, y_train, y_test, regressor_list):
    """
    function to produce regression and result for a list of regressors. scale (StandardScalar), model, and return results
    X = data
    y = target series
    regressor_list = list by regressor module    
    """ 
    #scale
    scalar = StandardScaler()
    X_scaled_train = scalar.fit_transform(X_train)       #fit has a memory, don't use on test
    X_scaled_test = scalar.transform(X_test)           #scalar is an instance that has the memory
    
    #model
    for reg in regressor_list:
        model = reg()                                        # instantiate the regressor
        model.fit(X_scaled_train, y_train)                            # fit the model
        y_pred = model.predict(X_scaled_test)                   # Predict the Test set results
        MSE = mean_squared_error(y_test, y_pred)
        R2 = r2_score(y_test, y_pred)
        print(f'Regressor: {str(reg)} \n MSE = {MSE} \n R2 = {R2} \n ----------------------------')