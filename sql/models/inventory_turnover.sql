SELECT
    p.sku_id,
    p.product_name,
    p.category,
    SUM(s.quantity * s.unit_cost) AS cogs_60d,
    AVG(i.stock_level)            AS avg_inventory,
    ROUND(
        SUM(s.quantity * s.unit_cost) /
        NULLIF(AVG(i.stock_level * s.unit_cost), 0), 2
    ) AS turnover_ratio
FROM sales_history s
JOIN products p  ON s.sku_id = p.sku_id
JOIN inventory i ON s.sku_id = i.sku_id
WHERE s.sale_date >='2024-11-01'
GROUP BY p.sku_id, p.product_name, p.category
ORDER BY turnover_ratio DESC;