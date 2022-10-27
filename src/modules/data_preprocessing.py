# DATA PREPROCESSING MODULE
# This module includes all functions that will be used in the feature selection and feature engineering process
# As well as any functions needed for EDA

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
        if (df['dep_time'] >=500 and df['dep_time'] < 1200):
            return 'Morning'
        elif (df['dep_time'] >=1200 and df['dep_time'] < 1700):
            return 'Afternoon'        
        elif (df['dep_time'] >= 1700 and df['dep_time'] < 2100): 
            return 'Evening'
        return 'Night'
    
    elif method == 'arr':
        if (df['arr_time'] >=500 and df['arr_time'] < 1200):
            return 'Morning'
        elif (df['arr_time'] >=1200 and df['arr_time'] < 1700):
            return 'Afternoon'        
        elif (df['arr_time'] >= 1700 and df['arr_time'] < 2100) :
            return 'Evening'

        
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
