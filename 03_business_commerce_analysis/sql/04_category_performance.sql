-- Product/category performance based on observed transaction sales.
SELECT
  p.DEPARTMENT, p.COMMODITY_DESC,
  SUM(t.SALES_VALUE) AS total_sales,
  COUNT(DISTINCT t.BASKET_ID) AS baskets,
  COUNT(DISTINCT t.household_key) AS customers,
  SUM(t.QUANTITY) AS units
FROM transaction_data t
LEFT JOIN product p ON t.PRODUCT_ID = p.PRODUCT_ID
WHERE t.SALES_VALUE >= 0
GROUP BY p.DEPARTMENT, p.COMMODITY_DESC
ORDER BY total_sales DESC;
