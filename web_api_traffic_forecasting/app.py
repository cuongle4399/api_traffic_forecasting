"""
Ứng dụng Web Đơn giản Giám sát & Dự báo Lưu lượng Web API
Phương pháp luận: Box-Jenkins SARIMA

Sinh viên thực hiện: Lê Quốc Cường (MSSV: 4651050031)
Giảng viên hướng dẫn: ThS. Lê Xuân Việt
Môn học: Dự báo chuỗi thời gian (Mã HP: 1050316)
Trường: Đại học Quy Nhơn (QNU)
GitHub: https://github.com/cuongle4399/api_traffic_forecasting
"""

import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Cấu hình trang - giao diện sáng, tối giản, thanh lịch
st.set_page_config(
    page_title="Dự báo Lưu lượng Web API - SARIMA (QNU)",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy biến giao diện sáng sủa, gọn nhẹ, dễ nhìn
st.markdown("""
<style>
    .reportview-container, .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    .main-title-box {
        background-color: #f0f4f8;
        border-left: 5px solid #0056b3;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 20px;
    }
    .main-title-box h3 {
        margin: 0;
        color: #003366;
        font-size: 22px;
        font-weight: 700;
    }
    .main-title-box p {
        margin: 5px 0 0 0;
        color: #495057;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# NẠP DỮ LIỆU
# -------------------------------------------------------------
@st.cache_data
def load_all_data():
    # 1. Dữ liệu gốc
    data_path = os.path.join(BASE_DIR, "data", "api_traffic_data.csv")
    df_raw = pd.read_csv(data_path)
    df_raw["timestamp"] = pd.to_datetime(df_raw["timestamp"])
    
    # 2. Dữ liệu dự báo
    fc_path = os.path.join(BASE_DIR, "output", "05_forecast_results.csv")
    df_fc = pd.read_csv(fc_path) if os.path.exists(fc_path) else None
    if df_fc is not None:
        df_fc["timestamp"] = pd.to_datetime(df_fc["timestamp"])
        
    # 3. Dữ liệu bất thường
    anom_path = os.path.join(BASE_DIR, "output", "06_detected_anomalies.csv")
    df_anom = pd.read_csv(anom_path) if os.path.exists(anom_path) else None
    if df_anom is not None:
        df_anom["timestamp"] = pd.to_datetime(df_anom["timestamp"])
        
    # 4. Bảng so sánh mô hình
    bench_path = os.path.join(BASE_DIR, "output", "08_model_benchmarks.csv")
    df_bench = pd.read_csv(bench_path) if os.path.exists(bench_path) else None
    
    return df_raw, df_fc, df_anom, df_bench

df_raw, df_fc, df_anom, df_bench = load_all_data()

# -------------------------------------------------------------
# THANH BÊN (SIDEBAR) ĐƠN GIẢN
# -------------------------------------------------------------
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(BASE_DIR), "extracted_logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=110)
        
    st.markdown("### 🎓 THÔNG TIN ĐỀ TÀI")
    st.markdown("""
    * **Sinh viên:** **Lê Quốc Cường**
    * **MSSV:** `4651050031`
    * **Giảng viên:** **ThS. Lê Xuân Việt**
    * **Môn học:** Dự báo chuỗi thời gian
    * **Mã học phần:** `1050316`
    * **Khoa:** Công nghệ Thông tin - ĐH Quy Nhơn
    """)
    st.markdown("---")
    st.markdown("### 🔗 KHO LƯU TRỮ GITHUB")
    st.markdown("[👉 cuongle4399/api_traffic_forecasting](https://github.com/cuongle4399/api_traffic_forecasting)")
    st.markdown("---")
    st.info("💡 **Gợi ý:** Bạn có thể dùng phím `Windows + Shift + S` chụp nhanh biểu đồ ở từng thẻ để dán vào báo cáo Word.")

# -------------------------------------------------------------
# TIÊU ĐỀ CHÍNH
# -------------------------------------------------------------
st.markdown("""
<div class="main-title-box">
    <h3>HỆ THỐNG DỰ BÁO LƯU LƯỢNG WEB API & PHÁT HIỆN BẤT THƯỜNG</h3>
    <p>Đề tài ứng dụng mô hình Box-Jenkins SARIMA(0,1,2)(0,1,1)[24] trên chuỗi dữ liệu 90 ngày (2.160 giờ)</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3 THẺ CHỈ SỐ TỔNG QUAN (METRICS)
# -------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Tổng số giờ quan sát", "2.160 giờ", "90 ngày liên tục")
col2.metric("Mô hình lựa chọn", "SARIMA(0,1,2)(0,1,1)[24]", "AIC = 25.004,03")
col3.metric("Sai số dự báo (RMSE)", "2.281,79 req/h", "MAPE: 24,42%")
col4.metric("Độ chuẩn xác cảnh báo", "100%", "0 cảnh báo sai")

st.markdown("---")

# -------------------------------------------------------------
# 3 TAB ĐƠN GIẢN, TRỰC QUAN
# -------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 1. Biểu đồ Dự báo SARIMA (Ngoài mẫu)",
    "🚨 2. Phát hiện Sự cố Bất thường (Ngưỡng 3-sigma)",
    "📊 3. Dữ liệu Gốc & So sánh Mô hình"
])

# =============================================================
# TAB 1: DỰ BÁO SARIMA
# =============================================================
with tab1:
    st.subheader("Kết quả Dự báo ngoài mẫu 432 giờ (18 ngày kiểm thử)")
    st.caption("Đường màu cam biểu thị giá trị dự báo SARIMA, dải màu xám là khoảng tin cậy 95%, so sánh trực tiếp với đường màu xanh thực tế.")
    
    if df_fc is not None:
        fig1 = go.Figure()
        
        # Dải tin cậy 95%
        fig1.add_trace(go.Scatter(
            x=df_fc["timestamp"],
            y=df_fc["upper_ci_95"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        fig1.add_trace(go.Scatter(
            x=df_fc["timestamp"],
            y=df_fc["lower_ci_95"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(180, 200, 230, 0.35)",
            name="Khoảng tin cậy 95%"
        ))
        
        # Đường thực tế
        fig1.add_trace(go.Scatter(
            x=df_fc["timestamp"],
            y=df_fc["actual"],
            mode="lines",
            name="Lưu lượng thực tế",
            line=dict(color="#1f77b4", width=2)
        ))
        
        # Đường dự báo SARIMA
        fig1.add_trace(go.Scatter(
            x=df_fc["timestamp"],
            y=df_fc["forecast"],
            mode="lines",
            name="Dự báo SARIMA",
            line=dict(color="#ff7f0e", width=2.5, dash="dash")
        ))
        
        fig1.update_layout(
            height=460,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Thời gian (Giờ)",
            yaxis_title="Số lượng Request / Giờ",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff"
        )
        fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
        fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
        
        st.plotly_chart(fig1, use_container_width=True)
        
        st.success("✅ **Nhận xét:** Mô hình SARIMA dự báo bám sát chu kỳ ngày đêm 24 giờ. Dự báo chính xác đỉnh cao điểm ban ngày và đáy thấp điểm rạng sáng, đạt hệ số tương quan cao ngoài mẫu.")

# =============================================================
# TAB 2: PHÁT HIỆN BẤT THƯỜNG
# =============================================================
with tab2:
    st.subheader("Nhận diện Sự cố Lưu lượng với Ngưỡng động 3 Độ lệch chuẩn (3-sigma)")
    st.caption("Các điểm tăng vọt (Spike) được đánh dấu bằng tam giác đỏ, các điểm sụt giảm (Drop) đánh dấu bằng tam giác tím.")
    
    if df_anom is not None:
        spikes = df_anom[df_anom["detected_spike"] == 1]
        drops = df_anom[df_anom["detected_drop"] == 1]
        
        fig2 = go.Figure()
        
        # Ngưỡng động
        fig2.add_trace(go.Scatter(
            x=df_anom["timestamp"],
            y=df_anom["dyn_upper"],
            mode="lines",
            name="Ngưỡng trên (+3σ)",
            line=dict(color="#d62728", width=1.5, dash="dot")
        ))
        fig2.add_trace(go.Scatter(
            x=df_anom["timestamp"],
            y=df_anom["dyn_lower"],
            mode="lines",
            name="Ngưỡng dưới (-3σ)",
            line=dict(color="#9467bd", width=1.5, dash="dot")
        ))
        
        # Đường thực tế
        fig2.add_trace(go.Scatter(
            x=df_anom["timestamp"],
            y=df_anom["actual"],
            mode="lines",
            name="Lưu lượng thực tế",
            line=dict(color="#4a5568", width=1.5)
        ))
        
        # Điểm bất thường Spike
        fig2.add_trace(go.Scatter(
            x=spikes["timestamp"],
            y=spikes["actual"],
            mode="markers",
            name="Tăng vọt bất thường (Spike)",
            marker=dict(color="#d62728", size=10, symbol="triangle-up")
        ))
        
        # Điểm bất thường Drop
        fig2.add_trace(go.Scatter(
            x=drops["timestamp"],
            y=drops["actual"],
            mode="markers",
            name="Sụt giảm bất thường (Drop)",
            marker=dict(color="#9467bd", size=10, symbol="triangle-down")
        ))
        
        fig2.update_layout(
            height=440,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Thời gian (Giờ)",
            yaxis_title="Lưu lượng (Req / Giờ)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff"
        )
        fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
        fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # Bảng danh sách các sự cố
        st.markdown("#### 📋 Danh sách các giờ xảy ra sự cố phát hiện được:")
        anom_list = df_anom[df_anom["detected_anomaly"] == 1].copy()
        if len(anom_list) > 0:
            anom_list["Loại sự cố"] = np.where(anom_list["detected_spike"] == 1, "Tăng vọt (Spike / DDoS)", "Sụt giảm (Drop / Outage)")
            anom_display = anom_list[["timestamp", "actual", "Loại sự cố"]].copy()
            anom_display.columns = ["Thời gian xảy ra", "Lưu lượng ghi nhận (req/h)", "Phân loại sự cố"]
            st.dataframe(anom_display, use_container_width=True, hide_index=True)

# =============================================================
# TAB 3: DỮ LIỆU GỐC & ĐỐI SÁNH MÔ HÌNH
# =============================================================
with tab3:
    st.subheader("Toàn bộ Chuỗi Dữ liệu Quan sát (90 Ngày - 2.160 Giờ)")
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=df_raw["timestamp"],
        y=df_raw["request_count"],
        mode="lines",
        name="Lưu lượng API gốc",
        line=dict(color="#0056b3", width=1.5)
    ))
    
    # Đánh dấu phân chia Train / Test (1.728 giờ)
    split_date = df_raw["timestamp"].iloc[1728]
    fig3.add_vline(x=split_date, line_width=2, line_dash="dash", line_color="#dc3545")
    fig3.add_annotation(x=split_date, y=df_raw["request_count"].max(), text="Phân chia Tập Huấn Luyện (80%) / Kiểm Thử (20%)", showarrow=True, arrowhead=1)
    
    fig3.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Thời gian",
        yaxis_title="Số lượng Request / Giờ",
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff"
    )
    fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
    fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("#### 🏆 Bảng Xếp Hạng & Đối Sánh Hiệu Năng Các Mô Hình Dự Báo:")
    if df_bench is not None:
        st.dataframe(df_bench, use_container_width=True, hide_index=True)
    else:
        st.info("Bảng so sánh mô hình cơ sở hiển thị tại file: output/08_model_benchmarks.csv")
