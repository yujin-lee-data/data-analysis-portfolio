from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
# 통일 차트 스타일 (프로젝트 02 강조색)
ACCENT = "#6D4AE0"
ACCENT_DK = "#4A2EA8"
ACCENT_LT = "#9B8AF0"
GREY = "#9AA6B2"
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
DATA = BASE / "data" / "actual_bigquery"
OUT = BASE / "data" / "output_csv"
CHART = BASE / "charts"
OUT.mkdir(parents=True, exist_ok=True)
CHART.mkdir(parents=True, exist_ok=True)

try:
    plt.rcParams["font.family"] = "NanumSquare"
except Exception:
    plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2E5E9E"
NAVY = "#1F4374"
CYAN = "#9FB6D8"
ORANGE = "#C5D3E8"
RED = "#16335A"
GRAY = "#9AA6B2"

seq = pd.read_csv(DATA / "04b_sequential_funnel_conversion_actual.csv")
dev = pd.read_csv(DATA / "05_device_conversion_actual.csv")
purch = pd.read_csv(DATA / "07_purchaser_vs_non_purchaser_actual.csv")
daily = pd.read_csv(DATA / "02_user_daily_activity_actual.csv")
cat = pd.read_csv(DATA / "06_category_conversion_actual.csv")

# Keep original CSV copies in output_csv for reproducibility.
for source in DATA.glob("*.csv"):
    target = OUT / source.name
    if not target.exists():
        pd.read_csv(source).to_csv(target, index=False)

labels = ["Session\nstart", "View\nitem", "Add to\ncart", "Begin\ncheckout", "Purchase"]
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.bar(labels, seq["users"], color=[NAVY, BLUE, CYAN, ORANGE, RED])
for i, v in enumerate(seq["users"]):
    ax.text(i, v + max(seq["users"]) * 0.02, f"{int(v):,}", ha="center", fontsize=11)
ax.set_title("Sequential Funnel Users (Defined Representative Flow)", fontsize=16, fontweight="bold")
ax.set_ylabel("Users")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()
fig.savefig(CHART / "01_funnel_sequential.png", dpi=200)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5.2))
drop = seq.iloc[1:].copy()
ax.bar(["Session→View", "View→Cart", "Cart→Checkout", "Checkout→Purchase"], drop["dropoff_from_previous"] * 100, color=[GRAY, RED, ORANGE, CYAN])
for i, v in enumerate(drop["dropoff_from_previous"] * 100):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontsize=12, fontweight="bold")
ax.set_ylim(0, 100)
ax.set_title("Drop-off Rate by Funnel Step", fontsize=16, fontweight="bold")
ax.set_ylabel("Drop-off rate (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()
fig.savefig(CHART / "02_dropoff_priority.png", dpi=200)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5.2))
dev2 = dev.sort_values("session_to_purchase_rate", ascending=False)
ax.bar(dev2["device_category"], dev2["session_to_purchase_rate"] * 100, color=[BLUE, CYAN, ORANGE])
for i, v in enumerate(dev2["session_to_purchase_rate"] * 100):
    ax.text(i, v + 0.05, f"{v:.2f}%", ha="center", fontsize=12)
ax.set_title("Session-to-Purchase Rate by Device", fontsize=16, fontweight="bold")
ax.set_ylabel("Conversion rate (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()
fig.savefig(CHART / "03_device_conversion.png", dpi=200)
plt.close(fig)

valid = cat.dropna(subset=["view_to_cart_rate"]).copy()
valid = valid[valid["view_item_users"] > 30].sort_values("view_to_cart_rate", ascending=False).head(8)
fig, ax = plt.subplots(figsize=(9, 5.2))
if len(valid):
    ax.barh(valid["item_category"][::-1], (valid["view_to_cart_rate"] * 100)[::-1], color=BLUE)
    for y, v in enumerate((valid["view_to_cart_rate"] * 100)[::-1]):
        ax.text(v + 0.3, y, f"{v:.1f}%", va="center", fontsize=10)
else:
    ax.text(0.5, 0.5, "Category-level view/add_to_cart fields require additional validation", ha="center", va="center")
ax.set_title("Category View-to-Cart Rate (Valid Categories Only)", fontsize=16, fontweight="bold")
ax.set_xlabel("View-to-cart rate (%)")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", alpha=0.2)
fig.tight_layout()
fig.savefig(CHART / "04_category_conversion.png", dpi=200)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5.2))
purch["group"] = purch["is_purchaser"].map({True: "Purchaser", False: "Non-purchaser"})
metrics = ["avg_view_item_events", "avg_add_to_cart_events", "avg_begin_checkout_events"]
x = np.arange(len(metrics)); width = 0.35
for _, row in purch.iterrows():
    offset = -width / 2 if row["group"] == "Non-purchaser" else width / 2
    ax.bar(x + offset, [row[m] for m in metrics], width=width, label=row["group"])
ax.set_xticks(x, ["View item", "Add to cart", "Begin checkout"])
ax.set_title("Average Key Events per User Group", fontsize=16, fontweight="bold")
ax.set_ylabel("Avg. events")
ax.legend(frameon=False)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", alpha=0.2)
fig.tight_layout()
fig.savefig(CHART / "05_purchaser_vs_non_purchaser.png", dpi=200)
plt.close(fig)

fig, ax = plt.subplots(figsize=(9, 5.2))
daily["event_dt"] = pd.to_datetime(daily["event_dt"])
ax.plot(daily["event_dt"], daily["active_users"], linewidth=2.2)
ax.set_title("Daily Active Users in Sample Period", fontsize=16, fontweight="bold")
ax.set_ylabel("Active users")
ax.set_xlabel("Event date")
ax.spines[["top", "right"]].set_visible(False)
ax.grid(alpha=0.2)
fig.autofmt_xdate()
fig.tight_layout()
fig.savefig(CHART / "07_daily_active_users.png", dpi=200)
plt.close(fig)

print("Charts regenerated from actual BigQuery CSV outputs.")
