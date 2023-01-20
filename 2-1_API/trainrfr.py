# Importing libraries
import os
import time
import pandas as pd
import numpy as np
import mlflow
from mlflow.models.signature import infer_signature
from sklearn.model_selection import train_test_split, ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import  OneHotEncoder, StandardScaler, LabelEncoder, LabelBinarizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from joblib import dump
import os



print("training model...")
    
dataset = pd.read_csv('master_lag_ml_inversed_revu-final.csv')

split_date = '2022-12-31'
train = dataset.loc[dataset['Date'] <= split_date].copy()
    
features_list = ['Nom_region', 'lag_1'
                , 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7', 'lag_8' 
                ,'lag_9', 'lag_10', 'lag_11', 'lag_12', 'lag_13', 'lag_14', 'lag_15', 'lag_364'
                , 'day', 'year', 'month', 'day_of_week'
                ]
target_variable = ['lag_inversed_1']


X_train = train.loc[:,features_list]
Y_train = train.loc[:,target_variable]
    
numeric_features = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'lag_6', 'lag_7', 
                'lag_8','lag_9', 'lag_10', 'lag_11', 'lag_12', 'lag_13', 'lag_14', 'lag_15', 'lag_364', 'year']
categorical_features = ['Nom_region', 'day_of_week', 'day', 'month']    

numeric_transformer = Pipeline(steps=[
        ('imputer', KNNImputer(n_neighbors=1)),
        ('scaler', StandardScaler()) 
    ])

categorical_transformer = Pipeline(steps=[('encoder', OneHotEncoder(drop='first'))])

preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features),
                                                 ('cat', categorical_transformer, categorical_features)])

model = Pipeline(steps=[("Preprocessing", preprocessor), ("Regressor",  RandomForestRegressor(random_state=0, n_jobs=-1))])    

model.fit(X_train, Y_train)
prediction = model.predict(X_train)
    
print("...Done!")


print("Saving model...")
dump(model, "elec.joblib")
print(f"Model has been saved here: {os.getcwd()}")