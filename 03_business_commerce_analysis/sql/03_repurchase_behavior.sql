-- Repurchase behavior based on distinct basket count.
WITH basket_sales AS (
  SELECT household_key, BASKET_ID, SUM(SALES_VALUE) AS basket_sales
  FROM transaction_data
  WHERE SALES_VALUE >= 0
  GROUP BY household_key, BASKET_ID
), customer_summary AS (
  SELECT household_key, COUNT(*) AS purchase_count, SUM(basket_sales) AS total_sales
  FROM basket_sales
  GROUP BY household_key
)
SELECT
  CASE WHEN purchase_count >= 2 THEN '2+ baskets' ELSE '1 basket' END AS repurchase_group,
  COUNT(*) AS customers,
  SUM(total_sales) AS total_sales,
  AVG(purchase_count) AS avg_purchase_count
FROM customer_summary
GROUP BY 1;
