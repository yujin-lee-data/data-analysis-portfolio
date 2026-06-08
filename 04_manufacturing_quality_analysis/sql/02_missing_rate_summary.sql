-- 결측률 구간별 변수 수 확인
SELECT missing_band, COUNT(*) AS feature_count, ROUND(AVG(missing_rate) * 100, 2) AS avg_missing_rate_pct
FROM feature_missing_summary
GROUP BY missing_band
ORDER BY avg_missing_rate_pct;
