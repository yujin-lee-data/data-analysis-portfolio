-- 09_category_user_event_summary.sql
-- 목적: 카테고리별 사용자 모수와 이벤트 수를 함께 확인한다.
-- 주의: 실제 GA4 BigQuery 원본에서는 items가 중첩 구조이므로 UNNEST(items)를 사용한다.

WITH base AS (
  SELECT
    event_name,
    user_pseudo_id,
    item.item_category AS item_category
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`,
  UNNEST(items) AS item
  WHERE event_name IN ('view_item', 'add_to_cart', 'begin_checkout', 'purchase')
    AND item.item_category IS NOT NULL
)
SELECT
  item_category,
  COUNT(DISTINCT user_pseudo_id) AS total_users,
  COUNT(*) AS total_events,
  COUNT(DISTINCT IF(event_name = 'view_item', user_pseudo_id, NULL)) AS view_item_users,
  COUNT(DISTINCT IF(event_name = 'add_to_cart', user_pseudo_id, NULL)) AS add_to_cart_users,
  COUNT(DISTINCT IF(event_name = 'begin_checkout', user_pseudo_id, NULL)) AS begin_checkout_users,
  COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL)) AS purchase_users,
  COUNTIF(event_name = 'view_item') AS view_item_events,
  COUNTIF(event_name = 'add_to_cart') AS add_to_cart_events,
  COUNTIF(event_name = 'begin_checkout') AS begin_checkout_events,
  COUNTIF(event_name = 'purchase') AS purchase_events,
  SAFE_DIVIDE(
    COUNT(DISTINCT IF(event_name = 'add_to_cart', user_pseudo_id, NULL)),
    COUNT(DISTINCT IF(event_name = 'view_item', user_pseudo_id, NULL))
  ) AS view_to_cart_rate,
  SAFE_DIVIDE(
    COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL)),
    COUNT(DISTINCT IF(event_name = 'view_item', user_pseudo_id, NULL))
  ) AS view_to_purchase_rate
FROM base
GROUP BY item_category
ORDER BY view_to_purchase_rate ASC;
