import os
import subprocess



def ensure_model():
    if not os.path.exists('./model/model.joblib'):
        print("Model not found. Training the model...")
        subprocess.run(["python", "train_data.py"], check=True)
    else:
        print("Model already exists. Skipping training.")

if __name__ == "__main__":
    ensure_model()
    from app import app
    app.run(debug=True, host='0.0.0.0')