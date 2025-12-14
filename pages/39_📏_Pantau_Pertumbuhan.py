import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Pantau Pertumbuhan Tanaman - AgriSensa",
    page_icon="📏",
    layout="wide"
)

# Header
st.title("📏 Pantau Pertumbuhan Tanaman")
st.markdown("""
**Growth Monitoring System**
Catat dan visualisasikan perkembangan tanaman Anda dari hari ke hari.
""")

# Sidebar Input
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    komoditas = st.selectbox("Pilih Komoditas", ["Jagung Hibrida", "Padi Inpari", "Cabai Rawit", "Melon"], index=0)
    
    st.divider()
    st.header("📝 Input Data Harian")
    tgl_catat = st.date_input("Tanggal Pencatatan", datetime.now())
    usia_hst = st.number_input("Usia Tanaman (HST)", min_value=1, value=30)
    tinggi = st.number_input("Tinggi Tanaman (cm)", min_value=0.0, value=75.0)
    jumlah_daun = st.number_input("Jumlah Daun (helai)", min_value=0, value=12)
    
    if st.button("Simpan Data ke Jurnal"):
        st.toast(f"Data {komoditas} (HST {usia_hst}) tersimpan!", icon="✅")

# Profile Data (Simulasi Standard)
profiles = {
    "Jagung Hibrida": {"max_h": 220, "panen_hst": 105, "growth_rate": 0.08},
    "Padi Inpari": {"max_h": 110, "panen_hst": 115, "growth_rate": 0.07},
    "Cabai Rawit": {"max_h": 80, "panen_hst": 90, "growth_rate": 0.05},
    "Melon": {"max_h": 200, "panen_hst": 70, "growth_rate": 0.12}
}
prof = profiles[komoditas]

# Main Layout
st.markdown(f"### 📊 Dashboard Monitoring: **{komoditas}**")

col_main, col_side = st.columns([3, 1])

with col_main:
    # 1. ADVANCED CHARTING
    # Generate historical data simulation (Logarithmic + Noise)
    days = np.arange(1, usia_hst + 15) # Prediksi ke depan dikit
    
    # Model Sigmoid Standar
    kt = prof['max_h']
    r = prof['growth_rate']
    mid = prof['panen_hst'] / 2
    
    # Standard Curve
    standard_curve = kt / (1 + np.exp(-r * (days - mid)))
    
    # Real data simulation (with slight variation)
    np.random.seed(42)
    noise = np.random.normal(0, 2, len(days))
    actual_curve = standard_curve * 1.05 + noise # Ceritanya performa 105%
    
    # Cut actual data to current age
    actual_data_viz = actual_curve[:usia_hst]
    days_viz = days[:usia_hst]
    
    # Future Prediction (Polynomial Regression Degree 2)
    if usia_hst > 5:
        z = np.polyfit(days_viz, actual_data_viz, 2)
        p = np.poly1d(z)
        future_days = np.arange(usia_hst, prof['panen_hst'] + 5)
        predicted_growth = p(future_days)
    else:
        future_days = []
        predicted_growth = []

    # Plotting
    fig = go.Figure()
    
    # Trace 1: Standar
    fig.add_trace(go.Scatter(x=days, y=standard_curve, mode='lines', name='Standar Varietas',
                             line=dict(color='gray', dash='dot')))
    
    # Trace 2: History Aktual
    fig.add_trace(go.Scatter(x=days_viz, y=actual_data_viz, mode='lines+markers', name='Aktual (Anda)',
                             line=dict(color='green', width=3)))
    
    # Trace 3: AI Prediction
    if len(future_days) > 0:
        fig.add_trace(go.Scatter(x=future_days, y=predicted_growth, mode='lines', name='AI Prediction',
                                 line=dict(color='orange', dash='dash')))
        
    fig.update_layout(title="Analisis & Prediksi Pertumbuhan (Real-time)", xaxis_title="Hari Setelah Tanam (HST)", yaxis_title="Tinggi (cm)")
    st.plotly_chart(fig, use_container_width=True)

    # 2. PHYSIOLOGICAL ANALYSIS (RGR)
    st.subheader("🧬 Analisis Fisiologis (Advanced)")
    if usia_hst > 5:
        # Hitung RGR (Relative Growth Rate)
        # RGR = (ln H2 - ln H1) / (t2 - t1)
        h2 = actual_data_viz[-1]
        h1 = actual_data_viz[-5] # 5 hari lalu
        rgr = (np.log(h2) - np.log(h1)) / 5
        
        col_p1, col_p2, col_p3 = st.columns(3)
        col_p1.metric("Laju Pertumbuhan Relatif (RGR)", f"{rgr:.4f} cm/cm/hari", delta="Sangat Bagus" if rgr > 0.05 else "Normal")
        
        # Narasi AI
        if rgr > 0.05:
            st.success("🚀 **Fase Eksponensial:** Tanaman sedang dalam masa pertumbuhan vegetatif maksimal. Tingkatkan asupan Nitrogen dan Air!")
        elif rgr < 0.01:
            st.warning("🛑 **Stagnasi:** Pertumbuhan melambat. Cek kesehatan akar atau serangan hama.")
        else:
            st.info("✅ **Stabil:** Pertumbuhan sesuai kurva logistik.")
            
with col_side:
    st.subheader("🎯 Prediksi Panen")
    
    # Hitung Estimasi berdasarkan AI
    target_h = prof['max_h'] * 0.9 # 90% size usually harvestable
    
    # Cari kapan predicted growth cross target
    harvest_day_ai = prof['panen_hst'] # Default
    if len(predicted_growth) > 0:
        for i, val in enumerate(predicted_growth):
            if val >= target_h:
                harvest_day_ai = future_days[i]
                break
    
    days_left = int(harvest_day_ai - usia_hst)
    tgl_panen = tgl_catat + timedelta(days=days_left)
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
        <h1 style="color: green; margin:0;">{days_left}</h1>
        <p>Hari Lagi</p>
        <hr>
        <small>Estimasi Tanggal:</small><br>
        <strong>{tgl_panen.strftime('%d %B %Y')}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.metric("Deviasi dari Standar", f"{(actual_data_viz[-1] - standard_curve[usia_hst-1]):.1f} cm", "Lebih Tinggi")
    
    st.markdown("### 🔔 Alerts")
    if actual_data_viz[-1] > standard_curve[usia_hst-1]:
        st.success("Pertumbuhan Di Atas Rata-rata!")
    else:
        st.error("Pertumbuhan Tertinggal!")

# 3. DATA EXPORT
st.write("---")
st.download_button("📥 Download Laporan Lengkap (PDF)", data="Dummy PDF Data", file_name=f"Laporan_Pertumbuhan_{komoditas}.pdf")

