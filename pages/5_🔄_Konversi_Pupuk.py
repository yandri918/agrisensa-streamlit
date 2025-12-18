# Fertilizer Logistics & Conversion v2.0
# Advanced Nutrient-to-Weight Engine & Organic Logistics

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
from datetime import datetime

st.set_page_config(page_title="Konversi & Logistik Pupuk", page_icon="🔄", layout="wide")

# ========== DATA & CONFIGURATION ==========

# Nutrient percentages (%) and standard prices
FERTILIZER_DATABASE = {
    # Anorganik
    "Urea": {"N": 46, "P": 0, "K": 0, "price": 2500, "type": "anorganik", "color": "#3b82f6"},
    "SP-36": {"N": 0, "P": 36, "K": 0, "price": 3000, "type": "anorganik", "color": "#10b981"},
    "KCl / MOP": {"N": 0, "P": 0, "K": 60, "price": 3500, "type": "anorganik", "color": "#f59e0b"},
    "ZA": {"N": 21, "P": 0, "K": 0, "price": 2200, "type": "anorganik", "color": "#06b6d4"},
    "NPK 15-15-15": {"N": 15, "P": 15, "K": 15, "price": 4000, "type": "anorganik", "color": "#8b5cf6"},
    "NPK 16-16-16": {"N": 16, "P": 16, "K": 16, "price": 4200, "type": "anorganik", "color": "#ec4899"},
    "TSP 46": {"N": 0, "P": 46, "K": 0, "price": 3800, "type": "anorganik", "color": "#14b8a6"},
    
    # Organik (Mass vs Volume)
    "Pupuk Kandang (Sapi)": {"N": 0.5, "P": 0.2, "K": 0.5, "price": 800, "type": "organik", "density": 0.5, "color": "#84cc16"},
    "Pupuk Kandang (Ayam)": {"N": 1.5, "P": 1.0, "K": 0.8, "price": 1200, "type": "organik", "density": 0.6, "color": "#65a30d"},
    "Kompos Matang": {"N": 1.2, "P": 0.8, "K": 1.2, "price": 1500, "type": "organik", "density": 0.55, "color": "#4d7c0f"},
    "Guano": {"N": 10.0, "P": 12.0, "K": 2.0, "price": 5000, "type": "organik", "density": 0.8, "color": "#166534"}
}

# Packaging options
BAG_SIZES = {
    "Karung Jumbo (50 kg)": 50,
    "Karung (40 kg)": 40,
    "Sak (25 kg)": 25,
    "Sak Kecil (10 kg)": 10,
    "Retail (5 kg)": 5
}

# Transportation profiles (Volume in m3, typical max weight in kg)
TRANSPORT_PROFILES = {
    "Motor / Pick-up Kecil": {"vol": 1.0, "weight": 800, "icon": "🛵"},
    "L300 / Carry": {"vol": 2.5, "weight": 1500, "icon": "🚐"},
    "Colt Diesel (Engkel)": {"vol": 6.0, "weight": 4000, "icon": "🚚"},
    "Truk Double (6 Ban)": {"vol": 9.0, "weight": 8000, "icon": "🚛"},
    "Fuso / Tronton": {"vol": 20.0, "weight": 15000, "icon": "🚢"}
}

# ========== DESIGN SYSTEM (Premium Glassmorphism) ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }

    .main { background-color: #f8fafc; }

    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .kpi-container {
        display: flex;
        gap: 15px;
        margin-bottom: 25px;
        overflow-x: auto;
        padding-bottom: 10px;
    }

    .kpi-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        min-width: 180px;
        flex: 1;
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }

    .kpi-value { font-size: 1.8rem; font-weight: 700; color: #0f172a; }
    .kpi-label { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }

    .unit-pill {
        background: #f1f5f9;
        color: #475569;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .stTable {
        border-radius: 15px !important;
        overflow: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP HEADER ==========
def main():
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size:2.8rem;">🔄 Logistik & Konversi v2.0</h1>
        <p style="margin:10px 0 0 0; opacity:0.9; font-size:1.1rem; font-weight:300;">
            Fertilizer Command Center: Dynamic Nutrient Conversion & Logistics ROI
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Navigation
    menu = st.sidebar.selectbox(
        "Navigasi Modul",
        ["🎯 Nutrient-to-Weight Engine", "🚚 Logistik & Armada", "💰 ROI Harga Satuan", "📦 Riwayat Belanja"]
    )

    st.sidebar.divider()
    st.sidebar.markdown("### ⚙️ Pengaturan Global")
    global_buffer = st.sidebar.slider("Buffer Cadangan (%)", 0, 20, 5)
    local_transport_cost = st.sidebar.number_input("Biaya per Trip (Rp)", value=250000, step=50000)

    if menu == "🎯 Nutrient-to-Weight Engine":
        st.subheader("🎯 Konversi Kebutuhan Hara ke Berat Pupuk")
        st.info("💡 Masukkan jumlah hara murni (N, P, K) yang Anda butuhkan, dan sistem akan menghitung berapa jumlah karung untuk setiap jenis pupuk.")
        
        # Scenario selection
        col_n, col_p, col_k = st.columns(3)
        with col_n:
            req_n = st.number_input("Target Nitrogen (kg N)", min_value=0.0, value=100.0, step=10.0, key="req_n")
        with col_p:
            req_p = st.number_input("Target Fosfor (kg P)", min_value=0.0, value=50.0, step=10.0, key="req_p")
        with col_k:
            req_k = st.number_input("Target Kalium (kg K)", min_value=0.0, value=50.0, step=10.0, key="req_k")
        
        st.markdown("---")
        st.markdown("### 📊 Perbandingan Kebutuhan Antar Pupuk")
        
        comparison_data = []
        for name, info in FERTILIZER_DATABASE.items():
            # Calculate weight needed for each nutrient if that's the only one targeted
            # Or if it's NPK, we calculate the governing nutrient
            
            w_n = (req_n / (info['N'] / 100)) if info['N'] > 0 else float('inf')
            w_p = (req_p / (info['P'] / 100)) if info['P'] > 0 else float('inf')
            w_k = (req_k / (info['K'] / 100)) if info['K'] > 0 else float('inf')
            
            # For this dashboard, we show "How much of THIS pupuk to get ALL of nutrient X?"
            # or for complex, the maximum needed to satisfy all targets
            if info['type'] == 'anorganik' and ('NPK' in name):
                target_weight = max(w_n if req_n > 0 else 0, w_p if req_p > 0 else 0, w_k if req_k > 0 else 0)
            else:
                # Find which target nutrient this fertilizer provides
                if req_n > 0 and info['N'] > 0: target_weight = w_n
                elif req_p > 0 and info['P'] > 0: target_weight = w_p
                elif req_k > 0 and info['K'] > 0: target_weight = w_k
                else: target_weight = 0
            
            if target_weight > 0 and target_weight != float('inf'):
                # Apply buffer
                final_weight = target_weight * (1 + global_buffer/100)
                total_cost = final_weight * info['price']
                
                comparison_data.append({
                    "Pupuk": name,
                    "Kandungan": f"N:{info['N']}% P:{info['P']}% K:{info['K']}%",
                    "Berat Dibutuhkan (kg)": round(final_weight, 1),
                    "Karung (50kg)": round(final_weight / 50, 1),
                    "Estimasi Biaya": f"Rp {total_cost:,.0f}"
                })
        
        if comparison_data:
            df_comp = pd.DataFrame(comparison_data)
            st.dataframe(df_comp, use_container_width=True, hide_index=True)
            
            # Visualization
            fig = go.Figure(go.Bar(
                x=df_comp['Pupuk'],
                y=df_comp['Berat Dibutuhkan (kg)'],
                marker_color=[FERTILIZER_DATABASE[n]['color'] for n in df_comp['Pupuk']],
                text=df_comp['Berat Dibutuhkan (kg)'],
                textposition='auto',
            ))
            fig.update_layout(title="Perbandingan Berat Pupuk untuk Target Hara yang Sama", yaxis_title="Berat (kg)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Pilih target hara (N, P, K) di atas untuk melihat perbandingan.")
        
        # Detailed breakdown
        st.markdown("---")
        st.subheader("📦 Rincian Pembelian")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Detail Konversi:**
            - Jenis Pupuk: **{fertilizer_type}**
            - Ukuran Kemasan: **{bag_size_name}**
            - Harga per kg: **Rp {price_per_kg:,.0f}**
            - Harga per karung: **Rp {cost_per_bag:,.0f}**
            """)
        
        with col2:
            st.markdown(f"""
            **Perhitungan:**
            - Kebutuhan: **{amount_kg:.1f} kg**
            - Karung dibutuhkan: **{bags_exact:.2f}** → **{bags_needed} karung**
            - Total pembelian: **{bags_needed} × {bag_size} kg = {total_kg:.1f} kg**
            - Kelebihan: **{excess_kg:.1f} kg** ({(excess_kg/amount_kg*100):.1f}%)
            """)
        
        # Shopping list
        st.markdown("---")
        st.subheader("🛒 Daftar Belanja")
        
        shopping_list = pd.DataFrame({
            'Jenis Pupuk': [fertilizer_type],
            'Ukuran': [bag_size_name],
            'Jumlah': [f"{bags_needed} karung"],
            'Total (kg)': [f"{total_kg:.1f} kg"],
            'Harga/karung': [f"Rp {cost_per_bag:,.0f}"],
            'Total Biaya': [f"Rp {total_cost:,.0f}"]
        })
        
        st.dataframe(shopping_list, use_container_width=True, hide_index=True)
        
        # Tips
        if excess_kg > bag_size * 0.5:
            st.warning(f"⚠️ **Perhatian:** Kelebihan pupuk cukup banyak ({excess_kg:.1f} kg). Pertimbangkan untuk menyimpan dengan baik atau gunakan untuk aplikasi berikutnya.")
        
        if excess_kg < bag_size * 0.1:
            st.success(f"✅ **Efisien:** Kelebihan pupuk minimal ({excess_kg:.1f} kg). Pembelian sudah optimal!")

else:  # From Calculator
    st.info("💡 **Fitur ini akan terintegrasi dengan Kalkulator Pupuk**")
    st.markdown("""
    Anda bisa langsung menggunakan hasil dari **Kalkulator Pupuk Holistik** untuk konversi otomatis.
    
    **Cara menggunakan:**
    1. Buka halaman **Kalkulator Pupuk**
    2. Hitung kebutuhan pupuk untuk tanaman Anda
    3. Hasil akan otomatis tersedia di sini untuk konversi
    
    *Fitur ini akan segera tersedia!*
    """)


    elif menu == "🚚 Logistik & Armada":
        st.subheader("🚚 Perencanaan Logistik & Armada")
        st.info("💡 Hitung kapasitas armada untuk angkutan pupuk curah (organik) maupun karungan.")
        
        col_l, col_r = st.columns([1, 1])
        
        with col_l:
            st.markdown("##### 📦 Data Muatan")
            fert_choice = st.selectbox("Pilih Jenis Pupuk", options=list(FERTILIZER_DATABASE.keys()))
            is_organic = FERTILIZER_DATABASE[fert_choice]['type'] == 'organik'
            
            if is_organic:
                calc_mode = st.radio("Mode Input", ["Berat (kg/ton)", "Volume (m³)"])
                if calc_mode == "Berat (kg/ton)":
                    total_mass = st.number_input("Total Berat (kg)", min_value=0, value=5000)
                    density = FERTILIZER_DATABASE[fert_choice]['density']
                    total_vol = (total_mass / 1000) / density
                else:
                    total_vol = st.number_input("Total Volume (m³)", min_value=0.0, value=10.0)
                    density = FERTILIZER_DATABASE[fert_choice]['density']
                    total_mass = total_vol * density * 1000
            else:
                total_mass = st.number_input("Total Berat (kg)", min_value=0, value=2000)
                total_vol = (total_mass / 1000) * 0.8 # Generic density for bags
                
        with col_r:
            st.markdown("##### 🚛 Kapasitas Armada")
            transport_choice = st.selectbox("Pilih Armada", options=list(TRANSPORT_PROFILES.keys()))
            profile = TRANSPORT_PROFILES[transport_choice]
            
            # Calculations
            truck_vol_cap = profile['vol']
            truck_mass_cap = profile['weight']
            
            # Limiting factor
            trips_by_vol = total_vol / truck_vol_cap
            trips_by_mass = total_mass / truck_mass_cap
            num_trips = int(max(trips_by_vol, trips_by_mass)) + (1 if max(trips_by_vol, trips_by_mass) % 1 > 0 else 0)
            
            total_logistics_cost = num_trips * local_transport_cost
            
        st.markdown("---")
        # Visual breakdown
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Volume Total</div>
                <div class="kpi-value">{total_vol:.1f} m³</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Jumlah Trip</div>
                <div class="kpi-value">{profile['icon']} {num_trips} Trip</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Total Logistik</div>
                <div class="kpi-value">Rp {total_logistics_cost:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
        <div class="glass-card" style="margin-top:20px;">
            <b>Analisis Pemuatan ({transport_choice}):</b><br>
            - Kebutuhan Volume: {total_vol:.2f} m³ / Kapasitas: {truck_vol_cap} m³ ({(total_vol/num_trips/truck_vol_cap*100):.1f}% efisiensi vol per trip)<br>
            - Kebutuhan Berat: {total_mass/1000:.2f} Ton / Kapasitas: {truck_mass_cap/1000} Ton ({(total_mass/num_trips/truck_mass_cap*100):.1f}% efisiensi berat per trip)
        </div>
        """, unsafe_allow_html=True)

    elif menu == "💰 ROI Harga Satuan":
        st.subheader("💰 Analisis Efisiensi Biaya per Satuan Hara")
        st.markdown("Menganalisis pupuk mana yang memberikan **Nilai Terbaik** untuk uang Anda berdasarkan kandungan hara murninya.")
        
        roi_data = []
        for name, info in FERTILIZER_DATABASE.items():
            total_nutrients = info['N'] + info['P'] + info['K']
            if total_nutrients > 0:
                cost_per_kg_nutrient = (info['price'] / total_nutrients) * 100
                roi_data.append({
                    "Pupuk": name,
                    "Nutrisi Total (%)": f"{total_nutrients}%",
                    "Harga/kg": info['price'],
                    "Harga per kg Hara Murni": round(cost_per_kg_nutrient, 0)
                })
        
        df_roi = pd.DataFrame(roi_data).sort_values("Harga per kg Hara Murni")
        
        st.write("---")
        st.table(df_roi)
        
        st.success("✅ **Tips:** Pupuk di bagian atas daftar memiliki biaya per unit hara paling rendah (paling hemat).")

    elif menu == "📦 Riwayat Belanja":
        st.subheader("📦 Pencatatan Inventaris & Belanja")
        st.warning("Fitur penyimpanan sedang disiapkan untuk integrasi dengan Buku Kas v2.5.")
        st.info("Hasil konversi Anda saat ini dapat dicetak sebagai PDF atau screenshot sebagai daftar belanja sementara.")

if __name__ == "__main__":
    main()
