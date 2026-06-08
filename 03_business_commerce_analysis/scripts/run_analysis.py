from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
# 통일 차트 스타일 (프로젝트 03 강조색)
ACCENT = "#2F855A"
ACCENT_DK = "#205B3E"
ACCENT_LT = "#93C4AC"
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

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / 'data' / 'raw'
OUT_CSV = BASE / 'outputs' / 'csv'
OUT_CHART = BASE / 'outputs' / 'charts'
PROCESSED = BASE / 'data' / 'processed'
for d in [OUT_CSV, OUT_CHART, PROCESSED]:
    d.mkdir(parents=True, exist_ok=True)

REQUIRED = [
    'transaction_data.csv', 'product.csv', 'campaign_table.csv',
    'campaign_desc.csv', 'coupon_redempt.csv', 'hh_demographic.csv'
]
missing = [f for f in REQUIRED if not (RAW / f).exists()]
if missing:
    raise FileNotFoundError(
        'Missing raw files in data/raw: ' + ', '.join(missing) +
        '. Download the Dunnhumby Complete Journey dataset and place CSV files there.'
    )

usecols_t = ['household_key','BASKET_ID','DAY','PRODUCT_ID','QUANTITY','SALES_VALUE','STORE_ID','RETAIL_DISC','WEEK_NO','COUPON_DISC','COUPON_MATCH_DISC']
t = pd.read_csv(RAW/'transaction_data.csv', usecols=usecols_t)
p = pd.read_csv(RAW/'product.csv')
ct = pd.read_csv(RAW/'campaign_table.csv')
cd = pd.read_csv(RAW/'campaign_desc.csv')
cr = pd.read_csv(RAW/'coupon_redempt.csv')
hh = pd.read_csv(RAW/'hh_demographic.csv')

tr = t.rename(columns={'BASKET_ID':'basket_id','PRODUCT_ID':'product_id','SALES_VALUE':'sales_value','WEEK_NO':'week_no','STORE_ID':'store_id','RETAIL_DISC':'retail_disc','COUPON_DISC':'coupon_disc','COUPON_MATCH_DISC':'coupon_match_disc','QUANTITY':'quantity','DAY':'day'})
prod = p.rename(columns={c:c.lower() for c in p.columns})
for c in ['sales_value','quantity','retail_disc','coupon_disc','coupon_match_disc','day','week_no']:
    tr[c] = pd.to_numeric(tr[c], errors='coerce')
tr = tr.dropna(subset=['household_key','basket_id','product_id','sales_value','day','week_no'])
tr = tr[tr['sales_value'] >= 0].copy()
tr['discount_amount'] = (-tr['retail_disc'].clip(upper=0)) + (-tr['coupon_disc'].clip(upper=0)) + (-tr['coupon_match_disc'].clip(upper=0))
tr['coupon_amount'] = (-tr['coupon_disc'].clip(upper=0)) + (-tr['coupon_match_disc'].clip(upper=0))
tr['coupon_line_flag'] = tr['coupon_amount'] > 0

basket = tr.groupby(['basket_id','household_key','day','week_no'], as_index=False).agg(
    basket_sales=('sales_value','sum'), basket_quantity=('quantity','sum'),
    basket_lines=('product_id','size'), distinct_products=('product_id','nunique'),
    coupon_amount=('coupon_amount','sum'), discount_amount=('discount_amount','sum')
)
basket['coupon_basket_flag'] = basket['coupon_amount'] > 0
basket.to_csv(PROCESSED/'basket_level.csv', index=False, encoding='utf-8-sig')

overview = pd.DataFrame([{
    'transaction_rows': len(tr), 'customers': tr['household_key'].nunique(),
    'baskets': basket['basket_id'].nunique(), 'products': tr['product_id'].nunique(),
    'stores': tr['store_id'].nunique(), 'relative_day_min': int(tr['day'].min()),
    'relative_day_max': int(tr['day'].max()), 'relative_week_min': int(tr['week_no'].min()),
    'relative_week_max': int(tr['week_no'].max()), 'total_sales_value': tr['sales_value'].sum(),
    'total_quantity': tr['quantity'].sum(), 'avg_basket_value': basket['basket_sales'].mean(),
    'median_basket_value': basket['basket_sales'].median(), 'avg_items_per_basket': basket['basket_lines'].mean(),
    'coupon_basket_rate': basket['coupon_basket_flag'].mean()
}])
overview.to_csv(OUT_CSV/'01_sales_overview.csv', index=False, encoding='utf-8-sig')

max_day = int(tr['day'].max())
cust = basket.groupby('household_key', as_index=False).agg(
    total_sales=('basket_sales','sum'), purchase_count=('basket_id','nunique'),
    active_weeks=('week_no','nunique'), first_day=('day','min'), last_day=('day','max'),
    total_quantity=('basket_quantity','sum'), coupon_baskets=('coupon_basket_flag','sum')
)
cust['avg_basket_value'] = cust['total_sales'] / cust['purchase_count']
cust['recency_from_dataset_end'] = max_day - cust['last_day']
cust['coupon_basket_rate'] = cust['coupon_baskets'] / cust['purchase_count']
cust = cust.sort_values('total_sales', ascending=False).reset_index(drop=True)
cust['sales_rank'] = np.arange(1, len(cust)+1)
cust['sales_rank_pct'] = cust['sales_rank'] / len(cust)
cust['sales_contribution_segment'] = pd.cut(cust['sales_rank_pct'], bins=[0,.2,.8,1], labels=['Top 20% customers','Middle 60% customers','Bottom 20% customers'], include_lowest=True)
cust['repurchase_group'] = np.where(cust['purchase_count'] >= 2, '2+ baskets', '1 basket')
cust.to_csv(OUT_CSV/'02_customer_sales_repurchase.csv', index=False, encoding='utf-8-sig')

seg = cust.groupby('sales_contribution_segment', observed=True).agg(customers=('household_key','nunique'), total_sales=('total_sales','sum'), avg_sales_per_customer=('total_sales','mean'), avg_purchase_count=('purchase_count','mean'), avg_coupon_basket_rate=('coupon_basket_rate','mean')).reset_index()
seg['sales_share'] = seg['total_sales'] / seg['total_sales'].sum()
seg.to_csv(OUT_CSV/'03_customer_segment_sales_contribution.csv', index=False, encoding='utf-8-sig')

rep = cust.groupby('repurchase_group').agg(customers=('household_key','nunique'), total_sales=('total_sales','sum'), avg_purchase_count=('purchase_count','mean'), avg_basket_value=('avg_basket_value','mean')).reset_index()
rep['customer_share'] = rep['customers'] / rep['customers'].sum()
rep['sales_share'] = rep['total_sales'] / rep['total_sales'].sum()
rep.to_csv(OUT_CSV/'04_repurchase_behavior_summary.csv', index=False, encoding='utf-8-sig')

cat = tr.merge(prod[['product_id','department','commodity_desc','brand']], on='product_id', how='left')
cat_summary = cat.groupby(['department','commodity_desc'], dropna=False).agg(total_sales=('sales_value','sum'), baskets=('basket_id','nunique'), customers=('household_key','nunique'), units=('quantity','sum'), coupon_line_rate=('coupon_line_flag','mean'), avg_sales_per_line=('sales_value','mean')).reset_index().sort_values('total_sales', ascending=False)
cat_summary['sales_share'] = cat_summary['total_sales'] / cat_summary['total_sales'].sum()
cat_summary.to_csv(OUT_CSV/'05_category_performance.csv', index=False, encoding='utf-8-sig')

weekly = basket.groupby('week_no', as_index=False).agg(weekly_sales=('basket_sales','sum'), active_customers=('household_key','nunique'), baskets=('basket_id','nunique'), avg_basket_value=('basket_sales','mean'), coupon_basket_rate=('coupon_basket_flag','mean'))
weekly.to_csv(OUT_CSV/'06_weekly_sales_trend.csv', index=False, encoding='utf-8-sig')

redeemer_keys = set(cr['household_key'].unique())
cust['coupon_redeemer_group'] = np.where(cust['household_key'].isin(redeemer_keys), 'coupon redeemer', 'non-redeemer')
coupon_vs = cust.groupby('coupon_redeemer_group').agg(customers=('household_key','nunique'), total_sales=('total_sales','sum'), avg_sales_per_customer=('total_sales','mean'), avg_purchase_count=('purchase_count','mean'), avg_basket_value=('avg_basket_value','mean'), avg_coupon_basket_rate=('coupon_basket_rate','mean')).reset_index()
coupon_vs['customer_share'] = coupon_vs['customers'] / coupon_vs['customers'].sum()
coupon_vs['sales_share'] = coupon_vs['total_sales'] / coupon_vs['total_sales'].sum()
coupon_vs.to_csv(OUT_CSV/'07_coupon_redeemer_vs_non_redeemer.csv', index=False, encoding='utf-8-sig')

ct2 = ct.rename(columns={c:c.lower() for c in ct.columns})
cd2 = cd.rename(columns={c:c.lower() for c in cd.columns})
cr2 = cr.rename(columns={c:c.lower() for c in cr.columns})
target = ct2.groupby(['campaign','description'], as_index=False).agg(target_households=('household_key','nunique'))
red = cr2.groupby('campaign', as_index=False).agg(redeemed_households=('household_key','nunique'), redemptions=('coupon_upc','size'), first_redemption_day=('day','min'), last_redemption_day=('day','max'))
camp = target.merge(red, on='campaign', how='left').merge(cd2, on=['campaign','description'], how='left')
for c in ['redeemed_households','redemptions']:
    camp[c] = camp[c].fillna(0).astype(int)
camp['response_rate_observed'] = np.where(camp['target_households'] > 0, camp['redeemed_households'] / camp['target_households'], np.nan)
camp['campaign_duration_days'] = camp['end_day'] - camp['start_day'] + 1
camp = camp.sort_values('response_rate_observed', ascending=False)
camp.to_csv(OUT_CSV/'08_campaign_response_summary.csv', index=False, encoding='utf-8-sig')

camp_type = camp.groupby('description').agg(campaigns=('campaign','nunique'), target_households=('target_households','sum'), redeemed_households=('redeemed_households','sum'), redemptions=('redemptions','sum')).reset_index()
camp_type['response_rate_observed'] = camp_type['redeemed_households'] / camp_type['target_households']
camp_type.to_csv(OUT_CSV/'09_campaign_type_response_summary.csv', index=False, encoding='utf-8-sig')

demo = cust.merge(hh.rename(columns={c:c.lower() for c in hh.columns}), on='household_key', how='inner')
demo_income = demo.groupby('income_desc', dropna=False).agg(customers=('household_key','nunique'), avg_total_sales=('total_sales','mean'), avg_purchase_count=('purchase_count','mean'), avg_coupon_basket_rate=('coupon_basket_rate','mean')).reset_index().sort_values('avg_total_sales', ascending=False)
demo_income.to_csv(OUT_CSV/'10_income_group_behavior_summary.csv', index=False, encoding='utf-8-sig')

metrics = {
    'customers': int(overview.loc[0,'customers']), 'baskets': int(overview.loc[0,'baskets']),
    'total_sales_value': float(overview.loc[0,'total_sales_value']), 'avg_basket_value': float(overview.loc[0,'avg_basket_value']),
    'period_days': f"DAY {int(tr['day'].min())}-{int(tr['day'].max())}",
    'period_weeks': f"WEEK {int(tr['week_no'].min())}-{int(tr['week_no'].max())}",
    'top20_sales_share': float(seg.loc[seg['sales_contribution_segment'].astype(str).eq('Top 20% customers'),'sales_share'].iloc[0]),
    'top_category': str(cat_summary.iloc[0]['commodity_desc']), 'top_category_sales_share': float(cat_summary.iloc[0]['sales_share']),
    'coupon_basket_rate': float(overview.loc[0,'coupon_basket_rate']),
    'best_campaign_type': str(camp_type.sort_values('response_rate_observed', ascending=False).iloc[0]['description']),
    'best_campaign_type_response': float(camp_type.sort_values('response_rate_observed', ascending=False).iloc[0]['response_rate_observed'])
}
(OUT_CSV/'00_key_metrics.json').write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8')

plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(9,5)); plot_seg=seg.copy(); plot_seg['sales_share_pct']=plot_seg['sales_share']*100
plt.bar(plot_seg['sales_contribution_segment'].astype(str), plot_seg['sales_share_pct']); plt.title('Sales Share by Customer Contribution Segment'); plt.ylabel('Sales Share (%)'); plt.xticks(rotation=15, ha='right'); plt.tight_layout(); plt.savefig(OUT_CHART/'customer_segment_sales_share.png', dpi=180); plt.close()
plt.figure(figsize=(9,5)); top=cat_summary.head(10).sort_values('total_sales'); plt.barh(top['commodity_desc'].astype(str), top['total_sales']); plt.title('Top 10 Commodity Groups by Sales'); plt.xlabel('Sales Value'); plt.tight_layout(); plt.savefig(OUT_CHART/'category_sales_top10.png', dpi=180); plt.close()
plt.figure(figsize=(9,5)); plt.plot(weekly['week_no'], weekly['weekly_sales'], marker='o', markersize=2); plt.title('Weekly Sales Trend (Relative WEEK_NO)'); plt.xlabel('Relative WEEK_NO'); plt.ylabel('Sales Value'); plt.tight_layout(); plt.savefig(OUT_CHART/'weekly_sales_trend.png', dpi=180); plt.close()
plt.figure(figsize=(8,5)); cv=coupon_vs.copy(); plt.bar(cv['coupon_redeemer_group'], cv['avg_sales_per_customer']); plt.title('Avg Sales per Customer: Coupon Redeemer vs Non-redeemer'); plt.ylabel('Avg Sales per Customer'); plt.tight_layout(); plt.savefig(OUT_CHART/'coupon_redeemer_avg_sales.png', dpi=180); plt.close()
plt.figure(figsize=(8,5)); cty=camp_type.sort_values('response_rate_observed', ascending=False); plt.bar(cty['description'], cty['response_rate_observed']*100); plt.title('Observed Coupon Redemption Response by Campaign Type'); plt.ylabel('Observed Response Rate (%)'); plt.tight_layout(); plt.savefig(OUT_CHART/'campaign_type_response_rate.png', dpi=180); plt.close()

print('Analysis completed. Outputs were saved under outputs/csv and outputs/charts.')
