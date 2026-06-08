-- 결측률, 그룹 차이, 변동성을 함께 고려한 점검 우선순위
SELECT feature, ROUND(priority_score, 3) AS priority_score, ROUND(group_difference_score, 3) AS group_difference_score,
       ROUND(missing_risk_score, 3) AS missing_risk_score, ROUND(variability_score, 3) AS variability_score,
       ROUND(outlier_score, 3) AS outlier_score, analysis_status
FROM quality_signal_priority
ORDER BY priority_score DESC
LIMIT 30;
