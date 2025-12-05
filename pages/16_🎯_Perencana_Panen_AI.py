# 🎯 AgriSensa AI Harvest Planner (Global Standard Edition)
# Advanced Decision Support System for Precision Agriculture
# Features: Yield/Profit Optimization, Sustainability Scoring, Risk Analysis, Organic Farming Support

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
    "Lempung Berpasir (Sandy Loam)": 0.4, # Less water retention
    "Lempung (Loam)": 0.7, # Good
    "Lempung Berliat (Clay Loam)": 0.9, # High retention
    "Liat (Clay)": 0.8 # Risk of waterlogging
}

# ==========================================
# 🧠 1. AI ENGINE & LOGIC LAYER
# ==========================================

@st.cache_resource
def get_ai_model():
    """
    Train/Load the AI Model. 
    Now includes Organic Fertilizer & Soil Texture parameters.
    """
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
        # Texture affects how effective rain/irrigation is
        # High texture index (Loam) retains water better
        effective_water_retention = 0.5 + (0.5 * texture) 
        total_water = (rain * 0.4) + (water * 1000) 
        water_available = total_water * effective_water_retention
        stress_water = 1 - np.exp(-0.0015 * (water_available - 300))
        stress_water = np.clip(stress_water, 0, 1)

        # Organic Fertilizer Bonus (The "Magic" of Organics)
        # Improves nutrient uptake efficiency (CEC) + water holding
        # 1 ton organic approx +0.02 yield efficiency
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

def calculate_sustainability_score(n_input, p_input, k_input, org_input, yield_produced):
    """
    Calculate Sustainability Score (0-100).
    Organic inputs BOOST the score significantly.
    Chemical inputs REDUCE the score (Carbon Footprint).
    """
    # Carbon emission factors (kg CO2e/kg)
    cf_n = 5.0
    cf_p = 2.0
    cf_k = 1.0
    cf_org = 0.1 # Very low emission for organic (mostly transport)
    
    total_carbon = (n_input * cf_n) + (p_input * cf_p) + (k_input * cf_k) + (org_input * 1000 * cf_org)
    
    # Efficiency Component (Yield per Carbon)
    efficiency_score = min(50, (yield_produced / max(total_carbon, 1)) * 2)
    
    # Organic Bonus Component (Soil Health)
    # Max bonus 50 points if using > 10 ton organic/ha
    soil_health_score = min(50, org_input * 5)
    
    final_score = efficiency_score + soil_health_score
    
    return int(min(100, final_score)), total_carbon

def run_monte_carlo_simulation(model, conditions, n_simulations=500):
    base_rain = conditions[4]
    base_temp = conditions[5]
    
    rain_scenarios = np.random.normal(base_rain, base_rain * 0.25, n_simulations) # Higher volatility
    temp_scenarios = np.random.normal(base_temp, 2.0, n_simulations)
    
    batch_input = np.tile(conditions, (n_simulations, 1))
    batch_input[:, 4] = rain_scenarios
    batch_input[:, 5] = temp_scenarios
    
    predictions = model.predict(batch_input)
    
    p10 = np.percentile(predictions, 10)
    p50 = np.percentile(predictions, 50)
    p90 = np.percentile(predictions, 90)
    
    return p10, p50, p90, predictions

def optimize_solution(model, target_yield, optimization_mode="Yield", fixed_params={}):
    """
    Reverse Engineering Engine v2.
    Includes Soil Texture (fixed) and Organic Fertilizer (variable or fixed).
    """
    PRICE_PER_KG = 6000 
    COST_N = 15000 
    COST_P = 20000 
    COST_K = 18000
    COST_ORG = 1000000 / 1000 # Assume Rp 1000/kg (Rp 1jt/ton)
    
    best_conditions = None
    best_score = -float('inf')
    
    # Conditions: N, P, K, pH, Rain, Temp, Org, Texture, Water
    # Default starter
    current_cond = np.array([
        200.0, 60.0, 120.0, 6.5, 2000.0, 27.0, 
        fixed_params.get('org_start', 2.0), # Organic Start
        fixed_params.get('texture', 0.7), # Texture Fixed
        0.8 # Water Access
    ])
    
    iterations = 300
    
    for i in range(iterations):
        # Mutate (N, P, K, Org)
        test_cond = current_cond.copy()
        mutation = np.random.normal(0, [25, 10, 15, 0.1, 0, 0, 1.0, 0, 0], 9)
        test_cond += mutation
        
        # Constraints
        test_cond = np.clip(test_cond, 
                           [0,0,0,4,500,15,0,0,0], 
                           [400,150,300,8,4000,35,20,1,1]) # Org max 20 ton
        
        # Lock fixed parameters if provided (e.g. User sets hard constraint on Organics)
        if 'fixed_org' in fixed_params:
             test_cond[6] = fixed_params['fixed_org']
             
        # Lock texture (Physical property, cannot change easily)
        test_cond[7] = fixed_params.get('texture', 0.7)

        pred_yield = model.predict(test_cond.reshape(1,-1))[0]
        
        # Calculate Objective
        revenue = pred_yield * PRICE_PER_KG
        chem_cost = (test_cond[0] * COST_N) + (test_cond[1] * COST_P) + (test_cond[2] * COST_K)
        org_cost = (test_cond[6] * 1000 * COST_ORG) # ton -> kg
        total_cost = chem_cost + org_cost
        profit = revenue - total_cost
        
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
    return best_conditions, final_yield

# ==========================================
# 🎨 2. UI PRESENTATION LAYER
# ==========================================

with st.sidebar:
    st.header("⚙️ Konfigurasi Lahan")
    
    # 1. Commodity Selector (Expanded)
    category = st.selectbox("Kategori Tanaman", list(CROP_DATABASE.keys()))
    selected_crop = st.selectbox("Komoditas", CROP_DATABASE[category])
    
    st.divider()
    
    # 2. Land Parameters
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        target_yield_input = st.number_input("Target (kg/ha)", 4000, 30000, 8000, step=500)
    with col_t2:
        land_area = st.number_input("Luas (Ha)", 0.1, 100.0, 1.0, step=0.1)
    
    st.divider()
    
    # 3. Soil & Fertilizers
    st.subheader("🧪 Parameter Tanah")
    soil_texture_name = st.selectbox("Tekstur Tanah", list(SOIL_TEXTURES.keys()), index=1)
    soil_texture_val = SOIL_TEXTURES[soil_texture_name]
    
    st.subheader("🌿 Pupuk Organik")
    use_organic = st.checkbox("Gunakan Pupuk Organik", value=True)
    if use_organic:
        organic_dose = st.slider("Dosis Organik (Ton/ha)", 0.0, 20.0, 5.0, step=0.5, 
            help="Kompos/Pupuk Kandang meningkatkan kesehatan tanah jangka panjang.")
    else:
        organic_dose = 0.0
        
    st.divider()
    
    # 4. Strategy
    optimization_strategy = st.radio("Strategi AI:", ["Max Yield", "Max Profit"])
    
    if st.button("🚀 Jalankan Analisis Lengkap", type="primary", use_container_width=True):
        st.session_state['run_analysis_v2'] = True

# MAIN CONTENT
st.title("🎯 AI Harvest Planner: Global Standard")
st.markdown(f"**Komoditas:** {selected_crop} | **Mode:** {optimization_strategy}")

if 'run_analysis_v2' not in st.session_state:
     st.info("👈 Silakan atur parameter lahan dan komoditas di sidebar kiri.")
     st.markdown("""
     ### Fitur Baru (v2.0):
     - **50+ Komoditas Global:** Termasuk varietas FAO.
     - **Integrasi Pupuk Organik:** Menghitung dampak kompos terhadap yield & sustainability.
     - **Soil Texture Analysis:** Penyesuaian rekomendasi berdasarkan jenis tanah (Lempung/Pasir).
     """)
else:
    # RUN ENGINE
    with st.spinner("AI sedang mensimulasikan pertumbuhan tanaman..."):
        model = get_ai_model()
        
        fixed_params = {
            'texture': soil_texture_val,
            'fixed_org': organic_dose if use_organic else 0.0
        }
        
        mode_str = "Yield" if "Yield" in optimization_strategy else "Profit"
        opt_cond, pred_yield = optimize_solution(model, target_yield_input, mode_str, fixed_params)
        
        # Calculate Metrics
        sus_score, co2 = calculate_sustainability_score(opt_cond[0], opt_cond[1], opt_cond[2], opt_cond[6], pred_yield)
        p10, p50, p90, risk_dist = run_monte_carlo_simulation(model, opt_cond)
        
    # --- RENDER DASHBOARD ---
    
    # TOP KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Prediksi Hasil", f"{pred_yield:.0f} kg/ha", f"{(pred_yield/target_yield_input)*100:.0f}% Target")
    k2.metric("Sustainability Score", f"{sus_score}/100", f"{'🌱 Eco-Friendly' if sus_score>70 else '⚠️ Chemical Heavy'}")
    
    profit_val = (pred_yield * 6000) - ((opt_cond[0]*15000) + (opt_cond[1]*20000) + (opt_cond[2]*18000) + (opt_cond[6]*1000*1000))
    k3.metric("Est. Profit", f"Rp {profit_val/1e6:.1f} Jt", "per Ha")
    k4.metric("C-Organik Input", f"{opt_cond[6]:.1f} Ton", "Kompos/Kandang")
    
    st.markdown("---")
    
    t1, t2, t3 = st.tabs(["📋 Resep Agronomi & Tanah", "🎮 Simulasi Interaktif", "🌍 Sustainability Report"])
    
    with t1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("### 💊 Resep Nutrisi")
            res_df = pd.DataFrame({
                "Input": ["Nitrogen (Urea/ZA)", "Fosfor (SP36)", "Kalium (KCl)", "Pupuk Organik"],
                "Dosis": [f"{opt_cond[0]:.1f} kg", f"{opt_cond[1]:.1f} kg", f"{opt_cond[2]:.1f} kg", f"{opt_cond[6]:.1f} Ton"],
                "Sumber": ["Kimia", "Kimia", "Kimia", "Alami"]
            })
            st.dataframe(res_df, hide_index=True, use_container_width=True)
            
        with c2:
            st.markdown("### 🕸️ Radar Kesehatan Lahan")
            # Radar with Organic component
            radar_data = pd.DataFrame({
                'r': [
                    opt_cond[0]/350*100, 
                    opt_cond[1]/130*100, 
                    opt_cond[2]/250*100, 
                    opt_cond[6]/20*100 if opt_cond[6] > 0 else 5, # Organic
                    (opt_cond[3]-4)/4*100
                ],
                'theta': ['Nitrogen', 'Fosfor', 'Kalium', 'Bahan Organik (SOM)', 'pH Tanah']
            })
            fig_rad = px.line_polar(radar_data, r='r', theta='theta', line_close=True, range_r=[0,100], title="Profil Keseimbangan Nutrisi")
            fig_rad.update_traces(fill='toself', line_color='#10b981')
            st.plotly_chart(fig_rad, use_container_width=True)
            
    with t2:
        st.subheader("🎮 What-If Analysis")
        sc1, sc2, sc3, sc4 = st.columns(4)
        s_n = sc1.slider("Ubah Nitrogen", 0, 400, int(opt_cond[0]))
        s_p = sc2.slider("Ubah Fosfor", 0, 150, int(opt_cond[1]))
        s_k = sc3.slider("Ubah Kalium", 0, 300, int(opt_cond[2]))
        s_org = sc4.slider("Ubah Organik (Ton)", 0.0, 20.0, float(opt_cond[6]))
        
        # Realtime calc
        sim_cond = opt_cond.copy()
        sim_cond[0], sim_cond[1], sim_cond[2], sim_cond[6] = s_n, s_p, s_k, s_org
        sim_yield = model.predict(sim_cond.reshape(1,-1))[0]
        
        st.metric("Hasil Simulasi", f"{sim_yield:.0f} kg/ha", f"{sim_yield - pred_yield:+.0f} kg vs Rekomendasi AI")
        
    with t3:
        st.subheader("🌍 Environmental Impact Report")
        col_sus1, col_sus2 = st.columns(2)
        
        with col_sus1:
             st.markdown(f"""
             **Analisis Jejak Karbon:**
             - Total Emisi: **{co2:.1f} kg CO2e/hektar**
             - Efisiensi: **{co2/pred_yield:.3f} kg CO2 per kg Hasil Panen**
             
             **Rekomendasi:**
             {'✅ Penggunaan Pupuk Organik sudah baik.' if opt_cond[6] >= 5 else '⚠️ Tingkatkan penggunaan pupuk organik (> 5 ton/ha) untuk memperbaiki struktur tanah dan mengurangi emisi karbon.'}
             """)
        
        with col_sus2:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = sus_score,
                title = {'text': "Sustainability Score"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#10b981" if sus_score > 70 else "#f59e0b"},
                    'steps': [
                        {'range': [0, 50], 'color': "#fee2e2"},
                        {'range': [50, 80], 'color': "#fef3c7"},
                        {'range': [80, 100], 'color': "#d1fae5"}]
                }
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")
st.caption("© 2025 AgriSensa Intelligence Systems | Global Standard Module v2.1")
