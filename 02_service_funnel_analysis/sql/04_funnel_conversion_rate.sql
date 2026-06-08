-- 이전 단계 대비 전환율/이탈률 계산
WITH step_users AS (
  SELECT 'session_start' AS step, 1 AS step_order, COUNT(DISTINCT IF(event_name='session_start', user_pseudo_id, NULL)) AS users
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  UNION ALL
  SELECT 'view_item', 2, COUNT(DISTINCT IF(event_name='view_item', user_pseudo_id, NULL))
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  UNION ALL
  SELECT 'add_to_cart', 3, COUNT(DISTINCT IF(event_name='add_to_cart', user_pseudo_id, NULL))
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  UNION ALL
  SELECT 'begin_checkout', 4, COUNT(DISTINCT IF(event_name='begin_checkout', user_pseudo_id, NULL))
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  UNION ALL
  SELECT 'purchase', 5, COUNT(DISTINCT IF(event_name='purchase', user_pseudo_id, NULL))
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
)
SELECT
  step, users,
  SAFE_DIVIDE(users, LAG(users) OVER (ORDER BY step_order)) AS conversion_from_previous,
  1 - SAFE_DIVIDE(users, LAG(users) OVER (ORDER BY step_order)) AS dropoff_from_previous,
  SAFE_DIVIDE(users, FIRST_VALUE(users) OVER (ORDER BY step_order)) AS overall_conversion_from_session
FROM step_users
ORDER BY step_order;
