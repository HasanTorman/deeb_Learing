import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import joblib
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Define the path to save the models
model_dir = os.path.dirname(os.path.abspath(__file__))
rf_model_path = os.path.join(model_dir, 'random_forest_model.pkl')
hw_model_path = os.path.join(model_dir, 'time_series_model.pkl')

# Load preprocessed data
df = pd.read_csv('preprocessed_activations.csv')

# Convert categorical features to numerical values using OneHotEncoder
categorical_features = ["user_id", "emulator_id", "ip", "phone_number", "device_type", "os_version"]
onehot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_features = onehot_encoder.fit_transform(df[categorical_features])

# Create a DataFrame with the encoded features
encoded_feature_names = onehot_encoder.get_feature_names_out(categorical_features)
encoded_df = pd.DataFrame(encoded_features, columns=encoded_feature_names)

# Combine encoded features with the original DataFrame (excluding the original categorical columns)
X = pd.concat([encoded_df, df[["country_code"]]], axis=1)
y = df["result"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest model
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

# Evaluate Random Forest model
y_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, y_pred)
print(f"Random Forest Model accuracy: {rf_accuracy * 100:.2f}%")

# Save the Random Forest model
joblib.dump(rf_model, rf_model_path)
joblib.dump(onehot_encoder, os.path.join(model_dir, 'onehot_encoder.pkl'))

# Prepare data for Time Series model
df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')
ts_data = df.set_index('timestamp').resample('H').sum()

# Train Exponential Smoothing model
hw_model = ExponentialSmoothing(ts_data['result'], seasonal='add', seasonal_periods=24).fit()

# Save the Time Series model
joblib.dump(hw_model, hw_model_path)
