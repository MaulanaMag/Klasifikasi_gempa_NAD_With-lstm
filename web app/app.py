from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)
# Load model dan komponen
model = load_model(r'h:\Keluarga\SANWH\AAA SAATNYA SKRIPSI\Web App\quake_app\gempa_model_NAD.h5')
scaler = joblib.load(r'h:\Keluarga\SANWH\AAA SAATNYA SKRIPSI\Web App\quake_app\scaler.pkl')
le = joblib.load(r'h:\Keluarga\SANWH\AAA SAATNYA SKRIPSI\Web App\quake_app\label_encoder.pkl')

# Load data kota Aceh
cities_df = pd.read_csv(r'h:\Keluarga\SANWH\AAA SAATNYA SKRIPSI\Web App\quake_app\aceh_cities.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    lat = float(data['lat'])
    lon = float(data['lon'])
    depth = float(data['depth'])
    mag = float(data['magnitude'])
    
    # Preprocessing
    features = np.array([[lat, lon, depth, mag]])
    scaled_features = scaler.transform(features)
    reshaped = scaled_features.reshape((scaled_features.shape[0], 1, scaled_features.shape[1]))
    
    # Prediksi
    prediction = model.predict(reshaped)
    class_idx = np.argmax(prediction)
    class_name = le.inverse_transform([class_idx])[0]
    
    return jsonify({'prediction': class_name})

@app.route('/get_city_coords')
def get_city_coords():
    city = request.args.get('city')
    coords = cities_df[cities_df['city'] == city][['lat', 'lon']].to_dict(orient='records')
    return jsonify(coords[0] if coords else {'lat': '', 'lon': ''})

if __name__ == '__main__':
    app.run(debug=True)