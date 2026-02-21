WITH daily_demand AS (
    SELECT
        sku_id,
        AVG(quantity) AS avg_daily_demand
    FROM sales_history
    WHERE sale_date >= '2024-11-01'
    GROUP BY sku_id
)
SELECT
    p.sku_id,
    p.product_name,
    p.category,
    i.stock_level,
    d.avg_daily_demand,
    p.lead_time_days,
    ROUND(d.avg_daily_demand * p.lead_time_days, 0)         AS demand_during_lead_time,
    i.stock_level - (d.avg_daily_demand * p.lead_time_days) AS safety_stock_buffer,
    CASE
        WHEN i.stock_level < (d.avg_daily_demand * p.lead_time_days)        THEN 'HIGH RISK'
        WHEN i.stock_level < (d.avg_daily_demand * p.lead_time_days * 1.25) THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END AS stockout_risk_flag
FROM products p
JOIN inventory i    ON p.sku_id = i.sku_id
JOIN daily_demand d ON p.sku_id = d.sku_id
ORDER BY safety_stock_buffer ASC;