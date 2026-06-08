SELECT
    order_id,
    order_status,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    CASE
        WHEN order_status = 'delivered' AND order_delivered_customer_date IS NULL THEN 'delivered_status_without_delivery_date'
        WHEN order_status <> 'delivered' AND order_delivered_customer_date IS NOT NULL THEN 'non_delivered_status_with_delivery_date'
        ELSE 'normal'
    END AS status_error_type
FROM orders
WHERE
    (order_status = 'delivered' AND order_delivered_customer_date IS NULL)
    OR (order_status <> 'delivered' AND order_delivered_customer_date IS NOT NULL);
