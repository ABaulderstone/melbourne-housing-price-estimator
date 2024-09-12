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
    # Load the data
    data = pd.read_csv('./melbourne_housing_data.csv')
    
    # Clean the data
    data = data.dropna(subset=['Price'])  # Remove rows where Price is NaN
    
    # Select features
    features = ['Suburb', 'Rooms', 'Bathroom']
    X = data[features]
    y = data['Price']

    # Remove rows with NaN in feature columns
    mask = X.notna().all(axis=1)
    X = X[mask]
    y = y[mask]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create preprocessing steps for numeric and categorical data
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

    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Create a pipeline with the preprocessor and the model
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', LinearRegression())])

    # Fit the pipeline
    pipeline.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean squared error: {mse}")
    print(f"R2 score: {r2}")

    # Save the model
    joblib.dump(pipeline, './model/model.joblib')

    print("Model trained and saved successfully.")

    # Print some data statistics
    print("\nData statistics:")
    print(f"Total samples: {len(data)}")
    print(f"Samples after cleaning: {len(X)}")
    print(f"Features used: {features}")

if __name__ == "__main__":
    train_and_save_model()