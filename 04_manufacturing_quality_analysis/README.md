# 반도체 공정 품질 신호 분석 프로젝트

> UCI SECOM 공개 반도체 제조 데이터로 공정 측정값의 결측률·Pass/Fail 그룹 차이·변동성을 분석하고 추가 점검이 필요한 품질 신호 후보를 우선순위화한 프로젝트입니다.
> **공개 데이터 기반 관찰 분석이며 불량 원인 확정이나 실제 공정 개선 성과를 주장하지 않습니다.**

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 분석 목적 | 공정 신호의 결측·그룹 차이·변동성을 종합해 점검 우선순위 후보 도출 |
| 사용 데이터 | UCI SECOM Dataset (Kaggle) |
| 사용 도구 | SQL(SQLite), Python (pandas, numpy, matplotlib) |
| 주요 산출물 | SQL 쿼리 8개, Python 분석 스크립트, 결과 CSV, 차트, PPT/PDF 보고서 |
| 분석 성격 | 익명화 공개 데이터 기반 관찰 분석 (원인 확정 아님) |

## 2. 데이터 출처

- 데이터셋: UCI SECOM Dataset (Kaggle 경유)
- 사용 파일: `uci-secom.csv` (행 1,567 / 열 592)
- 라벨: `Pass/Fail` (`-1=Pass`, `1=Fail`)
- 변수: 익명화된 공정 측정값 `0~589` → `feature_000~feature_589`로 변환
- 원본 파일은 약 6MB이며 바로 실행할 수 있도록 `data/raw/uci-secom.csv`로 포함했습니다.

### 데이터 출처 및 라이선스

- 출처: UCI Machine Learning Repository — SECOM Dataset (DOI: 10.24432/C54305). Kaggle 미러(`paresh2047/uci-semcom`)를 경유해 취득했습니다.
- 인용: *SECOM [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C54305*
- 라이선스: Creative Commons Attribution 4.0 International (CC BY 4.0). 적절한 출처 표기를 조건으로 공유·변형·재배포가 허용되며 본 저장소는 위 출처 표기와 함께 해당 라이선스에 따라 `uci-secom.csv`를 포함합니다.

## 3. 분석 질문

1. Pass/Fail 라벨 분포는 어떻게 나타나는가?
2. 어떤 공정 신호의 결측률이 높은가?
3. Pass 그룹과 Fail 그룹의 분포 차이가 큰 신호는 무엇인가?
4. 변동성·극단값 가능성이 큰 신호는 무엇인가?
5. 종합 기준으로 어떤 신호를 먼저 점검해야 하는가?

## 4. 주요 결과 요약

- 데이터는 1,567행 / 공정 신호 590개로 구성되며 Fail 비율은 6.6%(104건)로 라벨 불균형이 큽니다.
- 점검 우선순위 상위 후보(결측 40% 미만)는 `feature_294`, `feature_159`, `feature_510`입니다.
- 우선순위 점수는 그룹 차이 0.45, 변동성 0.25, 결측 위험 0.20, 극단값 0.10을 가중해 산정했습니다.
- 결측률 40% 이상 신호(`feature_158` 등)는 우선 점검 후보가 아니라 별도 데이터 품질 관리 후보로 분리했습니다.
- 보조 베이스라인 모델(numpy 로지스틱 회귀, 클래스 가중치 적용)은 불균형 데이터 특성상 정확도만으로 해석하기 어렵습니다. ROC-AUC 약 0.67은 참고용 보조 지표로만 사용합니다.

## 5. 실행 방법

```bash
pip install -r requirements.txt
python scripts/run_analysis.py
```

Windows에서 `python` 명령어가 실행되지 않으면 아래처럼 실행합니다.

```bash
py scripts/run_analysis.py
```

실행 후 `outputs/csv/`(결과 CSV), `outputs/figures/`(차트), `database/secom_analysis.sqlite`(실행 시 생성 DB)가 생성됩니다. DB 파일은 로컬 실행 결과물이며 GitHub 업로드 대상에는 포함하지 않습니다.

## 6. 폴더 구조

```text
04_manufacturing_quality_analysis/
├── README.md
├── BEGINNER_GUIDE.md
├── requirements.txt
├── data/
│   └── raw/          # uci-secom.csv 포함
├── docs/             # 분석 기획·데이터·지표·전처리 정의
├── sql/              # 공정 품질 분석 SQL 8개
├── scripts/          # run_analysis.py
├── outputs/
│   ├── csv/          # 분석 결과 CSV
│   └── figures/      # 차트 이미지
└── reports/          # PPT/PDF 보고서
```

## 7. 해석 시 주의사항

- 변수명이 익명화되어 실제 센서·공정 의미를 알 수 없으므로 본 분석은 불량 원인 판단이 아니라 추가 점검이 필요한 품질 신호 후보 도출로 해석합니다.
- 분포 차이·변동성이 큰 신호는 원인이 아니라 점검 후보이며 실제 현장 해석에는 공정 지식과 추가 검증이 필요합니다.
- 모델은 참고용 보조 지표이며 현장 적용 성능·불량률 감소·원인 판단으로 해석하지 않습니다.

## 8. 산출물

- 최종 PDF 보고서: `reports/04_manufacturing_quality_analysis_report.pdf`
- 최종 PPT 보고서: `reports/04_manufacturing_quality_analysis_report.pptx`
