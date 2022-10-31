# Midterm Project: Flight Delay Prediction
### A Capstone project by [@HalleypC](https://github.com/HalleypC) and [@BRCanada](https://github.com/BRCanada)

## Objective
The objective of this project was to clean, analyse and engineer features for a dataset that contained flight data for 2018 and 2019. We were required to train a sufficient model for use in predicting flight delays a week in advance using a 2020 'test' set. 

## Our Process
#### 1. Early Data Analysis (EDA)
Our first course of action was to complete the assigned EDA tasks assigned by Lighthouse Labs to obtain some insight into what this specific data set entails, and patterns that can be isolated as separate features for model training. These notebooks can be reviewed in our [EDA_Notebooks Folder](Midterm_Project/EDA_Notebooks).

#### 2. Function Definition
Through the process of EDA, we developed a multitude of methods that assisted us in visualizing data, creating new feature columns and in one case (**Task 3**) a robust API call function that allowed us to create city-specific weather data for both origin and destination airports. These functions were organized into the following python scripts:
*    [data_preprocessing.py](Midterm_Project/src/modules/data_preprocessing.py)
*    [figure_generation.py](Midterm_Project/src/modules/figure_generation.py)
*    [modeling.py](Midterm_Project/src/modules/modeling.py)

#### 3. Model/Feature Selection
In order to identify the best models to use for this task, we broke down our modeling process into 5 separate stages, which also incorporated the feature selection process throughout.

1. [Model 0](Midterm_Project/Models/Model_0.ipynb) - This model notebook encompassed interpreting the initial dataset, and separating certain features into more concise parts (i.e. datetime64 column to day, month, year column. We also ran some scatterplots and heatmaps to get a better idea of how each individual feature correlated with the others. Given the nature of our task, we decided on three main Regression functions to test on this initial dataset: [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html), [Epsilon-Support Vector Regression](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html?highlight=svr#sklearn.svm.SVR), and [RandomForest Regression](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html?highlight=random+forest+regressor#sklearn.ensemble.RandomForestRegressor). We found that most models performed abysmally with the base dataset's numeric features, with r2 scores being negative for both SVR and RFR, while Linear Regression returned an r2 of ~1.5%.
<br>
<br>
2. [Model 1](Midterm_Project/Models/Model_1.ipynb) - This notebook focused on expanding the feature list from Model 0, namely through one-hot encoding categorical features with the 'object' d-type. We also incorporated our new weather columns from [EDA Task 3](Midterm_Project/EDA_Notebooks/EDA_Task3.ipynb) here, created a mean delay per carrier column, and added our time of day columns using the function developed for our [EDA Task 4](Midterm_Project/EDA_Notebooks/EDA_Task4.ipynb) notebook. These new columns were also numerically encoded. Including these new features resulted in negative r2 scores across all three Regression models.
<br>
<br>
3. [Model 2](Midterm_Project/Models/Model_2.ipynb) - Due to the results found from the previous model, we wanted to see if the results of categorical encoding would net similar results. The same features were used from the final Model 1 dataframe, and results from the categorically encoded features came out slightly worse than Model 1.
<br>
<br>
4. [Model 3](Midterm_Project/Models/Model_3.ipynb) - In this model, we worked at fine-tuning the hyperparameters of our three chosen models to try and achieve better r2 scores for our categorically encoded dataset from Model 2. While the hyperparameter tuning improved the r2 scores considerably, our final results were still sub-par for the categorical set:
    *    **LR**: ~0.076
    *    **RFR**: ~0.080
    *    **SVR**: ~0.031
<br>
<br>
5. [Model 4](Midterm_Project/Models/Model_4.ipynb) - Our final Model 4 Notebook repeats the hypertuning process as Model 3, however we used the one-hot encoded features from Model 1 instead of our categorical features from Model 2. After Hyperparameter tuning we came to the following results:
    *    **LR**: ~0.050
    *    **RFR**: ~0.079
    *    **SVR**: ~0.055
    <br>
After these results, we decided to use this dataset alongside the      Random Forest Regressor model to make our final flight predictions.

#### 4. Results
Our final predicted results were exported to the [HC_BR_Submission.csv](Midterm_Project/data/HC_BR_Submission.csv) file. 



