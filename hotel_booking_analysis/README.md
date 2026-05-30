# 🏨 Hotel Booking Demand Analysis

> Analyzing 119,390 hotel bookings to uncover cancellation patterns and revenue loss drivers using SQL + Python visualizations.

---

## 📁 Project Structure

```
hotel_booking_analysis/
├── data/
│   ├── generate_data.py          # Generates the ~119k-row dataset & SQLite DB
│   ├── hotel_bookings.csv        # Raw booking data (119,390 rows × 15 columns)
│   └── hotel_bookings.db         # SQLite database
├── sql/
│   └── analysis_queries.sql      # 10 analytical SQL queries
├── visualizations/
│   ├── 01_hotel_type_comparison.png
│   ├── 02_lead_time_cancellation.png
│   ├── 03_customer_type_cancellation.png
│   ├── 04_country_analysis.png
│   ├── 05_monthly_trend.png
│   ├── 06_revenue_lost.png
│   ├── 07_correlation_heatmap.png
│   └── 08_deposit_type.png
├── reports/
│   └── business_report.md        # Full findings + 5 recommendations
├── analysis.py                   # Main script: runs SQL, generates all charts
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install pandas matplotlib seaborn numpy

# 2. Generate the dataset and SQLite database
cd data/
python generate_data.py

# 3. Run the full analysis (SQL queries + 8 charts)
cd ..
python analysis.py
```

All visualizations are saved to `visualizations/`.  
Full findings are in `reports/business_report.md`.

---

## 📊 Dataset Schema

| Column | Description |
|--------|-------------|
| `hotel` | City Hotel or Resort Hotel |
| `is_canceled` | 1 = cancelled, 0 = confirmed |
| `lead_time` | Days between booking and arrival |
| `arrival_date_year` | Year of arrival |
| `arrival_date_month` | Month of arrival (1–12) |
| `stays_in_weekend_nights` | Weekend nights booked |
| `stays_in_week_nights` | Weekday nights booked |
| `customer_type` | Transient / Contract / Group / Transient-Party |
| `country` | Guest country of origin (ISO code) |
| `adr` | Average Daily Rate ($) |
| `total_nights` | Total length of stay |
| `revenue` | Actual revenue (0 if cancelled) |
| `deposit_type` | No Deposit / Non Refund / Refundable |
| `distribution_channel` | TA/TO / Direct / Corporate / GDS |
| `market_segment` | Online TA / Offline TA / Direct / Corporate / etc. |

---

## 🔍 Key Findings

| Finding | Insight |
|---------|---------|
| **Overall cancel rate** | 28.8% (34,377 of 119,390 bookings) |
| **City vs Resort** | City: 31.4% cancel · Resort: 23.8% cancel |
| **Lead time impact** | 0–6 days: 12.4% cancel → 365+ days: 52.0% cancel |
| **Best customer type** | Contract (15.3% cancel rate) |
| **Revenue lost** | ~$8.08M in potential revenue not realised |

---

## 💡 Top 5 Business Recommendations

1. **Tiered non-refundable rates** for bookings 6+ months in advance  
2. **Dynamic overbooking** calibrated by lead-time for city hotels  
3. **Off-season promotions with value-adds** to reduce speculative early bookings  
4. **Expand corporate contract agreements** — lowest cancellation segment  
5. **Soft-commitment deposits + re-confirmation nudges** for high-cancel countries  

See `reports/business_report.md` for the full analysis.

---

## 🛠 Tech Stack

| Tool | Usage |
|------|-------|
| Python 3 | Core language |
| pandas | Data manipulation |
| SQLite3 | SQL querying |
| Matplotlib | Bar, line, grouped charts |
| Seaborn | Correlation heatmap |
| NumPy | Numerical operations |

---

## 📚 Data Source

Modeled on the [Hotel Booking Demand Dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)
by Nuno Antonio, Ana Almeida, and Luis Nunes — ~119k real booking records from two Portuguese hotels.
