import psycopg2
from psycopg2 import sql
from faker import Faker
from datetime import datetime, timedelta
import random

# Connection parameters
DATABASE_URL = "postgresql://postgres:0000@localhost:5432/testdb"

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Predefined failure reasons
failure_reasons = [
    "wait 1 hour to reactivate",
    "This account is not allowed to use WhatsApp"
]

# Function to create fake user data
def create_fake_user():
    user_id = fake.uuid4()
    emulator_id = fake.uuid4()
    return (user_id, emulator_id)

# Function to create fake activation data
def create_fake_activation(user_id, emulator_id):
    ip = fake.ipv4()
    phone_number = fake.phone_number()
    country_code = fake.country_code()
    city = fake.city()
    country = fake.country()
    vpn_provider = fake.company()
    sms_provider = 'SMS Activate'
    result = random.choice(["success", "fail"])
    error_message = fake.sentence(nb_words=6) if result == "fail" else ""
    device_type = random.choice(["mobile", "tablet", "desktop"])
    os_version = random.choice(["android_10", "ios_14", "windows_10"])
    timestamp = fake.date_time_between(start_date='-1y', end_date='now')
    emulator_time = timestamp + timedelta(minutes=random.randint(1, 10))
    activation_country_time = timestamp + timedelta(minutes=random.randint(1, 10))
    vpn_country_time = timestamp + timedelta(minutes=random.randint(1, 10))
    failure_reason = random.choice(failure_reasons) if result == "fail" else ""
    cost = round(fake.random_number(digits=4) / 100, 2)  # Cost between 0.00 and 99.99
    return (
        user_id, emulator_id, ip, phone_number, country_code, city, country,
        vpn_provider, sms_provider, result, error_message, device_type, os_version,
        timestamp, emulator_time, activation_country_time, vpn_country_time,
        failure_reason, cost
    )

# Function to create fake IP limit data
def create_fake_ip_limit():
    ip = fake.ipv4()
    activation_count = fake.random_int(min=0, max=4)
    max_activations = 4
    time_window_start = fake.date_time_between(start_date='-1y', end_date='now')
    time_window_end = time_window_start + timedelta(hours=1)
    return (ip, activation_count, max_activations, time_window_start, time_window_end)

# Function to create fake available IP data
def create_fake_available_ip():
    ip = fake.ipv4()
    return (ip,)

# Function to create fake used phone number data
def create_fake_used_phone_number():
    phone_number = fake.phone_number()
    cost = round(fake.random_number(digits=4) / 100, 2)  # Cost between 0.00 and 99.99
    return (phone_number, cost)

# Insert fake user data
def insert_fake_user(cursor, user_id, emulator_id):
    cursor.execute(
        sql.SQL("INSERT INTO users (user_id, emulator_id) VALUES (%s, %s)"),
        [user_id, emulator_id]
    )

# Insert fake activation data
def insert_fake_activation(cursor, activation_data):
    cursor.execute(
        sql.SQL("""
            INSERT INTO activations 
            (user_id, emulator_id, ip, phone_number, country_code, city, country, vpn_provider, sms_provider, result, error_message, device_type, os_version, timestamp, emulator_time, activation_country_time, vpn_country_time, failure_reason, cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """),
        activation_data
    )

# Insert fake IP limit data
def insert_fake_ip_limit(cursor, ip_limit_data):
    cursor.execute(
        sql.SQL("""
            INSERT INTO ip_limits 
            (ip, activation_count, max_activations, time_window_start, time_window_end)
            VALUES (%s, %s, %s, %s, %s)
        """),
        ip_limit_data
    )

# Insert fake available IP data
def insert_fake_available_ip(cursor, available_ip_data):
    cursor.execute(
        sql.SQL("INSERT INTO available_ips (ip) VALUES (%s)"),
        available_ip_data
    )

# Insert fake used phone number data
def insert_fake_used_phone_number(cursor, used_phone_number_data):
    cursor.execute(
        sql.SQL("INSERT INTO used_phone_numbers (phone_number, cost) VALUES (%s, %s)"),
        used_phone_number_data
    )

# Generate and insert data
def generate_and_insert_data(num_records):
    for _ in range(num_records):
        user_id, emulator_id = create_fake_user()
        insert_fake_user(cursor, user_id, emulator_id)
        
        # Insert multiple activations for each user
        for _ in range(5):  # Adjust the range to add more/less activations per user
            activation_data = create_fake_activation(user_id, emulator_id)
            insert_fake_activation(cursor, activation_data)

        # Insert IP limit data
        ip_limit_data = create_fake_ip_limit()
        insert_fake_ip_limit(cursor, ip_limit_data)
        
        # Insert available IP data
        available_ip_data = create_fake_available_ip()
        insert_fake_available_ip(cursor, available_ip_data)
    
    # Insert used phone number data
    for _ in range(num_records):
        used_phone_number_data = create_fake_used_phone_number()
        insert_fake_used_phone_number(cursor, used_phone_number_data)
    
    # Commit the transaction
    conn.commit()

# Generate and insert 10 fake user records and other data
generate_and_insert_data(10)

# Close the connection
cursor.close()
conn.close()
