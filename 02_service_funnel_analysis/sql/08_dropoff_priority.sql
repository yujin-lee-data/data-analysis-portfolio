-- 이탈 우선순위 계산: 이탈률과 이탈 사용자 수를 함께 반영
WITH step_users AS (
  SELECT 1 AS step_order, 'session_start' AS step, COUNT(DISTINCT IF(event_name='session_start', user_pseudo_id, NULL)) AS users FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131' UNION ALL
  SELECT 2, 'view_item', COUNT(DISTINCT IF(event_name='view_item', user_pseudo_id, NULL)) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131' UNION ALL
  SELECT 3, 'add_to_cart', COUNT(DISTINCT IF(event_name='add_to_cart', user_pseudo_id, NULL)) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131' UNION ALL
  SELECT 4, 'begin_checkout', COUNT(DISTINCT IF(event_name='begin_checkout', user_pseudo_id, NULL)) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131' UNION ALL
  SELECT 5, 'purchase', COUNT(DISTINCT IF(event_name='purchase', user_pseudo_id, NULL)) FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*` WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
), calc AS (
  SELECT
    step_order, step, users,
    LAG(users) OVER (ORDER BY step_order) AS previous_users
  FROM step_users
)
SELECT
  step,
  users,
  previous_users - users AS dropoff_users,
  1 - SAFE_DIVIDE(users, previous_users) AS dropoff_rate,
  (previous_users - users) * (1 - SAFE_DIVIDE(users, previous_users)) AS priority_score
FROM calc
WHERE previous_users IS NOT NULL
ORDER BY priority_score DESC;
