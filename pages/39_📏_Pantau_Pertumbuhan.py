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
    st.header("📝 Input Data Harian")
    tgl_catat = st.date_input("Tanggal Pencatatan", datetime.now())
    usia_hst = st.number_input("Usia Tanaman (HST)", min_value=0, value=15)
    tinggi = st.number_input("Tinggi Tanaman (cm)", min_value=0.0, value=25.5)
    jumlah_daun = st.number_input("Jumlah Daun (helai)", min_value=0, value=8)
    diameter = st.number_input("Diameter Batang (mm)", min_value=0.0, value=5.2)
    
    if st.button("Simpan Data"):
        st.success(f"Data tanggal {tgl_catat} berhasil disimpan!")
        # In real app, this would append to DB/CSV

# Main Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Grafik Pertumbuhan")
    
    # Dummy Data Generator for Visualization
    days = list(range(0, 31, 3)) # Data setiap 3 hari
    
    # Sigmoid growth curve logic
    kt = 50 # Carrying capacity (max height)
    r = 0.15 # growth rate
    heights = [kt / (1 + np.exp(-r * (t - 15))) for t in days] # Logistic function
    
    leafs = [int(h/3 + 2) for h in heights] # Correlation height vs leaves
    
    df_growth = pd.DataFrame({
        "Hari Setelah Tanam (HST)": days,
        "Tinggi (cm)": heights,
        "Jumlah Daun": leafs
    })
    
    # Interactive Chart
    fig = px.line(df_growth, x="Hari Setelah Tanam (HST)", y=["Tinggi (cm)", "Jumlah Daun"],
                  markers=True, title="Kurva Pertumbuhan (S-Curve)")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 **Analisis:** Laju pertumbuhan tanaman Anda berada di fase **Eksponensial** (Cepat). Pastikan nutrisi Nitrogen (N) tercukupi.")

with col2:
    st.subheader("📊 Statistik Vital")
    
    last_h = heights[-1]
    prev_h = heights[-2]
    growth_rate = (last_h - prev_h) / 3 # cm per day
    
    st.metric("Tinggi Saat Ini", f"{last_h:.1f} cm", f"{last_h - prev_h:.1f} cm (3 hari)")
    st.metric("Laju Pertumbuhan", f"{growth_rate:.2f} cm/hari", "Normal")
    st.metric("Estimasi Panen", "15 Hari Lagi", "Sesuai Jadwal")
    
    st.write("---")
    st.write("**Catatan Lapangan:**")
    st.text_area("Notes", "Daun tampak hijau segar. Tidak ada tanda serangan hama.", height=100)

# History Data Table
st.subheader("🗃️ Riwayat Pencatatan")
st.dataframe(df_growth, use_container_width=True)

# Comparison Feature
st.subheader("🆚 Komparasi Varietas")
col_a, col_b = st.columns(2)
with col_a:
    varietas_a = [h * 1.0 for h in heights]
    varietas_b = [h * 0.8 for h in heights] # Slower growth
    
    df_compare = pd.DataFrame({
        "HST": days,
        "Varietas Unggul (Anda)": varietas_a,
        "Varietas Lokal": varietas_b
    })
    
    fig_comp = px.line(df_compare, x="HST", y=["Varietas Unggul (Anda)", "Varietas Lokal"],
                       title="Perbandingan Tinggi Tanaman vs Standar")
    st.plotly_chart(fig_comp, use_container_width=True)

with col_b:
    st.markdown("""
    **Kesimpulan:**
    Tanaman Anda memiliki performa **20% lebih baik** dibanding rata-rata varietas lokal pada usia yang sama. 
    
    *Rekomendasi:* 
    Pertahankan pola irigasi dan pemupukan saat ini.
    """)
