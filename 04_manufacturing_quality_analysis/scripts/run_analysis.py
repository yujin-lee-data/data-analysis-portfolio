import sqlite3
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# 통일 차트 스타일 (프로젝트 04 강조색: 크림슨 빨강)
# 차트 라벨은 글꼴 호환을 위해 영어로 작성합니다.
# ---------------------------------------------------------------------------
ACCENT = "#C0392B"     # P4 대표색 (크림슨 빨강)
ACCENT_DK = "#8A281E"  # 강조(상위 1순위 등)
ACCENT_LT = "#E2A39C"  # 보조 톤
GREY = "#C2C8D0"       # 일반/주의 신호
GREY_DK = "#6B7280"
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.edgecolor": "#D9DDE3", "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": "#EEF0F3", "grid.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 11, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.titlecolor": "#1B2330", "text.color": "#2B2F36",
    "axes.labelcolor": "#5B6472", "xtick.color": "#5B6472", "ytick.color": "#5B6472",
})

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw" / "uci-secom.csv"
OUT_CSV = BASE / "outputs" / "csv"
OUT_FIG = BASE / "outputs" / "figures"
DB_DIR = BASE / "database"
for p in [OUT_CSV, OUT_FIG, DB_DIR]:
    p.mkdir(parents=True, exist_ok=True)


def pct_score(series):
    return (series.rank(pct=True, method="average") * 5).fillna(0)


# ---------------------------------------------------------------------------
# 보조 베이스라인 모델 (순수 numpy 로지스틱 회귀)
# 목적: 품질 신호 후보를 "참고용 보조 지표"로 보기 위함. 실제 공정 적용/성능 주장 아님.
# scikit-learn 등 무거운 의존성 없이 어디서나 재현 가능하도록 numpy로만 구현.
# ---------------------------------------------------------------------------
def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def _train_logreg(X, y, lr=0.5, epochs=500, l2=1e-2):
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    pos = max(y.sum(), 1.0)
    neg = max((1 - y).sum(), 1.0)
    w_pos = neg / pos  # 클래스 불균형 보정 (Fail 가중치 ↑)
    sw = np.where(y == 1, w_pos, 1.0)
    sw = sw / sw.mean()
    for _ in range(epochs):
        p = _sigmoid(X @ w + b)
        grad = sw * (p - y)
        gw = X.T @ grad / n + l2 * w
        gb = grad.mean()
        w -= lr * gw
        b -= lr * gb
    return w, b


def _auc(y_true, score):
    # Mann-Whitney U 기반 ROC AUC (numpy)
    order = np.argsort(score)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(score) + 1)
    pos = y_true == 1
    n_pos = pos.sum()
    n_neg = (~pos).sum()
    if n_pos == 0 or n_neg == 0:
        return np.nan
    return (ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def baseline_model(work, features, miss):
    use = miss.loc[miss["missing_rate"] < 0.4, "feature"].tolist()
    X = work[use].astype(float).copy()
    X = X.fillna(X.median())
    y = (work["Pass/Fail"] == 1).astype(int).to_numpy()
    Xv = X.to_numpy()

    rng = np.random.default_rng(42)
    idx = rng.permutation(len(y))
    cut = int(len(y) * 0.7)
    tr, te = idx[:cut], idx[cut:]

    mu, sd = Xv[tr].mean(0), Xv[tr].std(0)
    sd[sd == 0] = 1.0
    Xtr, Xte = (Xv[tr] - mu) / sd, (Xv[te] - mu) / sd

    w, b = _train_logreg(Xtr, y[tr])
    prob_te = _sigmoid(Xte @ w + b)
    pred_te = (prob_te >= 0.5).astype(int)

    tp = int(((pred_te == 1) & (y[te] == 1)).sum())
    fp = int(((pred_te == 1) & (y[te] == 0)).sum())
    fn = int(((pred_te == 0) & (y[te] == 1)).sum())
    acc = float((pred_te == y[te]).mean())
    recall_fail = tp / (tp + fn) if (tp + fn) else np.nan
    precision_fail = tp / (tp + fp) if (tp + fp) else np.nan
    auc = float(_auc(y[te], prob_te))

    metrics = pd.DataFrame(
        [
            ["model_type", "logistic_regression_numpy_baseline"],
            ["role", "auxiliary_reference_only"],
            ["n_features_used", len(use)],
            ["n_train", len(tr)],
            ["n_test", len(te)],
            ["test_fail_count", int(y[te].sum())],
            ["accuracy", round(acc, 3)],
            ["recall_fail", round(recall_fail, 3) if pd.notna(recall_fail) else np.nan],
            ["precision_fail", round(precision_fail, 3) if pd.notna(precision_fail) else np.nan],
            ["roc_auc", round(auc, 3) if pd.notna(auc) else np.nan],
            ["note", "imbalanced data; accuracy alone is misleading; reference signal only"],
        ],
        columns=["metric", "value"],
    )

    importance = (
        pd.DataFrame({"feature": use, "abs_coefficient": np.abs(w)})
        .sort_values("abs_coefficient", ascending=False)
        .reset_index(drop=True)
    )
    return metrics, importance


def main():
    if not RAW.exists():
        raise FileNotFoundError(f"Raw data not found: {RAW}\nPlace uci-secom.csv in data/raw/ and rerun.")
    df = pd.read_csv(RAW)
    feature_cols = [c for c in df.columns if c not in ["Time", "Pass/Fail"]]
    rename_map = {c: f"feature_{int(c):03d}" for c in feature_cols}
    work = df.rename(columns=rename_map).copy()
    work["label_name"] = work["Pass/Fail"].map({-1: "Pass", 1: "Fail"})
    work["Time"] = pd.to_datetime(work["Time"], errors="coerce")
    features = [rename_map[c] for c in feature_cols]
    work.to_csv(OUT_CSV / "secom_merged.csv", index=False)

    label_dist = work.groupby(["Pass/Fail", "label_name"], dropna=False).size().reset_index(name="count")
    label_dist["rate"] = label_dist["count"] / len(work)
    label_dist.to_csv(OUT_CSV / "label_distribution.csv", index=False)

    miss = work[features].isna().sum().rename("missing_count").reset_index().rename(columns={"index": "feature"})
    miss["total_count"] = len(work)
    miss["missing_rate"] = miss["missing_count"] / len(work)
    miss["missing_band"] = pd.cut(miss["missing_rate"], bins=[-0.001, 0.1, 0.4, 1.001], labels=["low_under_10pct", "medium_10_to_40pct", "high_over_40pct"])
    miss.to_csv(OUT_CSV / "feature_missing_summary.csv", index=False)
    miss[miss["missing_rate"] >= 0.4].sort_values("missing_rate", ascending=False).to_csv(OUT_CSV / "high_missing_features.csv", index=False)

    rows = []
    for f in features:
        s = work[f]
        pass_s = work.loc[work["Pass/Fail"] == -1, f].dropna()
        fail_s = work.loc[work["Pass/Fail"] == 1, f].dropna()
        overall_std = s.std(skipna=True)
        pass_mean = pass_s.mean() if len(pass_s) else np.nan
        fail_mean = fail_s.mean() if len(fail_s) else np.nan
        mean_diff = fail_mean - pass_mean if pd.notna(fail_mean) and pd.notna(pass_mean) else np.nan
        std_diff = mean_diff / overall_std if overall_std and pd.notna(mean_diff) and overall_std != 0 else np.nan
        rows.append({"feature": f, "pass_count": len(pass_s), "fail_count": len(fail_s), "pass_mean": pass_mean, "fail_mean": fail_mean, "mean_difference_fail_minus_pass": mean_diff, "pass_median": pass_s.median() if len(pass_s) else np.nan, "fail_median": fail_s.median() if len(fail_s) else np.nan, "overall_std": overall_std, "standardized_mean_difference": std_diff, "abs_standardized_mean_difference": abs(std_diff) if pd.notna(std_diff) else np.nan})
    gdiff = pd.DataFrame(rows).merge(miss[["feature", "missing_rate", "missing_count"]], on="feature")
    gdiff.sort_values("abs_standardized_mean_difference", ascending=False).to_csv(OUT_CSV / "feature_group_difference.csv", index=False)

    var_rows = []
    for f in features:
        s = work[f].dropna()
        if len(s) == 0:
            var_rows.append({"feature": f, "non_missing_count": 0, "mean": np.nan, "std": np.nan, "iqr": np.nan, "cv_abs": np.nan, "outlier_rate_iqr": np.nan})
            continue
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        out_rate = ((s < lower) | (s > upper)).mean() if iqr and pd.notna(iqr) else 0
        mean, std = s.mean(), s.std()
        cv_abs = abs(std / mean) if pd.notna(mean) and mean != 0 else np.nan
        var_rows.append({"feature": f, "non_missing_count": len(s), "mean": mean, "std": std, "iqr": iqr, "cv_abs": cv_abs, "outlier_rate_iqr": out_rate})
    var = pd.DataFrame(var_rows).merge(miss[["feature", "missing_rate"]], on="feature")
    var.sort_values("std", ascending=False).to_csv(OUT_CSV / "feature_variability_summary.csv", index=False)

    priority = gdiff[["feature", "abs_standardized_mean_difference", "standardized_mean_difference", "missing_rate"]].merge(var[["feature", "std", "iqr", "outlier_rate_iqr"]], on="feature", how="left")
    priority["group_difference_score"] = pct_score(priority["abs_standardized_mean_difference"])
    priority["missing_risk_score"] = pd.cut(priority["missing_rate"], [-0.001, 0.05, 0.1, 0.2, 0.4, 1.0], labels=[1, 2, 3, 4, 5]).astype(float)
    priority["variability_score"] = pct_score(priority["std"])
    priority["outlier_score"] = pct_score(priority["outlier_rate_iqr"])
    priority["priority_score"] = priority["group_difference_score"] * 0.45 + priority["missing_risk_score"] * 0.20 + priority["variability_score"] * 0.25 + priority["outlier_score"] * 0.10
    priority["analysis_status"] = np.where(priority["missing_rate"] >= 0.4, "review_with_caution_high_missing", "priority_review_candidate")
    priority = priority.sort_values("priority_score", ascending=False)
    priority.to_csv(OUT_CSV / "quality_signal_priority.csv", index=False)

    top_feats = priority[priority["missing_rate"] < 0.4].head(5)["feature"].tolist()
    work[["Time", "Pass/Fail", "label_name"] + top_feats].head(200).to_csv(OUT_CSV / "top_priority_signal_examples.csv", index=False)

    # 보조 베이스라인 모델 산출물
    model_metrics, model_importance = baseline_model(work, features, miss)
    model_metrics.to_csv(OUT_CSV / "model_baseline_metrics.csv", index=False)
    model_importance.to_csv(OUT_CSV / "model_feature_importance.csv", index=False)

    # ----- Figures (English labels) -----
    def savefig(name):
        plt.tight_layout(); plt.savefig(OUT_FIG / name, dpi=180, bbox_inches="tight"); plt.close()

    ld = label_dist.sort_values("Pass/Fail")
    bar_colors = [GREY if n == "Pass" else ACCENT for n in ld["label_name"]]
    plt.figure(figsize=(7, 4.2)); plt.bar(ld["label_name"], ld["count"], color=bar_colors)
    plt.title("Pass/Fail Label Distribution"); plt.ylabel("Count")
    for i, v in enumerate(ld["count"]): plt.text(i, v + 20, f"{v}\n({ld.iloc[i]['rate']:.1%})", ha="center", fontsize=9)
    savefig("01_label_distribution.png")

    plt.figure(figsize=(7, 4.2)); plt.hist(miss["missing_rate"], bins=30, color=ACCENT, edgecolor="white")
    plt.title("Feature Missing Rate Distribution"); plt.xlabel("Missing Rate"); plt.ylabel("Number of Features"); savefig("02_missing_rate_distribution.png")

    topm = miss.sort_values("missing_rate", ascending=False).head(15).sort_values("missing_rate")
    plt.figure(figsize=(7, 5)); plt.barh(topm["feature"], topm["missing_rate"], color=GREY)
    plt.title("Top Missing Features (data-quality watchlist)"); plt.xlabel("Missing Rate"); savefig("03_top_missing_features.png")

    topg = gdiff[gdiff["missing_rate"] < 0.4].sort_values("abs_standardized_mean_difference", ascending=False).head(15).sort_values("abs_standardized_mean_difference")
    plt.figure(figsize=(7, 5)); plt.barh(topg["feature"], topg["abs_standardized_mean_difference"], color=ACCENT)
    plt.title("Top Pass/Fail Difference Features"); plt.xlabel("Abs. Standardized Mean Difference"); savefig("04_top_group_difference_features.png")

    topv = var[var["missing_rate"] < 0.4].sort_values("std", ascending=False).head(15).sort_values("std")
    plt.figure(figsize=(7, 5)); plt.barh(topv["feature"], topv["std"], color=ACCENT_LT)
    plt.title("Top Variability Features"); plt.xlabel("Standard Deviation"); savefig("05_top_variability_features.png")

    topp = priority[priority["missing_rate"] < 0.4].head(20).sort_values("priority_score")
    pcolors = [ACCENT] * len(topp); pcolors[-1] = ACCENT_DK
    plt.figure(figsize=(7, 6)); plt.barh(topp["feature"], topp["priority_score"], color=pcolors)
    plt.title("Top 20 Quality Signal Priority Candidates"); plt.xlabel("Priority Score"); savefig("06_quality_signal_priority_top20.png")

    top_feature = priority[priority["missing_rate"] < 0.4].iloc[0]["feature"]
    pass_vals = work.loc[work["Pass/Fail"] == -1, top_feature].dropna(); fail_vals = work.loc[work["Pass/Fail"] == 1, top_feature].dropna()
    plt.figure(figsize=(6.6, 4.5))
    bp = plt.boxplot([pass_vals, fail_vals], tick_labels=["Pass", "Fail"], showfliers=False, patch_artist=True)
    for patch, c in zip(bp["boxes"], [GREY, ACCENT]): patch.set_facecolor(c); patch.set_edgecolor("#8A8F98")
    for med in bp["medians"]: med.set_color("#2B2F36")
    plt.title(f"Pass/Fail Distribution: {top_feature}"); plt.ylabel("Measured Value"); savefig("07_pass_fail_boxplot_top_feature.png")

    topi = model_importance.head(15).sort_values("abs_coefficient")
    plt.figure(figsize=(7, 5)); plt.barh(topi["feature"], topi["abs_coefficient"], color=ACCENT)
    plt.title("Baseline Logistic Coefficients (auxiliary reference)"); plt.xlabel("Abs. Standardized Coefficient"); savefig("08_model_baseline_feature_importance.png")

    conn = sqlite3.connect(DB_DIR / "secom_analysis.sqlite")
    label_dist.to_sql("label_distribution", conn, if_exists="replace", index=False)
    miss.to_sql("feature_missing_summary", conn, if_exists="replace", index=False)
    gdiff.to_sql("feature_group_difference", conn, if_exists="replace", index=False)
    var.to_sql("feature_variability_summary", conn, if_exists="replace", index=False)
    priority.to_sql("quality_signal_priority", conn, if_exists="replace", index=False)
    model_metrics.to_sql("model_baseline_metrics", conn, if_exists="replace", index=False)
    model_importance.to_sql("model_feature_importance", conn, if_exists="replace", index=False)
    work[["Time", "Pass/Fail", "label_name"] + top_feats].to_sql("top_priority_signal_examples", conn, if_exists="replace", index=False)
    conn.close()
    print("Analysis completed. Check outputs/csv and outputs/figures.")


if __name__ == "__main__":
    main()
