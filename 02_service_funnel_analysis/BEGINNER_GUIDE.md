# 초보자 실행 가이드

> 이 문서는 GA4 기반 서비스 퍼널 분석 프로젝트를 처음 여는 사람도 실행 흐름을 이해할 수 있도록 정리한 안내서입니다.

## 1. 이 프로젝트가 하는 일
사용자가 쇼핑몰에서 들어오고, 상품을 보고, 장바구니에 담고, 결제를 시작하고, 구매하는 흐름을 단계별로 봅니다. 어느 단계에서 사용자가 많이 빠져나가는지 확인하는 프로젝트입니다.

## 2. 필요한 준비물
- Python 3.10 이상
- 인터넷에서 패키지를 설치할 수 있는 환경
- Google BigQuery에서 GA4 공개 데이터셋을 조회할 수 있는 계정

## 3. 데이터 준비 방법
1. BigQuery에서 GA4 Ecommerce 공개 데이터셋을 엽니다.
2. `sql` 폴더의 SQL을 순서대로 실행합니다.
3. 결과를 CSV로 저장합니다.
4. 저장한 CSV를 `data/actual_bigquery` 또는 `data/output_csv` 폴더에 넣습니다.

이미 이 압축 파일 안에는 분석에 사용한 결과 CSV가 들어 있으므로 바로 Python 실행도 가능합니다.

## 4. 패키지 설치
터미널에서 프로젝트 폴더로 이동한 뒤 아래 명령어를 입력합니다.

```bash
pip install -r requirements.txt
```

## 5. Python 실행
아래 명령어를 입력합니다.

```bash
python python/run_analysis_actual.py
```

실행이 끝나면 `charts` 폴더에 차트 이미지가 생성됩니다.

## 6. 결과 확인
- 표 결과: `data/output_csv`
- 차트 이미지: `charts`
- 최종 PDF 보고서: `reports/02_service_funnel_analysis_report.pdf`
- 최종 PPT 보고서: `reports/02_service_funnel_analysis_report.pptx`

## 7. 자주 발생하는 오류
- 파일 경로 오류: BigQuery 결과 CSV가 `data/actual_bigquery` 또는 `data/output_csv` 폴더에 있는지 확인합니다.
- 패키지 설치 오류: `pip install -r requirements.txt`를 다시 실행합니다.
- 한글 글꼴 표시 오류: 분석 결과에는 영향이 없으며 실행 환경에 따라 차트 글꼴이 다르게 보일 수 있습니다.

## 8. 해석 시 주의사항
이 프로젝트는 GA4 공개 샘플 데이터를 활용한 관찰 분석입니다. 따라서 실제 회사 내부 데이터 분석 결과나 실제 개선 성과를 의미하지 않습니다. 분석 결과는 본 데이터 기준으로 전환 흐름을 비교하고 추가 점검이 필요한 구간을 정리한 결과로 해석했습니다.
