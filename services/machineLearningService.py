import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sqlalchemy import create_engine

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
    
    # Convert categorical columns to numeric codes
    categorical_columns = ["country_code", "user_id", "emulator_id", "ip", "phone_number", "device_type", "os_version"]
    for column in categorical_columns:
        df[column] = df[column].astype('category').cat.codes
    
    return df

def train_random_forest_model(df):
    """
    Trains a Random Forest model on the given data and prints detailed metrics.
    
    Args:
        df (pd.DataFrame): The prepared data.
    
    Returns:
        RandomForestClassifier: The trained Random Forest model.
    """
    # Features and target
    X = df[["user_id", "emulator_id", "ip", "phone_number", "country_code", "device_type", "os_version"]]
    y = df["result"]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)
    
    # Predict and calculate accuracy
    y_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, y_pred)
    print(f"Random Forest Model accuracy: {rf_accuracy * 100:.2f}%")
    
    # Print additional metrics
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
    # Resample data by hour and sum the results
    ts_data = df.set_index('timestamp').resample('h').sum()
    
    # Initialize and train the Holt-Winters model
    hw_model = ExponentialSmoothing(ts_data['result'], seasonal='add', seasonal_periods=24).fit()
    
    # Evaluate the time series model
    ts_forecast = hw_model.forecast(24)
    print("\nHolt-Winters Model Forecast for the next 24 hours:")
    print(ts_forecast)
    
    return hw_model

def main():
    """
    Main function to execute the data preparation and model training.
    """
    # Prepare data
    df = prepare_data()
    
    # Train models
    rf_model = train_random_forest_model(df)
    hw_model = train_time_series_model(df)
    
    # Additional usage for models can be added here
    # ...

if __name__ == "__main__":
    main()
