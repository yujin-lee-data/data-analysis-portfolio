-- Demographic summary for households available in hh_demographic only.
WITH basket_sales AS (
  SELECT household_key, BASKET_ID, SUM(SALES_VALUE) AS basket_sales
  FROM transaction_data
  WHERE SALES_VALUE >= 0
  GROUP BY household_key, BASKET_ID
), customer_summary AS (
  SELECT household_key, SUM(basket_sales) AS total_sales, COUNT(*) AS purchase_count
  FROM basket_sales
  GROUP BY household_key
)
SELECT
  h.INCOME_DESC,
  COUNT(*) AS customers,
  AVG(c.total_sales) AS avg_total_sales,
  AVG(c.purchase_count) AS avg_purchase_count
FROM customer_summary c
JOIN hh_demographic h ON c.household_key = h.household_key
GROUP BY h.INCOME_DESC
ORDER BY avg_total_sales DESC;
