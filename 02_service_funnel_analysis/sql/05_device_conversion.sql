-- 디바이스별 퍼널 전환율
WITH base AS (
  SELECT user_pseudo_id, device.category AS device_category, event_name
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
    AND event_name IN ('session_start','view_item','add_to_cart','begin_checkout','purchase')
)
SELECT
  device_category,
  COUNT(DISTINCT IF(event_name='session_start', user_pseudo_id, NULL)) AS session_start_users,
  COUNT(DISTINCT IF(event_name='view_item', user_pseudo_id, NULL)) AS view_item_users,
  COUNT(DISTINCT IF(event_name='add_to_cart', user_pseudo_id, NULL)) AS add_to_cart_users,
  COUNT(DISTINCT IF(event_name='begin_checkout', user_pseudo_id, NULL)) AS begin_checkout_users,
  COUNT(DISTINCT IF(event_name='purchase', user_pseudo_id, NULL)) AS purchase_users,
  SAFE_DIVIDE(COUNT(DISTINCT IF(event_name='purchase', user_pseudo_id, NULL)), COUNT(DISTINCT IF(event_name='session_start', user_pseudo_id, NULL))) AS session_to_purchase_rate
FROM base
GROUP BY device_category
ORDER BY session_to_purchase_rate DESC;
