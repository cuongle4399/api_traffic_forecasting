# Web Application API Request Volume Forecasting and Anomaly Detection Using Box-Jenkins SARIMA Methodology

## 📌 Thông Tin Tác Giả & Đề Tài
* **Sinh viên thực hiện**: Lê Quốc Cường
* **Mã sinh viên**: 4651050031
* **Đơn vị đào tạo**: Khoa Công nghệ Thông tin - Trường Đại học Quy Nhơn (QNU)
* **Học phần**: Dự báo chuỗi thời gian (Time Series Forecasting) / Dự đoán thời gian
* **Năm thực hiện**: 2026
* **Đề tài**: *Web Application API Request Volume Forecasting and Anomaly Detection Using Box-Jenkins SARIMA Methodology* (Dự đoán lưu lượng yêu cầu API của ứng dụng web và phát hiện bất thường bằng phương pháp Box-Jenkins SARIMA)

---

## 🎯 Mục Tiêu Dự Án
1. **Dự báo chính xác lưu lượng API (Traffic Volume Forecasting)**: Giúp kỹ sư hệ thống (DevOps/SRE) chủ động cấp phát tài nguyên tự động (Auto-scaling), tối ưu hóa chi phí hạ tầng điện toán đám mây (AWS/GCP/Azure) và đảm bảo cam kết chất lượng dịch vụ (SLA).
2. **Tuân thủ quy trình Box-Jenkins chuẩn mực**: Nhận dạng (Identification) $\rightarrow$ Ước lượng (Estimation) $\rightarrow$ Chẩn đoán kiểm định (Diagnostic Checking) $\rightarrow$ Dự báo (Forecasting).
3. **Phát hiện bất thường động (Dynamic Anomaly Detection)**: Nhận diện các sự kiện rủi ro cao như tấn công từ chối dịch vụ (DDoS), Bot cào dữ liệu (Scraping), sự cố sập cổng API (Gateway Outage/Crash) dựa trên khoảng tin cậy thống kê $\pm 3\sigma$.
4. **Đánh giá & So sánh đa mô hình**: Đối sánh SARIMA với các mô hình Baseline (Naive, Seasonal Naive, Moving Average, Holt-Winters, ARIMA).

---

## 📂 Cấu Trúc Mã Nguồn

```text
web_api_traffic_forecasting/
├── data/
│   └── api_traffic_data.csv          # Dữ liệu chuỗi thời gian lưu lượng API 90 ngày (2,160 giờ)
├── src/
│   ├── __init__.py
│   ├── data_loader.py                # Nạp, tiền xử lý và sinh tập dữ liệu chuỗi thời gian thực tế
│   ├── eda.py                        # Phân tích thống kê mô tả, kiểm định nghiệm đơn vị (ADF, KPSS), ACF/PACF
│   ├── sarima_model.py               # Tìm kiếm tham số Grid Search, khớp mô hình SARIMAX, chẩn đoán phần dư
│   ├── forecaster.py                 # Dự báo đa bước ngoài mẫu (Out-of-sample), tính toán RMSE, MAE, MAPE, R2
│   ├── anomaly_detector.py           # Phát hiện bất thường qua ngưỡng động 3-sigma, tính ma trận nhầm lẫn
│   └── visualizer.py                 # Xuất các biểu đồ trực quan hóa độ phân giải cao (300 DPI)
├── figures/                          # Toàn bộ biểu đồ xuất bản phục vụ báo cáo khoa học
│   ├── 01_raw_traffic_series.png
│   ├── 02_seasonal_decomposition.png
│   ├── 03_stationarity_differencing.png
│   ├── 04_acf_pacf_analysis.png
│   ├── 05_sarima_diagnostic_plots.png
│   ├── 06_forecast_vs_actual.png
│   ├── 07_anomaly_detection_results.png
│   └── 08_model_comparison_metrics.png
├── output/                           # Bảng số liệu thống kê định dạng CSV & JSON
│   ├── 01_descriptive_stats.csv
│   ├── 02_stationarity_tests.csv
│   ├── 03_grid_search_sarima.csv
│   ├── 04_ljung_box_test.csv
│   ├── 05_forecast_results.csv
│   ├── 06_detected_anomalies.csv
│   ├── 07_anomaly_metrics.csv
│   ├── 08_model_benchmarks.csv
│   └── summary_results.json
├── evaluate_baseline.py              # Đánh giá so sánh hiệu năng các mô hình cơ sở
├── main.py                           # Luồng thực thi toàn diện từ đầu đến cuối (End-to-End Pipeline)
├── requirements.txt                  # Danh mục các thư viện phụ thuộc
└── README.md                         # Hướng dẫn chi tiết
```

---

## 🚀 Hướng Dẫn Cài Đặt và Chạy

### 1. Cài đặt môi trường
Đảm bảo đã cài đặt Python 3.10 trở lên. Cài đặt các thư viện phụ thuộc qua terminal:
```bash
pip install -r requirements.txt
```

### 2. Chạy toàn bộ hệ thống (End-to-End Pipeline)
Chạy script chính để tự động thực hiện toàn bộ quy trình:
```bash
cd "web_api_traffic_forecasting"
python main.py
```

Toàn bộ các biểu đồ chất lượng cao và bảng kết quả thống kê sẽ được lưu vào thư mục `figures/` và `output/`.
