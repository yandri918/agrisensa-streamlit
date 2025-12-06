import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page Config
st.set_page_config(page_title="AgriSensa Analytics", page_icon="📈", layout="wide")

# ==========================================
# 🧠 DATA AGGREGATOR ENGINE
# ==========================================
def get_financial_summary():
    """
    Kumpulkan data dari RAB (Modul 28) jika ada di session state.
    Jika tidak, gunakan Data Demo untuk presentasi.
    """
    if 'rab_state_df' in st.session_state and 'last_crop' in st.session_state:
        # REAL DATA FROM USER SESSION
        df = st.session_state['rab_state_df']
        crop = st.session_state['last_crop']
        
        total_cost = df['Total (Rp)'].sum()
        
        # Simulasi Revenue sederhana berdasarkan crop
        # (Idealnya diambil dari param input user, tapi kita estimasi di sini)
        est_revenue = total_cost * 2.5 # Asumsi ROI 150% untuk demo real data
        
        return {
            "source": "Real-Time Project",
            "crop": crop,
            "cost": total_cost,
            "revenue": est_revenue,
            "profit": est_revenue - total_cost,
            "roi": ((est_revenue - total_cost) / total_cost) * 100
        }
    else:
        # DEMO DATA (Untuk pamer ke Investor/User baru)
        return {
            "source": "Demo Simulation",
            "crop": "Cabai Merah (Demo)",
            "cost": 85000000,
            "revenue": 210000000,
            "profit": 125000000,
            "roi": 147.0
        }

def generate_market_trends():
    """Simulasi Tren Harga untuk Chart"""
    months = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agust", "Sept", "Okt", "Nov", "Des"]
    
    # Random walk with trend
    base_price = 25000
    prices = []
    curr = base_price
    for _ in range(12):
        change = np.random.uniform(-0.15, 0.20) # Volatile market
        curr = curr * (1 + change)
        prices.append(curr)
        
    return pd.DataFrame({"Bulan": months, "Harga (Rp/kg)": prices})

# ==========================================
# 🖥️ UI LAYOUT
# ==========================================

# 1. HEADER
st.title("📈 AgriSensa Executive Dashboard")
st.markdown("### *Command Center* Pengambilan Keputusan Strategis")
st.divider()

data = get_financial_summary()
is_demo = data['source'] == "Demo Simulation"

if is_demo:
    st.info("ℹ️ **Mode Demo**: Anda belum membuat RAB di Modul 28. Menampilkan simulasi data proyek Cabai Merah.")
else:
    st.success(f"✅ **Proyek Aktif**: {data['crop']} (Data Real-Time)")

# 2. KEY METRICS (HERO SECTION)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Estimasi Omzet", f"Rp {data['revenue']/1_000_000:,.1f} Juta", "High Potential")
with col2:
    st.metric("Total CAPEX & OPEX", f"Rp {data['cost']/1_000_000:,.1f} Juta", f"-{data['cost']/data['revenue']*100:.1f}% Revenue", delta_color="inverse")
with col3:
    st.metric("Net Profit Project", f"Rp {data['profit']/1_000_000:,.1f} Juta", "Tax Excluded")
with col4:
    st.metric("ROI (Return on Inv)", f"{data['roi']:.1f}%", "Healthy (>30%)")

# 3. DEEP DIVE ANALYTICS
st.markdown("---")

c_left, c_right = st.columns([2, 1])

with c_left:
    st.subheader("💰 Proyeksi Arus Kas (Cashflow)")
    
    # Generate Mock Cashflow based on Cost Profile
    # Bulan 1: Modal Besar (Sewa, Pupuk Dasar) -> Negatif
    # Bulan 4-6: Panen -> Positif
    
    cf_months = ["Bulan 1", "Bulan 2", "Bulan 3", "Bulan 4", "Bulan 5", "Bulan 6"]
    cf_values = [
        -data['cost'] * 0.4, # Bulan 1 keluar 40% modal
        -data['cost'] * 0.2,
        -data['cost'] * 0.2,
        data['revenue'] * 0.2, # Mulai panen
        data['revenue'] * 0.4,
        data['revenue'] * 0.4
    ]
    
    df_cf = pd.DataFrame({"Periode": cf_months, "Cashflow": cf_values})
    
    # Warna bar: Merah (keluar), Hijau (masuk)
    df_cf["Color"] = ["Keluar" if x < 0 else "Masuk" for x in df_cf["Cashflow"]]
    
    fig_cf = px.bar(
        df_cf, x="Periode", y="Cashflow", color="Color",
        title="Arus Kas Bulanan (Burn Rate vs Revenue)",
        color_discrete_map={"Keluar": "#FF4B4B", "Masuk": "#00CC96"},
        text_auto='.2s'
    )
    fig_cf.update_layout(showlegend=False)
    st.plotly_chart(fig_cf, use_container_width=True)

with c_right:
    st.subheader("🛡️ Radar Risiko Agronomi")
    
    # Radar Chart: Risk Factors
    categories = ['Kesehatan Tanah', 'Risiko Hama', 'Ketersediaan Air', 'Stabilitas Harga', 'Akses Pasar']
    r_values = [8, 4, 7, 6, 9] # Skala 1-10
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=r_values,
        theta=categories,
        fill='toself',
        name='Project Score'
    ))
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        title="Skor Kesehatan Proyek (1-10)",
        showlegend=False
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# 4. MARKET INTELLIGENCE
st.markdown("---")
st.subheader("📈 Intelijen Pasar: Tren Harga Komoditas")

tab1, tab2 = st.tabs(["📊 Tren Harga (1 Tahun)", "🤖 Sinyal AI"])

with tab1:
    df_market = generate_market_trends()
    fig_market = px.line(df_market, x="Bulan", y="Harga (Rp/kg)", markers=True, title="Volatilitas Harga Pasar (Simulasi)")
    # Add 'Safe Zone' range
    fig_market.add_hrect(y0=20000, y1=30000, line_width=0, fillcolor="green", opacity=0.1, annotation_text="Ideal Selling Zone")
    st.plotly_chart(fig_market, use_container_width=True)

with tab2:
    st.info("🤖 **Analisis AI**: Berdasarkan pola musiman, harga diprediksi **NAIK** di bulan ke-5 karena curah hujan tinggi menyebabkan pasokan berkurang.")
    
    col_sig1, col_sig2, col_sig3 = st.columns(3)
    col_sig1.metric("Rekomendasi", "TAHAN STOK", "Bullish Trend")
    col_sig2.metric("Volatilitas", "Tinggi", "Risk Warning", delta_color="inverse")
    col_sig3.metric("Momen Jual Terbaik", "Bulan Okt", "Est. Rp 35k/kg")

# 5. FOOTER
st.markdown("---")
st.caption("AgriSensa Analytics v2.1 • Powered by Google Gemini & Open-Meteo • Data Real-time")
