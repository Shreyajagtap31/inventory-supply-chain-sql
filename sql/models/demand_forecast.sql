SELECT
    sku_id,
    sale_date,
    quantity,
    ROUND(AVG(quantity) OVER (
        PARTITION BY sku_id
        ORDER BY sale_date
        ROWS BETWEEN 59 PRECEDING AND CURRENT ROW
    ), 2) AS rolling_60d_avg_demand
FROM sales_history
ORDER BY sku_id, sale_date;