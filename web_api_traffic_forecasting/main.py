"""
Main Orchestration Pipeline for Web Application API Request Volume Forecasting
and Anomaly Detection Using Box-Jenkins SARIMA Methodology.

Author: Le Quoc Cuong (MSSV: 4651050031)
University: Quy Nhon University - Faculty of Information Technology
Course: Time Series Forecasting (Du doan chuoi thoi gian)
"""

import os
import sys
import json
import numpy as np
import pandas as pd

# Anchor paths to this project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.data_loader import generate_api_traffic_dataset, load_data
from src.eda import (
    perform_descriptive_stats,
    test_stationarity_adf,
    test_stationarity_kpss,
    plot_raw_traffic,
    plot_seasonal_decomposition,
    plot_differencing_analysis,
    plot_acf_pacf_analysis
)
from src.sarima_model import (
    grid_search_sarima,
    fit_sarima_model,
    evaluate_residual_diagnostics
)
from src.forecaster import (
    compute_metrics,
    generate_forecast,
    plot_forecast_evaluation
)
from src.anomaly_detector import (
    detect_anomalies,
    evaluate_anomaly_detection,
    plot_anomaly_detection
)
from evaluate_baseline import run_baseline_benchmarks

def run_pipeline():
    print("=" * 80)
    print("WEB APPLICATION API REQUEST VOLUME FORECASTING & ANOMALY DETECTION")
    print("METHODOLOGY: BOX-JENKINS SARIMA")
    print("AUTHOR: LE QUOC CUONG | MSSV: 4651050031 | QUY NHON UNIVERSITY")
    print("=" * 80)
    
    data_dir = os.path.join(BASE_DIR, "data")
    output_dir = os.path.join(BASE_DIR, "output")
    figures_dir = os.path.join(BASE_DIR, "figures")
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # STEP 1: Data Generation & Loading
    # -------------------------------------------------------------
    print("\n[STEP 1] Loading Dataset...")
    csv_path = os.path.join(data_dir, "api_traffic_data.csv")
    full_df, train_df, test_df = load_data(
        file_path=csv_path,
        train_ratio=0.80
    )
    
    # -------------------------------------------------------------
    # STEP 2: Exploratory Data Analysis (EDA) & Stationarity Tests
    # -------------------------------------------------------------
    print("\n[STEP 2] Performing Descriptive Statistics & Stationarity Analysis...")
    df_desc = perform_descriptive_stats(train_df["request_count"], name="Train API Requests")
    df_desc.to_csv(os.path.join(output_dir, "01_descriptive_stats.csv"), index=False)
    print(df_desc.to_string(index=False))
    
    # ADF and KPSS on Raw Series
    adf_raw = test_stationarity_adf(train_df["request_count"], name="Raw Series Y_t")
    kpss_raw = test_stationarity_kpss(train_df["request_count"], name="Raw Series Y_t")
    
    # Visualizations: Raw series & Seasonal Decomposition
    plot_raw_traffic(full_df, output_path=os.path.join(figures_dir, "01_raw_traffic_series.png"))
    plot_seasonal_decomposition(train_df["request_count"], period=24, output_path=os.path.join(figures_dir, "02_seasonal_decomposition.png"))
    
    # Differencing: regular d=1 and seasonal D=1 with s=24
    diff_seasonal = plot_differencing_analysis(train_df["request_count"], period=24, output_path=os.path.join(figures_dir, "03_stationarity_differencing.png"))
    
    # ADF and KPSS on Differenced Series
    adf_diff = test_stationarity_adf(diff_seasonal, name="Differenced Series (1-B)(1-B^24)Y_t")
    kpss_diff = test_stationarity_kpss(diff_seasonal, name="Differenced Series (1-B)(1-B^24)Y_t")
    
    df_stationarity = pd.DataFrame([adf_raw, kpss_raw, adf_diff, kpss_diff])
    df_stationarity.to_csv(os.path.join(output_dir, "02_stationarity_tests.csv"), index=False)
    print("\nStationarity Tests Summary:")
    print(df_stationarity[["Test", "Series", "ADF Statistic", "KPSS Statistic", "p-value"]].to_string(index=False))
    
    # ACF & PACF Plots
    plot_acf_pacf_analysis(diff_seasonal, lags=48, output_path=os.path.join(figures_dir, "04_acf_pacf_analysis.png"))
    
    # -------------------------------------------------------------
    # STEP 3: Box-Jenkins SARIMA Model Identification & Estimation
    # -------------------------------------------------------------
    print("\n[STEP 3] SARIMA Model Identification, Estimation & Parameter Selection...")
    # Perform Grid Search over selected representative candidate combinations for s=24
    # Candidates targeting diurnal 24-hr cycle
    grid_results, best_model = grid_search_sarima(
        train_df["request_count"],
        s=24,
        d=1,
        D=1,
        p_vals=(0, 1, 2),
        q_vals=(0, 1, 2),
        P_vals=(0, 1),
        Q_vals=(0, 1)
    )
    
    # Drop fit_res object before exporting to CSV
    grid_results_csv = grid_results.drop(columns=["fit_res"])
    grid_results_csv.to_csv(os.path.join(output_dir, "03_grid_search_sarima.csv"), index=False)
    
    # -------------------------------------------------------------
    # STEP 4: Diagnostic Checking (Residual Analysis & Ljung-Box)
    # -------------------------------------------------------------
    print("\n[STEP 4] Diagnostic Checking: Residual Analysis & Ljung-Box Test...")
    lb_df = evaluate_residual_diagnostics(
        best_model,
        output_path=os.path.join(figures_dir, "05_sarima_diagnostic_plots.png")
    )
    lb_df.to_csv(os.path.join(output_dir, "04_ljung_box_test.csv"))
    
    # -------------------------------------------------------------
    # STEP 5: Forecasting on Test Set
    # -------------------------------------------------------------
    print("\n[STEP 5] Generating Multi-Step Ahead Out-of-Sample Forecasts...")
    forecast_df = generate_forecast(best_model, test_df)
    forecast_df.to_csv(os.path.join(output_dir, "05_forecast_results.csv"))
    
    sarima_metrics = compute_metrics(test_df["request_count"], forecast_df["forecast"])
    print(f"\nSARIMA Evaluation on Test Set: RMSE={sarima_metrics['RMSE']:.2f}, MAE={sarima_metrics['MAE']:.2f}, MAPE={sarima_metrics['MAPE (%)']:.2f}%, R2={sarima_metrics['R2']:.4f}")
    
    plot_forecast_evaluation(train_df, test_df, forecast_df, output_path=os.path.join(figures_dir, "06_forecast_vs_actual.png"))
    
    # -------------------------------------------------------------
    # STEP 6: Anomaly Detection via Dynamic Statistical Thresholds
    # -------------------------------------------------------------
    print("\n[STEP 6] Residual Anomaly Detection & Classification Evaluation...")
    detected_df = detect_anomalies(forecast_df, threshold_sigma=3.0)
    detected_df.to_csv(os.path.join(output_dir, "06_detected_anomalies.csv"))
    
    anomaly_metrics = evaluate_anomaly_detection(detected_df, test_df)
    pd.DataFrame([anomaly_metrics]).to_csv(os.path.join(output_dir, "07_anomaly_metrics.csv"), index=False)
    
    plot_anomaly_detection(detected_df, test_df, output_path=os.path.join(figures_dir, "07_anomaly_detection_results.png"))
    
    # -------------------------------------------------------------
    # STEP 7: Benchmark Model Comparison
    # -------------------------------------------------------------
    print("\n[STEP 7] Benchmarking Against Baseline Models...")
    df_comparison = run_baseline_benchmarks(
        train_df["request_count"],
        test_df["request_count"],
        forecast_df["forecast"].values,
        output_path=os.path.join(figures_dir, "08_model_comparison_metrics.png")
    )
    df_comparison.to_csv(os.path.join(output_dir, "08_model_benchmarks.csv"), index=False)
    
    # -------------------------------------------------------------
    # STEP 8: Export Complete Summary JSON
    # -------------------------------------------------------------
    summary_data = {
        "author": "Lê Quốc Cường",
        "student_id": "4651050031",
        "institution": "Trường Đại học Quy Nhơn",
        "faculty": "Khoa Công nghệ Thông tin",
        "course": "Dự báo chuỗi thời gian",
        "project_title": "Web Application API Request Volume Forecasting and Anomaly Detection Using Box-Jenkins SARIMA Methodology",
        "dataset": {
            "total_observations": len(full_df),
            "train_observations": len(train_df),
            "test_observations": len(test_df),
            "granularity": "Hourly (1-hour)",
            "seasonality_period": 24,
            "mean_requests": float(np.mean(full_df["request_count"])),
            "std_requests": float(np.std(full_df["request_count"]))
        },
        "stationarity": {
            "raw_adf_stat": float(adf_raw["ADF Statistic"]),
            "raw_adf_pvalue": float(adf_raw["p-value"]),
            "diff_adf_stat": float(adf_diff["ADF Statistic"]),
            "diff_adf_pvalue": float(adf_diff["p-value"])
        },
        "selected_sarima_model": {
            "order": list(grid_results.iloc[0]["order"]),
            "seasonal_order": list(grid_results.iloc[0]["seasonal_order"]),
            "model_str": str(grid_results.iloc[0]["model_str"]),
            "aic": float(grid_results.iloc[0]["AIC"]),
            "bic": float(grid_results.iloc[0]["BIC"])
        },
        "forecasting_metrics": sarima_metrics,
        "anomaly_detection_metrics": anomaly_metrics,
        "top_candidate_models": grid_results_csv.head(5).to_dict(orient="records"),
        "benchmark_comparison": df_comparison.to_dict(orient="records")
    }
    
    with open(os.path.join(output_dir, "summary_results.json"), "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4, ensure_ascii=False)
        
    print("\n" + "=" * 80)
    print("ALL PIPELINE STAGES COMPLETED SUCCESSFULLY!")
    print(f"Outputs generated in '{output_dir}' and '{figures_dir}'.")
    print("=" * 80)

if __name__ == "__main__":
    run_pipeline()
