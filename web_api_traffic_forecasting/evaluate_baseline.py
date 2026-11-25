"""
Baseline Comparison Module for Benchmarking SARIMA Performance.
Compares SARIMA against:
1. Naive Persistence (Lag 1)
2. Seasonal Naive (Lag 24)
3. Simple Moving Average (SMA-24)
4. Holt-Winters Triple Exponential Smoothing
5. Non-Seasonal ARIMA(1,1,1)
6. Proposed Box-Jenkins SARIMA(1,1,1)(1,1,1)[24]
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error

def run_baseline_benchmarks(train_series, test_series, sarima_pred, output_path="web_api_traffic_forecasting/figures/08_model_comparison_metrics.png"):
    """
    Fits and evaluates all benchmark baseline models.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    n_test = len(test_series)
    
    # 1. Naive (Lag 1)
    last_train_val = train_series.iloc[-1]
    pred_naive = np.full(n_test, last_train_val)
    
    # 2. Seasonal Naive (Lag 24)
    pred_snaive = np.tile(train_series.iloc[-24:].values, int(np.ceil(n_test / 24)))[:n_test]
    
    # 3. Simple Moving Average (SMA-24)
    sma_24 = train_series.rolling(24).mean().iloc[-1]
    pred_sma = np.full(n_test, sma_24)
    
    # 4. Holt-Winters Exponential Smoothing
    hw_model = ExponentialSmoothing(
        train_series,
        trend="add",
        seasonal="add",
        seasonal_periods=24,
        initialization_method="estimated"
    ).fit()
    pred_hw = hw_model.forecast(n_test)
    
    # 5. Non-Seasonal ARIMA(1, 1, 1)
    arima_model = ARIMA(train_series, order=(1, 1, 1)).fit()
    pred_arima = arima_model.forecast(n_test)
    
    # 6. Proposed SARIMA
    pred_sarima = sarima_pred
    
    models = {
        "Naive (Lag 1)": pred_naive,
        "Seasonal Naive (Lag 24)": pred_snaive,
        "Moving Average (SMA-24)": pred_sma,
        "ARIMA (1,1,1) [No Seasonality]": pred_arima,
        "Holt-Winters Exp Smoothing": pred_hw,
        "Proposed SARIMA (Box-Jenkins)": pred_sarima
    }
    
    y_true = test_series.values
    results = []
    for name, pred in models.items():
        pred_arr = np.array(pred)
        rmse = np.sqrt(mean_squared_error(y_true, pred_arr))
        mae = mean_absolute_error(y_true, pred_arr)
        mask = y_true != 0
        mape = np.mean(np.abs((y_true[mask] - pred_arr[mask]) / y_true[mask])) * 100
        results.append({
            "Model": name,
            "RMSE": round(rmse, 2),
            "MAE": round(mae, 2),
            "MAPE (%)": round(mape, 2)
        })
        
    df_metrics = pd.DataFrame(results).sort_values("RMSE").reset_index(drop=True)
    print("\nBenchmark Model Comparison Results:")
    print(df_metrics.to_string(index=False))
    
    # Visualization: Bar Chart of Model Metrics
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300)
    colors = ["#2ca02c" if "SARIMA" in m else "#1f77b4" for m in df_metrics["Model"]]
    
    # RMSE
    axes[0].barh(df_metrics["Model"], df_metrics["RMSE"], color=colors, edgecolor="black", height=0.6)
    axes[0].set_title("Root Mean Squared Error (RMSE)", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("RMSE (Lower is Better)")
    axes[0].grid(True, linestyle="--", alpha=0.5, axis="x")
    for i, v in enumerate(df_metrics["RMSE"]):
        axes[0].text(v + 15, i, f"{v:.1f}", va="center", fontsize=9, fontweight="bold")
        
    # MAE
    axes[1].barh(df_metrics["Model"], df_metrics["MAE"], color=colors, edgecolor="black", height=0.6)
    axes[1].set_title("Mean Absolute Error (MAE)", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("MAE (Lower is Better)")
    axes[1].grid(True, linestyle="--", alpha=0.5, axis="x")
    for i, v in enumerate(df_metrics["MAE"]):
        axes[1].text(v + 15, i, f"{v:.1f}", va="center", fontsize=9, fontweight="bold")
        
    # MAPE
    axes[2].barh(df_metrics["Model"], df_metrics["MAPE (%)"], color=colors, edgecolor="black", height=0.6)
    axes[2].set_title("Mean Absolute Percentage Error (MAPE %)", fontsize=11, fontweight="bold")
    axes[2].set_xlabel("MAPE % (Lower is Better)")
    axes[2].grid(True, linestyle="--", alpha=0.5, axis="x")
    for i, v in enumerate(df_metrics["MAPE (%)"]):
        axes[2].text(v + 0.3, i, f"{v:.2f}%", va="center", fontsize=9, fontweight="bold")
        
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
    
    return df_metrics
