SELECT
    order_id,
    order_status,
    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    CASE
        WHEN order_approved_at IS NOT NULL
             AND order_approved_at < order_purchase_timestamp THEN 'approved_before_purchase'
        WHEN order_delivered_carrier_date IS NOT NULL
             AND order_approved_at IS NOT NULL
             AND order_delivered_carrier_date < order_approved_at THEN 'carrier_before_approved'
        WHEN order_delivered_customer_date IS NOT NULL
             AND order_delivered_carrier_date IS NOT NULL
             AND order_delivered_customer_date < order_delivered_carrier_date THEN 'customer_before_carrier'
        WHEN order_delivered_customer_date IS NOT NULL
             AND order_delivered_customer_date < order_purchase_timestamp THEN 'delivered_before_purchase'
        ELSE 'normal'
    END AS date_error_type
FROM orders
WHERE
    (order_approved_at IS NOT NULL AND order_approved_at < order_purchase_timestamp)
    OR (order_delivered_carrier_date IS NOT NULL AND order_approved_at IS NOT NULL AND order_delivered_carrier_date < order_approved_at)
    OR (order_delivered_customer_date IS NOT NULL AND order_delivered_carrier_date IS NOT NULL AND order_delivered_customer_date < order_delivered_carrier_date)
    OR (order_delivered_customer_date IS NOT NULL AND order_delivered_customer_date < order_purchase_timestamp);
