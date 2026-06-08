# 데이터 정의서

> 이 문서는 분석에 사용한 데이터 구조, 주요 컬럼과 해석 유의사항을 정리합니다.

## 1. 사용 데이터

본 프로젝트에서는 Olist Brazilian E-Commerce Public Dataset을 사용했습니다. 이 데이터는 주문, 결제, 주문 상품, 판매자, 고객, 리뷰, 상품 정보를 포함하고 있어 운영 데이터의 정합성 문제를 분석하기에 적합합니다.

## 2. 분석 단위

| 구분 | 내용 |
|---|---|
| 기본 분석 단위 | order_id |
| 보조 분석 단위 | seller_id |
| 추가 분석 기준 | order_status, error_type, month |

## 3. orders 테이블

| 컬럼명 | 의미 | 분석 활용 |
|---|---|---|
| order_id | 주문 ID | 주문 단위 기본 key |
| customer_id | 고객 ID | 고객 테이블과 연결 |
| order_status | 주문 상태 | 상태값 정합성 점검 |
| order_purchase_timestamp | 주문 발생 시각 | 주문 흐름의 시작점 |
| order_approved_at | 결제 승인 시각 | 승인일 누락 및 날짜 순서 점검 |
| order_delivered_carrier_date | 배송사 전달 시각 | 배송 흐름 점검 |
| order_delivered_customer_date | 고객 수령 시각 | 배송 완료 여부 점검 |
| order_estimated_delivery_date | 예상 배송일 | 배송 지연 여부 점검 |

## 4. payments 테이블

| 컬럼명 | 의미 | 분석 활용 |
|---|---|---|
| order_id | 주문 ID | 주문 테이블과 연결 |
| payment_sequential | 결제 순번 | 복수 결제 여부 확인 |
| payment_type | 결제 수단 | 결제 유형 확인 |
| payment_installments | 할부 개월 수 | 결제 조건 확인 |
| payment_value | 결제 금액 | 금액 정합성 점검 |

## 5. order_items 테이블

| 컬럼명 | 의미 | 분석 활용 |
|---|---|---|
| order_id | 주문 ID | 주문 테이블과 연결 |
| order_item_id | 주문 내 상품 순번 | 한 주문 내 상품 수 확인 |
| product_id | 상품 ID | 상품 테이블과 연결 |
| seller_id | 판매자 ID | 판매자별 오류율 분석 |
| shipping_limit_date | 배송 처리 제한일 | 배송 처리 기준 확인 |
| price | 상품 가격 | 금액 정합성 점검 |
| freight_value | 배송비 | 결제 금액과 비교 |

## 6. sellers 테이블

| 컬럼명 | 의미 | 분석 활용 |
|---|---|---|
| seller_id | 판매자 ID | 판매자 단위 분석 key |
| seller_zip_code_prefix | 판매자 우편번호 | 지역 정보 보조 분석 |
| seller_city | 판매자 도시 | 지역 정보 보조 분석 |
| seller_state | 판매자 주 | 지역 정보 보조 분석 |

## 7. reviews 테이블

| 컬럼명 | 의미 | 분석 활용 |
|---|---|---|
| review_id | 리뷰 ID | 리뷰 단위 key |
| order_id | 주문 ID | 주문 데이터와 연결 |
| review_score | 리뷰 점수 | 배송 지연 및 운영 문제와의 관계 보조 확인 |
| review_creation_date | 리뷰 작성일 | 리뷰 발생 시점 확인 |
| review_answer_timestamp | 리뷰 응답 시각 | 응답 흐름 보조 확인 |

## 8. 데이터 사용 시 주의점

payments와 order_items 테이블은 하나의 주문에 여러 결제 또는 여러 상품이 포함될 수 있어 `order_id`가 여러 번 나타날 수 있습니다. 따라서 중복 여부를 판단하기 전에 테이블의 분석 단위와 컬럼 의미를 먼저 확인했습니다.
