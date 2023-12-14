CREATE TABLE IF NOT EXISTS accounts (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    address_1 VARCHAR(128),
    address_2 VARCHAR(128),
    city VARCHAR(128),
    city_state VARCHAR(128),
    zip_code VARCHAR(128),
    join_date DATE
);