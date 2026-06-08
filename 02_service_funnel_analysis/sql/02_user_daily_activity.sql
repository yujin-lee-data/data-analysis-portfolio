-- 일자별 활성 사용자와 주요 이벤트 수
SELECT
  PARSE_DATE('%Y%m%d', event_date) AS event_dt,
  COUNT(DISTINCT user_pseudo_id) AS active_users,
  COUNTIF(event_name = 'view_item') AS view_item_events,
  COUNTIF(event_name = 'add_to_cart') AS add_to_cart_events,
  COUNTIF(event_name = 'begin_checkout') AS begin_checkout_events,
  COUNTIF(event_name = 'purchase') AS purchase_events
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
GROUP BY event_dt
ORDER BY event_dt;
