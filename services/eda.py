import pandas as pd

# Load preprocessed data
df = pd.read_csv('preprocessed_activations.csv')

# Analyze failure reasons
failure_reasons = df[df["result"] == 0]["failure_reason"].value_counts()
print("Failure Reasons:\n", failure_reasons)

# Analyze relationship between phone number, IP, and failure reasons
failure_analysis = df[df["result"] == 0].groupby(["phone_number", "ip", "failure_reason"]).size().reset_index(name='counts')
print("Failure Analysis:\n", failure_analysis)

# Analyze relationship between phone number and failure reasons
phone_number_failure_analysis = df[df["result"] == 0].groupby(["phone_number", "failure_reason"]).size().reset_index(name='counts')
print("Phone Number Failure Analysis:\n", phone_number_failure_analysis)

# Analyze relationship between IP and failure reasons
ip_failure_analysis = df[df["result"] == 0].groupby(["ip", "failure_reason"]).size().reset_index(name='counts')
print("IP Failure Analysis:\n", ip_failure_analysis)
