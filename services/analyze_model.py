import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def analyze(data):
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["result"] = df["result"].map({"success": 1, "fail": 0})

    # Calculate number of attempts per IP per hour
    df['hour'] = df['timestamp'].dt.hour
    ip_hourly_attempts = df.groupby(['ip', 'hour']).size().reset_index(name='attempts')

    # Add number of attempts as a feature
    df = df.merge(ip_hourly_attempts, on=['ip', 'hour'])

    X = df[['ip', 'hour', 'attempts']]
    y = df['result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, y_pred)
    print(f"Random Forest Model accuracy: {rf_accuracy * 100:.2f}%")

    # Extract feature importances
    feature_importances = rf_model.feature_importances_
    print(f"Feature importances: {feature_importances}")

    return rf_model, feature_importances

# Read data from JSON
import sys
import json

data = json.loads(sys.stdin.read())
analyze(data)
