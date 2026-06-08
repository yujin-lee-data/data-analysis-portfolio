# GA4 기반 서비스 퍼널 분석 프로젝트

> Google BigQuery GA4 공개 이커머스 샘플 데이터로 사용자 대표 행동 흐름(`session_start → view_item → add_to_cart → begin_checkout → purchase`)을 정의하고 단계별 전환율·이탈률과 우선 점검 구간을 분석한 프로젝트입니다.
> **공개 데이터 기반 관찰 분석이며 실제 개선 성과나 인과관계를 주장하지 않습니다.**

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 분석 목적 | 5단계 이커머스 퍼널의 전환·이탈 구간 진단 및 우선 점검 구간 도출 |
| 사용 데이터 | GA4 Ecommerce Sample (Google BigQuery Public Dataset) |
| 사용 도구 | BigQuery SQL, Python (pandas, numpy, matplotlib) |
| 주요 산출물 | 재현용 SQL, BigQuery 결과 CSV, 차트, PPT/PDF 보고서 |
| 분석 성격 | 공개 샘플 데이터 기반 관찰 분석 (개선 성과 아님) |

## 2. 데이터 출처

- 데이터셋: Google BigQuery Public Dataset — GA4 Ecommerce Sample
- 본 저장소에는 BigQuery 결과 CSV와 재현용 SQL/Python 코드만 포함합니다(원본 로그는 BigQuery에서 조회).
- 데이터 기준 기간은 공개 데이터셋의 이벤트 발생 기간이며 프로젝트 수행 기간이 아닙니다.

## 3. 분석 질문

1. 정의한 순차 퍼널에서 단계별 전환율·이탈률은 어떻게 나타나는가?
2. 어느 구간의 이탈이 가장 커서 우선 점검 대상인가?
3. 디바이스·카테고리 세그먼트에 따라 전환 차이가 있는가?
4. 구매자와 비구매자의 핵심 이벤트 행동은 어떻게 다른가?

## 4. 주요 결과 요약

- 퍼널 시작(`session_start`) 사용자 약 267,116명 기준으로 분석했습니다.
- `view_item → add_to_cart` 구간 이탈률이 79.5%로 가장 높아 우선 점검 구간으로 관찰됩니다.
- `add_to_cart → begin_checkout` 이탈률 61.8%, `begin_checkout → purchase` 이탈률 7.9%입니다.
- 디바이스별 session-to-purchase 전환율은 큰 차이가 나타나지 않아 디바이스 단독보다 퍼널 단계별 점검이 우선입니다.

(모두 공개 샘플 데이터 기준 관찰 결과이며 실제 서비스 개선 성과를 의미하지 않습니다.)

## 5. 실행 방법

이미 BigQuery 결과 CSV가 포함되어 있어 바로 차트 재생성이 가능합니다.

```bash
pip install -r requirements.txt
python python/run_analysis_actual.py     # 또는: python scripts/run_analysis.py (동일 동작 래퍼)
```

실행 후 `charts/`에 차트가 생성됩니다. (Windows에서 `python`이 안 되면 `py` 사용)

## 6. 폴더 구조

```text
02_service_funnel_analysis/
├── README.md
├── BEGINNER_GUIDE.md
├── requirements.txt
├── sql/        # BigQuery 재현용 SQL
├── data/
│   ├── actual_bigquery/   # BigQuery 결과 CSV 원본
│   └── output_csv/        # 차트 재생성용 결과 CSV
├── python/     # 분석·차트 재생성 코드 (메인)
├── charts/     # 리포트용 차트 이미지
├── reports/     # PPT/PDF 보고서
├── scripts/       # run_analysis.py (python/ 실행 래퍼)
└── docs/          # 분석 기획·데이터·지표·전처리 정의
```

## 7. 해석 시 주의사항

- 퍼널은 분석자가 정의한 대표 행동 흐름이며 모든 사용자 여정을 대변하지 않습니다.
- 사용자 기준 집계와 이벤트 기준 집계는 구분해 해석해야 합니다.
- 카테고리별 결과는 이벤트별 item 파라미터 적재 범위의 영향을 받아 추가 검증이 필요합니다.

## 8. 산출물

- 최종 PDF 보고서: `reports/02_service_funnel_analysis_report.pdf`
- 최종 PPT 보고서: `reports/02_service_funnel_analysis_report.pptx`
