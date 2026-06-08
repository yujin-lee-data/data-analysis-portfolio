SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS order_ratio
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;
