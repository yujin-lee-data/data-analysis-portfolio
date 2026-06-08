-- Weekly sales trend. WEEK_NO is a relative dataset period variable.
SELECT
  WEEK_NO,
  SUM(SALES_VALUE) AS weekly_sales,
  COUNT(DISTINCT household_key) AS active_customers,
  COUNT(DISTINCT BASKET_ID) AS baskets
FROM transaction_data
WHERE SALES_VALUE >= 0
GROUP BY WEEK_NO
ORDER BY WEEK_NO;
