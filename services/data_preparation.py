import pandas as pd
from sqlalchemy import create_engine

# Database connection
DATABASE_URL = "postgresql://postgres:0000@localhost:5432/testdb"
engine = create_engine(DATABASE_URL)

# Read data from PostgreSQL
df = pd.read_sql('SELECT * FROM activations', engine)

# Preprocess the data
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["emulator_time"] = pd.to_datetime(df["emulator_time"])
df["activation_country_time"] = pd.to_datetime(df["activation_country_time"])
df["vpn_country_time"] = pd.to_datetime(df["vpn_country_time"])
df["result"] = df["result"].map({"success": 1, "fail": 0})
df["country_code"] = df["country_code"].astype('category').cat.codes

df.to_csv('preprocessed_activations.csv', index=False)
