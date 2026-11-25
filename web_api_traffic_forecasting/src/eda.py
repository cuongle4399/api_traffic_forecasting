"""
Exploratory Data Analysis (EDA) and Stationarity Testing Module.
Performs descriptive statistics, ADF/KPSS unit root testing,
seasonal decomposition, and autocorrelation (ACF/PACF) diagnostics.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Publication-grade plotting aesthetics
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

def perform_descriptive_stats(series, name="API Requests"):
    """
    Computes rigorous descriptive statistics.
    """
    stats = {
        "Metric": [
            "Count", "Mean", "Std Dev", "Min", "25th Percentile (Q1)",
            "Median (Q2)", "75th Percentile (Q3)", "Max", "Skewness", "Kurtosis"
        ],
        "Value": [
            len(series),
            float(np.mean(series)),
            float(np.std(series)),
            float(np.min(series)),
            float(np.percentile(series, 25)),
            float(np.median(series)),
            float(np.percentile(series, 75)),
            float(np.max(series)),
            float(pd.Series(series).skew()),
            float(pd.Series(series).kurt())
        ]
    }
    df_stats = pd.DataFrame(stats)
    return df_stats

def test_stationarity_adf(series, name="Series"):
    """
    Augmented Dickey-Fuller (ADF) Test.
    H0: The series has a unit root (Non-Stationary).
    H1: The series has no unit root (Stationary).
    """
    result = adfuller(series.dropna(), autolag="AIC")
    res_dict = {
        "Test": "Augmented Dickey-Fuller (ADF)",
        "Series": name,
        "ADF Statistic": result[0],
        "p-value": result[1],
        "Used Lags": result[2],
        "Observations": result[3],
        "Critical Value (1%)": result[4]["1%"],
        "Critical Value (5%)": result[4]["5%"],
        "Critical Value (10%)": result[4]["10%"],
        "Is Stationary (p < 0.05)": result[1] < 0.05
    }
    return res_dict

def test_stationarity_kpss(series, name="Series", regression="c"):
    """
    KPSS Test.
    H0: The process is trend-stationary (or level-stationary).
    H1: The process has a unit root (Non-Stationary).
    """
    # suppress warnings for p-value out of bounds
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = kpss(series.dropna(), regression=regression, nlags="auto")
    res_dict = {
        "Test": "KPSS Test",
        "Series": name,
        "KPSS Statistic": result[0],
        "p-value": result[1],
        "Lags": result[2],
        "Critical Value (1%)": result[3]["1%"],
        "Critical Value (5%)": result[3]["5%"],
        "Critical Value (10%)": result[3]["10%"],
        "Is Stationary (p >= 0.05)": result[1] >= 0.05
    }
    return res_dict

def plot_raw_traffic(df, output_path="web_api_traffic_forecasting/figures/01_raw_traffic_series.png"):
    """
    Plots the full API request volume series with weekday/weekend nuance and anomaly highlights.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(13, 5), dpi=300)
    
    ax.plot(df.index, df["request_count"], color="#1f77b4", linewidth=1.1, label="Hourly API Request Volume")
    
    # Highlight anomalies in ground truth
    anom = df[df["is_anomaly"] == 1]
    if len(anom) > 0:
        ax.scatter(anom.index, anom["request_count"], color="#d62728", s=45, zorder=5, label="Ground-Truth Anomalies", edgecolors="black", linewidth=0.6)
        
    ax.set_title("Web Application API Request Volume (90-Day Hourly Log)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Timestamp", fontsize=11, labelpad=8)
    ax.set_ylabel("Request Volume (Req / Hour)", fontsize=11, labelpad=8)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")

def plot_seasonal_decomposition(series, period=24, output_path="web_api_traffic_forecasting/figures/02_seasonal_decomposition.png"):
    """
    Classical additive decomposition: Y_t = Trend_t + Seasonal_t + Residual_t.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    decomp = seasonal_decompose(series, model="additive", period=period)
    
    fig, axes = plt.subplots(4, 1, figsize=(13, 9), sharex=True, dpi=300)
    
    axes[0].plot(decomp.observed, color="#1f77b4", linewidth=1)
    axes[0].set_ylabel("Observed", fontsize=10, fontweight="bold")
    axes[0].set_title(f"Time Series Decomposition (Additive, Period s={period} Hours)", fontsize=12, fontweight="bold")
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    axes[1].plot(decomp.trend, color="#ff7f0e", linewidth=1.3)
    axes[1].set_ylabel("Trend", fontsize=10, fontweight="bold")
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    # For seasonal, plot first 7 days for clear visibility
    axes[2].plot(decomp.seasonal, color="#2ca02c", linewidth=1)
    axes[2].set_ylabel("Seasonal (Diurnal)", fontsize=10, fontweight="bold")
    axes[2].grid(True, linestyle="--", alpha=0.5)
    
    axes[3].scatter(decomp.resid.index, decomp.resid, color="#7f7f7f", s=8, alpha=0.7)
    axes[3].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[3].set_ylabel("Residuals", fontsize=10, fontweight="bold")
    axes[3].set_xlabel("Timestamp", fontsize=10)
    axes[3].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
    return decomp

def plot_differencing_analysis(series, period=24, output_path="web_api_traffic_forecasting/figures/03_stationarity_differencing.png"):
    """
    Compares Raw Series vs First Differencing (d=1) vs Seasonal Differencing (d=1, D=1, s=24).
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    diff_regular = series.diff().dropna()
    diff_seasonal = diff_regular.diff(period).dropna()
    
    fig, axes = plt.subplots(3, 1, figsize=(13, 8), dpi=300)
    
    axes[0].plot(series, color="#1f77b4", linewidth=1)
    axes[0].set_title("Original Series Y_t (Non-Stationary with Trend & Seasonality)", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Y_t", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    axes[1].plot(diff_regular, color="#ff7f0e", linewidth=0.9)
    axes[1].set_title(r"First Regular Difference $\nabla Y_t = Y_t - Y_{t-1}$ (Detrended)", fontsize=11, fontweight="bold")
    axes[1].set_ylabel(r"$\nabla Y_t$", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    axes[2].plot(diff_seasonal, color="#2ca02c", linewidth=0.9)
    axes[2].set_title(r"First Regular & Seasonal Difference $\nabla \nabla_{24} Y_t = (1-B)(1-B^{24}) Y_t$ (Stationary)", fontsize=11, fontweight="bold")
    axes[2].set_ylabel(r"$\nabla \nabla_{24} Y_t$", fontsize=10)
    axes[2].set_xlabel("Timestamp", fontsize=10)
    axes[2].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
    return diff_seasonal

def plot_acf_pacf_analysis(series_diff, lags=50, output_path="web_api_traffic_forecasting/figures/04_acf_pacf_analysis.png"):
    """
    Plots Autocorrelation Function (ACF) and Partial Autocorrelation Function (PACF)
    for model identification of (p, d, q) and (P, D, Q)_s.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(13, 7), dpi=300)
    
    plot_acf(series_diff, lags=lags, ax=axes[0], color="#1f77b4", vlines_kwargs={"linewidth": 1.2})
    axes[0].set_title(r"Sample Autocorrelation Function (ACF) of Differenced Series $(1-B)(1-B^{24})Y_t$", fontsize=11, fontweight="bold")
    axes[0].set_ylabel("Autocorrelation", fontsize=10)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    plot_pacf(series_diff, lags=lags, ax=axes[1], color="#d62728", method="ywm", vlines_kwargs={"linewidth": 1.2})
    axes[1].set_title(r"Sample Partial Autocorrelation Function (PACF) of Differenced Series $(1-B)(1-B^{24})Y_t$", fontsize=11, fontweight="bold")
    axes[1].set_ylabel("Partial Autocorrelation", fontsize=10)
    axes[1].set_xlabel("Lag (Hours)", fontsize=10)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
