import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker()
np.random.seed(42)

NUM_SKUS = 10000
DAYS = 365

categories = ["Electronics", "Apparel", "Food & Beverage", "Home & Garden",
              "Sports", "Automotive", "Toys", "Health & Beauty"]

print("Generating products...")
products = pd.DataFrame({
    "sku_id":         [f"SKU-{i:05d}" for i in range(1, NUM_SKUS + 1)],
    "product_name":   [fake.word().capitalize() + " " + fake.word().capitalize() for _ in range(NUM_SKUS)],
    "category":       np.random.choice(categories, NUM_SKUS),
    "supplier_id":    [f"SUP-{np.random.randint(1, 200):03d}" for _ in range(NUM_SKUS)],
    "lead_time_days": np.random.randint(3, 30, NUM_SKUS),
    "reorder_point":  np.random.randint(50, 500, NUM_SKUS),
    "unit_cost":      np.round(np.random.uniform(2.5, 500.0, NUM_SKUS), 2)
})

print("Generating inventory...")
inventory = pd.DataFrame({
    "sku_id":       products["sku_id"],
    "stock_level":  np.random.randint(0, 1000, NUM_SKUS),
    "warehouse":    np.random.choice(["WH-EAST", "WH-WEST", "WH-CENTRAL"], NUM_SKUS),
    "last_updated": pd.Timestamp("2024-12-31")
})

print("Generating sales history (this takes 2-5 mins)...")
dates = pd.date_range("2024-01-01", periods=DAYS)
sales_records = []
for i, sku in enumerate(products["sku_id"]):
    if i % 1000 == 0:
        print(f"  Processing SKU {i:,} of {NUM_SKUS:,}...")
    base_demand = np.random.randint(1, 50)
    noise = np.random.normal(0, 3, DAYS)
    seasonal = 5 * np.sin(np.linspace(0, 2 * np.pi, DAYS))
    quantities = np.clip(base_demand + noise + seasonal, 0, None).astype(int)
    unit_cost = products.loc[products["sku_id"] == sku, "unit_cost"].values[0]
    for date, qty in zip(dates, quantities):
        if qty > 0:
            sales_records.append({
                "sku_id":    sku,
                "sale_date": date.date(),
                "quantity":  qty,
                "unit_cost": unit_cost
            })

sales_history = pd.DataFrame(sales_records)

print("Generating suppliers...")
suppliers = pd.DataFrame({
    "supplier_id":       [f"SUP-{i:03d}" for i in range(1, 201)],
    "supplier_name":     [fake.company() for _ in range(200)],
    "reliability_score": np.round(np.random.uniform(0.6, 1.0, 200), 2),
    "avg_lead_time":     np.random.randint(3, 30, 200)
})

print("Generating purchase orders...")
purchase_orders = pd.DataFrame({
    "order_id":       [f"PO-{i:06d}" for i in range(1, 5001)],
    "sku_id":         np.random.choice(products["sku_id"], 5000),
    "order_date":     [pd.Timestamp(d).date() for d in np.random.choice(pd.date_range("2024-01-01", "2024-12-31"), 5000)],
    "order_quantity": np.random.randint(10, 1000, 5000),
    "supplier_id":    [f"SUP-{np.random.randint(1, 200):03d}" for _ in range(5000)]
})

print("Saving CSVs...")
os.makedirs("data/processed", exist_ok=True)
products.to_csv("data/processed/products.csv", index=False)
inventory.to_csv("data/processed/inventory.csv", index=False)
sales_history.to_csv("data/processed/sales_history.csv", index=False)
suppliers.to_csv("data/processed/suppliers.csv", index=False)
purchase_orders.to_csv("data/processed/purchase_orders.csv", index=False)

print("Data generated successfully!")
print(f"   Products:        {len(products):,} rows")
print(f"   Sales History:   {len(sales_history):,} rows")
print(f"   Purchase Orders: {len(purchase_orders):,} rows")