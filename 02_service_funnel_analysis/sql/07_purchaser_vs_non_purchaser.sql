-- 구매자/비구매자 행동량 비교용 사용자 단위 집계
WITH user_events AS (
  SELECT
    user_pseudo_id,
    COUNT(*) AS total_events,
    COUNTIF(event_name='view_item') AS view_item_events,
    COUNTIF(event_name='add_to_cart') AS add_to_cart_events,
    COUNTIF(event_name='begin_checkout') AS begin_checkout_events,
    COUNTIF(event_name='purchase') AS purchase_events
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  GROUP BY user_pseudo_id
)
SELECT
  purchase_events > 0 AS is_purchaser,
  AVG(total_events) AS avg_total_events,
  AVG(view_item_events) AS avg_view_item_events,
  AVG(add_to_cart_events) AS avg_add_to_cart_events,
  AVG(begin_checkout_events) AS avg_begin_checkout_events
FROM user_events
GROUP BY is_purchaser;
