-- 품질 라벨별 분포 차이가 큰 측정 신호 Top 20
SELECT feature, ROUND(abs_standardized_mean_difference, 4) AS abs_std_mean_diff, ROUND(missing_rate * 100, 2) AS missing_rate_pct
FROM feature_group_difference
WHERE missing_rate < 0.40
ORDER BY abs_standardized_mean_difference DESC
LIMIT 20;
