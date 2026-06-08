-- 사용자/세션 내 이벤트 발생 순서를 반영한 순차 퍼널 계산 예시
-- 독립적인 단계별 DISTINCT 집계와 달리, 이전 단계 이후 다음 단계가 발생했는지 확인합니다.
WITH base AS (
  SELECT
    user_pseudo_id,
    (SELECT value.int_value FROM UNNEST(event_params) WHERE key = 'ga_session_id') AS ga_session_id,
    event_name,
    TIMESTAMP_MICROS(event_timestamp) AS event_ts
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
    AND event_name IN ('session_start','view_item','add_to_cart','begin_checkout','purchase')
), per_session AS (
  SELECT
    user_pseudo_id,
    ga_session_id,
    MIN(IF(event_name = 'session_start', event_ts, NULL)) AS session_start_ts,
    MIN(IF(event_name = 'view_item', event_ts, NULL)) AS view_item_ts,
    MIN(IF(event_name = 'add_to_cart', event_ts, NULL)) AS add_to_cart_ts,
    MIN(IF(event_name = 'begin_checkout', event_ts, NULL)) AS begin_checkout_ts,
    MIN(IF(event_name = 'purchase', event_ts, NULL)) AS purchase_ts
  FROM base
  GROUP BY user_pseudo_id, ga_session_id
), flags AS (
  SELECT
    user_pseudo_id,
    ga_session_id,
    session_start_ts IS NOT NULL AS reached_session_start,
    view_item_ts IS NOT NULL AND view_item_ts >= session_start_ts AS reached_view_item,
    add_to_cart_ts IS NOT NULL AND add_to_cart_ts >= view_item_ts AS reached_add_to_cart,
    begin_checkout_ts IS NOT NULL AND begin_checkout_ts >= add_to_cart_ts AS reached_begin_checkout,
    purchase_ts IS NOT NULL AND purchase_ts >= begin_checkout_ts AS reached_purchase
  FROM per_session
  WHERE session_start_ts IS NOT NULL
), step_users AS (
  SELECT 1 AS step_order, 'session_start' AS step, COUNT(DISTINCT IF(reached_session_start, user_pseudo_id, NULL)) AS users FROM flags UNION ALL
  SELECT 2, 'view_item', COUNT(DISTINCT IF(reached_view_item, user_pseudo_id, NULL)) FROM flags UNION ALL
  SELECT 3, 'add_to_cart', COUNT(DISTINCT IF(reached_add_to_cart, user_pseudo_id, NULL)) FROM flags UNION ALL
  SELECT 4, 'begin_checkout', COUNT(DISTINCT IF(reached_begin_checkout, user_pseudo_id, NULL)) FROM flags UNION ALL
  SELECT 5, 'purchase', COUNT(DISTINCT IF(reached_purchase, user_pseudo_id, NULL)) FROM flags
)
SELECT
  step,
  users,
  SAFE_DIVIDE(users, LAG(users) OVER (ORDER BY step_order)) AS conversion_from_previous,
  1 - SAFE_DIVIDE(users, LAG(users) OVER (ORDER BY step_order)) AS dropoff_from_previous,
  SAFE_DIVIDE(users, FIRST_VALUE(users) OVER (ORDER BY step_order)) AS overall_conversion_from_session
FROM step_users
ORDER BY step_order;
