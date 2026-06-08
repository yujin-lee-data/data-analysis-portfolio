SELECT
    o.order_id,
    o.order_status,
    o.order_purchase_timestamp,
    p.order_id AS payment_order_id
FROM orders o
LEFT JOIN payments p
    ON o.order_id = p.order_id
WHERE p.order_id IS NULL;
