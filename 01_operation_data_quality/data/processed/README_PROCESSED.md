# 데이터 폴더 안내

> 이 문서는 분석 실행 후 생성되는 결과 CSV의 역할을 설명합니다.

## 1. 포함 파일

- `error_summary.csv`: 오류 후보 유형별 건수와 비율
- `priority_score.csv`: 빈도·영향도·긴급도를 반영한 검수 우선순위 점수
- `seller_error_rate.csv`: 판매자별 오류 후보 비율 (주문 30건 이상 판매자 대상)
- `late_delivery_review_score.csv`: 배송 지연 여부별 평균 리뷰 점수 (orders는 주문 단위 고유 개수, 고유 order_id 기준)
- `late_delivery_review_ttest.csv`: 배송 지연 여부에 따른 리뷰 점수 평균 차이 Welch t-test 보조 결과 (group_n은 리뷰 행 단위 개수이며 한 주문에 리뷰가 둘 이상 있는 경우가 일부 있어 위 score 표의 주문 수와 다를 수 있습니다. 평균·검정 결론에는 영향이 없습니다.)
- `amount_mismatch_top10.csv`: 금액 불일치 후보 상위 사례 10건

## 2. 재현 방법

`data/raw` 원본 CSV를 넣고 `py scripts/run_analysis.py`를 실행하면 이 폴더의 결과 파일은 다시 생성될 수 있습니다.
