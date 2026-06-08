-- 상품 카테고리별 조회/장바구니/구매 전환율
WITH item_events AS (
  SELECT
    user_pseudo_id,
    event_name,
    item.item_category AS item_category
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
  UNNEST(items) AS item
  WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
    AND event_name IN ('view_item','add_to_cart','begin_checkout','purchase')
)
SELECT
  item_category,
  COUNT(DISTINCT IF(event_name='view_item', user_pseudo_id, NULL)) AS view_item_users,
  COUNT(DISTINCT IF(event_name='add_to_cart', user_pseudo_id, NULL)) AS add_to_cart_users,
  COUNT(DISTINCT IF(event_name='purchase', user_pseudo_id, NULL)) AS purchase_users,
  SAFE_DIVIDE(COUNT(DISTINCT IF(event_name='add_to_cart', user_pseudo_id, NULL)), COUNT(DISTINCT IF(event_name='view_item', user_pseudo_id, NULL))) AS view_to_cart_rate,
  SAFE_DIVIDE(COUNT(DISTINCT IF(event_name='purchase', user_pseudo_id, NULL)), COUNT(DISTINCT IF(event_name='view_item', user_pseudo_id, NULL))) AS view_to_purchase_rate
FROM item_events
WHERE item_category IS NOT NULL
GROUP BY item_category
ORDER BY view_to_purchase_rate ASC;
