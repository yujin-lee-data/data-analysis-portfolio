# 커머스 고객 · 매출 · 프로모션 분석 프로젝트

> Dunnhumby `The Complete Journey` 공개 데이터로 고객군 매출 기여도, 재구매 행동, 상품군 매출 구조, 쿠폰·캠페인 반응 차이를 분석한 비즈니스·커머스 프로젝트입니다.
> **공개 데이터 기반 관찰 분석이며 실제 매출 결과나 인과효과를 주장하지 않습니다.**

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 분석 목적 | 매출을 구성하는 고객·상품·프로모션 반응 구조 해석 및 관리 우선순위 정리 |
| 사용 데이터 | Dunnhumby - The Complete Journey (Kaggle) |
| 사용 도구 | SQL, Python (pandas, numpy, matplotlib) |
| 주요 산출물 | SQL 쿼리 8개, Python 분석 스크립트, 결과 CSV 10개, 차트, PPT/PDF 보고서 |
| 분석 성격 | 공개 관찰 데이터 기반 (쿠폰·캠페인은 인과가 아닌 반응 차이) |

## 2. 데이터 출처

- 데이터셋: Kaggle `Dunnhumby - The Complete Journey`
- 사용 파일: `transaction_data.csv`, `product.csv`, `campaign_table.csv`, `campaign_desc.csv`, `coupon_redempt.csv`, `hh_demographic.csv`
- 원본 CSV는 용량·출처 관리를 위해 GitHub 업로드 대상에서 제외합니다(`.gitignore` 처리). Kaggle에서 내려받아 `data/raw/`에 배치합니다.
- `DAY`, `WEEK_NO`는 데이터셋 내부의 상대 기간 변수이며 실제 날짜가 아닙니다.

## 3. 분석 질문

1. 전체 매출과 구매 활동은 어떤 규모로 나타나는가?
2. 매출 기여도가 높은 고객군은 전체 매출에서 어느 정도 비중을 차지하는가?
3. 재구매 고객과 단일 구매 고객의 행동 차이는 어떻게 나타나는가?
4. 어떤 상품군이 매출과 고객 접점에서 중요한가?
5. 쿠폰 사용·캠페인 반응 고객은 비사용 고객과 어떤 관찰상 차이를 보이는가?

## 4. 주요 결과 요약

- 분석 대상: 고객 2,500명, 장바구니 276,484개, 총 매출값 8,057,463 (SALES_VALUE 합계), 기준 기간 DAY 1–711 / WEEK 1–102.
- 매출 상위 20% 고객군이 전체 매출의 53.0%를 차지(파레토 구조)했습니다.
- 최상위 상품군은 `COUPON/MISC ITEMS`로 전체 매출의 6.4%, 쿠폰 장바구니 비율은 6.1%입니다.
- 캠페인 유형별 관찰 응답률은 `TypeA`가 가장 높게 나타났습니다. 단, 선택 편향이 포함된 관찰 차이이며 인과효과가 아닙니다.

## 5. 실행 방법

```bash
pip install -r requirements.txt
python scripts/run_analysis.py     # Windows에서 안 되면: py scripts/run_analysis.py
```

실행 후 `outputs/csv/`(결과 CSV)와 `outputs/charts/`(차트)가 생성됩니다.

## 6. 폴더 구조

```text
03_business_commerce_analysis/
├── README.md
├── BEGINNER_GUIDE.md
├── requirements.txt
├── data/
│   └── raw/          # Dunnhumby 원본 CSV 직접 배치, GitHub 제외
├── docs/             # 분석 기획·데이터·지표·전처리 정의
├── sql/              # 커머스 분석 SQL 8개
├── scripts/          # run_analysis.py
├── reports/          # PPT/PDF 보고서
└── outputs/
    ├── csv/          # 분석 결과 CSV 10개
    └── charts/       # 차트 이미지
```

## 7. 해석 시 주의사항

- 본 분석은 공개 관찰 데이터를 기준으로 한 결과이며 실제 기업 내부 성과로 해석하지 않습니다.
- 쿠폰·캠페인 분석은 무작위 실험(A/B 테스트)이 아니므로 프로모션의 매출 증가 효과를 단정할 수 없습니다. 실제 증분 효과는 별도 실험 또는 추가 검증이 필요합니다.
- `DAY`, `WEEK_NO`는 데이터셋 내부의 상대 기간 변수이며 매출값은 `SALES_VALUE` 기준으로 실제 원화 매출이 아닙니다.

## 8. 산출물

- 최종 PDF 보고서: `reports/03_business_commerce_analysis_report.pdf`
- 최종 PPT 보고서: `reports/03_business_commerce_analysis_report.pptx`
