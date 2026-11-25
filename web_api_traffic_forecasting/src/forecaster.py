"""
Forecasting and Performance Evaluation Module.
Generates multi-step and rolling out-of-sample forecasts, prediction intervals,
and calculates benchmark evaluation metrics (RMSE, MAE, MAPE, R2).
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def calculate_mape(y_true, y_pred):
    """
    Mean Absolute Percentage Error.
    """
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # Avoid division by zero
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

def compute_metrics(y_true, y_pred):
    """
    Computes all standard time series regression metrics.
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = calculate_mape(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    metrics = {
        "RMSE": float(rmse),
        "MAE": float(mae),
        "MAPE (%)": float(mape),
        "R2": float(r2)
    }
    return metrics

def generate_forecast(fitted_model, test_df, full_df=None):
    """
    Generates out-of-sample forecast for the test set along with 95% confidence intervals.
    Uses get_forecast for rigorous statespace prediction intervals.
    """
    steps = len(test_df)
    forecast_res = fitted_model.get_forecast(steps=steps)
    
    mean_forecast = forecast_res.predicted_mean
    mean_forecast.index = test_df.index
    
    conf_int = forecast_res.conf_int(alpha=0.05)  # 95% Confidence Interval
    conf_int.index = test_df.index
    conf_int.columns = ["lower_ci_95", "upper_ci_95"]
    conf_int["lower_ci_95"] = np.maximum(0, conf_int["lower_ci_95"])  # Traffic cannot be negative
    
    # 99.7% (3-sigma) interval
    conf_int_99 = forecast_res.conf_int(alpha=0.003)
    conf_int["lower_ci_99"] = np.maximum(0, conf_int_99.iloc[:, 0].values)
    conf_int["upper_ci_99"] = conf_int_99.iloc[:, 1].values
    
    forecast_df = pd.DataFrame({
        "actual": test_df["request_count"],
        "forecast": mean_forecast,
        "lower_ci_95": conf_int["lower_ci_95"],
        "upper_ci_95": conf_int["upper_ci_95"],
        "lower_ci_99": conf_int["lower_ci_99"],
        "upper_ci_99": conf_int["upper_ci_99"]
    }, index=test_df.index)
    
    return forecast_df

def plot_forecast_evaluation(train_df, test_df, forecast_df, output_path="web_api_traffic_forecasting/figures/06_forecast_vs_actual.png"):
    """
    Visualizes Actual vs Forecasted values on the test set with 95% confidence bounds.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 6), dpi=300)
    
    # Show last 7 days of training for seamless context
    train_slice = train_df.iloc[-168:]
    ax.plot(train_slice.index, train_slice["request_count"], color="#7f7f7f", linewidth=1.1, label="Historical Training (Last 7 Days)", alpha=0.8)
    
    # Actual test series
    ax.plot(test_df.index, test_df["request_count"], color="#1f77b4", linewidth=1.2, label="Actual API Traffic (Test Set)")
    
    # Forecast
    ax.plot(forecast_df.index, forecast_df["forecast"], color="#d62728", linestyle="--", linewidth=1.4, label="SARIMA Forecast Point Estimate")
    
    # 95% Confidence Band
    ax.fill_between(
        forecast_df.index,
        forecast_df["lower_ci_95"],
        forecast_df["upper_ci_95"],
        color="#ff9896",
        alpha=0.35,
        label="95% Confidence Interval"
    )
    
    ax.set_title("SARIMA Model Forecast vs Actual API Traffic (Out-of-Sample Test Set)", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Timestamp", fontsize=11, labelpad=8)
    ax.set_ylabel("Request Volume (Req / Hour)", fontsize=11, labelpad=8)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
