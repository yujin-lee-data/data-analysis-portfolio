-- 퍼널 단계별 고유 사용자 수
SELECT
  event_name AS funnel_step,
  COUNT(DISTINCT user_pseudo_id) AS users
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE _TABLE_SUFFIX BETWEEN '20201101' AND '20210131'
  AND event_name IN ('session_start','view_item','add_to_cart','begin_checkout','purchase')
GROUP BY funnel_step
ORDER BY CASE funnel_step
  WHEN 'session_start' THEN 1
  WHEN 'view_item' THEN 2
  WHEN 'add_to_cart' THEN 3
  WHEN 'begin_checkout' THEN 4
  WHEN 'purchase' THEN 5
END;
