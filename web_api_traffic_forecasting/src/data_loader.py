"""
Data Loader and Generator Module for Web Application API Request Volume Forecasting.
Generates and loads hourly API traffic data with realistic diurnal and weekly cycles,
trend, stochastic noise, and ground-truth anomaly events.
"""

import os
import numpy as np
import pandas as pd

def generate_api_traffic_dataset(
    start_date="2026-08-01 00:00:00",
    days=90,
    random_seed=42,
    output_path="web_api_traffic_forecasting/data/api_traffic_data.csv"
):
    """
    Generates a 90-day hourly web API traffic dataset (2160 observations).
    Includes diurnal cycles (s=24), weekly seasonality, positive trend,
    and distinct ground-truth anomaly events.
    """
    np.random.seed(random_seed)
    n_hours = days * 24
    timestamps = pd.date_range(start=start_date, periods=n_hours, freq="h")
    
    # 1. Base trend: steady growth reflecting user adoption
    t = np.arange(n_hours)
    base_load = 5000.0
    trend = 0.85 * t  # Linear growth
    
    # 2. Daily Seasonality (Diurnal cycle, period = 24 hours)
    # Peak at 14:00 (work) and 20:00 (evening leisure), trough at 04:00
    hour = timestamps.hour.values
    daily_pattern = (
        1800 * np.sin(2 * np.pi * (hour - 8) / 24)
        + 600 * np.sin(4 * np.pi * (hour - 8) / 24)
    )
    
    # 3. Weekly Seasonality (Weekend effect: ~75% of weekday traffic)
    day_of_week = timestamps.dayofweek.values  # 0=Monday, 6=Sunday
    weekly_mult = np.where(day_of_week < 5, 1.0, 0.75)
    
    # 4. Stochastic Gaussian White Noise
    noise = np.random.normal(loc=0.0, scale=320.0, size=n_hours)
    
    # Combine baseline signal
    traffic = (base_load + trend + daily_pattern) * weekly_mult + noise
    
    # 5. Realistic Latency and 5xx Error Counts
    # Under normal conditions: latency ~45ms, 5xx ~ 2-5
    latency = 42.0 + (traffic / 250.0) + np.random.normal(0, 3.5, size=n_hours)
    error_5xx = np.maximum(0, np.random.poisson(lam=3.0, size=n_hours))
    
    # Anomaly labels
    is_anomaly = np.zeros(n_hours, dtype=int)
    anomaly_type = ["Normal"] * n_hours
    
    # 6. Inject Ground-Truth Anomaly Events (in the latter portion / test set)
    # Event 1: DDoS Attack / API Scraping Bot Flood (Day 75, hours 14-17)
    idx_ddos = np.where((timestamps >= "2026-10-14 14:00:00") & (timestamps <= "2026-10-14 17:00:00"))[0]
    traffic[idx_ddos] += np.array([12500, 18500, 16000, 11000])
    latency[idx_ddos] += np.array([180, 320, 290, 140])
    error_5xx[idx_ddos] += np.array([45, 120, 95, 30])
    is_anomaly[idx_ddos] = 1
    for i in idx_ddos:
        anomaly_type[i] = "DDoS_Spike"
        
    # Event 2: Upstream Gateway Outage / Database Breakdown (Day 82, hours 02-05)
    idx_outage = np.where((timestamps >= "2026-10-21 02:00:00") & (timestamps <= "2026-10-21 05:00:00"))[0]
    traffic[idx_outage] = np.maximum(50, traffic[idx_outage] * 0.12)
    latency[idx_outage] = 5.0  # Fast failing connections
    error_5xx[idx_outage] += np.array([80, 150, 130, 40])
    is_anomaly[idx_outage] = 1
    for i in idx_outage:
        anomaly_type[i] = "Outage_Drop"
        
    # Event 3: Flash Crowd / E-Commerce Midnight Promotion (Day 87, hours 20-22)
    idx_flash = np.where((timestamps >= "2026-10-26 20:00:00") & (timestamps <= "2026-10-26 22:00:00"))[0]
    traffic[idx_flash] += np.array([9200, 11500, 8400])
    latency[idx_flash] += np.array([65, 85, 50])
    is_anomaly[idx_flash] = 1
    for i in idx_flash:
        anomaly_type[i] = "Flash_Crowd"
        
    # Ensure traffic is non-negative and rounded to integer requests
    traffic = np.maximum(0, np.round(traffic)).astype(int)
    latency = np.round(latency, 2)
    
    df = pd.DataFrame({
        "timestamp": timestamps,
        "request_count": traffic,
        "latency_ms": latency,
        "error_5xx": error_5xx,
        "is_anomaly": is_anomaly,
        "anomaly_type": anomaly_type
    })
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created and saved to: {output_path} ({len(df)} records)")
    return df

def load_data(file_path="web_api_traffic_forecasting/data/api_traffic_data.csv", train_ratio=0.80):
    """
    Loads dataset and splits into chronological Train and Test sets.
    """
    if not os.path.exists(file_path):
        generate_api_traffic_dataset(output_path=file_path)
        
    df = pd.read_csv(file_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    
    # Train-test split (Chronological, no shuffling for time series)
    split_idx = int(len(df) * train_ratio)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    
    print(f"Data Loaded: Total={len(df)} samples, Train={len(train_df)} ({train_ratio*100:.0f}%), Test={len(test_df)} ({(1-train_ratio)*100:.0f}%)")
    return df, train_df, test_df

if __name__ == "__main__":
    generate_api_traffic_dataset()
