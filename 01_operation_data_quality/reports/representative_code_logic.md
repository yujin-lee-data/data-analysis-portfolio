# 대표 코드 로직

> 이 문서는 프로젝트의 핵심 SQL/Python 로직과 활용 목적을 정리합니다.

## 1. 금액 불일치 후보 탐지 SQL

```sql
WITH item_amount AS (
    SELECT
        order_id,
        SUM(price + freight_value) AS item_total_amount
    FROM order_items
    GROUP BY order_id
),
payment_amount AS (
    SELECT
        order_id,
        SUM(payment_value) AS payment_total_amount
    FROM payments
    GROUP BY order_id
)
SELECT
    i.order_id,
    i.item_total_amount,
    p.payment_total_amount,
    ROUND(p.payment_total_amount - i.item_total_amount, 2) AS amount_diff
FROM item_amount i
JOIN payment_amount p
    ON i.order_id = p.order_id
WHERE ABS(p.payment_total_amount - i.item_total_amount) >= 1
ORDER BY ABS(p.payment_total_amount - i.item_total_amount) DESC;
```

## 2. 우선순위 점수 계산 Python

```python
priority['priority_score'] = (
    priority['frequency_score'] * 0.4 +
    priority['impact_score'] * 0.4 +
    priority['urgency_score'] * 0.2
).round(2)
```

## 3. 배송 지연 후보 생성 Python

```python
orders['late_delivery'] = (
    orders['order_delivered_customer_date'].notna() &
    orders['order_estimated_delivery_date'].notna() &
    (orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date'])
)
```

## 4. 배송 지연과 리뷰 점수 Welch t-test

```python
t_stat, p_value = stats.ttest_ind(false_scores, true_scores, equal_var=False)
```

본 프로젝트의 통계 검정은 인과관계 판단이 아니라 두 그룹의 평균 차이를 보조적으로 확인하기 위한 목적입니다.
