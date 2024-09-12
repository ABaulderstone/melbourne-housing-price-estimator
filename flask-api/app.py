from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import csv

app = Flask(__name__)
CORS(app)




def get_unique_suburbs(csv_file_path):
    suburbs = set()
    
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            suburbs.add(row['Suburb'].title())
    
    return sorted(suburbs)

model = joblib.load('./model/model.joblib')
suburbs = get_unique_suburbs('./melbourne_housing_data.csv')

@app.route('/suburbs')
def list_suburbs(): 
    return jsonify({'suburbs': suburbs})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    
    prediction = model.predict(df)
    
    return jsonify({'predicted_price': prediction[0]})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')