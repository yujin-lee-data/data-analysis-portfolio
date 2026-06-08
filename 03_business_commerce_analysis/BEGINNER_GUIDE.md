# 초보자 실행 가이드

> 이 문서는 커머스 고객·매출·프로모션 분석 프로젝트를 처음 여는 사람도 실행 흐름을 이해할 수 있도록 정리한 안내서입니다.

## 1. 이 프로젝트가 하는 일

Dunnhumby 공개 커머스 데이터를 활용해 고객군별 매출 기여도, 재구매 행동, 상품군 매출 구조, 쿠폰·캠페인 반응 차이를 확인합니다. 분석 결과는 실제 매출 증가나 프로모션 인과효과가 아니라 공개 관찰 데이터 기준의 반응 차이로 해석합니다.

## 2. 필요한 준비물

- Python 3.10 이상
- 인터넷에서 패키지를 설치할 수 있는 환경
- Kaggle에서 다운로드한 Dunnhumby 원본 CSV

## 3. 데이터 준비 방법

Kaggle에서 `Dunnhumby - The Complete Journey` 데이터셋을 다운로드한 뒤 아래 CSV 파일을 `data/raw/` 폴더에 넣습니다.

```text
transaction_data.csv
product.csv
campaign_table.csv
campaign_desc.csv
coupon_redempt.csv
hh_demographic.csv
```

원본 CSV는 용량과 출처 관리를 위해 GitHub에 포함하지 않았습니다.

> 원본 데이터가 없으면 전체 재실행은 불가합니다. 이는 코드 오류가 아니라 공개 데이터 원본 다운로드가 필요한 구조입니다. 해당 파일은 `.gitignore` 설정에 따라 업로드 대상에서 제외됩니다.

## 4. 패키지 설치

터미널 또는 명령 프롬프트에서 프로젝트 폴더로 이동한 뒤 아래 명령어를 입력합니다.

```bash
pip install -r requirements.txt
```

## 5. Python 실행

```bash
python scripts/run_analysis.py
```

Windows에서 `python` 명령어가 실행되지 않으면 아래처럼 실행합니다.

```bash
py scripts/run_analysis.py
```

## 6. 결과 확인

- 결과 CSV: `outputs/csv/`
- 차트 이미지: `outputs/charts/`
- 최종 PDF 보고서: `reports/03_business_commerce_analysis_report.pdf`
- 최종 PPT 보고서: `reports/03_business_commerce_analysis_report.pptx`

## 7. 자주 발생하는 오류

- `Missing raw files`: 필수 CSV를 `data/raw/`에 넣었는지 확인합니다.
- `ModuleNotFoundError`: `pip install -r requirements.txt`를 먼저 실행합니다.
- 한글 글꼴 표시 오류: 분석 결과에는 영향이 없으며 실행 환경에 따라 차트 글꼴이 다르게 보일 수 있습니다.

## 8. 해석 시 주의사항

- `DAY`, `WEEK_NO`는 실제 달력 날짜가 아니라 데이터셋 내부 상대 기간 변수입니다.
- 매출값은 실제 원화 매출이 아니라 원본 데이터의 `SALES_VALUE` 기준입니다.
- 쿠폰·캠페인 분석은 무작위 실험이 아니므로 인과효과로 해석하지 않습니다.
- 결과는 본 공개 데이터 기준의 관찰 결과이며 실제 기업 내부 성과로 해석하지 않습니다.
