-- Pass/Fail 라벨 분포 확인
SELECT label_name, count, ROUND(rate * 100, 2) AS rate_pct
FROM label_distribution
ORDER BY label_name;
