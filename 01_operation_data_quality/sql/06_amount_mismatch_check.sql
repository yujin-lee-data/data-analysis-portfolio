WITH item_amount AS (
    SELECT
        order_id,
        SUM(price + freight_value) AS item_total_amount
    FROM order_items
    GROUP BY order_id
),
payment_amount AS (
    SELECT
        order_id,
        SUM(payment_value) AS payment_total_amount
    FROM payments
    GROUP BY order_id
)
SELECT
    i.order_id,
    i.item_total_amount,
    p.payment_total_amount,
    ROUND(p.payment_total_amount - i.item_total_amount, 2) AS amount_diff
FROM item_amount i
JOIN payment_amount p
    ON i.order_id = p.order_id
WHERE ABS(p.payment_total_amount - i.item_total_amount) >= 1
ORDER BY ABS(p.payment_total_amount - i.item_total_amount) DESC
LIMIT 10;
