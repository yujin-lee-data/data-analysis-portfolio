-- 결측률이 높은 측정 신호 후보
SELECT feature, missing_count, ROUND(missing_rate * 100, 2) AS missing_rate_pct
FROM feature_missing_summary
WHERE missing_rate >= 0.40
ORDER BY missing_rate DESC, feature
LIMIT 50;
