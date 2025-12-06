# 🎯 AgriSensa AI Harvest Planner (Global Standard Edition)
# Advanced Decision Support System for Precision Agriculture
# Features: Yield/Profit Optimization, Sustainability Scoring, Risk Analysis, Deep Integration (Modul 6, 18, 25, 26, 27)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import requests
import sys
import os

# Add root to path to allow importing app.services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.services.ai_farm_service import get_ai_model, optimize_solution

st.set_page_config(page_title="AI Harvest Planner Pro", page_icon="🎯", layout="wide")

# ==========================================
# 🌳 DATA DICTIONARY (CROP DATABASE)
# ==========================================

CROP_DATABASE = {
    "Tanaman Pangan": [
        "Padi (Inpari 32)", "Padi (Ciherang)", "Padi (IR64)", "Padi (Sidenuk)",
        "Jagung Hibrida", "Jagung Manis", "Jagung Pakan",
        "Kedelai (Grobogan)", "Kedelai (Anjasmoro)",
        "Kacang Tanah", "Kacang Hijau", "Ubi Kayu (Singkong)", "Ubi Jalar"
    ],
    "Hortikultura (Sayur)": [
        "Cabai Merah Besar", "Cabai Rawit", "Cabai Keriting",
        "Tomat", "Kentang", "Bawang Merah", "Bawang Putih",
        "Kubis/Kol", "Wortel", "Sawi/Caisim", "Bayam", "Kangkung",
        "Terong", "Timun", "Kacang Panjang", "Brokoli"
    ],
    "Buah-buahan": [
        "Semangka", "Melon", "Pepaya", "Nanas", "Pisang",
        "Jeruk Siam", "Mangga", "Durian", "Alpukat", "Manggis"
    ],
    "Perkebunan": [
        "Kelapa Sawit", "Kopi Arabika", "Kopi Robusta", 
        "Kakao (Cokelat)", "Tebu", "Karet", "Lada", "Cengkeh", "Jambu Mete"
    ]
}

SOIL_TEXTURES = {
    "Lempung Berpasir (Sandy Loam)": 0.4, 
    "Lempung (Loam)": 0.7, 
    "Lempung Berliat (Clay Loam)": 0.9, 
    "Liat (Clay)": 0.8 
}

PEST_STRATEGIES = {
    "Organic (Nabati)": {"cost_factor": 1.0, "risk_reduction": 0.3, "tox_score": 0, "desc": "Ramah lingkungan, risiko hama moderat"},
    "IPM (Terpadu)": {"cost_factor": 1.5, "risk_reduction": 0.6, "tox_score": 20, "desc": "Seimbang, kimia hanya jika perlu"},
    "Konvensional": {"cost_factor": 2.5, "risk_reduction": 0.8, "tox_score": 60, "desc": "Preventif terjadwal, biaya tinggi"},
    "Agresif (Intensif)": {"cost_factor": 4.0, "risk_reduction": 0.95, "tox_score": 100, "desc": "Sangat mahal, risiko hama minimal, bahaya residu"}
}

# ==========================================
# 🔗 INTEGRATION API LAYER (REAL & MOCK)
# ==========================================

def mock_market_price_api(commodity):
    """
    Simulates fetching data from Modul 6 (Analisis Tren Harga).
    Returns a predicted price based on commodity type.
    """
    base_prices = {
        "Padi": 6000, "Jagung": 5000, "Kedelai": 10000,
        "Cabai": 45000, "Bawang": 30000, "Tomat": 12000, "Kentang": 15000,
        "Sawit": 2500, "Kopi": 40000
    }
    
    # Simple fuzzy matching
    price = 6000
    for key, val in base_prices.items():
        if key in commodity:
            price = val
            break
            
    # Add random fluctuation to simulate "Market Trend"
    fluctuation = np.random.uniform(0.9, 1.2)
    predicted_price = int(price * fluctuation)
    
    trend = "Naik 📈" if fluctuation > 1.05 else "Turun 📉" if fluctuation < 0.95 else "Stabil 📊"
    return predicted_price, trend

def get_real_weather_api(lat, lon):
    """
    Fetches REAL data from Open-Meteo API (Same as Modul 27).
    Returns rain (seasonal estimate) and temp (current).
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,rain",
            "daily": "rain_sum,precipitation_probability_max",
            "timezone": "auto"
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # 1. Temperature (Real Current)
            temp = data['current']['temperature_2m']
            
            # 2. Rain (Seasonal Estimate for AI)
            # AI needs "Seasonal Rain (mm)". API gives "Daily Forecast".
            # Logic: Calculate avg daily rain from 7-day forecast -> multiply by season length (e.g. 100 days)
            daily_rain_sums = data['daily']['rain_sum']
            avg_daily_rain = sum(daily_rain_sums) / len(daily_rain_sums)
            
            # Adjust based on season probability
            # If avg is very low (<1mm), likely dry season -> 500-1000mm estimate
            # If avg implies wet season -> 2000-3000mm estimate
            seasonal_rain_est = avg_daily_rain * 120 # Estimate for 4 months season
            
            # Clamp to realistic tropical bounds (Yearly often 2000-4000mm)
            # If forecast says 0 rain (dry week), we don't want 0 seasonal rain.
            # Use 'climate baseline' + forecast anomaly
            baseline_rain = 2000 
            anomaly = (avg_daily_rain - 5) * 100 # Simple shift
            final_rain = max(500, baseline_rain + anomaly)
            
            return int(final_rain), temp
            
    except Exception as e:
        st.error(f"Gagal koneksi Open-Meteo: {e}")
        
    return 2000, 27.0 # Fallback

# ==========================================
# 🧠 AI ENGINE & LOGIC LAYER
# ==========================================

# AI Model & Logic now imported from app.services.ai_farm_service

def calculate_sustainability_score(n_input, p_input, k_input, org_input, yield_produced, pest_strategy):
    """Calculate Sustainability Score (0-100)."""
    # 1. Carbon Logic
    cf_n = 5.0
    cf_p = 2.0
    cf_k = 1.0
    total_carbon = (n_input * cf_n) + (p_input * cf_p) + (k_input * cf_k)
    efficiency_score = min(40, (yield_produced / max(total_carbon, 1)) * 1.5) # Max 40 points
    
    # 2. Pesticide Toxicity Logic
    tox_penalty = PEST_STRATEGIES[pest_strategy]['tox_score'] * 0.4 # Max 40 points penalty
    
    # 3. Organic Bonus Logic
    organic_bonus = min(20, org_input * 2) # Max 20 points
    
    # Final Calculation
    base_score = efficiency_score + organic_bonus + 40 # Base 40
    final_score = base_score - tox_penalty
    
    return int(np.clip(final_score, 0, 100)), total_carbon

def run_monte_carlo_simulation(model, conditions, pest_strategy, n_simulations=500):
    """Simulate yield risks with Monte Carlo."""
    base_rain = conditions[4]
    base_temp = conditions[5]
    
    risk_reduction = PEST_STRATEGIES[pest_strategy]['risk_reduction']
    pesticide_volatility = 0.3 * (1 - risk_reduction) 
    weather_volatility = 0.15 
    
    final_predictions = []
    
    for _ in range(n_simulations):
        # Weather randomization
        rain_sim = np.random.normal(base_rain, base_rain * 0.2)
        temp_sim = np.random.normal(base_temp, 2.0)
        
        # Pest Event
        pest_event = np.random.random() < 0.3 
        pest_damage = 0
        if pest_event:
             damage_potential = np.random.uniform(0.2, 0.6) 
             actual_damage = damage_potential * (1 - risk_reduction)
             pest_damage = actual_damage
             
        sim_input = conditions.copy()
        sim_input[4] = rain_sim
        sim_input[5] = temp_sim
        
        pred = model.predict(sim_input.reshape(1, -1))[0]
        final_yield = pred * (1 - pest_damage)
        final_predictions.append(final_yield)

    final_predictions = np.array(final_predictions)
    
    p10 = np.percentile(final_predictions, 10)
    p50 = np.percentile(final_predictions, 50)
    p90 = np.percentile(final_predictions, 90)
    
    return p10, p50, p90, final_predictions

# optimize_solution now imported from app.services.ai_farm_service

# ==========================================
# 🎨 UI PRESENTATION LAYER
# ==========================================

with st.sidebar:
    st.header("⚙️ Konfigurasi Lahan")
    
    # INTEGRATION: Modul 6 (Market Price)
    category = st.selectbox("Kategori Tanaman", list(CROP_DATABASE.keys()))
    selected_crop = st.selectbox("Komoditas", CROP_DATABASE[category])
    
    # Fetch Dynamic Price
    with st.spinner("Mengambil tren harga pasar..."):
        market_price, market_trend = mock_market_price_api(selected_crop)
    
    st.caption(f"💰 Harga Pasar (Modul 6): **Rp {market_price:,} /kg** ({market_trend})")
    
    st.divider()
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        target_yield_input = st.number_input("Target (kg/ha)", 4000, 30000, 8000, step=500)
    with col_t2:
        land_area = st.number_input("Luas (Ha)", 0.1, 100.0, 1.0, step=0.1)
    
    st.divider()
    
    # INTEGRATION: Modul 27 (Weather)
    st.subheader("🌦️ Kondisi Iklim")
    
    # Check if Modul 27 location exists in Session State
    has_modul_27_loc = 'data_lat' in st.session_state and 'data_lon' in st.session_state
    
    if has_modul_27_loc:
       use_location_data = st.checkbox(f"📍 Gunakan Lokasi Modul 27", value=True)
       st.caption(f"Koordinat: {st.session_state['data_lat']:.4f}, {st.session_state['data_lon']:.4f}")
    else:
       use_location_data = st.checkbox("📍 Integrasi Modul 27 (Lokasi Saya)", value=False)
       if use_location_data:
           st.warning("⚠️ Belum ada lokasi tersimpan di Modul 27. Menggunakan Default (Jakarta).")
    
    if use_location_data:
        # Determine Lat/Lon
        lat = st.session_state.get('data_lat', -6.2088)
        lon = st.session_state.get('data_lon', 106.8456)
        
        # Real API Call
        with st.spinner("Mengambil data Open-Meteo Real-time..."):
            curah_hujan_val, temp_val = get_real_weather_api(lat, lon)
            
        st.success(f"Open-Meteo: Rain Est {curah_hujan_val}mm, Temp {temp_val:.1f}°C")
    else:
        curah_hujan_val = 2000.0
        temp_val = 27.0
        st.caption("Pilih opsi di atas untuk data real.")
    
    st.divider()
    
    st.subheader("🧪 Parameter Tanah")
    soil_texture_name = st.selectbox("Tekstur Tanah", list(SOIL_TEXTURES.keys()), index=1)
    
    st.subheader("🌿 Manajemen Input")
    use_organic = st.checkbox("Pupuk Organik", value=True)
    organic_dose = st.slider("Dosis Organik (Ton/ha)", 0.0, 20.0, 5.0, step=0.5) if use_organic else 0.0
    
    pest_strategy = st.select_slider("Strategi Hama", options=list(PEST_STRATEGIES.keys()), value="IPM (Terpadu)")
    st.caption(f"ℹ️ {PEST_STRATEGIES[pest_strategy]['desc']}")
        
    st.divider()
    
    optimization_strategy = st.radio("Strategi AI:", ["Max Yield", "Max Profit"])
    
    if st.button("🚀 Jalankan Analisis Lengkap", type="primary", use_container_width=True):
        st.session_state['run_analysis_v4'] = True

# MAIN CONTENT
st.title("🎯 AI Harvest Planner: Command Center")
st.markdown(f"**Komoditas:** {selected_crop} | **Harga:** Rp {market_price:,}/kg | **Mode:** {optimization_strategy}")

if 'run_analysis_v4' not in st.session_state:
     st.info("👈 Silakan atur parameter lahan. Aktifkan 'Integrasi Modul 27' di sidebar untuk hasil akurat.")
else:
    with st.spinner("AI mensimulasikan pertumbuhan, pasar, & risiko..."):
        model = get_ai_model()
        
        fixed_params = {
            'texture': SOIL_TEXTURES[soil_texture_name],
            'fixed_org': organic_dose,
            'pest_strategy': pest_strategy,
            'rain': curah_hujan_val, # From Real Weather API
            'temp': temp_val
        }
        
        mode_str = "Yield" if "Yield" in optimization_strategy else "Profit"
        
        # Using dynamic market price from Integration
        # optimize_solution returns a DICTIONARY from shared service now
        opt_result = optimize_solution(model, target_yield_input, mode_str, fixed_params, price_per_kg=market_price)
        
        # Legacy mapping for this file visualization
        opt_cond = [
            opt_result['n_kg'], opt_result['p_kg'], opt_result['k_kg'], 
            0, 0, 0, # Placeholders for pH, Rain, Temp (not needed for visualization array index)
            opt_result['organic_ton']
        ]
        pred_yield = opt_result['predicted_yield']
        pest_cost = opt_result['pest_cost']
        
        sus_score, co2 = calculate_sustainability_score(opt_cond[0], opt_cond[1], opt_cond[2], opt_cond[6], pred_yield, pest_strategy)
        p10, p50, p90, risk_dist = run_monte_carlo_simulation(model, opt_cond, pest_strategy)
        
    # DASHBOARD
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Prediksi Hasil", f"{pred_yield:.0f} kg/ha", f"{(pred_yield/target_yield_input)*100:.0f}% Target")
    k2.metric("Sustainability Score", f"{sus_score}/100", f"{'🌱 Eco-Friendly' if sus_score>70 else '⚠️ Chemical Heavy'}")
    
    # Profit calculation with DYNAMIC Price
    profit_val = (pred_yield * market_price) - ((opt_cond[0]*15000) + (opt_cond[1]*20000) + (opt_cond[2]*18000) + (opt_cond[6]*1000*1000) + pest_cost)
    k3.metric("Est. Profit", f"Rp {profit_val/1e6:.1f} Jt", f"Harga: {market_price}/kg")
    
    k4.metric("Keamanan Hasil (P10)", f"{p10:.0f} kg", "Worst Case Scenario")
    
    st.markdown("---")
    
    t1, t2, t3, t4 = st.tabs(["📋 Resep & Belanja", "🎮 Skenario", "🌍 Sustainability", "⚖️ Neraca Biaya"])
    
    with t1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("### 💊 Resep Input")
            res_df = pd.DataFrame({
                "Parameter": ["Nitrogen", "Fosfor", "Kalium", "Organik", "Pestisida"],
                "Nilai": [f"{opt_cond[0]:.1f} kg", f"{opt_cond[1]:.1f} kg", f"{opt_cond[2]:.1f} kg", f"{opt_cond[6]:.1f} Ton", pest_strategy],
                "Kategori": ["Kimia", "Kimia", "Kimia", "Alami", "Proteksi"]
            })
            st.dataframe(res_df, hide_index=True, use_container_width=True)
            
            st.divider()
            st.markdown("#### 🛍️ Tindakan Lanjut (Integrasi)")
            
            # INTEGRATION: Modul 25 (Fertilizer Catalog)
            if st.button("🛒 Beli Pupuk (Katalog Modul 25)", use_container_width=True):
                st.switch_page("pages/25_🧪_Katalog_Pupuk_Harga.py")
            
            # INTEGRATION: Modul 18 & 26 (Pesticides)
            if "Organic" in pest_strategy:
                if st.button("🌿 Lihat Resep Nabati (Modul 18)", use_container_width=True):
                    st.switch_page("pages/18_🌿_Pestisida_Nabati.py")
            else:
                if st.button("🔬 Cek Bahan Aktif Aman (Modul 26)", use_container_width=True):
                    st.switch_page("pages/26_🔬_Direktori_Bahan_Aktif.py")
            
        with c2:
            radar_data = pd.DataFrame({
                'r': [
                    opt_cond[0]/350*100, 
                    opt_cond[1]/130*100, 
                    opt_cond[2]/250*100, 
                    PEST_STRATEGIES[pest_strategy]['cost_factor']*25, # Protection Intensity
                    opt_cond[6]/20*100 if opt_cond[6] > 0 else 5
                ],
                'theta': ['N', 'P', 'K', 'Proteksi Hama', 'Bahan Organik']
            })
            fig_rad = px.line_polar(radar_data, r='r', theta='theta', line_close=True, range_r=[0,100], title="Profil Input Agronomi")
            fig_rad.update_traces(fill='toself', line_color='#10b981')
            st.plotly_chart(fig_rad, use_container_width=True)

    with t2:
        st.subheader("🎲 Analisis Risiko (Monte Carlo)")
        st.info(f"Strategi **{pest_strategy}** memberikan perlindungan risiko sebesar **{PEST_STRATEGIES[pest_strategy]['risk_reduction']*100:.0f}%** terhadap gagal panen.")
        
        hist_fig = px.histogram(risk_dist, nbins=40, title=f"Distribusi Peluang Hasil (N=500 Simulasi)", 
                               color_discrete_sequence=['#3b82f6'])
        hist_fig.add_vline(x=p10, line_dash="dash", line_color="red", annotation_text="Gagal (P10)")
        hist_fig.add_vline(x=p50, line_dash="solid", line_color="green", annotation_text="Ekspektasi")
        st.plotly_chart(hist_fig, use_container_width=True)

    with t3:
        st.subheader("🌍 Dampak Lingkungan")
        col_env1, col_env2 = st.columns(2)
        with col_env1:
            st.metric("Total Emisi CO2e", f"{co2:.1f} kg/ha")
            st.metric("Toksisitas Pestisida", f"{PEST_STRATEGIES[pest_strategy]['tox_score']}/100", "Indeks Bahaya")
        with col_env2:
            st.warning("Strategi Agresif meningkatkan risiko residu kimia pada produk dan membunuh musuh alami. Di rekomendasikan menggunakan IPM.")
            
    with t4:
        st.subheader("💰 Struktur Biaya")
        costs = {
            "Pupuk Kimia": (opt_cond[0]*15000) + (opt_cond[1]*20000) + (opt_cond[2]*18000),
            "Pupuk Organik": (opt_cond[6]*1000*1000),
            "Pestisida & Hama": pest_cost
        }
        fig_pie = px.pie(values=list(costs.values()), names=list(costs.keys()), title="Breakdown Biaya Operasional")
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.caption("© 2025 AgriSensa Intelligence Systems | v3.1 Real-time Open-Meteo Integration")
