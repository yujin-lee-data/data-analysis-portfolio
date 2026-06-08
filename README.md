# 데이터 분석 포트폴리오

> 공개 데이터 기반 데이터 분석 포트폴리오입니다.  
SQL, Python, 시각화, 보고서를 활용한 4개 도메인 분석 프로젝트를 포함합니다.

> **모든 프로젝트는 공개 데이터 기반 관찰 분석입니다.**  
> 실제 기업 내부 데이터가 아니며 실제 개선 성과나 인과관계를 주장하지 않습니다.

---

## 1. 프로젝트 구성

| # | 프로젝트 | 도메인 | 주요 기술 | 데이터 |
|---|---|---|---|---|
| 01 | [서비스 운영 데이터 품질 관리](./01_operation_data_quality/) | 운영·정합성 | SQL, Python, scipy | Olist E-Commerce (Kaggle) |
| 02 | [GA4 기반 서비스 퍼널 분석](./02_service_funnel_analysis/) | 서비스·전환 | BigQuery SQL, Python | GA4 Sample (BigQuery Public) |
| 03 | [커머스 고객·매출·프로모션 분석](./03_business_commerce_analysis/) | 비즈니스·커머스 | SQL, Python, pandas | Dunnhumby Complete Journey (Kaggle) |
| 04 | [반도체 공정 품질 신호 분석](./04_manufacturing_quality_analysis/) | 제조·품질 | SQL, Python, numpy | UCI SECOM (Kaggle) |

---

## 2. 프로젝트별 역할

### 01. 서비스 운영 데이터 품질 관리
주문·결제·배송·판매자 테이블 간 정합성 기준을 정의하고 SQL로 검수 후보를 탐지한 뒤 Python으로 검수 우선순위를 산정했습니다.  
**핵심 포인트:** 결과를 오류 확정이 아닌 검수 후보로 표현하고 발생 건수·영향도·긴급도 기반 우선순위를 설계했습니다.

### 02. GA4 기반 서비스 퍼널 분석
Google BigQuery GA4 공개 샘플 데이터를 활용해 5단계 이커머스 퍼널을 정의하고 단계별 전환율·이탈률·우선 점검 구간을 분석했습니다.  
**핵심 포인트:** 순차 퍼널 기준을 정의하고 디바이스·카테고리 세그먼트는 보조 분석으로 활용했습니다. 결과는 실제 개선 성과가 아닌 관찰 데이터 기반 시사점입니다.

### 03. 커머스 고객·매출·프로모션 분석
Dunnhumby Complete Journey 공개 데이터로 고객군 매출 기여도, 재구매 행동, 상품군 매출 구조, 쿠폰·캠페인 반응 차이를 분석했습니다.  
**핵심 포인트:** 상위 고객군의 매출 기여 구조를 확인하고 쿠폰·캠페인 결과는 인과효과가 아닌 관찰 데이터 기준 반응 차이로 해석했습니다.

### 04. 반도체 공정 품질 신호 분석
UCI SECOM 공개 반도체 제조 데이터로 590개 공정 측정값의 결측률·Pass/Fail 그룹 차이·변동성을 분석하고 점검 우선순위를 도출했습니다.  
**핵심 포인트:** 변수 익명화 한계를 명시하고 불량 원인 규명이 아닌 품질 신호 점검 후보 도출로 정리했습니다. ML 결과는 참고용 보조 지표로만 활용했습니다.

---

## 3. 저장소 구조

```text
data-analysis-portfolio/
├─ 01_operation_data_quality/
│  ├─ sql/                  # 정합성 탐지 SQL 쿼리 8개
│  ├─ scripts/              # Python 분석 실행 파일
│  ├─ data/raw/             # 원본 데이터 배치 안내 문서
│  ├─ data/processed/       # 분석 결과 CSV
│  ├─ figures/              # 차트 이미지
│  ├─ docs/                 # 분석 기획·데이터·지표·전처리 정의
│  ├─ reports/              # PPT/PDF 보고서 및 결과 요약
│  ├─ README.md
│  ├─ BEGINNER_GUIDE.md
│  └─ requirements.txt
├─ 02_service_funnel_analysis/
│  ├─ sql/                  # BigQuery 재현용 SQL
│  ├─ python/               # Python 차트 재생성 코드
│  ├─ scripts/              # 실행 래퍼
│  ├─ data/actual_bigquery/ # BigQuery 결과 CSV 원본
│  ├─ data/output_csv/      # 차트 재생성용 결과 CSV
│  ├─ charts/               # 차트 이미지
│  ├─ docs/                 # 분석 기획·데이터·지표·전처리 정의
│  ├─ reports/               # PPT/PDF 보고서
│  ├─ README.md
│  ├─ BEGINNER_GUIDE.md
│  └─ requirements.txt
├─ 03_business_commerce_analysis/
│  ├─ sql/                  # 커머스 분석 SQL 8개
│  ├─ scripts/              # Python 분석 실행 파일
│  ├─ data/raw/             # 원본 데이터 배치 안내 문서
│  ├─ outputs/csv/          # 분석 결과 CSV
│  ├─ outputs/charts/       # 차트 이미지
│  ├─ docs/                 # 분석 기획·데이터·지표·전처리 정의
│  ├─ reports/              # PPT/PDF 보고서
│  ├─ README.md
│  ├─ BEGINNER_GUIDE.md
│  └─ requirements.txt
├─ 04_manufacturing_quality_analysis/
│  ├─ sql/                  # 공정 품질 분석 SQL 8개
│  ├─ scripts/              # Python 분석 실행 파일
│  ├─ data/raw/             # uci-secom.csv 포함
│  ├─ outputs/csv/          # 분석 결과 CSV
│  ├─ outputs/figures/      # 차트 이미지
│  ├─ docs/                 # 분석 기획·데이터·지표·전처리 정의
│  ├─ reports/              # PPT/PDF 보고서
│  ├─ README.md
│  ├─ BEGINNER_GUIDE.md
│  └─ requirements.txt
├─ .gitignore
└─ README.md
```

---

## 4. 실행 방법

각 프로젝트 폴더의 `BEGINNER_GUIDE.md`를 먼저 확인합니다. 공통 실행 흐름은 아래와 같습니다.

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 분석 실행
python scripts/run_analysis.py
```

**원본 데이터 필요 여부**

- P1: Kaggle에서 Olist 데이터를 다운로드한 뒤 `data/raw/`에 배치해야 합니다.
- P2: 제공된 BigQuery 결과 CSV 기반으로 차트를 재생성할 수 있습니다. 별도 다운로드는 필요하지 않습니다.
- P3: Kaggle에서 Dunnhumby 데이터를 다운로드한 뒤 `data/raw/`에 배치해야 합니다.
- P4: `data/raw/uci-secom.csv`가 포함되어 있어 바로 실행할 수 있습니다.

---

## 5. 분석 원칙

- 모든 분석은 **공개 데이터 기반 관찰 분석**입니다.
- 실제 기업 내부 데이터처럼 표현하지 않습니다.
- 인과효과를 단정하지 않습니다.
- 분석 결과는 검수 후보, 우선 점검 후보, 반응 차이, 추가 검증 필요 수준으로 표현합니다.
- 모든 코드와 결과는 재현 가능하게 정리했습니다.

---

## 6. 데이터 출처 및 라이선스

- **P1 Olist Brazilian E-Commerce (Kaggle):** 원본 CSV는 저장소에 포함하지 않으며 Kaggle에서 직접 내려받아 사용합니다(원 출처의 이용 약관 적용).
- **P2 GA4 Ecommerce Sample (Google BigQuery Public Dataset):** 원본 로그는 BigQuery에서 조회하며 저장소에는 분석 결과 CSV만 포함합니다.
- **P3 Dunnhumby - The Complete Journey (Kaggle):** 원본 CSV는 저장소에 포함하지 않으며 Kaggle에서 직접 내려받아 사용합니다(원 출처의 이용 약관 적용).
- **P4 UCI SECOM (UCI Machine Learning Repository, DOI: 10.24432/C54305):** Creative Commons Attribution 4.0 International (CC BY 4.0). 출처 표기를 조건으로 재배포가 허용되어 `04_manufacturing_quality_analysis/data/raw/uci-secom.csv`로 포함했습니다.
