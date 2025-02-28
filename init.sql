CREATE TABLE IF NOT EXISTS azure_costs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    subscription_id VARCHAR(50),
    resource_group VARCHAR(100),
    product_name VARCHAR(255),
    meter_category VARCHAR(100),
    meter_subcategory VARCHAR(100),
    quantity DECIMAL(18,6),
    cost DECIMAL(18,6),
    currency VARCHAR(10),
    charge_type VARCHAR(50),
    pricing_model VARCHAR(50)
);
