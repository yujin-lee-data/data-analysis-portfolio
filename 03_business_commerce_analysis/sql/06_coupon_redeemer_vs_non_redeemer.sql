-- Observational comparison only: coupon redemption is not randomly assigned here.
WITH basket_sales AS (
  SELECT household_key, BASKET_ID, SUM(SALES_VALUE) AS basket_sales
  FROM transaction_data
  WHERE SALES_VALUE >= 0
  GROUP BY household_key, BASKET_ID
), customer_summary AS (
  SELECT household_key, SUM(basket_sales) AS total_sales, COUNT(*) AS purchase_count
  FROM basket_sales
  GROUP BY household_key
), redeemers AS (
  SELECT DISTINCT household_key FROM coupon_redempt
)
SELECT
  CASE WHEN r.household_key IS NULL THEN 'non-redeemer' ELSE 'coupon redeemer' END AS coupon_redeemer_group,
  COUNT(*) AS customers,
  SUM(c.total_sales) AS total_sales,
  AVG(c.total_sales) AS avg_sales_per_customer,
  AVG(c.purchase_count) AS avg_purchase_count
FROM customer_summary c
LEFT JOIN redeemers r ON c.household_key = r.household_key
GROUP BY 1;
