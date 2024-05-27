import psycopg2
from psycopg2 import sql
from faker import Faker

# Connection parameters
DATABASE_URL = "postgresql://postgres:0000@localhost:5432/testdb"

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Function to create fake user data
def create_fake_user():
    user_id = fake.unique.uuid4()
    emulator_id = fake.unique.uuid4()
    return (user_id, emulator_id)

# Function to create fake activation data
def create_fake_activation(user_id, emulator_id):
    ip = fake.ipv4()
    phone_number = fake.phone_number()
    country_code = fake.country_code()
    result = fake.random_element(elements=("success", "fail"))
    error_message = fake.sentence(nb_words=6) if result == "fail" else ""
    device_type = fake.random_element(elements=("mobile", "tablet", "desktop"))
    os_version = fake.random_element(elements=("android_10", "ios_14", "windows_10"))
    timestamp = fake.date_time_this_year()
    return (user_id, emulator_id, ip, phone_number, country_code, result, error_message, device_type, os_version, timestamp)

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
            (user_id, emulator_id, ip, phone_number, country_code, result, error_message, device_type, os_version, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """),
        activation_data
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
    
    # Commit the transaction
    conn.commit()

# Generate and insert 10 fake user records
generate_and_insert_data(10)

# Close the connection
cursor.close()
conn.close()
