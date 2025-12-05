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
# 🔗 INTEGRATION MOCK API LAYER
# ==========================================
# Simulating internal APIs from other modules

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

def mock_weather_api(lat, lon):
    """
    Simulates fetching data from Modul 27 (Cuaca Pertanian).
    Returns rain and temp based on location.
    """
    # Mock logic based on lat/lon hash
    np.random.seed(int(lat+lon))
    rain = np.random.randint(1500, 3500)
    temp = np.random.uniform(24.0, 31.0)
    return rain, temp

# ==========================================
# 🧠 AI ENGINE & LOGIC LAYER
# ==========================================

@st.cache_resource
def get_ai_model():
    """Train/Load the AI Model."""
    np.random.seed(42)
    n_samples = 3000
    
    # Feature Engineering: 
    # 0: N, 1: P, 2: K, 3: pH, 4: Rain, 5: Temp, 
    # 6: Organic_Matter_Input (ton/ha), 7: Soil_Texture_Index (0-1), 8: Water_Access
    X = np.random.rand(n_samples, 9)
    
    # Scale to realistic agronomic ranges
    X[:, 0] = X[:, 0] * 350 + 20     # N: 20-370 kg/ha
    X[:, 1] = X[:, 1] * 120 + 10     # P: 10-130 kg/ha
    X[:, 2] = X[:, 2] * 250 + 20     # K: 20-270 kg/ha
    X[:, 3] = X[:, 3] * 4.5 + 4.0   # pH: 4.0-8.5
    X[:, 4] = X[:, 4] * 3500 + 500  # Rain: 500-4000 mm
    X[:, 5] = X[:, 5] * 20 + 15     # Temp: 15-35 C
    X[:, 6] = X[:, 6] * 20          # Organic Fert: 0-20 ton/ha
    X[:, 7] = X[:, 7]               # Soil Texture: 0-1
    X[:, 8] = X[:, 8]               # Water Access: 0-1

    # Complex Biological Yield Function
    def biological_yield_curve(n, p, k, ph, rain, temp, org, texture, water):
        # Optimal points
        opt_n, opt_p, opt_k = 200, 70, 150
        opt_ph, opt_rain, opt_temp = 6.5, 1800, 27
        
        # Stress factors
        stress_n = 1 - np.exp(-0.012 * n)
        stress_p = 1 - np.exp(-0.04 * p)
        stress_k = 1 - np.exp(-0.015 * k)
        
        # Bell curves
        stress_ph = np.exp(-0.5 * ((ph - opt_ph)/1.2)**2)
        stress_temp = np.exp(-0.5 * ((temp - opt_temp)/5.0)**2)
        
        # Water & Soil Interaction
        effective_water_retention = 0.5 + (0.5 * texture) 
        total_water = (rain * 0.4) + (water * 1000) 
        water_available = total_water * effective_water_retention
        stress_water = 1 - np.exp(-0.0015 * (water_available - 300))
        stress_water = np.clip(stress_water, 0, 1)

        # Organic Fertilizer Bonus
        som_bonus = 1 + (org * 0.015) 
        
        # Base Yield
        base_yield = 12000 
        
        # Combined yield
        algo_yield = base_yield * (stress_n * stress_p * stress_k * stress_ph * stress_temp * stress_water) * som_bonus
        
        # Add random biological variability
        algo_yield += np.random.normal(0, 500, len(n) if isinstance(n, np.ndarray) else 1)
        
        return np.maximum(algo_yield, 0)

    y = biological_yield_curve(X[:,0], X[:,1], X[:,2], X[:,3], X[:,4], X[:,5], X[:,6], X[:,7], X[:,8])

    model = RandomForestRegressor(n_estimators=150, max_depth=14, random_state=42)
    model.fit(X, y)
    return model

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

def optimize_solution(model, target_yield, optimization_mode="Yield", fixed_params={}, price_per_kg=6000):
    COST_N = 15000 
    COST_P = 20000 
    COST_K = 18000
    COST_ORG = 1000 # Rp 1000/kg
    
    # Pest Cost Logic
    p_strat = fixed_params.get('pest_strategy', "IPM (Terpadu)")
    pest_cost_base = 2000000 # 2 Juta per ha base
    pest_cost_total = pest_cost_base * PEST_STRATEGIES[p_strat]['cost_factor']

    best_conditions = None
    best_score = -float('inf')
    
    # Starting point based on weather input or default
    start_rain = fixed_params.get('rain', 2000.0)
    start_temp = fixed_params.get('temp', 27.0)
    
    current_cond = np.array([
        200.0, 60.0, 120.0, 6.5, start_rain, start_temp, 
        fixed_params.get('org_start', 2.0), 
        fixed_params.get('texture', 0.7), 
        0.8 
    ])
    
    iterations = 250
    
    for i in range(iterations):
        test_cond = current_cond.copy()
        mutation = np.random.normal(0, [25, 10, 15, 0.1, 0, 0, 1.0, 0, 0], 9)
        test_cond += mutation
        test_cond = np.clip(test_cond, 
                           [0,0,0,4,500,15,0,0,0], 
                           [400,150,300,8,4000,35,20,1,1]) # Org max 20 ton
        
        # Enforce fixed weather if provided (don't optimize weather, it's a constraint)
        test_cond[4] = start_rain
        test_cond[5] = start_temp
        
        if 'fixed_org' in fixed_params:
             test_cond[6] = fixed_params['fixed_org']
        test_cond[7] = fixed_params.get('texture', 0.7)

        pred_yield = model.predict(test_cond.reshape(1,-1))[0]
        
        # Economic Calculation
        revenue = pred_yield * price_per_kg
        chem_cost = (test_cond[0] * COST_N) + (test_cond[1] * COST_P) + (test_cond[2] * COST_K)
        org_cost = (test_cond[6] * 1000 * COST_ORG)
        total_variable_cost = chem_cost + org_cost + pest_cost_total
        
        profit = revenue - total_variable_cost
        
        if optimization_mode == "Profit":
            score = profit
        else:
            diff = abs(pred_yield - target_yield)
            score = -diff 
            
        if score > best_score:
            best_score = score
            best_conditions = test_cond
            current_cond = test_cond 
            
    final_yield = model.predict(best_conditions.reshape(1,-1))[0]
    return best_conditions, final_yield, pest_cost_total

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
    use_location_data = st.checkbox("📍 Integrasi Modul 27 (Lokasi Saya)", value=False)
    
    if use_location_data:
        # Simulate getting location
        st.info("Mengambil data iklim mikroklimat dari Modul 27...")
        curah_hujan_val, temp_val = mock_weather_api(-6.2, 106.8) # Mock Jakarta coords
        st.success(f"Lokasi Terdeteksi: Rain {curah_hujan_val}mm, Temp {temp_val:.1f}°C")
    else:
        curah_hujan_val = 2000.0
        temp_val = 27.0
        st.caption("Gunakan checkbox di atas untuk data real-time.")
    
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
     st.info("👈 Silakan atur parameter lahan. Aktifkan 'Integrasi Modul' di sidebar untuk hasil lebih akurat.")
else:
    with st.spinner("AI mensimulasikan pertumbuhan, pasar, & risiko..."):
        model = get_ai_model()
        
        fixed_params = {
            'texture': SOIL_TEXTURES[soil_texture_name],
            'fixed_org': organic_dose,
            'pest_strategy': pest_strategy,
            'rain': curah_hujan_val, # From Weather Module logic
            'temp': temp_val
        }
        
        mode_str = "Yield" if "Yield" in optimization_strategy else "Profit"
        
        # Using dynamic market price from Integration
        opt_cond, pred_yield, pest_cost = optimize_solution(model, target_yield_input, mode_str, fixed_params, price_per_kg=market_price)
        
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
st.caption("© 2025 AgriSensa Intelligence Systems | v3.0 Deep Integration (Modul 6, 16, 18, 25, 26, 27)")
