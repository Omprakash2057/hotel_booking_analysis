"""
Hotel Booking Demand Analysis
Runs all SQL queries, generates all visualizations, prints findings.
"""

import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os

# ── Paths ───────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB   = os.path.join(BASE, 'data', 'hotel_bookings.db')
VIZ  = os.path.join(BASE, 'visualizations')
os.makedirs(VIZ, exist_ok=True)

conn = sqlite3.connect(DB)

# ── Palette / style ──────────────────────────────────────────────────────────
CITY   = '#E63946'
RESORT = '#457B9D'
DARK   = '#1D3557'
LIGHT  = '#F1FAEE'
ACC    = '#F4A261'

plt.rcParams.update({
    'figure.facecolor': LIGHT,
    'axes.facecolor':   LIGHT,
    'font.family':      'DejaVu Sans',
    'axes.spines.top':  False,
    'axes.spines.right':False,
})

# ═══════════════════════════════════════════════════════════════════════════════
# 1. Overview KPIs
# ═══════════════════════════════════════════════════════════════════════════════
total = pd.read_sql("SELECT COUNT(*) AS n, SUM(is_canceled) AS c, ROUND(SUM(revenue),0) AS rev FROM bookings", conn)
print("\n══ OVERVIEW ══════════════════════════════════")
print(f"  Total bookings : {int(total['n'][0]):,}")
print(f"  Cancellations  : {int(total['c'][0]):,}  ({100*int(total['c'][0])/int(total['n'][0]):.1f}%)")
print(f"  Total revenue  : ${float(total['rev'][0]):,.0f}")

# ═══════════════════════════════════════════════════════════════════════════════
# 2. Cancellation by hotel type
# ═══════════════════════════════════════════════════════════════════════════════
hotel_df = pd.read_sql("""
    SELECT hotel,
           COUNT(*) AS total,
           SUM(is_canceled) AS cancelled,
           ROUND(100.0*SUM(is_canceled)/COUNT(*),2) AS cancel_rate,
           ROUND(SUM(revenue),0) AS revenue,
           ROUND(AVG(adr),2) AS avg_adr
    FROM bookings GROUP BY hotel""", conn)
print("\n══ BY HOTEL TYPE ═════════════════════════════")
print(hotel_df.to_string(index=False))

# ── Fig 1 : Hotel type comparison ──────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.patch.set_facecolor(LIGHT)
fig.suptitle('Hotel Type Comparison', fontsize=16, fontweight='bold', color=DARK, y=1.01)

colors = [CITY if h == 'City Hotel' else RESORT for h in hotel_df['hotel']]

for ax, col, label in zip(axes,
                           ['cancel_rate','avg_adr','revenue'],
                           ['Cancellation Rate (%)', 'Avg Daily Rate ($)', 'Total Revenue ($)']):
    bars = ax.bar(hotel_df['hotel'], hotel_df[col], color=colors, edgecolor='white', linewidth=1.5, width=0.5)
    ax.set_title(label, fontsize=12, color=DARK, pad=8)
    ax.set_ylabel(label, fontsize=9, color='#555')
    ax.tick_params(labelsize=9)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x()+bar.get_width()/2, h+h*0.02,
                f'{h:,.1f}' if col!='revenue' else f'${h/1e6:.1f}M',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK)

legend = [mpatches.Patch(color=CITY, label='City Hotel'),
          mpatches.Patch(color=RESORT, label='Resort Hotel')]
fig.legend(handles=legend, loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '01_hotel_type_comparison.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 1 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 3. Lead-time buckets
# ═══════════════════════════════════════════════════════════════════════════════
lead_df = pd.read_sql("""
    SELECT
        CASE WHEN lead_time<7   THEN '0-6d'
             WHEN lead_time<30  THEN '7-29d'
             WHEN lead_time<90  THEN '30-89d'
             WHEN lead_time<180 THEN '90-179d'
             WHEN lead_time<365 THEN '180-364d'
             ELSE '365+d' END AS bucket,
        COUNT(*) AS total,
        SUM(is_canceled) AS cancelled,
        ROUND(100.0*SUM(is_canceled)/COUNT(*),2) AS cancel_rate
    FROM bookings GROUP BY bucket ORDER BY MIN(lead_time)""", conn)
print("\n══ BY LEAD TIME ══════════════════════════════")
print(lead_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(11, 5))
fig.patch.set_facecolor(LIGHT)
norm = plt.Normalize(lead_df['cancel_rate'].min(), lead_df['cancel_rate'].max())
bar_colors = plt.cm.RdYlGn_r(norm(lead_df['cancel_rate'].values))
bars = ax.bar(lead_df['bucket'], lead_df['cancel_rate'], color=bar_colors, edgecolor='white', linewidth=1.5)
ax.set_title('Cancellation Rate by Lead-Time Bucket', fontsize=14, fontweight='bold', color=DARK, pad=12)
ax.set_xlabel('Lead Time (days before arrival)', fontsize=11, color='#555')
ax.set_ylabel('Cancellation Rate (%)', fontsize=11, color='#555')
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, h+0.3, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold', color=DARK)
ax.set_facecolor(LIGHT)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '02_lead_time_cancellation.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 2 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 4. Customer type
# ═══════════════════════════════════════════════════════════════════════════════
cust_df = pd.read_sql("""
    SELECT customer_type,
           COUNT(*) AS total,
           SUM(is_canceled) AS cancelled,
           ROUND(100.0*SUM(is_canceled)/COUNT(*),2) AS cancel_rate,
           ROUND(AVG(adr),2) AS avg_adr
    FROM bookings GROUP BY customer_type ORDER BY cancel_rate DESC""", conn)
print("\n══ BY CUSTOMER TYPE ══════════════════════════")
print(cust_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(LIGHT)
palette = [CITY, ACC, RESORT, DARK]
bars = ax.barh(cust_df['customer_type'], cust_df['cancel_rate'],
               color=palette[:len(cust_df)], edgecolor='white', linewidth=1.5)
ax.set_title('Cancellation Rate by Customer Type', fontsize=14, fontweight='bold', color=DARK, pad=12)
ax.set_xlabel('Cancellation Rate (%)', fontsize=11, color='#555')
for bar in bars:
    w = bar.get_width()
    ax.text(w+0.3, bar.get_y()+bar.get_height()/2, f'{w:.1f}%',
            va='center', fontsize=10, fontweight='bold', color=DARK)
ax.set_facecolor(LIGHT)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '03_customer_type_cancellation.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 3 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 5. Top 10 countries by cancellations
# ═══════════════════════════════════════════════════════════════════════════════
country_df = pd.read_sql("""
    SELECT country,
           COUNT(*) AS total,
           SUM(is_canceled) AS cancelled,
           ROUND(100.0*SUM(is_canceled)/COUNT(*),2) AS cancel_rate,
           ROUND(SUM(revenue),0) AS revenue
    FROM bookings GROUP BY country ORDER BY cancelled DESC LIMIT 10""", conn)
print("\n══ TOP 10 COUNTRIES (cancellations) ══════════")
print(country_df.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(LIGHT)
fig.suptitle('Top 10 Countries – Cancellations & Revenue', fontsize=14, fontweight='bold', color=DARK)

colors2 = plt.cm.Blues_r(np.linspace(0.2, 0.8, len(country_df)))
axes[0].barh(country_df['country'][::-1], country_df['cancelled'][::-1],
             color=colors2[::-1], edgecolor='white')
axes[0].set_title('Total Cancellations', fontsize=11, color=DARK)
axes[0].set_xlabel('Cancellations', fontsize=9)
axes[0].set_facecolor(LIGHT)

axes[1].barh(country_df['country'][::-1], country_df['revenue'][::-1]/1e6,
             color=colors2[::-1], edgecolor='white')
axes[1].set_title('Earned Revenue ($ M)', fontsize=11, color=DARK)
axes[1].set_xlabel('Revenue ($M)', fontsize=9)
axes[1].set_facecolor(LIGHT)

for ax in axes:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig(os.path.join(VIZ, '04_country_analysis.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 4 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 6. Monthly trend
# ═══════════════════════════════════════════════════════════════════════════════
monthly = pd.read_sql("""
    SELECT arrival_date_year AS yr, arrival_date_month AS mo,
           COUNT(*) AS total,
           SUM(is_canceled) AS cancelled,
           ROUND(100.0*SUM(is_canceled)/COUNT(*),2) AS cancel_rate,
           ROUND(SUM(revenue),0) AS revenue
    FROM bookings GROUP BY yr, mo ORDER BY yr, mo""", conn)
monthly['period'] = monthly['yr'].astype(str)+'-'+monthly['mo'].astype(str).str.zfill(2)

fig, ax1 = plt.subplots(figsize=(14, 5))
fig.patch.set_facecolor(LIGHT)
ax1.set_facecolor(LIGHT)
ax2 = ax1.twinx()

ax1.fill_between(range(len(monthly)), monthly['revenue']/1e6, alpha=0.25, color=RESORT)
ax1.plot(range(len(monthly)), monthly['revenue']/1e6, color=RESORT, linewidth=2, label='Revenue ($M)')
ax2.plot(range(len(monthly)), monthly['cancel_rate'], color=CITY, linewidth=2, linestyle='--', label='Cancel Rate (%)')

ax1.set_xticks(range(0, len(monthly), 3))
ax1.set_xticklabels(monthly['period'].iloc[::3], rotation=45, ha='right', fontsize=8)
ax1.set_ylabel('Revenue ($M)', color=RESORT, fontsize=11)
ax2.set_ylabel('Cancellation Rate (%)', color=CITY, fontsize=11)
ax1.set_title('Monthly Revenue vs Cancellation Rate (2015-2017)', fontsize=14, fontweight='bold', color=DARK, pad=12)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left', fontsize=9)
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '05_monthly_trend.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 5 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. Revenue lost
# ═══════════════════════════════════════════════════════════════════════════════
rev_df = pd.read_sql("""
    SELECT hotel,
           ROUND(SUM(CASE WHEN is_canceled=1 THEN adr*total_nights ELSE 0 END),0) AS lost,
           ROUND(SUM(revenue),0) AS earned
    FROM bookings GROUP BY hotel""", conn)
print("\n══ REVENUE LOST ══════════════════════════════")
print(rev_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(LIGHT)
x = np.arange(len(rev_df))
w = 0.35
b1 = ax.bar(x-w/2, rev_df['earned']/1e6, w, label='Earned Revenue', color=RESORT, edgecolor='white')
b2 = ax.bar(x+w/2, rev_df['lost']/1e6,   w, label='Lost Revenue',   color=CITY,   edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels(rev_df['hotel'], fontsize=11)
ax.set_ylabel('Revenue ($M)', fontsize=11, color='#555')
ax.set_title('Earned vs Lost Revenue by Hotel Type', fontsize=14, fontweight='bold', color=DARK, pad=12)
ax.legend(fontsize=10)
ax.set_facecolor(LIGHT)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for bar in list(b1)+list(b2):
    h = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, h+0.1, f'${h:.1f}M',
            ha='center', va='bottom', fontsize=9, fontweight='bold', color=DARK)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '06_revenue_lost.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 6 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 8. Correlation heatmap
# ═══════════════════════════════════════════════════════════════════════════════
raw = pd.read_sql("""
    SELECT is_canceled, lead_time, adr, total_nights, stays_in_week_nights,
           stays_in_weekend_nights
    FROM bookings""", conn)
corr = raw.corr()

fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor(LIGHT)
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm',
            center=0, square=True, linewidths=.5, ax=ax,
            cbar_kws={'shrink': .8})
ax.set_title('Feature Correlation Matrix', fontsize=14, fontweight='bold', color=DARK, pad=12)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '07_correlation_heatmap.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 7 saved")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. Deposit type impact
# ═══════════════════════════════════════════════════════════════════════════════
dep_df = pd.read_sql("""
    SELECT deposit_type, COUNT(*) AS total,
           SUM(is_canceled) AS cancelled,
           ROUND(100.0*SUM(is_canceled)/COUNT(*),2) AS cancel_rate
    FROM bookings GROUP BY deposit_type ORDER BY cancel_rate DESC""", conn)
print("\n══ DEPOSIT TYPE ══════════════════════════════")
print(dep_df.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor(LIGHT)
colors3 = [CITY, ACC, RESORT]
bars = ax.bar(dep_df['deposit_type'], dep_df['cancel_rate'],
              color=colors3[:len(dep_df)], edgecolor='white', linewidth=1.5, width=0.5)
ax.set_title('Cancellation Rate by Deposit Type', fontsize=13, fontweight='bold', color=DARK, pad=10)
ax.set_ylabel('Cancellation Rate (%)', fontsize=10)
ax.set_facecolor(LIGHT)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
for bar in bars:
    h = bar.get_height()
    ax.text(bar.get_x()+bar.get_width()/2, h+0.4, f'{h:.1f}%',
            ha='center', va='bottom', fontsize=11, fontweight='bold', color=DARK)
plt.tight_layout()
plt.savefig(os.path.join(VIZ, '08_deposit_type.png'), dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ Fig 8 saved")

conn.close()
print("\n✅  All visualizations saved to:", VIZ)
