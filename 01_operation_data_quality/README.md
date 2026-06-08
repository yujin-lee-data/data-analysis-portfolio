# 서비스 운영 데이터 품질 관리 프로젝트

> 공개 이커머스 데이터로 주문·결제·배송·판매자 테이블의 정합성 기준을 정의하고 SQL/Python으로 오류 후보를 탐지해 검수 우선순위를 도출한 프로젝트입니다.
> **공개 데이터 기반 관찰 분석이며 실제 오류 확정이나 개선 성과·인과관계를 주장하지 않습니다.**

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 분석 목적 | 주문·결제·배송 데이터의 정합성 점검 및 검수 우선순위 도출 |
| 사용 데이터 | Olist Brazilian E-Commerce Public Dataset (Kaggle) |
| 사용 도구 | SQL, Python (pandas, numpy, scipy, matplotlib) |
| 주요 산출물 | SQL 쿼리 8개, Python 분석 스크립트, 결과 CSV, 차트, PPT/PDF 보고서 |
| 분석 성격 | 공개 데이터 기반 관찰 분석 (오류 "확정"이 아닌 "검수 후보") |

## 2. 데이터 출처

- 데이터셋: Olist Brazilian E-Commerce Public Dataset
- 출처: Kaggle
- 원본 CSV는 용량·출처 관리를 위해 GitHub 업로드 대상에서 제외합니다(`.gitignore` 처리). 재현하려면 Kaggle에서 내려받아 `data/raw/`에 배치합니다.

```text
olist_orders_dataset.csv        olist_order_payments_dataset.csv
olist_order_items_dataset.csv   olist_sellers_dataset.csv
olist_order_reviews_dataset.csv
```

## 3. 분석 질문

1. 주문·결제·배송 데이터에서 어떤 정합성 오류 후보가 발생하는가?
2. 오류 유형별 발생 빈도와 비중은 어떻게 다른가?
3. 어떤 오류 유형을 먼저 검수해야 운영상 효율적인가?
4. 판매자별 오류율로 우선 확인 대상을 정할 수 있는가?
5. 배송 지연은 고객 리뷰 점수와 어떤 차이를 보이는가?

## 4. 주요 결과 요약

| 분석 항목 | 결과 |
|---|---|
| 배송 지연 후보 | 7,827건 (전체 주문의 7.87%) |
| 날짜 역전 후보 | 1,382건 (1.39%) |
| 금액 불일치 후보 | 250건 (0.25%) |
| 검수 우선순위 1위 | 금액 불일치 후보 (가중 점수 4.2) |
| 평균 리뷰 점수 | 배송 지연 없음 4.21점 / 배송 지연 2.57점 (Welch t=85.23, p<0.001) |

발생 건수는 배송 지연 후보가 가장 많지만 영향도·긴급도까지 가중한 우선순위에서는 금액 불일치 후보가 가장 높게 나타났습니다. 단순 건수뿐 아니라 결제·정산 신뢰도와 고객 경험에 미칠 수 있는 영향을 함께 고려해야 함을 보여줍니다. (점수는 검수 순서를 정하기 위한 가정이며 실제 기업 정책이 아닙니다.)

## 5. 실행 방법

```bash
# 1) 패키지 설치  (Windows는 py, Mac/Linux는 python3)
py -m pip install -r requirements.txt        # Windows
python3 -m pip install -r requirements.txt   # Mac/Linux

# 2) 분석 실행
py scripts/run_analysis.py                   # Windows
python3 scripts/run_analysis.py              # Mac/Linux
```

실행 후 `data/processed/`(CSV), `figures/`(차트), `reports/analysis_result_summary.md`(요약)가 생성됩니다.

## 6. 폴더 구조

```text
01_operation_data_quality/
├── README.md
├── BEGINNER_GUIDE.md
├── requirements.txt
├── data/
│   ├── raw/          # Olist 원본 CSV (직접 배치, GitHub 제외)
│   └── processed/    # 분석 결과 CSV
├── docs/             # 분석 기획·데이터·지표·전처리 정의
├── sql/              # 정합성 탐지 SQL 8개
├── scripts/          # run_analysis.py
├── figures/          # 차트 이미지
└── reports/          # PPT/PDF 보고서, 결과 요약
```

## 7. 해석 시 주의사항

- 오류 후보는 실제 오류 확정이 아니라 운영자가 추가 확인해야 할 검수 후보입니다.
- 금액 불일치 후보는 쿠폰·포인트·부분 취소·환불 등 내부 정책을 알 수 없어 정산 오류로 단정하지 않습니다.
- 배송 지연과 리뷰 점수 차이는 보조 신호이며 배송 지연이 낮은 리뷰의 직접적 원인이라고 단정하지 않습니다.
- 리뷰 점수 표(`late_delivery_review_score.csv`)의 건수는 주문 단위 고유 개수이고 Welch t-test의 group_n은 리뷰 행 단위 개수입니다. 한 주문에 리뷰가 둘 이상 있는 사례가 일부 있어 두 수치가 다를 수 있으나, 평균과 검정 결론에는 영향을 주지 않습니다.

## 8. 산출물

- 최종 PDF 보고서: `reports/01_operation_data_quality_report.pdf`
- 최종 PPT 보고서: `reports/01_operation_data_quality_report.pptx`
