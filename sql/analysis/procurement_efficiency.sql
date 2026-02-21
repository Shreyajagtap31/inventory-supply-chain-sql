SELECT
    p.sku_id,
    p.category,
    COUNT(po.order_id)             AS total_orders,
    AVG(po.order_quantity)         AS avg_order_qty,
    p.reorder_point,
    ROUND(100.0 * SUM(CASE WHEN po.order_quantity >= p.reorder_point THEN 1 ELSE 0 END)
        / COUNT(po.order_id), 1)   AS procurement_efficiency_pct
FROM products p
JOIN purchase_orders po ON p.sku_id = po.sku_id
GROUP BY p.sku_id, p.category, p.reorder_point
ORDER BY procurement_efficiency_pct ASC;