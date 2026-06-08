-- Customer-level contribution: revenue concentration, not customer lifetime value prediction.
WITH basket_sales AS (
  SELECT household_key, BASKET_ID, SUM(SALES_VALUE) AS basket_sales
  FROM transaction_data
  WHERE SALES_VALUE >= 0
  GROUP BY household_key, BASKET_ID
), customer_sales AS (
  SELECT household_key, SUM(basket_sales) AS total_sales, COUNT(*) AS purchase_count
  FROM basket_sales
  GROUP BY household_key
)
SELECT
  household_key, total_sales, purchase_count,
  total_sales / NULLIF(purchase_count, 0) AS avg_basket_value
FROM customer_sales
ORDER BY total_sales DESC;
