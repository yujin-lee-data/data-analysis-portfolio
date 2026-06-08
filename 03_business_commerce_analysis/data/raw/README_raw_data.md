# 데이터 폴더 안내

> 이 문서는 원본 데이터 배치 방법과 GitHub 업로드 제외 기준을 설명합니다.

이 폴더에는 Kaggle에서 직접 다운로드한 Dunnhumby The Complete Journey 원본 CSV 파일을 넣습니다.

## 1. 필수 파일

- `transaction_data.csv`
- `product.csv`
- `campaign_table.csv`
- `campaign_desc.csv`
- `coupon_redempt.csv`
- `hh_demographic.csv`

## 2. 재현 및 업로드 유의사항

원본 CSV는 용량과 출처 관리를 고려해 GitHub에 포함하지 않았습니다. 재현하려면 Kaggle에서 원본 데이터를 다운로드한 뒤 이 폴더에 배치합니다. 해당 파일은 `.gitignore` 설정에 따라 업로드 대상에서 제외됩니다.

> 원본 데이터가 없으면 전체 재실행은 불가합니다. 이는 코드 오류가 아니라 공개 데이터 원본 다운로드가 필요한 구조입니다.
