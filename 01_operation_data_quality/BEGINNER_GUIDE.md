# 초보자 실행 가이드

> 이 문서는 서비스 운영 데이터 품질 관리 프로젝트를 처음 여는 사람도 실행 흐름을 이해할 수 있도록 정리한 안내서입니다.

## 1. 이 프로젝트가 하는 일

Olist 공개 이커머스 데이터를 활용해 주문·결제·배송·판매자 데이터의 정합성을 점검합니다. 분석 결과는 실제 오류 확정이 아니라 운영자가 추가로 확인할 수 있는 검수 후보와 우선순위를 정리한 결과입니다.

## 2. 필요한 준비물

- Python 3.10 이상
- 인터넷에서 패키지를 설치할 수 있는 환경
- Kaggle에서 다운로드한 Olist 원본 CSV

## 3. 데이터 준비 방법

Kaggle에서 `Olist Brazilian E-Commerce Public Dataset`을 다운로드한 뒤 아래 파일을 `data/raw/` 폴더에 넣습니다.

```text
olist_orders_dataset.csv
olist_order_payments_dataset.csv
olist_order_items_dataset.csv
olist_sellers_dataset.csv
olist_order_reviews_dataset.csv
```

원본 CSV는 용량과 출처 관리를 위해 GitHub에 포함하지 않았습니다.

> 원본 데이터가 없으면 전체 재실행은 불가합니다. 이는 코드 오류가 아니라 공개 데이터 원본 다운로드가 필요한 구조입니다.

## 4. 패키지 설치

터미널 또는 명령 프롬프트에서 프로젝트 폴더로 이동한 뒤 아래 명령어를 입력합니다.

```bash
pip install -r requirements.txt
```

Windows에서 `python` 명령어가 실행되지 않으면 `py` 명령어를 사용할 수 있습니다.

## 5. Python 실행

```bash
python scripts/run_analysis.py
```

Windows에서 `python` 명령어가 실행되지 않으면 아래처럼 실행합니다.

```bash
py scripts/run_analysis.py
```

## 6. 결과 확인

- 결과 CSV: `data/processed/`
- 차트 이미지: `figures/`
- 분석 결과 요약: `reports/analysis_result_summary.md`
- 최종 PDF 보고서: `reports/01_operation_data_quality_report.pdf`
- 최종 PPT 보고서: `reports/01_operation_data_quality_report.pptx`

## 7. 자주 발생하는 오류

- 파일 경로 오류: 원본 CSV가 `data/raw/` 폴더에 있는지 확인합니다.
- 패키지 설치 오류: `pip install -r requirements.txt`를 다시 실행합니다.
- 한글 글꼴 표시 오류: 분석 결과에는 영향이 없으며 실행 환경에 따라 차트 글꼴이 다르게 보일 수 있습니다.

## 8. 해석 시 주의사항

- 본 프로젝트는 공개 데이터 기반 관찰 분석입니다.
- `payments.order_id`와 `order_items.order_id`는 한 주문에 여러 결제 또는 여러 상품이 포함될 수 있어 중복이 정상 구조일 수 있습니다.
- 금액 차이, 배송 지연, 날짜 역전 등은 실제 오류 확정이 아니라 검수 후보로 해석합니다.
- 실제 원인 판단에는 결제 정책, 쿠폰·포인트·환불 정책, 배송 정책 등 추가 정보가 필요합니다.
