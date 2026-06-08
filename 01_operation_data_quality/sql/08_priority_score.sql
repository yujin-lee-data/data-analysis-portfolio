WITH error_summary AS (
    SELECT 'amount_mismatch' AS error_type,
           COUNT(*) AS error_count,
           5 AS impact_score,
           5 AS urgency_score
    FROM (
        SELECT
            i.order_id,
            SUM(i.price + i.freight_value) AS item_total_amount,
            SUM(p.payment_value) AS payment_total_amount
        FROM order_items i
        JOIN payments p ON i.order_id = p.order_id
        GROUP BY i.order_id
    ) t
    WHERE ABS(payment_total_amount - item_total_amount) >= 1

    UNION ALL

    SELECT 'payment_missing' AS error_type,
           COUNT(*) AS error_count,
           5 AS impact_score,
           5 AS urgency_score
    FROM orders o
    LEFT JOIN payments p
        ON o.order_id = p.order_id
    WHERE p.order_id IS NULL

    UNION ALL

    SELECT 'date_reversal' AS error_type,
           COUNT(*) AS error_count,
           4 AS impact_score,
           4 AS urgency_score
    FROM orders
    WHERE
        (order_approved_at IS NOT NULL AND order_approved_at < order_purchase_timestamp)
        OR (order_delivered_customer_date IS NOT NULL AND order_delivered_customer_date < order_purchase_timestamp)

    UNION ALL

    SELECT 'late_delivery' AS error_type,
           COUNT(*) AS error_count,
           3 AS impact_score,
           3 AS urgency_score
    FROM orders
    WHERE order_delivered_customer_date > order_estimated_delivery_date
)
SELECT
    error_type,
    error_count,
    impact_score,
    urgency_score,
    NTILE(5) OVER (ORDER BY error_count) AS frequency_score,
    ROUND(
        NTILE(5) OVER (ORDER BY error_count) * 0.4
        + impact_score * 0.4
        + urgency_score * 0.2,
        2
    ) AS priority_score
FROM error_summary
ORDER BY priority_score DESC;
