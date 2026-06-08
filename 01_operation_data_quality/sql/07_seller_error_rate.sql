WITH seller_orders AS (
    SELECT DISTINCT
        oi.seller_id,
        oi.order_id
    FROM order_items oi
),
error_orders AS (
    SELECT o.order_id
    FROM orders o
    LEFT JOIN payments p
        ON o.order_id = p.order_id
    WHERE p.order_id IS NULL

    UNION

    SELECT order_id
    FROM orders
    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NULL

    UNION

    SELECT order_id
    FROM orders
    WHERE order_delivered_customer_date > order_estimated_delivery_date
)
SELECT
    so.seller_id,
    COUNT(DISTINCT so.order_id) AS total_orders,
    COUNT(DISTINCT eo.order_id) AS error_orders,
    ROUND(COUNT(DISTINCT eo.order_id) * 100.0 / COUNT(DISTINCT so.order_id), 2) AS error_rate
FROM seller_orders so
LEFT JOIN error_orders eo
    ON so.order_id = eo.order_id
GROUP BY so.seller_id
HAVING COUNT(DISTINCT so.order_id) >= 30
ORDER BY error_rate DESC;
