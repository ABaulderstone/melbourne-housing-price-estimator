import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def train_and_save_model():
    data = pd.read_csv('./melbourne_housing_data.csv')
    data = data.dropna(subset=['Price'])  
    

    features = ['Suburb', 'Rooms', 'Bathroom']
    X = data[features]
    y = data['Price']

  
    mask = X.notna().all(axis=1)
    X = X[mask]
    y = y[mask]

  
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    numeric_features = ['Rooms', 'Bathroom']
    categorical_features = ['Suburb']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', LinearRegression())])

 
    pipeline.fit(X_train, y_train)

 
    y_pred = pipeline.predict(X_test)

    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean squared error: {mse}")
    print(f"R2 score: {r2}")

   
    joblib.dump(pipeline, './model/model.joblib')

    print("Model trained and saved successfully.")


if __name__ == "__main__":
    train_and_save_model()