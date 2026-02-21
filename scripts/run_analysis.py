import duckdb
import pandas as pd

con = duckdb.connect()

con.execute("CREATE VIEW products        AS SELECT * FROM read_csv_auto('data/processed/products.csv')")
con.execute("CREATE VIEW inventory       AS SELECT * FROM read_csv_auto('data/processed/inventory.csv')")
con.execute("CREATE VIEW sales_history   AS SELECT * FROM read_csv_auto('data/processed/sales_history.csv')")
con.execute("CREATE VIEW purchase_orders AS SELECT * FROM read_csv_auto('data/processed/purchase_orders.csv')")

print("Running inventory turnover model...")
turnover = con.execute(open("sql/models/inventory_turnover.sql").read()).df()

print("Running stockout risk model...")
stockout = con.execute(open("sql/models/stockout_risk.sql").read()).df()

print("Running procurement efficiency model...")
procurement = con.execute(open("sql/analysis/procurement_efficiency.sql").read()).df()

turnover.to_csv("data/processed/inventory_turnover_output.csv", index=False)
stockout.to_csv("data/processed/stockout_risk_output.csv", index=False)
procurement.to_csv("data/processed/procurement_efficiency_output.csv", index=False)

total = len(stockout)
high  = len(stockout[stockout["stockout_risk_flag"] == "HIGH RISK"])
med   = len(stockout[stockout["stockout_risk_flag"] == "MEDIUM RISK"])
low   = len(stockout[stockout["stockout_risk_flag"] == "LOW RISK"])
avg_efficiency = procurement["procurement_efficiency_pct"].mean()

print("=" * 45)
print("     INVENTORY RISK SUMMARY REPORT")
print("=" * 45)
print(f"  Total SKUs Analyzed   : {total:,}")
print(f"  HIGH RISK             : {high:,}  ({100*high/total:.1f}%)")
print(f"  MEDIUM RISK           : {med:,}  ({100*med/total:.1f}%)")
print(f"  LOW RISK              : {low:,}  ({100*low/total:.1f}%)")
print(f"  Avg Procurement Eff.  : {avg_efficiency:.1f}%")
print("=" * 45)
print("All outputs saved to data/processed/")