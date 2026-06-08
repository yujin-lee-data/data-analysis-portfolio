-- 변동성이 큰 측정 신호 후보
SELECT feature, non_missing_count, ROUND(std, 4) AS std, ROUND(iqr, 4) AS iqr, ROUND(outlier_rate_iqr * 100, 2) AS outlier_rate_pct
FROM feature_variability_summary
WHERE missing_rate < 0.40
ORDER BY std DESC
LIMIT 30;
