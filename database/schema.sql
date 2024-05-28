-- Create the database
CREATE DATABASE activation_db;

-- Connect to the database
\c activation_db

-- Create the employees table to track employees and their associated emulator IDs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    emulator_id VARCHAR(255) NOT NULL
);

-- Create the activations table to track all activation attempts
CREATE TABLE activations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    emulator_id VARCHAR(255) NOT NULL,
    ip VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    country_code VARCHAR(50),
    city VARCHAR(255),
    country VARCHAR(255),
    vpn_provider VARCHAR(255),
    sms_provider VARCHAR(255) DEFAULT 'SMS Activate',
    result VARCHAR(50),
    error_message VARCHAR(255),
    device_type VARCHAR(255),
    os_version VARCHAR(50),
    timestamp TIMESTAMPTZ,
    emulator_time TIMESTAMPTZ,
    activation_country_time TIMESTAMPTZ,
    vpn_country_time TIMESTAMPTZ,
    failure_reason VARCHAR(255),
    cost DECIMAL(10, 2) DEFAULT 0.00
);

-- Create the ip_limits table to track IP usage limits
CREATE TABLE ip_limits (
    ip VARCHAR(255) PRIMARY KEY,
    activation_count INT DEFAULT 0,
    max_activations INT DEFAULT 4,
    time_window_start TIMESTAMPTZ,
    time_window_end TIMESTAMPTZ
);

-- Create the available_ips table to store available IPs
CREATE TABLE available_ips (
    ip VARCHAR(255) PRIMARY KEY
);

-- Create the used_phone_numbers table to store used phone numbers and their costs
CREATE TABLE used_phone_numbers (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(255) NOT NULL,
    cost DECIMAL(10, 2) DEFAULT 0.00,
    UNIQUE(phone_number)
);

-- Create the external_factors table to store external factors affecting activation success
CREATE TABLE external_factors (
    id SERIAL PRIMARY KEY,
    factor_type VARCHAR(50),  -- نوع العامل (تحديث، سياسة، إلخ)
    description TEXT,         -- وصف العامل
    date TIMESTAMPTZ          -- تاريخ العامل
);
