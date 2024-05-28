import sys
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder

def analyze(data):
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["emulator_time"] = pd.to_datetime(df["emulator_time"])
    df["activation_country_time"] = pd.to_datetime(df["activation_country_time"])
    df["vpn_country_time"] = pd.to_datetime(df["vpn_country_time"])
    df["result"] = df["result"].map({"success": 1, "fail": 0})
    df["country_code"] = df["country_code"].astype('category').cat.codes

    # Convert datetime columns to Unix timestamps
    df["timestamp"] = df["timestamp"].astype('int64') / 10**9
    df["emulator_time"] = df["emulator_time"].astype('int64') / 10**9
    df["activation_country_time"] = df["activation_country_time"].astype('int64') / 10**9
    df["vpn_country_time"] = df["vpn_country_time"].astype('int64') / 10**9

    # Features and target variable
    X = df[["user_id", "emulator_id", "ip", "phone_number", "country_code", "timestamp", "device_type", "os_version", "emulator_time", "activation_country_time", "vpn_country_time"]]
    y = df["result"]

    # One-hot encoding for categorical features
    categorical_features = ["user_id", "emulator_id", "ip", "phone_number", "device_type", "os_version"]
    onehot_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_features = onehot_encoder.fit_transform(X[categorical_features])

    # Create a DataFrame with the encoded features
    encoded_feature_names = onehot_encoder.get_feature_names_out(categorical_features)
    encoded_df = pd.DataFrame(encoded_features, columns=encoded_feature_names)

    # Combine encoded features with the original DataFrame (excluding the original categorical columns)
    X = pd.concat([encoded_df.reset_index(drop=True), X[["country_code", "timestamp", "emulator_time", "activation_country_time", "vpn_country_time"]].reset_index(drop=True)], axis=1)

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training the RandomForestClassifier
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)

    # Making predictions and evaluating the model
    y_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, y_pred)
    return rf_accuracy

if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    accuracy = analyze(data)
    print(f"Random Forest Model accuracy: {accuracy * 100:.2f}%")
