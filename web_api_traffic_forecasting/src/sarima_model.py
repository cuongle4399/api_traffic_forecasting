"""
Box-Jenkins SARIMA Modeling and Diagnostic Checking Module.
Implements hyperparameter grid search, SARIMAX model estimation,
information criteria ranking (AIC, BIC), and full residual diagnostics.
"""

import os
import itertools
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf

def grid_search_sarima(train_series, s=24, d=1, D=1, p_vals=(0, 1, 2), q_vals=(0, 1, 2), P_vals=(0, 1), Q_vals=(0, 1)):
    """
    Evaluates candidate SARIMA(p,d,q)x(P,D,Q)_s models using AIC, AICc, and BIC.
    """
    candidates = [
        (1, 1, 1, 1, 1, 1),
        (1, 1, 1, 0, 1, 1),
        (1, 1, 1, 1, 1, 0),
        (0, 1, 1, 1, 1, 1),
        (1, 1, 0, 1, 1, 1),
        (2, 1, 1, 1, 1, 1),
        (1, 1, 2, 1, 1, 1),
        (0, 1, 1, 0, 1, 1),
        (1, 1, 0, 1, 1, 0),
        (2, 1, 0, 1, 1, 1),
        (0, 1, 2, 0, 1, 1),
        (2, 1, 2, 1, 1, 1),
    ]
    results = []
    
    print(f"Beginning Box-Jenkins Grid Search over {len(candidates)} candidate models (s={s})...")
    
    for (p, d_, q, P, D_, Q) in candidates:
        order = (p, d_, q)
        seasonal_order = (P, D_, Q, s)
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                model = SARIMAX(
                    train_series,
                    order=order,
                    seasonal_order=seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )
                fit_res = model.fit(disp=False, maxiter=40)
                
            aic = fit_res.aic
            bic = fit_res.bic
            hqic = fit_res.hqic
            results.append({
                "order": order,
                "seasonal_order": seasonal_order,
                "model_str": f"SARIMA({p},{d_},{q})({P},{D_},{Q})[{s}]",
                "AIC": round(aic, 2),
                "BIC": round(bic, 2),
                "HQIC": round(hqic, 2),
                "Log-Likelihood": round(fit_res.llf, 2),
                "fit_res": fit_res
            })
            print(f"  -> SARIMA({p},{d_},{q})({P},{D_},{Q})[{s}]: AIC={aic:.2f}, BIC={bic:.2f}")
        except Exception as e:
            print(f"  Failed for SARIMA({p},{d_},{q})({P},{D_},{Q})[{s}]: {e}")
            continue
            
    df_results = pd.DataFrame(results).sort_values("AIC").reset_index(drop=True)
    best_candidate = df_results.iloc[0]
    print(f"\nOptimal Model Selected: {best_candidate['model_str']} with AIC={best_candidate['AIC']}")
    return df_results, best_candidate["fit_res"]

def fit_sarima_model(train_series, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24)):
    """
    Directly fits the specified SARIMA model.
    """
    print(f"Fitting SARIMA{order}x{seasonal_order} on {len(train_series)} training observations...")
    model = SARIMAX(
        train_series,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    fitted_model = model.fit(disp=False, maxiter=50)
    print(fitted_model.summary().tables[0])
    return fitted_model

def evaluate_residual_diagnostics(fitted_model, output_path="web_api_traffic_forecasting/figures/05_sarima_diagnostic_plots.png"):
    """
    Computes 4-panel Box-Jenkins residual diagnostics:
    1. Standardized Residuals
    2. Histogram + Kernel Density Estimate vs N(0,1)
    3. Normal Q-Q Plot
    4. Residual Autocorrelation (Correlogram)
    And executes the Ljung-Box Portmanteau Test.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    resid = fitted_model.resid
    std_resid = (resid - np.mean(resid)) / np.std(resid)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), dpi=300)
    
    # 1. Standardized Residuals
    axes[0, 0].plot(std_resid.index, std_resid, color="#1f77b4", linewidth=0.8)
    axes[0, 0].axhline(0, color="black", linestyle="--", linewidth=0.8)
    axes[0, 0].axhline(3, color="red", linestyle=":", linewidth=0.8, alpha=0.7)
    axes[0, 0].axhline(-3, color="red", linestyle=":", linewidth=0.8, alpha=0.7)
    axes[0, 0].set_title("Standardized Residuals", fontsize=11, fontweight="bold")
    axes[0, 0].set_ylabel("Standardized Errors")
    axes[0, 0].grid(True, linestyle="--", alpha=0.5)
    
    # 2. Histogram + KDE vs N(0, 1)
    x_axis = np.linspace(-4, 4, 200)
    axes[0, 1].hist(std_resid, bins=35, density=True, color="#aec7e8", edgecolor="white", alpha=0.7, label="Residuals")
    kde = stats.gaussian_kde(std_resid.dropna())
    axes[0, 1].plot(x_axis, kde(x_axis), color="#d62728", linewidth=1.5, label="KDE Fit")
    axes[0, 1].plot(x_axis, stats.norm.pdf(x_axis, 0, 1), color="#2ca02c", linestyle="--", linewidth=1.5, label="N(0, 1) Standard")
    axes[0, 1].set_title("Histogram & Density Estimate vs Normal", fontsize=11, fontweight="bold")
    axes[0, 1].set_ylabel("Density")
    axes[0, 1].legend(loc="upper right", frameon=True)
    axes[0, 1].grid(True, linestyle="--", alpha=0.5)
    
    # 3. Normal Q-Q Plot
    stats.probplot(std_resid.dropna(), dist="norm", plot=axes[1, 0])
    axes[1, 0].get_lines()[0].set_color("#1f77b4")
    axes[1, 0].get_lines()[0].set_markersize(4)
    axes[1, 0].get_lines()[1].set_color("#d62728")
    axes[1, 0].get_lines()[1].set_linewidth(1.5)
    axes[1, 0].set_title("Normal Q-Q Plot", fontsize=11, fontweight="bold")
    axes[1, 0].grid(True, linestyle="--", alpha=0.5)
    
    # 4. Correlogram (ACF of Residuals)
    plot_acf(resid.dropna(), lags=36, ax=axes[1, 1], color="#1f77b4", vlines_kwargs={"linewidth": 1.2})
    axes[1, 1].set_title("Residual Autocorrelation (Correlogram)", fontsize=11, fontweight="bold")
    axes[1, 1].set_xlabel("Lag (Hours)")
    axes[1, 1].set_ylabel("Autocorrelation")
    axes[1, 1].grid(True, linestyle="--", alpha=0.5)
    
    plt.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
    
    # Ljung-Box Test up to lag 24
    lb_df = acorr_ljungbox(resid.dropna(), lags=[6, 12, 18, 24, 36], return_df=True)
    print("\nLjung-Box Portmanteau Test for Residual Independence:")
    print(lb_df)
    
    return lb_df
