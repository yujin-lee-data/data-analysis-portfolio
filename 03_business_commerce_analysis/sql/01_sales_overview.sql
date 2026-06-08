-- Sales overview from raw transaction_data.csv loaded as transaction_data
-- DAY/WEEK_NO are relative period fields inside the public dataset, not project execution dates.
SELECT
  COUNT(*) AS transaction_rows,
  COUNT(DISTINCT household_key) AS customers,
  COUNT(DISTINCT BASKET_ID) AS baskets,
  COUNT(DISTINCT PRODUCT_ID) AS products,
  MIN(DAY) AS relative_day_min,
  MAX(DAY) AS relative_day_max,
  MIN(WEEK_NO) AS relative_week_min,
  MAX(WEEK_NO) AS relative_week_max,
  SUM(SALES_VALUE) AS total_sales_value,
  SUM(QUANTITY) AS total_quantity
FROM transaction_data
WHERE SALES_VALUE >= 0;
