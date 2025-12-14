import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page config
st.set_page_config(
    page_title="Pantau Pertumbuhan Tanaman - AgriSensa",
    page_icon="📏",
    layout="wide"
)

# Constants & Setup
DATA_FILE = "data/growth_journal.csv"

# Ensure Data Directory and File Exist
if not os.path.exists('data'):
    os.makedirs('data')

def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun'])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun'])
    return pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun'])

def save_data(tgl, komoditas, hst, tinggi, daun):
    df = load_data()
    # Check if entry exists for this date and commodity to avoid dupes? 
    # For now, let's just append. simpler.
    new_data = pd.DataFrame({
        'tanggal': [tgl],
        'komoditas': [komoditas],
        'usia_hst': [hst],
        'tinggi_cm': [tinggi],
        'jumlah_daun': [daun]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

init_data()

# Header
st.title("📏 Pantau Pertumbuhan Tanaman")
st.markdown("""
**Growth Monitoring System (Dynamic)**
Input data harian tanamanmu dan biarkan AI menganalisis laju pertumbuhan serta prediksi panennya.
""")

# Sidebar Input
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    komoditas = st.selectbox("Pilih Komoditas", ["Jagung Hibrida", "Padi Inpari", "Cabai Rawit", "Melon"], index=0)
    
    st.divider()
    st.header("📝 Input Data Harian")
    tgl_catat = st.date_input("Tanggal Pencatatan", datetime.now())
    usia_hst = st.number_input("Usia Tanaman (HST)", min_value=1, value=1)
    tinggi = st.number_input("Tinggi Tanaman (cm)", min_value=0.0, value=0.0)
    jumlah_daun = st.number_input("Jumlah Daun (helai)", min_value=0, value=0)
    
    if st.button("💾 Simpan Data ke Jurnal"):
        save_data(tgl_catat, komoditas, usia_hst, tinggi, jumlah_daun)
        st.toast(f"Data {komoditas} (HST {usia_hst}) berhasil disimpan!", icon="✅")
        st.rerun()

    st.info("💡 Data tersimpan di `data/growth_journal.csv`")

# Profile Data (Standar)
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

# --- DATA PROCESSING ---
df = load_data()
df_filtered = df[df['komoditas'] == komoditas].sort_values(by='usia_hst')

# Calculate Standard Curve for Visualization Background
max_days = prof['panen_hst'] + 15
days_standard = np.arange(1, max_days)
kt = prof['max_h']
r = prof['growth_rate']
mid = prof['panen_hst'] / 2
standard_curve = kt / (1 + np.exp(-r * (days_standard - mid)))

with col_main:
    fig = go.Figure()
    
    # 1. Trace Standard
    fig.add_trace(go.Scatter(x=days_standard, y=standard_curve, mode='lines', name='Standar Varietas',
                             line=dict(color='gray', dash='dot')))
    
    # 2. Trace Actual Data
    if not df_filtered.empty:
        fig.add_trace(go.Scatter(x=df_filtered['usia_hst'], y=df_filtered['tinggi_cm'], 
                                 mode='lines+markers', name='Data Aktual Anda',
                                 line=dict(color='green', width=3)))
        
        # 3. AI Prediction (Polynomial Regression)
        # Needs at least 3 points for decent Poly Degree 2, else Degree 1
        if len(df_filtered) >= 2:
            try:
                # Degree determination
                degree = 2 if len(df_filtered) >= 3 else 1
                
                z = np.polyfit(df_filtered['usia_hst'], df_filtered['tinggi_cm'], degree)
                p = np.poly1d(z)
                
                last_hst = df_filtered['usia_hst'].iloc[-1]
                future_days = np.arange(last_hst, prof['panen_hst'] + 10)
                predicted_growth = p(future_days)
                
                # Filter negative predictions or crazy drops implies harvest/death, just clip at max possible or 0
                predicted_growth = np.maximum(predicted_growth, 0)
                
                fig.add_trace(go.Scatter(x=future_days, y=predicted_growth, mode='lines', name='AI Prediction (Trend)',
                                         line=dict(color='orange', dash='dash')))
            except Exception as e:
                st.warning(f"Belum cukup data untuk prediksi AI: {e}")
                predicted_growth = []
                future_days = []
        else:
            predicted_growth = []
            future_days = []
    else:
        st.info("👋 Belum ada data. Silakan input data harian di sidebar untuk melihat grafik.")
        predicted_growth = []
        future_days = []

    fig.update_layout(title="Analisis & Prediksi Pertumbuhan (Real-time)", 
                      xaxis_title="Hari Setelah Tanam (HST)", yaxis_title="Tinggi (cm)",
                      hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # 4. PHYSIOLOGICAL ANALYSIS (RGR)
    st.subheader("🧬 Analisis Fisiologis (Real-Data)")
    
    if len(df_filtered) >= 2:
        # Get last two data points
        last_point = df_filtered.iloc[-1]
        prev_point = df_filtered.iloc[-2]
        
        h2, t2 = last_point['tinggi_cm'], last_point['usia_hst']
        h1, t1 = prev_point['tinggi_cm'], prev_point['usia_hst']
        
        # Avoid division by zero
        delta_t = t2 - t1
        if delta_t > 0 and h1 > 0 and h2 > 0:
            rgr = (np.log(h2) - np.log(h1)) / delta_t
            
            col_p1, col_p2 = st.columns(2)
            col_p1.metric("Laju Pertumbuhan Relatif (RGR)", f"{rgr:.4f} cm/cm/hari", 
                          delta="Positif" if rgr > 0 else "Stagnan/Negatif")
            
            with col_p2:
                if rgr > 0.1:
                    st.success("🚀 **Fase Eksponensial Cepat**: Nutrisi sangat cukup!")
                elif rgr > 0.01:
                    st.info("✅ **Pertumbuhan Stabil**: Lanjutkan perawatan.")
                else:
                    st.warning("🛑 **Stagnasi**: Cek kondisi tanah/air segera.")
        else:
            st.write("Data tidak valid untuk perhitungan logaritmik (tinggi <= 0 atau hari sama).")
    else:
        st.write("Min. 2 data history diperlukan untuk analisis laju pertumbuhan.")

    # 5. Show Data Table
    with st.expander("📂 Buka Log Data Pertumbuhan"):
        st.dataframe(df_filtered)
        if not df_filtered.empty:
            # Delete button logic could go here (complicated in Streamlit plain, skip for now unless requested)
            pass

with col_side:
    st.subheader("🎯 Status Panen")
    
    if not df_filtered.empty and len(future_days) > 0:
        # Hitung Estimasi
        target_h = prof['max_h'] * 0.9
        
        harvest_hst_ai = prof['panen_hst'] # Default fallback
        
        # Check intersection with target
        # Combine actual and predicted to find first crossing
        found = False
        
        # Check if already reached in actual
        if df_filtered['tinggi_cm'].max() >= target_h:
            st.success("🎉 Tanaman sudah mencapai tinggi panen!")
            days_left = 0
        else:
            # Check prediction
            for i, val in enumerate(predicted_growth):
                if val >= target_h:
                    harvest_hst_ai = future_days[i]
                    found = True
                    break
            
            current_hst = df_filtered['usia_hst'].iloc[-1]
            days_left = int(harvest_hst_ai - current_hst)
            
            if days_left < 0: days_left = 0
            
            # Estimate date
            tgl_prediksi = datetime.now() + timedelta(days=days_left) # Approx based on run time, better if based on last input date? 
            # Actually better to base on Last Input Date + Days Left
            # But 'days_left' is (Target HST - Current HST). 
            # So Target Date = Last Input Date + (Target HST - Current HST) implies assuming continuous growth from now.
            # But strict calculation:
            # Last Input Date + (Target HST - Last Input HST) days.
            
            last_date_str = df_filtered['tanggal'].iloc[-1]
            try:
                last_date = datetime.strptime(str(last_date_str), "%Y-%m-%d")
            except:
                last_date = datetime.now()
                
            est_date = last_date + timedelta(days=days_left)
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: #e8f5e9; border-radius: 10px; border: 1px solid #c8e6c9;">
                <h2 style="color: #2e7d32; margin:0;">{days_left} Hari</h2>
                <small>Menuju Panen Optimal</small>
                <hr style="margin: 10px 0;">
                <div style="font-size: 0.9em;">Estimasi Tanggal:<br><strong>{est_date.strftime('%d %b %Y')}</strong></div>
            </div>
            """, unsafe_allow_html=True)
            
            if not found:
                st.caption("ℹ️ Prediksi belum mencapai target tinggi dalam rentang waktu normal (mungkin varietas pendek/kerdil).")

        # Current Status
        curr_h = df_filtered['tinggi_cm'].iloc[-1]
        std_h_at_hst = prof['max_h'] / (1 + np.exp(-prof['growth_rate'] * (current_hst - prof['panen_hst']/2)))
        
        dev = curr_h - std_h_at_hst
        st.write("")
        st.metric("Deviasi Visual", f"{dev:.1f} cm", delta_color="normal" if dev > -10 else "inverse")
        
        if dev < -15:
            st.error("⚠️ TERTINGGAL JAUH! Periksa hama/penyakit.")
        elif dev > 15:
            st.warning("⚠️ TERLALU JANGKUNG! Awas rebah batang.")
        else:
            st.success("✅ Pertumbuhan Normal")

    else:
        st.info("Input minimal 2 data harian untuk melihat prediksi panen.")

# Download Data Button
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        st.download_button("📥 Backup CSV Data", f, file_name="growth_journal_backup.csv")
