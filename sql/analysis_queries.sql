-- ============================================================
-- Hotel Booking Demand Analysis – SQL Queries (SQLite)
-- ============================================================

-- 1. Overall cancellation rate
SELECT
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS total_cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct
FROM bookings;

-- 2. Cancellation rate by hotel type
SELECT
    hotel,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct,
    ROUND(AVG(adr), 2)                                     AS avg_daily_rate,
    ROUND(SUM(revenue), 2)                                 AS total_revenue
FROM bookings
GROUP BY hotel
ORDER BY cancel_rate_pct DESC;

-- 3. Cancellation rate by customer type
SELECT
    customer_type,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct,
    ROUND(AVG(adr), 2)                                     AS avg_daily_rate
FROM bookings
GROUP BY customer_type
ORDER BY cancel_rate_pct DESC;

-- 4. Cancellation rate by lead-time bucket
SELECT
    CASE
        WHEN lead_time < 7   THEN '0-6 days'
        WHEN lead_time < 30  THEN '7-29 days'
        WHEN lead_time < 90  THEN '30-89 days'
        WHEN lead_time < 180 THEN '90-179 days'
        WHEN lead_time < 365 THEN '180-364 days'
        ELSE                      '365+ days'
    END                                                    AS lead_time_bucket,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct
FROM bookings
GROUP BY lead_time_bucket
ORDER BY MIN(lead_time);

-- 5. Top 10 countries by cancellation volume
SELECT
    country,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct,
    ROUND(SUM(revenue), 2)                                 AS total_revenue
FROM bookings
GROUP BY country
ORDER BY cancelled DESC
LIMIT 10;

-- 6. Monthly cancellation trend
SELECT
    arrival_date_year                                      AS year,
    arrival_date_month                                     AS month,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct,
    ROUND(SUM(revenue), 2)                                 AS monthly_revenue
FROM bookings
GROUP BY year, month
ORDER BY year, month;

-- 7. Revenue lost due to cancellations
SELECT
    hotel,
    ROUND(SUM(CASE WHEN is_canceled = 1 THEN adr * total_nights ELSE 0 END), 2)   AS revenue_lost,
    ROUND(SUM(revenue), 2)                                                          AS revenue_earned,
    ROUND(100.0 * SUM(CASE WHEN is_canceled = 1 THEN adr * total_nights ELSE 0 END)
          / (SUM(revenue) + SUM(CASE WHEN is_canceled = 1 THEN adr * total_nights ELSE 0 END)), 2) AS pct_revenue_lost
FROM bookings
GROUP BY hotel;

-- 8. Deposit type vs cancellation
SELECT
    deposit_type,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct
FROM bookings
GROUP BY deposit_type
ORDER BY cancel_rate_pct DESC;

-- 9. Market segment performance
SELECT
    market_segment,
    COUNT(*)                                               AS total_bookings,
    SUM(is_canceled)                                       AS cancelled,
    ROUND(100.0 * SUM(is_canceled) / COUNT(*), 2)         AS cancel_rate_pct,
    ROUND(AVG(adr), 2)                                     AS avg_daily_rate,
    ROUND(SUM(revenue), 2)                                 AS total_revenue
FROM bookings
GROUP BY market_segment
ORDER BY total_revenue DESC;

-- 10. Average lead time for cancelled vs confirmed bookings
SELECT
    is_canceled,
    ROUND(AVG(lead_time), 1)                              AS avg_lead_time,
    ROUND(AVG(adr), 2)                                    AS avg_daily_rate,
    ROUND(AVG(total_nights), 2)                           AS avg_nights
FROM bookings
GROUP BY is_canceled;
