import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

# Database connection URL
DATABASE_URL = "postgresql://postgres:0000@localhost:5432/testdb"

# Create a database connection
engine = create_engine(DATABASE_URL)

def prepare_data():
    """
    Reads data from the database and prepares it for modeling.
    
    Returns:
        pd.DataFrame: The prepared data.
    """
    # Read data from the activations table
    df = pd.read_sql('SELECT * FROM activations', engine)
    
    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Map result column to binary values
    df["result"] = df["result"].map({"success": 1, "fail": 0})
    
    return df

def encode_data(df):
    """
    Encodes categorical columns using OneHotEncoder and returns the transformed DataFrame.
    
    Args:
        df (pd.DataFrame): The input data.
    
    Returns:
        pd.DataFrame: The transformed data.
        OneHotEncoder: The fitted OneHotEncoder instance.
    """
    categorical_columns = ["country_code", "user_id", "emulator_id", "ip", "phone_number", "device_type", "os_version", "vpn_provider"]
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    encoded_cats = encoder.fit_transform(df[categorical_columns])
    encoded_df = pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out(categorical_columns))
    
    df = df.drop(columns=categorical_columns)
    df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    
    return df, encoder

def train_random_forest_model(df):
    """
    Trains a Random Forest model on the given data and prints detailed metrics.
    
    Args:
        df (pd.DataFrame): The prepared data.
    
    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    # Features and target
    X = df.drop(columns=["result", "timestamp"])
    y = df["result"]
    
    # Convert all columns to numeric, setting errors='coerce' to convert non-numeric values to NaN
    X = X.apply(pd.to_numeric, errors='coerce')
    
    # Drop rows with NaN values
    X = X.dropna()
    y = y[X.index]
    
    # Check the shapes of X and y
    print(f"Shape of X: {X.shape}")
    print(f"Shape of y: {y.shape}")
    
    # Ensure there are enough samples to split
    if X.shape[0] == 0:
        raise ValueError("The dataset has no samples after preprocessing. Please check your data and preprocessing steps.")
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)
    
    # Predict and calculate accuracy
    y_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, y_pred)
    
    # Print metrics
    print(f"Random Forest Model accuracy: {rf_accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    return rf_model

def train_time_series_model(df):
    """
    Trains a Holt-Winters Exponential Smoothing model on the given data.
    
    Args:
        df (pd.DataFrame): The prepared data.
    
    Returns:
        ExponentialSmoothing: The trained Holt-Winters model.
    """
    # Resample data by hour and sum the results, excluding non-numeric columns
    ts_data = df.set_index('timestamp').resample('h').sum(numeric_only=True)
    
    # Initialize and train the Holt-Winters model
    hw_model = ExponentialSmoothing(ts_data['result'], seasonal='add', seasonal_periods=24).fit()
    
    # Forecast the next 24 hours
    ts_forecast = hw_model.forecast(24)
    print("\nHolt-Winters Model Forecast for the next 24 hours:")
    print(ts_forecast)
    
    # Save forecast to CSV
    ts_forecast.to_csv('forecast.csv')
    
    # Plot the forecast
    ts_forecast.plot(title='Holt-Winters Forecast for the next 24 hours')
    plt.xlabel('Time')
    plt.ylabel('Forecasted Value')
    plt.show()
    
    return hw_model

def should_activate(user_id, emulator_id, ip, phone_number, country_code, timestamp, device_type, os_version):
    """
    Predict if an activation should proceed based on new input data.
    
    Args:
        user_id (str): User ID.
        emulator_id (str): Emulator ID.
        ip (str): IP address.
        phone_number (str): Phone number.
        country_code (str): Country code.
        timestamp (pd.Timestamp): Timestamp of the activation attempt.
        device_type (str): Device type.
        os_version (str): OS version.
    
    Returns:
        bool: True if activation should proceed, False otherwise.
    """
    data = {
        "user_id": [user_id],
        "emulator_id": [emulator_id],
        "ip": [ip],
        "phone_number": [phone_number],
        "country_code": [country_code],
        "timestamp": [timestamp],
        "device_type": [device_type],
        "os_version": [os_version],
        "vpn_provider": ["default"]  # Add a default value for vpn_provider
    }
    df = pd.DataFrame(data)
    
    # Encode categorical columns using the fitted OneHotEncoder
    encoded_cats = encoder.transform(df[categorical_columns])
    encoded_df = pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out(categorical_columns))
    
    df = df.drop(columns=categorical_columns)
    df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    
    # Ensure all columns are numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # Handle any NaN values (if any)
    df = df.fillna(0)
    
    # Predict with Random Forest model
    rf_prediction = rf_model.predict(df)
    
    # Forecast with Holt-Winters model
    ts_forecast = hw_model.forecast(24)
    
    # Combine results to make a decision
    if rf_prediction[0] == 1 and ts_forecast.mean() > 0.5:
        return True
    else:
        return False

def main():
    """
    Main function to execute the data preparation and model training.
    """
    global rf_model, hw_model, encoder, categorical_columns
    
    # Prepare data
    df = prepare_data()
    
    # Check the shape of the initial DataFrame
    print(f"Initial DataFrame shape: {df.shape}")
    
    # Define categorical columns for encoding
    categorical_columns = ["country_code", "user_id", "emulator_id", "ip", "phone_number", "device_type", "os_version", "vpn_provider"]
    
    # Encode categorical columns
    df, encoder = encode_data(df)
    
    # Check the shape of the encoded DataFrame
    print(f"Shape of the encoded DataFrame: {df.shape}")
    
    # Train models
    rf_model = train_random_forest_model(df)
    hw_model = train_time_series_model(df)
    
    # Example usage of the model
    user_id = "user1"
    emulator_id = "emu1"
    ip = "192.168.1.1"
    phone_number = "+123456789"
    country_code = "US"
    timestamp = pd.Timestamp.now()
    device_type = "Android"
    os_version = "9.0"
    
    if should_activate(user_id, emulator_id, ip, phone_number, country_code, timestamp, device_type, os_version):
        print("Proceed with activation")
    else:
        print("Avoid activation")

if __name__ == "__main__":
    main()
