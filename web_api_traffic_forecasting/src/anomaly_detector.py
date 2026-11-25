"""
Statistical and Residual-Based Anomaly Detection Module.
Detects unexpected traffic spikes (DDoS, Bot scraping) and drops (outages, network partitions)
using dynamic prediction intervals and residual Z-score thresholding.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support

def detect_anomalies(forecast_df, threshold_sigma=3.0):
    """
    Identifies anomalies where actual observations breach dynamic prediction limits.
    threshold_sigma: 3.0 represents a 99.7% confidence envelope.
    """
    df = forecast_df.copy()
    
    # Calculate forecast residuals and normalized errors
    df["residual"] = df["actual"] - df["forecast"]
    
    # We use upper_ci_99 and lower_ci_99 or dynamic residual std
    # In addition, calculate rolling / global standard deviation of residuals under normal conditions
    sigma_resid = np.std(df["residual"])
    mean_resid = np.mean(df["residual"])
    
    # Standard dynamic bounds
    df["dyn_upper"] = df["forecast"] + threshold_sigma * sigma_resid
    df["dyn_lower"] = np.maximum(0, df["forecast"] - threshold_sigma * sigma_resid)
    
    # Flag spikes and drops
    df["detected_spike"] = (df["actual"] > df["dyn_upper"]).astype(int)
    df["detected_drop"] = (df["actual"] < df["dyn_lower"]).astype(int)
    df["detected_anomaly"] = ((df["detected_spike"] == 1) | (df["detected_drop"] == 1)).astype(int)
    
    df["detection_label"] = "Normal"
    df.loc[df["detected_spike"] == 1, "detection_label"] = "Detected_Spike"
    df.loc[df["detected_drop"] == 1, "detection_label"] = "Detected_Drop"
    
    return df

def evaluate_anomaly_detection(detected_df, ground_truth_df):
    """
    Evaluates detection metrics against ground-truth labels.
    """
    y_true = ground_truth_df["is_anomaly"].values
    y_pred = detected_df["detected_anomaly"].values
    
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    prec, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="binary")
    acc = (tp + tn) / (tp + tn + fp + fn)
    
    report = {
        "True_Positives (TP)": int(tp),
        "False_Positives (FP)": int(fp),
        "True_Negatives (TN)": int(tn),
        "False_Negatives (FN)": int(fn),
        "Precision": float(prec),
        "Recall": float(recall),
        "F1_Score": float(f1),
        "Accuracy": float(acc)
    }
    
    print("\nAnomaly Detection Evaluation Matrix:")
    for k, v in report.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")
            
    return report

def plot_anomaly_detection(detected_df, ground_truth_df, output_path="web_api_traffic_forecasting/figures/07_anomaly_detection_results.png"):
    """
    Generates rich 2-panel anomaly detection figure:
    1. Actual Traffic vs Dynamic 3-sigma Bounds with flagged anomalies
    2. Residual Error Series with +/- 3-sigma threshold lines
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(14, 9), sharex=True, dpi=300)
    
    # Panel 1: Time Series with Dynamic Threshold Bounds
    axes[0].plot(detected_df.index, detected_df["actual"], color="#1f77b4", linewidth=1.1, label="Actual Traffic", alpha=0.9)
    axes[0].plot(detected_df.index, detected_df["forecast"], color="#2ca02c", linestyle="--", linewidth=1.2, label="SARIMA Expected Baseline")
    axes[0].plot(detected_df.index, detected_df["dyn_upper"], color="#ff7f0e", linestyle=":", linewidth=1.2, label=r"Dynamic Upper Bound ($\hat{y}_t + 3\sigma$)")
    axes[0].plot(detected_df.index, detected_df["dyn_lower"], color="#ff7f0e", linestyle=":", linewidth=1.2, label=r"Dynamic Lower Bound ($\hat{y}_t - 3\sigma$)")
    
    # Mark detected anomalies
    spikes = detected_df[detected_df["detected_spike"] == 1]
    drops = detected_df[detected_df["detected_drop"] == 1]
    
    if len(spikes) > 0:
        axes[0].scatter(spikes.index, spikes["actual"], color="#d62728", s=65, zorder=6, marker="^", label="Detected Spike (DDoS/Flash)", edgecolors="black")
    if len(drops) > 0:
        axes[0].scatter(drops.index, drops["actual"], color="#9467bd", s=65, zorder=6, marker="v", label="Detected Drop (Outage/Crash)", edgecolors="black")
        
    axes[0].set_title("Web Application API Anomaly Detection via Dynamic SARIMA Prediction Bounds", fontsize=12, fontweight="bold")
    axes[0].set_ylabel("Request Volume (Req / Hour)", fontsize=10)
    axes[0].legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    axes[0].grid(True, linestyle="--", alpha=0.5)
    
    # Panel 2: Residual Error Process
    resid = detected_df["residual"]
    sigma_resid = np.std(resid)
    axes[1].plot(detected_df.index, resid, color="#333333", linewidth=1.0, label=r"Residual Error $e_t = y_t - \hat{y}_t$")
    axes[1].axhline(0, color="black", linestyle="-", linewidth=0.8)
    axes[1].axhline(3 * sigma_resid, color="red", linestyle="--", linewidth=1.2, label=r"Upper Anomaly Threshold ($+3\sigma$)")
    axes[1].axhline(-3 * sigma_resid, color="red", linestyle="--", linewidth=1.2, label=r"Lower Anomaly Threshold ($-3\sigma$)")
    
    # Fill normal zone
    axes[1].fill_between(detected_df.index, -3 * sigma_resid, 3 * sigma_resid, color="#d3d3d3", alpha=0.3, label="Normal Operation Zone (99.7%)")
    
    axes[1].set_title(r"Standardized Prediction Residuals and $\pm 3\sigma$ Thresholding", fontsize=12, fontweight="bold")
    axes[1].set_ylabel("Error (Req / Hour)", fontsize=10)
    axes[1].set_xlabel("Timestamp", fontsize=10)
    axes[1].legend(loc="upper left", frameon=True, facecolor="white", framealpha=0.9)
    axes[1].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
