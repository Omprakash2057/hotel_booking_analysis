# Hotel Booking Demand Analysis — Business Report

## Executive Summary

Analysis of **119,390 hotel bookings** across City and Resort hotel properties
(2015–2017) reveals a **28.8% overall cancellation rate**, translating to
**~$8.08 million in lost potential revenue**. The patterns uncovered point to
clear, actionable levers: lead-time pricing, deposit policy reform, and
segment-specific incentives.

---

## Key Findings

### 1. City Hotels Cancel Far More Than Resort Hotels
| Hotel Type   | Bookings | Cancellation Rate | Revenue Earned | Revenue Lost |
|-------------|----------|-------------------|----------------|--------------|
| City Hotel  | 78,799   | **31.4%**         | $13.1M         | $5.95M       |
| Resort Hotel| 40,591   | **23.8%**         | $6.8M          | $2.13M       |

City hotels account for **74% of total cancellations** despite representing
66% of bookings. Leisure-motivated resort guests appear more committed once
they book; city hotel guests (largely business/transient) cancel more readily.

---

### 2. Booking Lead-Time is the Strongest Predictor of Cancellation
| Lead Time      | Cancel Rate |
|----------------|-------------|
| 0–6 days       | **12.4%**   |
| 7–29 days      | 19.3%       |
| 30–89 days     | 28.6%       |
| 90–179 days    | 35.6%       |
| 180–364 days   | 44.2%       |
| **365+ days**  | **52.0%**   |

Bookings placed **6+ months in advance cancel at more than 4× the rate** of
same-week bookings. Early bookers are either planning speculatively or find
better deals closer to arrival.

---

### 3. Transient Customers Drive the Most Volume and Cancellations
| Customer Type   | Cancel Rate | Bookings |
|----------------|-------------|----------|
| Transient-Party | 30.7%       | 14,384   |
| Transient       | 30.6%       | 89,538   |
| Group           | 20.8%       | 3,697    |
| **Contract**    | **15.3%**   | 11,771   |

Contract customers are the most reliable segment. Transient customers—who
make up ~87% of all bookings—are also the most likely to cancel.

---

### 4. Portugal (PRT) Dominates in Both Bookings and Cancellations
Portugal accounts for ~29% of all bookings and roughly 29% of cancellations,
suggesting domestic market dynamics (high online platform usage, speculative
booking behavior) contribute disproportionately. The UK, France, Spain, and
Germany round out the top 5.

---

### 5. Deposit Type Has Surprisingly Little Effect (as Currently Structured)
| Deposit Type | Cancel Rate |
|-------------|-------------|
| No Deposit  | 28.8%       |
| Non Refund  | 28.8%       |
| Refundable  | 27.6%       |

This counter-intuitive finding (non-refundable deposits not reducing cancellations)
suggests customers are either booking non-refundable rates speculatively or the
non-refundable pricing is not enough of a deterrent. A re-pricing strategy is needed.

---

## 5 Business Recommendations

### Recommendation 1: Tiered Non-Refundable Rates for Early Bookings
**Problem:** 365+ day bookings cancel at 52%.  
**Action:** Offer a meaningful discount (12–18%) for non-refundable bookings
made 6+ months in advance. Guests willing to commit get savings; the hotel locks
in revenue. Complement with a mid-rate "partially refundable" tier (refundable
only 90+ days before arrival) for 90–180 day bookings.  
**Expected impact:** Reduce long-lead cancellations by 20–30%, securing an
estimated additional **$1.2–1.8M in annual revenue**.

---

### Recommendation 2: Dynamic Overbooking Strategy for City Hotels
**Problem:** City hotels cancel at 31.4% vs. 23.8% for resorts.  
**Action:** Implement data-driven overbooking calibrated by lead-time band
and season. For city hotels, safe overbooking at 8–12% for bookings >90 days
out can offset expected no-shows without significant walk-in risk.  
**Note:** Pair with a guest walk protocol and partner hotel agreements to
handle rare oversell events.

---

### Recommendation 3: Off-Season Promotions to Reduce Speculative Early Bookings
**Problem:** Monthly analysis shows predictable low-season troughs (Jan–Feb,
Nov) where revenue dips and cancellation rates climb.  
**Action:** Launch targeted early-bird campaigns for shoulder/off-season
arrivals that include value-adds (complimentary breakfast, late checkout,
parking) rather than just rate discounts. Early bookers choosing added value
over a refundable option are more likely to show up.

---

### Recommendation 4: Contract Rate Expansion for Corporate Clients
**Problem:** Contract customers cancel at only 15.3% but represent just 9.9%
of bookings.  
**Action:** Actively grow corporate contract agreements, particularly for
city hotels where business travel dominates. Offer volume-discount contracts
with guaranteed minimums and penalties for under-delivery. Target companies
with recurring multi-night travel patterns.  
**Expected impact:** Each 1% shift from Transient to Contract mix could
reduce the overall cancellation rate by ~0.15 percentage points.

---

### Recommendation 5: Country-Specific Cancellation Nudges (Portugal Focus)
**Problem:** Portugal accounts for 29% of bookings and a proportional share
of cancellations, suggesting high OTA (Online Travel Agency) usage with easy
cancel policies.  
**Action:** For high-volume countries, work with OTA channel partners to
introduce a "soft commitment" nudge — e.g., a small deposit (10%) captured at
booking with full refund if cancelled 30+ days out. This breaks the pattern of
zero-friction speculative booking without alienating customers.  
**Complement with:** Email re-confirmation campaigns at 60, 30, and 7 days
before arrival for all transient bookings with >90-day lead times.

---

## Data & Methodology

- **Dataset:** ~119,390 bookings, synthetic data modeled on Kaggle's Hotel
  Booking Demand dataset (Nuno Antonio et al.)
- **Storage:** SQLite database (`hotel_bookings.db`)
- **Querying:** 10 SQL analytical queries grouped by hotel type, customer
  type, country, lead-time, deposit type, market segment, and time period
- **Visualization:** Matplotlib & Seaborn (8 charts)
- **Tools:** Python 3, pandas, NumPy

---

*Report generated from `analysis.py` — see `sql/analysis_queries.sql` for all queries.*
