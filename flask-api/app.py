from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)

model = joblib.load('./model/model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    
    prediction = model.predict(df)
    
    return jsonify({'predicted_price': prediction[0]})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')