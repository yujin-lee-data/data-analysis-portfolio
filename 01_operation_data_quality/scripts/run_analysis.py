from pathlib import Path
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
# 통일 차트 스타일 (프로젝트 01 강조색)
ACCENT = "#F2B41E"
ACCENT_DK = "#9A6A00"
ACCENT_LT = "#F8D070"
GREY = "#9AA6B2"
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#D9DDE3", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": "#EEF0F3", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 11, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.titlecolor": "#1B2330", "text.color": "#2B2F36",
    "axes.labelcolor": "#5B6472", "xtick.color": "#5B6472", "ytick.color": "#5B6472",
    "axes.prop_cycle": cycler(color=[ACCENT, GREY, ACCENT_LT, ACCENT_DK]),
})

try:
    from scipy import stats
except ImportError:
    stats = None

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / 'data' / 'raw'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
FIG_DIR = BASE_DIR / 'figures'
REPORT_DIR = BASE_DIR / 'reports'

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = {
    'orders': 'olist_orders_dataset.csv',
    'payments': 'olist_order_payments_dataset.csv',
    'items': 'olist_order_items_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'reviews': 'olist_order_reviews_dataset.csv',
}


def load_data():
    missing = [name for name in REQUIRED_FILES.values() if not (RAW_DIR / name).exists()]
    if missing:
        print('아래 파일이 data/raw 폴더에 없습니다.')
        for f in missing:
            print(f'  - {f}')
        print('\nKaggle에서 Olist Brazilian E-Commerce Public Dataset을 다운로드한 뒤 data/raw 폴더에 넣어주세요.')
        sys.exit(1)

    data = {}
    for key, filename in REQUIRED_FILES.items():
        data[key] = pd.read_csv(RAW_DIR / filename)
    return data


def prepare_orders(orders):
    date_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
    ]
    orders = orders.copy()
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col], errors='coerce')
    return orders


def build_error_flags(orders, payments, items):
    orders = orders.copy()

    # E01. 주문은 있는데 결제 정보가 없는 경우
    payment_order_ids = set(payments['order_id'].unique())
    orders['payment_missing'] = ~orders['order_id'].isin(payment_order_ids)

    # E02. delivered 상태인데 고객 수령일이 없는 경우
    orders['delivered_without_date'] = (
        (orders['order_status'] == 'delivered') &
        (orders['order_delivered_customer_date'].isna())
    )

    # E03. delivered가 아닌데 고객 수령일이 존재하는 경우
    orders['non_delivered_with_date'] = (
        (orders['order_status'] != 'delivered') &
        (orders['order_delivered_customer_date'].notna())
    )

    # E04. 날짜 순서가 논리적으로 맞지 않는 경우
    orders['approved_before_purchase'] = (
        orders['order_approved_at'].notna() &
        (orders['order_approved_at'] < orders['order_purchase_timestamp'])
    )
    orders['carrier_before_approved'] = (
        orders['order_delivered_carrier_date'].notna() &
        orders['order_approved_at'].notna() &
        (orders['order_delivered_carrier_date'] < orders['order_approved_at'])
    )
    orders['customer_before_carrier'] = (
        orders['order_delivered_customer_date'].notna() &
        orders['order_delivered_carrier_date'].notna() &
        (orders['order_delivered_customer_date'] < orders['order_delivered_carrier_date'])
    )
    orders['delivered_before_purchase'] = (
        orders['order_delivered_customer_date'].notna() &
        (orders['order_delivered_customer_date'] < orders['order_purchase_timestamp'])
    )
    orders['date_reversal'] = (
        orders['approved_before_purchase'] |
        orders['carrier_before_approved'] |
        orders['customer_before_carrier'] |
        orders['delivered_before_purchase']
    )

    # E06. 배송 지연
    orders['late_delivery'] = (
        orders['order_delivered_customer_date'].notna() &
        orders['order_estimated_delivery_date'].notna() &
        (orders['order_delivered_customer_date'] > orders['order_estimated_delivery_date'])
    )

    # E05. 결제금액과 상품가격+배송비 합계 차이 후보
    item_amount = items.groupby('order_id').agg(
        item_total_amount=('price', 'sum'),
        freight_total_amount=('freight_value', 'sum')
    ).reset_index()
    item_amount['expected_total_amount'] = item_amount['item_total_amount'] + item_amount['freight_total_amount']

    payment_amount = payments.groupby('order_id').agg(
        payment_total_amount=('payment_value', 'sum')
    ).reset_index()

    amount_check = item_amount.merge(payment_amount, on='order_id', how='inner')
    amount_check['amount_diff'] = amount_check['payment_total_amount'] - amount_check['expected_total_amount']
    amount_check['amount_mismatch'] = amount_check['amount_diff'].abs() >= 1

    orders = orders.merge(
        amount_check[['order_id', 'expected_total_amount', 'payment_total_amount', 'amount_diff', 'amount_mismatch']],
        on='order_id',
        how='left'
    )
    orders['amount_mismatch'] = orders['amount_mismatch'].fillna(False)

    error_cols = [
        'payment_missing',
        'delivered_without_date',
        'non_delivered_with_date',
        'date_reversal',
        'amount_mismatch',
        'late_delivery',
    ]
    orders['has_error_candidate'] = orders[error_cols].any(axis=1)
    return orders, amount_check


def summarize_errors(order_flags):
    error_cols = [
        'payment_missing',
        'delivered_without_date',
        'non_delivered_with_date',
        'date_reversal',
        'amount_mismatch',
        'late_delivery',
    ]
    rows = []
    total_orders = len(order_flags)
    for col in error_cols:
        count = int(order_flags[col].sum())
        rows.append({
            'error_type': col,
            'error_count': count,
            'error_rate': round(count / total_orders * 100, 2) if total_orders else 0
        })
    return pd.DataFrame(rows).sort_values('error_count', ascending=False)


def seller_error_rate(order_flags, items):
    seller_orders = items[['order_id', 'seller_id']].drop_duplicates()
    seller_error = seller_orders.merge(
        order_flags[['order_id', 'has_error_candidate']],
        on='order_id',
        how='left'
    )
    seller_error['has_error_candidate'] = seller_error['has_error_candidate'].fillna(False)
    summary = seller_error.groupby('seller_id').agg(
        total_orders=('order_id', 'nunique'),
        error_orders=('has_error_candidate', 'sum')
    ).reset_index()
    summary['error_rate'] = (summary['error_orders'] / summary['total_orders'] * 100).round(2)
    summary = summary[summary['total_orders'] >= 30].sort_values('error_rate', ascending=False)
    return summary


def priority_score(error_summary):
    priority = error_summary.copy()
    impact_map = {
        'payment_missing': 5,
        'delivered_without_date': 4,
        'non_delivered_with_date': 4,
        'date_reversal': 4,
        'amount_mismatch': 5,
        'late_delivery': 3,
    }
    urgency_map = {
        'payment_missing': 5,
        'delivered_without_date': 4,
        'non_delivered_with_date': 4,
        'date_reversal': 4,
        'amount_mismatch': 5,
        'late_delivery': 3,
    }
    priority['impact_score'] = priority['error_type'].map(impact_map)
    priority['urgency_score'] = priority['error_type'].map(urgency_map)
    # 오류 건수 순위를 1~5 점수로 변환. 같은 값이 있어도 안정적으로 처리.
    priority['frequency_score'] = pd.qcut(
        priority['error_count'].rank(method='first'),
        q=5,
        labels=[1, 2, 3, 4, 5],
        duplicates='drop'
    ).astype(int)
    priority['priority_score'] = (
        priority['frequency_score'] * 0.4 +
        priority['impact_score'] * 0.4 +
        priority['urgency_score'] * 0.2
    ).round(2)
    return priority.sort_values('priority_score', ascending=False)


def amount_mismatch_top10(amount_check):
    result = amount_check[amount_check['amount_mismatch']].copy()
    result['abs_amount_diff'] = result['amount_diff'].abs()
    result = result.sort_values('abs_amount_diff', ascending=False).head(10).reset_index(drop=True)

    # 보고서에서는 실제 order_id 대신 case_id를 사용해 가독성을 높입니다.
    # 상세 재현이 필요한 경우 원본 amount_check.csv에서 동일한 금액 차이를 기준으로 확인할 수 있습니다.
    result['case_id'] = [f'case_{i+1}' for i in range(len(result))]
    result['note'] = '검수 후보'
    return result[['case_id', 'expected_total_amount', 'payment_total_amount', 'amount_diff', 'abs_amount_diff', 'note']]


def late_delivery_review_detail(orders, reviews):
    merged = orders[['order_id', 'late_delivery']].merge(
        reviews[['order_id', 'review_score']],
        on='order_id',
        how='inner'
    )
    summary = merged.groupby('late_delivery').agg(
        orders=('order_id', 'nunique'),
        avg_review_score=('review_score', 'mean')
    ).reset_index()
    summary['avg_review_score'] = summary['avg_review_score'].round(2)

    ttest_rows = []
    false_scores = merged.loc[merged['late_delivery'] == False, 'review_score'].dropna()
    true_scores = merged.loc[merged['late_delivery'] == True, 'review_score'].dropna()
    if stats is not None and len(false_scores) > 1 and len(true_scores) > 1:
        t_stat, p_value = stats.ttest_ind(false_scores, true_scores, equal_var=False)
        p_display = '<0.001' if p_value < 0.001 else round(float(p_value), 6)
        t_display = round(float(t_stat), 6)
    else:
        t_display = np.nan
        p_display = np.nan

    ttest_rows.append({
        'test_name': 'Welch t-test',
        'group_1': 'late_delivery_false',
        'group_1_n': int(len(false_scores)),
        'group_1_mean': round(float(false_scores.mean()), 4) if len(false_scores) else np.nan,
        'group_2': 'late_delivery_true',
        'group_2_n': int(len(true_scores)),
        'group_2_mean': round(float(true_scores.mean()), 4) if len(true_scores) else np.nan,
        'mean_difference_group1_minus_group2': round(float(false_scores.mean() - true_scores.mean()), 4) if len(false_scores) and len(true_scores) else np.nan,
        't_statistic': t_display,
        'p_value': p_display,
        'interpretation_note': '통계적으로 평균 차이는 확인되나, 인과관계를 의미하지 않음'
    })
    ttest = pd.DataFrame(ttest_rows)
    return merged, summary, ttest


def plot_error_summary(error_summary):
    d = error_summary.sort_values('error_count')
    plt.figure(figsize=(9, 5))
    plt.barh(d['error_type'], d['error_count'])
    for i, v in enumerate(d['error_count']):
        plt.text(v, i, f'  {int(v):,}', va='center', fontsize=10)
    plt.title('Error Candidate Count by Type')
    plt.xlabel('Count')
    plt.margins(x=0.12)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'error_type_distribution.png', dpi=200)
    plt.close()


def plot_seller_top10(seller_summary):
    top10 = seller_summary.head(10).copy()
    if top10.empty:
        return
    top10['seller_label'] = [f'seller_{chr(65+i)}' for i in range(len(top10))]
    d = top10.sort_values('error_rate')
    plt.figure(figsize=(9, 5))
    plt.barh(d['seller_label'], d['error_rate'])
    plt.title('Top 10 Sellers by Error Candidate Rate')
    plt.xlabel('Error Candidate Rate (%)')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'seller_error_rate_top10.png', dpi=200)
    plt.close()


def plot_priority(priority):
    d = priority.sort_values('priority_score')
    plt.figure(figsize=(9, 5))
    bars = plt.barh(d['error_type'], d['priority_score'])
    try:
        bars[-1].set_color(ACCENT_DK)
    except Exception:
        pass
    for i, v in enumerate(d['priority_score']):
        plt.text(v, i, f'  {v:.1f}', va='center', fontsize=10)
    plt.title('Inspection Priority Score by Error Type')
    plt.xlabel('Priority Score')
    plt.margins(x=0.12)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'priority_score.png', dpi=200)
    plt.close()


def plot_late_review(summary):
    if summary.empty:
        return
    labels = summary['late_delivery'].map({False: 'Not Late', True: 'Late'}).astype(str)
    plt.figure(figsize=(6, 5))
    plt.bar(labels, summary['avg_review_score'])
    plt.title('Average Review Score by Late Delivery')
    plt.xlabel('Late Delivery')
    plt.ylabel('Average Review Score')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'late_delivery_review_score.png', dpi=200)
    plt.close()


def plot_review_distribution(merged):
    if merged.empty:
        return
    not_late = merged.loc[merged['late_delivery'] == False, 'review_score'].dropna()
    late = merged.loc[merged['late_delivery'] == True, 'review_score'].dropna()
    plt.figure(figsize=(8, 5))
    bins = np.arange(0.5, 6.5, 1)
    plt.hist(not_late, bins=bins, density=True, alpha=0.55, label='Not Late')
    plt.hist(late, bins=bins, density=True, alpha=0.55, label='Late')
    plt.title('Review Score Distribution by Late Delivery')
    plt.xlabel('Review Score')
    plt.ylabel('Density')
    plt.xticks([1, 2, 3, 4, 5])
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'review_score_distribution_by_late_delivery.png', dpi=200)
    plt.close()


def plot_amount_top10(top10):
    if top10.empty:
        return
    plot_df = top10.copy().reset_index(drop=True)
    plot_df['case_id'] = [f'case_{i+1}' for i in range(len(plot_df))]
    plt.figure(figsize=(8, 5))
    plt.barh(plot_df['case_id'], plot_df['abs_amount_diff'])
    plt.gca().invert_yaxis()
    plt.title('Top 10 Amount Mismatch Candidates')
    plt.xlabel('Absolute Amount Difference')
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'amount_mismatch_top10.png', dpi=200)
    plt.close()


def write_summary_txt(error_summary, seller_summary, priority, late_review, ttest, amount_top10):
    lines = []
    lines.append('# 분석 결과 요약\n')
    lines.append('이 파일은 scripts/run_analysis.py 실행 후 자동 생성된 요약입니다.\n')
    lines.append('## 오류 후보 유형별 현황\n')
    lines.append(error_summary.to_markdown(index=False))
    lines.append('\n\n## 검수 우선순위\n')
    lines.append(priority.to_markdown(index=False))
    lines.append('\n\n## 금액 불일치 상위 10건\n')
    lines.append(amount_top10.to_markdown(index=False) if not amount_top10.empty else '금액 불일치 후보가 없습니다.')
    lines.append('\n\n## 판매자별 오류율 상위 10개\n')
    lines.append(seller_summary.head(10).to_markdown(index=False) if not seller_summary.empty else '주문 수 30건 이상 조건을 만족하는 판매자가 없습니다.')
    lines.append('\n\n## 배송 지연 여부와 리뷰 점수\n')
    lines.append(late_review.to_markdown(index=False) if not late_review.empty else '분석 가능한 리뷰 데이터가 없습니다.')
    lines.append('\n\n## 배송 지연과 리뷰 점수 Welch t-test\n')
    lines.append(ttest.to_markdown(index=False) if not ttest.empty else 't-test 결과가 없습니다.')
    lines.append('\n\n> ※ 표본 수 안내: 위 "배송 지연 여부와 리뷰 점수" 표의 건수(orders)는 주문 단위 고유 개수(고유 order_id 기준)이고, Welch t-test의 group_n은 리뷰 행 단위 개수입니다. Olist 리뷰 데이터에는 한 주문에 리뷰가 둘 이상 존재하는 사례가 일부 있어 두 값이 다를 수 있으며, 평균과 검정 결론에는 영향을 주지 않습니다.\n')
    lines.append('\n\n## 해석 주의사항\n')
    lines.append('본 분석의 결과는 실제 오류 확정이 아니라 검수 후보 탐지 결과입니다. 공개 데이터에는 쿠폰, 환불, 포인트, 내부 상태 변경 이력 등이 포함되어 있지 않으므로 추가 확인이 필요합니다. 또한 배송 지연과 리뷰 점수 차이는 인과관계가 아니라 보조 신호로 해석했습니다.\n')
    (REPORT_DIR / 'analysis_result_summary.md').write_text('\n'.join(lines), encoding='utf-8')


def main():
    data = load_data()
    orders = prepare_orders(data['orders'])
    payments = data['payments']
    items = data['items']
    reviews = data['reviews']

    order_flags, amount_check = build_error_flags(orders, payments, items)
    error_summary = summarize_errors(order_flags)
    seller_summary = seller_error_rate(order_flags, items)
    priority = priority_score(error_summary)
    amount_top10 = amount_mismatch_top10(amount_check)
    review_merged, late_review, ttest = late_delivery_review_detail(order_flags, reviews)

    order_flags.to_csv(PROCESSED_DIR / 'order_error_flags.csv', index=False, encoding='utf-8-sig')
    amount_check.to_csv(PROCESSED_DIR / 'amount_check.csv', index=False, encoding='utf-8-sig')
    amount_top10.to_csv(PROCESSED_DIR / 'amount_mismatch_top10.csv', index=False, encoding='utf-8-sig')
    error_summary.to_csv(PROCESSED_DIR / 'error_summary.csv', index=False, encoding='utf-8-sig')
    seller_summary.to_csv(PROCESSED_DIR / 'seller_error_rate.csv', index=False, encoding='utf-8-sig')
    priority.to_csv(PROCESSED_DIR / 'priority_score.csv', index=False, encoding='utf-8-sig')
    late_review.to_csv(PROCESSED_DIR / 'late_delivery_review_score.csv', index=False, encoding='utf-8-sig')
    ttest.to_csv(PROCESSED_DIR / 'late_delivery_review_ttest.csv', index=False, encoding='utf-8-sig')

    plot_error_summary(error_summary)
    plot_seller_top10(seller_summary)
    plot_priority(priority)
    plot_amount_top10(amount_top10)
    plot_late_review(late_review)
    plot_review_distribution(review_merged)
    write_summary_txt(error_summary, seller_summary, priority, late_review, ttest, amount_top10)

    print('분석이 완료되었습니다.')
    print(f'- 결과 CSV: {PROCESSED_DIR}')
    print(f'- 차트 이미지: {FIG_DIR}')
    print(f'- 결과 요약: {REPORT_DIR / "analysis_result_summary.md"}')


if __name__ == '__main__':
    main()
