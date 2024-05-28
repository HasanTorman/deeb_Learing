import os
import pandas as pd
import joblib
from datetime import datetime

# Define the path to load the models
model_dir = os.path.dirname(os.path.abspath(__file__))
rf_model_path = os.path.join(model_dir, 'random_forest_model.pkl')
hw_model_path = os.path.join(model_dir, 'time_series_model.pkl')
encoder_path = os.path.join(model_dir, 'onehot_encoder.pkl')

# Load models
rf_model = joblib.load(rf_model_path)
hw_model = joblib.load(hw_model_path)
onehot_encoder = joblib.load(encoder_path)

def should_activate(user_id, emulator_id, ip, phone_number, country_code, timestamp, device_type, os_version, emulator_time, activation_country_time, vpn_country_time):
    data = {
        "user_id": [user_id],
        "emulator_id": [emulator_id],
        "ip": [ip],
        "phone_number": [phone_number],
        "country_code": [country_code],
        "timestamp": [timestamp],
        "device_type": [device_type],
        "os_version": [os_version],
        "emulator_time": [emulator_time],
        "activation_country_time": [activation_country_time],
        "vpn_country_time": [vpn_country_time]
    }
    df = pd.DataFrame(data)
    df["country_code"] = df["country_code"].astype('category').cat.codes
    
    # Encode categorical features
    categorical_features = ["user_id", "emulator_id", "ip", "phone_number", "device_type", "os_version"]
    encoded_features = onehot_encoder.transform(df[categorical_features])
    encoded_feature_names = onehot_encoder.get_feature_names_out(categorical_features)
    encoded_df = pd.DataFrame(encoded_features, columns=encoded_feature_names)
    
    # Combine encoded features with the original DataFrame (excluding the original categorical columns)
    df_combined = pd.concat([encoded_df, df[["country_code"]]], axis=1)
    
    # Predict with Random Forest model
    rf_prediction = rf_model.predict(df_combined)
    
    # Forecast with Time Series model
    ts_forecast = hw_model.forecast(24)
    
    # Combine results for decision
    if rf_prediction[0] == 1 and ts_forecast.mean() > 0.5:
        return True
    else:
        return False

# Example usage
user_id = "user1"
emulator_id = "emulator1"
ip = "192.168.1.1"
phone_number = "+123456789"
country_code = "US"
timestamp = pd.Timestamp.now()
device_type = "Android"
os_version = "9.0"
emulator_time = pd.Timestamp.now()
activation_country_time = pd.Timestamp.now()
vpn_country_time = pd.Timestamp.now()

if should_activate(user_id, emulator_id, ip, phone_number, country_code, timestamp, device_type, os_version, emulator_time, activation_country_time, vpn_country_time):
    print("Proceed with activation")
else:
    print("Avoid activation")
