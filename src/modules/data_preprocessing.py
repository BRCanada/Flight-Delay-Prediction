# DATA PREPROCESSING MODULE
# This module includes all functions that will be used in the feature selection and feature engineering process
# As well as any functions needed for EDA

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
def make_regions(df):
    """
    Function to take state codes of a dataframe and assign them
    to a new feature using inverse dictionary mapping
    
    df = dataframe
    
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
    
    for index in states['state_id'].index:
        for region, state in state_codes.items():
            if states['state_id'][index] in state:
                states['region'][index] = str(region)
#-------------------------------------
