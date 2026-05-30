import pandas as pd
import numpy as np
import sqlite3
import os

np.random.seed(42)
N = 119390

hotels = np.random.choice(['City Hotel', 'Resort Hotel'], size=N, p=[0.66, 0.34])
customer_types = np.random.choice(['Transient', 'Contract', 'Transient-Party', 'Group'],
                                   size=N, p=[0.75, 0.10, 0.12, 0.03])
countries = np.random.choice(
    ['PRT','GBR','FRA','ESP','DEU','ITA','IRL','USA','BEL','NLD',
     'CHE','BRA','AUT','SWE','NOR','POL','ROU','CHN','AUS','RUS'],
    size=N,
    p=[0.29,0.12,0.10,0.08,0.07,0.05,0.04,0.04,0.03,0.03,
       0.03,0.02,0.02,0.02,0.01,0.01,0.01,0.01,0.01,0.01]
)

lead_times = np.concatenate([
    np.random.randint(0, 7, int(N * 0.15)),
    np.random.randint(7, 30, int(N * 0.22)),
    np.random.randint(30, 90, int(N * 0.25)),
    np.random.randint(90, 180, int(N * 0.20)),
    np.random.randint(180, 365, int(N * 0.12)),
    np.random.randint(365, 737, int(N * 0.06)),
])
np.random.shuffle(lead_times)
if len(lead_times) < N:
    lead_times = np.append(lead_times, np.random.randint(0, 365, N - len(lead_times)))
lead_times = lead_times[:N]

def get_cancel_prob(hotel, lead_time, customer_type):
    base = 0.37 if hotel == 'City Hotel' else 0.28
    if lead_time < 7:
        base *= 0.4
    elif lead_time < 30:
        base *= 0.6
    elif lead_time < 90:
        base *= 0.9
    elif lead_time < 180:
        base *= 1.1
    elif lead_time < 365:
        base *= 1.4
    else:
        base *= 1.6
    if customer_type == 'Contract':
        base *= 0.5
    elif customer_type == 'Group':
        base *= 0.7
    return min(base, 0.95)

cancel_probs = np.array([get_cancel_prob(hotels[i], lead_times[i], customer_types[i]) for i in range(N)])
is_canceled = (np.random.random(N) < cancel_probs).astype(int)

adr_base = np.where(hotels == 'City Hotel',
                    np.random.normal(105, 30, N),
                    np.random.normal(95, 35, N))
adr_base = np.clip(adr_base, 10, 450)

stays_week = np.random.choice([0,1,2,3,4,5], size=N, p=[0.40,0.25,0.20,0.10,0.03,0.02])
stays_weekend = np.random.choice([0,1,2,3], size=N, p=[0.35,0.35,0.25,0.05])
total_nights = stays_week + stays_weekend
total_nights = np.where(total_nights == 0, 1, total_nights)
revenue = adr_base * total_nights * (1 - is_canceled)

arrival_month = np.random.choice(range(1, 13), size=N,
    p=[0.06,0.05,0.07,0.08,0.09,0.10,0.11,0.12,0.10,0.09,0.07,0.06])
arrival_year = np.random.choice([2015, 2016, 2017], size=N, p=[0.30, 0.40, 0.30])

deposit_types = np.random.choice(['No Deposit', 'Non Refund', 'Refundable'],
                                  size=N, p=[0.875, 0.115, 0.010])
distribution_channels = np.random.choice(['TA/TO', 'Direct', 'Corporate', 'GDS'],
                                          size=N, p=[0.82, 0.10, 0.06, 0.02])
market_segments = np.random.choice(['Online TA', 'Offline TA/TO', 'Direct', 'Corporate',
                                    'Groups', 'Complementary', 'Aviation'],
                                   size=N, p=[0.47, 0.20, 0.11, 0.09, 0.08, 0.03, 0.02])

df = pd.DataFrame({
    'hotel': hotels,
    'is_canceled': is_canceled,
    'lead_time': lead_times,
    'arrival_date_year': arrival_year,
    'arrival_date_month': arrival_month,
    'stays_in_weekend_nights': stays_weekend,
    'stays_in_week_nights': stays_week,
    'customer_type': customer_types,
    'country': countries,
    'adr': adr_base.round(2),
    'total_nights': total_nights,
    'revenue': revenue.round(2),
    'deposit_type': deposit_types,
    'distribution_channel': distribution_channels,
    'market_segment': market_segments,
})

out = os.path.join(os.path.dirname(__file__), 'hotel_bookings.csv')
df.to_csv(out, index=False)
print(f"Dataset saved: {out}  |  Shape: {df.shape}")

# Load into SQLite
db_path = os.path.join(os.path.dirname(__file__), 'hotel_bookings.db')
conn = sqlite3.connect(db_path)
df.to_sql('bookings', conn, if_exists='replace', index=False)
conn.close()
print(f"SQLite DB saved: {db_path}")
