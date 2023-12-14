CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_code VARCHAR(64) UNIQUE,
    product_description VARCHAR(256)
);

CREATE INDEX IF NOT EXISTS idx_product_code ON products(product_code);