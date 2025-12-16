
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Page Config
st.set_page_config(
    page_title="Rantai Pasok & Logistik",
    page_icon="🚚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .metric-card {
        background: #fff7ed;
        border-left: 5px solid #ea580c;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #9a3412; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🚚 Rantai Pasok Pangan</h1><p>Manajemen Logistik, Margin, & Timing Pasar Induk</p></div>', unsafe_allow_html=True)

# DATA REFERENCES
PASAR_INDUK = {
    "PI Kramat Jati (Jakarta)": {"peak_start": 23, "peak_end": 4, "lat": -6.27, "lon": 106.87},
    "PI Tanah Tinggi (Tangerang)": {"peak_start": 22, "peak_end": 3, "lat": -6.17, "lon": 106.66},
    "PI Cibitung (Bekasi)": {"peak_start": 21, "peak_end": 2, "lat": -6.24, "lon": 107.08},
    "PI Caringin (Bandung)": {"peak_start": 20, "peak_end": 1, "lat": -6.94, "lon": 107.57}
}

VEHICLES = {
    "Pick Up (L300)": {"kapasitas": 1000, "km_per_liter": 9, "sewa": 350000},
    "Engkel (4 Roda)": {"kapasitas": 2200, "km_per_liter": 7, "sewa": 600000},
    "Colt Diesel (6 Roda)": {"kapasitas": 4500, "km_per_liter": 5, "sewa": 900000},
    "Fuso (10 Roda)": {"kapasitas": 12000, "km_per_liter": 3, "sewa": 1500000},
}

# TABS
tab1, tab2, tab3 = st.tabs(["🚛 Kalkulator Logistik", "💰 Analisis Margin (Tata Niaga)", "⏱️ Radar Pasar Induk"])

# --- TAB 1: LOGISTICS CALCULATOR ---
with tab1:
    st.markdown("### 🚛 Estimasi Biaya Kirim & Susut Bobot")
    st.info("Menghitung HPP Transportasi per Kg agar tidak boncos di jalan.")
    
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.subheader("1. Data Pengiriman")
        jarak = st.number_input("Jarak Tempuh (km)", 10, 1000, 150)
        jenis_truk = st.selectbox("Jenis Armada", list(VEHICLES.keys()))
        muatan_kg = st.number_input(f"Total Muatan (kg) - Max {VEHICLES[jenis_truk]['kapasitas']}kg", 100, VEHICLES[jenis_truk]['kapasitas'], int(VEHICLES[jenis_truk]['kapasitas']*0.9))
        
        st.subheader("2. Biaya Operasional")
        harga_bbm = st.number_input("Harga Solar/BBM (Rp/liter)", 5000, 20000, 6800)
        biaya_sopir = st.number_input("Upah Sopir + Kernet (Rp)", 0, 2000000, 250000)
        biaya_tol = st.number_input("Biaya Tol/Parkir/Pungli (Rp)", 0, 2000000, 150000)
        
    with col_l2:
        st.subheader("3. Risiko Susut (Shrinkage)")
        jenis_muatan = st.selectbox("Jenis Komoditas", ["Sayur Daun (Bayam/Sawit)", "Sayur Buah (Cabe/Tomat)", "Umbi-umbian (Kentang/Bawang)", "Buah Keras (Semangka/Melon)"])
        
        # Shrinkage Logic per 100km/Time
        susut_factor = 0.0 # % per 100km roughly
        if "Daun" in jenis_muatan: susut_factor = 2.5
        elif "Sayur Buah" in jenis_muatan: susut_factor = 1.2
        elif "Umbi" in jenis_muatan: susut_factor = 0.5
        elif "Keras" in jenis_muatan: susut_factor = 0.3
        
        est_susut_pct = (jarak / 100) * susut_factor
        berat_susut = muatan_kg * (est_susut_pct / 100)
        berat_jual = muatan_kg - berat_susut
        
        # Cost Calc
        veh_data = VEHICLES[jenis_truk]
        liter_bbm = jarak / veh_data['km_per_liter']
        total_bbm = liter_bbm * harga_bbm
        # Sewa is usually daily, assuming 1 trip fits in rental
        # Note: If own car, sewa = maintenance depreciation.
        
        total_biaya = total_bbm + biaya_sopir + biaya_tol + veh_data['sewa']
        hpp_per_kg_awal = total_biaya / muatan_kg
        hpp_per_kg_akhir = total_biaya / berat_jual # Real logistic cost based on sellable weight
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Biaya Total: Rp {total_biaya:,.0f}</h3>
            <p>HPP Logistik (Awal): <b>Rp {hpp_per_kg_awal:,.0f} /kg</b></p>
            <p>HPP Logistik (Real): <b>Rp {hpp_per_kg_akhir:,.0f} /kg</b> (Setelah Susut)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning(f"⚠️ **Estimasi Susut:** {est_susut_pct:.1f}% ({berat_susut:.0f} kg hilang diperjalanan). \nBerat siap jual: {berat_jual:.0f} kg.")

        # Breakdown Chart
        cost_data = pd.DataFrame({
            "Komponen": ["Sewa Truk", "BBM", "Sopir", "Tol/Lainnya", "Kerugian Susut (Valuasi)"],
            "Nilai": [veh_data['sewa'], total_bbm, biaya_sopir, biaya_tol, 0] # Susut not cash cost but opportunity cost
        })
        fig_pie = px.pie(cost_data.iloc[:-1], values='Nilai', names='Komponen', title="Komposisi Biaya Distribusi", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: MARGIN ANALYSIS ---
with tab2:
    st.markdown("### 💰 Analisis & Distribusi Margin")
    st.info("Bandingkan struktur harga (Siapa makan untung?) antara Pasar Tradisional vs Modern.")
    
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        st.subheader("Data Harga (Simulasi)")
        harga_petani = st.number_input("Harga di Petani (Farm Gate)", 1000, 100000, 5000, step=500)
        
        st.markdown("**Jalur Tradisional:**")
        margin_pengepul = st.slider("Margin Pengepul Desa (%)", 5, 30, 15)
        margin_bandar = st.slider("Margin Bandar Besar (%)", 5, 30, 10)
        margin_pedagang = st.slider("Margin Pengecer Pasar (%)", 10, 50, 25)
        cost_logistik_trad = st.number_input("Biaya Logistik Total (Rp/kg)", 500, 5000, 1500)
        
        st.markdown("---")
        st.markdown("**Jalur Modern (Supermarket):**")
        margin_supplier = st.slider("Margin Supplier/Aggregator (%)", 10, 40, 20)
        margin_retail = st.slider("Margin Supermarket (%)", 15, 60, 35)
        cost_logistik_mod = st.number_input("Biaya Packing & Logistik (Rp/kg)", 1000, 10000, 2500)
        
    with col_t2:
        # Waterfall Logic Traditional
        p1 = harga_petani
        c_p1 = p1 * (margin_pengepul/100)
        p2 = p1 + c_p1 # Pengepul
        c_trs = cost_logistik_trad # Logistik
        p3 = p2 + c_trs # Landed Cost Pasar Induk
        c_p3 = p3 * (margin_bandar/100) # Bandar Margin
        p4 = p3 + c_p3 # Harga Jual Bandar
        c_p4 = p4 * (margin_pedagang/100) # Pengecer Margin
        p_final_trad = p4 + c_p4
        
        # Waterfall Logic Modern
        m1 = harga_petani
        c_ops = cost_logistik_mod # Packing + Sorting + Kirim DC
        m2 = m1 + c_ops
        c_m2 = m2 * (margin_supplier/100)
        m3 = m2 + c_m2 # Harga Masuk DC (Buying Price)
        c_m3 = m3 * (margin_retail/100)
        p_final_mod = m3 + c_m3
        
        mode_view = st.radio("Pilih View:", ["Jalur Tradisional", "Jalur Modern"], horizontal=True)
        
        if mode_view == "Jalur Tradisional":
            fig_wf = go.Figure(go.Waterfall(
                name = "Struktur Harga", orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "relative", "total"],
                x = ["Harga Petani", "Margin Pengepul", "Ongkos Kirim", "Margin Bandar", "Margin Pengecer", "Harga Konsumen"],
                y = [p1, c_p1, c_trs, c_p3, c_p4, p_final_trad],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            final_p = p_final_trad
            
        else:
             fig_wf = go.Figure(go.Waterfall(
                name = "Struktur Harga", orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "total"],
                x = ["Harga Petani", "Biaya Ops (Sortir/Pack/Kirim)", "Margin Supplier", "Margin Supermarket", "Harga Konsumen"],
                y = [m1, c_ops, c_m2, c_m3, p_final_mod],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
             final_p = p_final_mod

        fig_wf.update_layout(title=f"Pembentukan Harga Akhir: Rp {final_p:,.0f}", waterfallgap = 0.3)
        st.plotly_chart(fig_wf, use_container_width=True)
        
        share_petani = (harga_petani / final_p) * 100
        st.info(f"💡 **Farmer's Share:** Petani hanya menikmati **{share_petani:.1f}%** dari harga yang dibayar konsumen akhir.")

# --- TAB 3: MARKET TIMING ---
with tab3:
    st.markdown("### ⏱️ Radar Pasar Induk (Golden Hour)")
    st.info("Ketahui jam emas lelang (harga tertinggi) agar truk tiba tepat waktu.")
    
    col_tm1, col_tm2 = st.columns(2)
    
    with col_tm1:
        target_pasar = st.selectbox("Pilih Pasar Induk Tujuan", list(PASAR_INDUK.keys()))
        data_pasar = PASAR_INDUK[target_pasar]
        
        jam_est_tempuh = st.slider("Estimasi Lama Perjalanan (Jam)", 1, 24, 6)
        
        peak_start = data_pasar['peak_start'] # e.g 23 (11 PM)
        peak_end = data_pasar['peak_end'] # e.g 4 (4 AM)
        
        # Display Info
        start_str = f"{peak_start}:00"
        end_str = f"0{peak_end}:00" if peak_end < 10 else f"{peak_end}:00"
        st.success(f"🔥 **Jam Sibuk (Harga Terbaik):** {start_str} s/d {end_str} WIB")
        
    with col_tm2:
        st.subheader("🕑 Rekomendasi Jam Berangkat")
        
        # Calculate departure to arrive at start of peak
        # Logic: Arrive at peak_start.
        # Dep = Peak - Travel. 
        # Handle day wrapping (e.g. peak 23, travel 4 -> dep 19. Peak 02, travel 4 -> dep 22 prev day)
        
        arrival_target = peak_start
        dep_hour = arrival_target - jam_est_tempuh
        day_offset = "Hari yang Sama"
        
        if dep_hour < 0:
            dep_hour += 24
            day_offset = "Hari Sebelumnya (Kemarin)"
            
        st.markdown(f"""
        <div style='text-align: center; border: 2px dashed #ea580c; padding: 20px; border-radius: 10px;'>
            <h3>Truk Harus Berangkat Pukul:</h3>
            <h1 style='font-size: 3rem; color: #ea580c;'>{int(dep_hour):02d}:00 WIB</h1>
            <p>({day_offset})</p>
            <hr>
            <p>Agar tiba pukul <b>{peak_start}:00</b> (Awal Lelang)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple Gauge Risk
        risk_lvl = "Aman"
        if jam_est_tempuh > 12: risk_lvl = "Tinggi (Sopir Lelah/Macet)"
        elif jam_est_tempuh > 8: risk_lvl = "Sedang"
        
        st.caption(f"Status Risiko Perjalanan: **{risk_lvl}**")

# Footer
st.markdown("---")
st.caption("AgriSensa Logistics - Mengamankan Profit dari Kebun ke Kota.")
