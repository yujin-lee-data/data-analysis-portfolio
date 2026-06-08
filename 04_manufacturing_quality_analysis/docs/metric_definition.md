# 지표 정의서

> 이 문서는 분석에 사용한 핵심 지표와 계산·해석 기준을 정리합니다.

> 해석 원칙: 본 프로젝트는 공개 데이터 기준의 관찰 분석입니다. 실제 제조 공정의 구체적 판단을 확정하거나 성과를 검증하지 않습니다. 결과는 우선 점검 후보를 정리하기 위한 참고 자료이며 현장 해석에는 공정 지식과 추가 검증이 필요합니다.

## 1. 라벨 지표

| 지표 | 정의 | 해석 |
|---|---|---|
| Pass Count | `Pass/Fail = -1`인 건수 | 공개 데이터 기준 정상 판정 수 |
| Fail Count | `Pass/Fail = 1`인 건수 | 공개 데이터 기준 Fail 판정 수 |
| Fail Rate | Fail Count / Total Count | 공개 데이터 기준 Fail 라벨 비율 |

## 2. 결측 지표

| 지표 | 정의 | 사용 목적 |
|---|---|---|
| Missing Count | 해당 변수의 결측 건수 | 데이터 품질 상태 확인 |
| Missing Rate | Missing Count / 전체 행 수 | 관리 주의 변수 확인 |
| Missing Band | 결측률 구간 | 분석 제외/주의/사용 가능 후보 구분 |

결측 구간 기준은 다음과 같습니다.

| 구간 | 기준 | 해석 |
|---|---|---|
| Low | 10% 미만 | 기본 분석 가능 |
| Medium | 10% 이상 40% 미만 | 주의 관찰 필요 |
| High | 40% 이상 | 해석 주의 또는 제외 후보 |

## 3. Pass/Fail 그룹 차이 지표

| 지표 | 정의 | 해석 |
|---|---|---|
| Pass Mean | Pass 그룹의 평균 | 정상 라벨 측정값 평균 |
| Fail Mean | Fail 그룹의 평균 | Fail 라벨 측정값 평균 |
| Mean Difference | Fail Mean - Pass Mean | 그룹 간 평균 차이 |
| Standardized Mean Difference | 평균 차이 / 전체 표준편차 | 변수 단위 차이를 보정한 차이 |
| Abs Standardized Mean Difference | 표준화 평균 차이의 절댓값 | 차이 크기 중심 정렬에 사용 |

## 4. 변동성 지표

| 지표 | 정의 | 해석 |
|---|---|---|
| Standard Deviation | 측정값 표준편차 | 값의 변동성 |
| IQR | 3사분위수 - 1사분위수 | 중앙 50% 구간의 퍼짐 |
| Outlier Rate IQR | IQR 기준 범위 밖 값 비율 | 극단값 가능성 참고 지표 |

## 5. 우선순위 점수

최종 점검 우선순위 점수는 다음 기준을 종합합니다.

```text
Priority Score = 0.45 * Group Difference Score
               + 0.20 * Missing Risk Score
               + 0.25 * Variability Score
               + 0.10 * Outlier Score
```

| 구성 요소 | 의미 | 가중치 |
|---|---|---:|
| Group Difference Score | Pass/Fail 간 차이가 큰 정도 | 45% |
| Missing Risk Score | 결측 관리 필요성 | 20% |
| Variability Score | 측정값 변동성 | 25% |
| Outlier Score | IQR 기준 극단값 비율 | 10% |

이 점수는 실제 원인 확정 점수가 아니라 본 공개 데이터 기준으로 추가 점검할 측정 신호 후보를 정렬하기 위한 분석용 기준입니다.
