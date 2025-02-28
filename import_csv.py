import os
import pandas as pd
import mysql.connector
from datetime import datetime

db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "azure"),
    "password": os.getenv("MYSQL_PASSWORD", "azurepassword"),
    "database": os.getenv("MYSQL_DATABASE", "azure_costs"),
}

csv_file = os.getenv("CSV_FILE_PATH", "/data/azure_costs.csv")

def convert_date_mysql_format(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None

df = pd.read_csv(csv_file)

df = df.rename(columns={
    "Date": "date",
    "SubscriptionId": "subscription_id",
    "ResourceGroup": "resource_group",
    "ProductName": "product_name",
    "MeterCategory": "meter_category",
    "MeterSubCategory": "meter_subcategory",
    "Quantity": "quantity",
    "CostInBillingCurrency": "cost",
    "BillingCurrencyCode": "currency",
    "ChargeType": "charge_type",
    "PricingModel": "pricing_model"
})[["date", "subscription_id", "resource_group", "product_name",
     "meter_category", "meter_subcategory", "quantity", "cost",
     "currency", "charge_type", "pricing_model"]]

df["date"] = df["date"].apply(convert_date_mysql_format)

df = df.fillna({
    "subscription_id": "UNKNOWN",
    "resource_group": "UNKNOWN",
    "product_name": "UNKNOWN",
    "meter_category": "UNKNOWN",
    "meter_subcategory": "UNKNOWN",
    "quantity": 0.0,
    "cost": 0.0,
    "currency": "N/A",
    "charge_type": "N/A",
    "pricing_model": "N/A"
})

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

query = """
    INSERT INTO azure_costs 
    (date, subscription_id, resource_group, product_name, meter_category, meter_subcategory, quantity, cost, currency, charge_type, pricing_model) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(query, tuple(row))

conn.commit()
cursor.close()
conn.close()

print("✅ CSV imported successfully into MySQL!")
