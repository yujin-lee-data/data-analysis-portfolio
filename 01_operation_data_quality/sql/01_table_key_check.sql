SELECT 'orders' AS table_name,
       COUNT(*) AS row_count,
       COUNT(DISTINCT order_id) AS distinct_order_count
FROM orders
UNION ALL
SELECT 'payments' AS table_name,
       COUNT(*) AS row_count,
       COUNT(DISTINCT order_id) AS distinct_order_count
FROM payments
UNION ALL
SELECT 'order_items' AS table_name,
       COUNT(*) AS row_count,
       COUNT(DISTINCT order_id) AS distinct_order_count
FROM order_items;
