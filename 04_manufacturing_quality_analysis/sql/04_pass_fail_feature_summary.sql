-- Pass/Fail 그룹 간 평균 차이 요약
SELECT feature, pass_count, fail_count, ROUND(pass_mean, 4) AS pass_mean, ROUND(fail_mean, 4) AS fail_mean,
       ROUND(mean_difference_fail_minus_pass, 4) AS mean_diff,
       ROUND(standardized_mean_difference, 4) AS std_mean_diff
FROM feature_group_difference
WHERE missing_rate < 0.40
ORDER BY ABS(standardized_mean_difference) DESC
LIMIT 30;
