#!/bin/bash
set -e

# Check if the model file exists
if [ ! -f "/app/model/spark_melbourne_house_price_model/metadata/part-00000" ]; then
    echo "Model not found. Training new model..."
    python3 /app/train_model.py
else
    echo "Model found. Skipping training."
fi

# Start the Flask application
python3 /app/app.py