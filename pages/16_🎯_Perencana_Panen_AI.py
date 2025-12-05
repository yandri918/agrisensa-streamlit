# 🎯 AgriSensa AI Harvest Planner (Global Standard Edition)
# Advanced Decision Support System for Precision Agriculture
# Features: Yield/Profit Optimization, Sustainability Scoring, Risk Analysis

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

st.set_page_config(page_title="AI Harvest Planner Pro", page_icon="🎯", layout="wide")

# ==========================================
# 🧠 1. AI ENGINE & LOGIC LAYER
# ==========================================

@st.cache_resource
def get_ai_model():
    """
    Train/Load the AI Model. 
    In production, this would load a pre-trained .pkl file.
    Here we generate high-quality synthetic data based on FAO standards.
    """
    np.random.seed(42)
    n_samples = 2000
    
    # Feature Engineering: N, P, K, pH, Rainfall, Temp, Soil_Organic_Matter (SOM), Water_Access
    X = np.random.rand(n_samples, 8)
    
    # Scale to realistic agronomic ranges
    X[:, 0] = X[:, 0] * 300 + 50     # N: 50-350 kg/ha
    X[:, 1] = X[:, 1] * 100 + 10     # P: 10-110 kg/ha
    X[:, 2] = X[:, 2] * 200 + 30     # K: 30-230 kg/ha
    X[:, 3] = X[:, 3] * 4 + 4       # pH: 4.0-8.0
    X[:, 4] = X[:, 4] * 3000 + 500  # Rain: 500-3500 mm
    X[:, 5] = X[:, 5] * 20 + 15     # Temp: 15-35 C
    X[:, 6] = X[:, 6] * 4 + 1       # SOM: 1-5%
    X[:, 7] = X[:, 7]               # Water Access: 0-1 (Index)

    # Complex Non-Linear Yield Function (Simulating biological reponse)
    # Liebig's Law of Minimum approximation
    
    def biological_yield_curve(n, p, k, ph, rain, temp, som, water):
        # Optimal points (generic C3 crop like Rice/Wheat)
        opt_n, opt_p, opt_k = 200, 60, 120
        opt_ph, opt_rain, opt_temp = 6.5, 1500, 27
        
        # Stress factors (0.0 to 1.0)
        stress_n = 1 - np.exp(-0.015 * n)
        stress_p = 1 - np.exp(-0.05 * p)
        stress_k = 1 - np.exp(-0.02 * k)
        
        # Bell curves for environmental factors
        stress_ph = np.exp(-0.5 * ((ph - opt_ph)/1.0)**2)
        stress_temp = np.exp(-0.5 * ((temp - opt_temp)/5.0)**2)
        
        # Water stress (Rain + Irrigation Access)
        effective_water = rain + (water * 1000)
        stress_water = 1 - np.exp(-0.002 * (effective_water - 500))
        stress_water = np.clip(stress_water, 0, 1)

        # SOM Bonus
        som_bonus = 1 + (som * 0.05) 

        # Base Yield Potential (e.g., 10 tons/ha)
        base_yield = 12000 
        
        # Combined yield
        algo_yield = base_yield * (stress_n * stress_p * stress_k * stress_ph * stress_temp * stress_water) * som_bonus
        
        # Add random biological variability
        algo_yield += np.random.normal(0, 500, len(n) if isinstance(n, np.ndarray) else 1)
        
        return np.maximum(algo_yield, 0)

    y = biological_yield_curve(X[:,0], X[:,1], X[:,2], X[:,3], X[:,4], X[:,5], X[:,6], X[:,7])

    model = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42)
    model.fit(X, y)
    return model

def calculate_sustainability_score(n_input, p_input, K_input, yield_produced):
    """
    Calculate Sustainability Score (0-100) based on Carbon Footprint & Efficiency.
    Factors (kg CO2e per kg nutrient): N=5.0, P=2.0, K=1.0 (Approx GlobalGAP)
    """
    carbon_footprint = (n_input * 5.0) + (p_input * 2.0) + (K_input * 1.0)
    
    # Efficiency: kg Yield per kg CO2 emitted
    efficiency = yield_produced / max(carbon_footprint, 1)
    
    # Score logic
    # Benchmark: > 20 kg yield/kg CO2 is excellent (Score 100), < 5 is poor
    score = min(100, (efficiency / 20) * 100)
    
    return int(score), carbon_footprint

def run_monte_carlo_simulation(model, conditions, n_simulations=500):
    """
    Risk Analysis: Simulate yield distribution under weather uncertainty.
    Variability: Rainfall (+- 30%), Temp (+- 2 C)
    """
    base_rain = conditions[4]
    base_temp = conditions[5]
    
    # Generate scenarios
    rain_scenarios = np.random.normal(base_rain, base_rain * 0.2, n_simulations) # 20% volatility
    temp_scenarios = np.random.normal(base_temp, 2.0, n_simulations) # 2 deg volatility
    
    # Prepare batch input
    batch_input = np.tile(conditions, (n_simulations, 1))
    batch_input[:, 4] = rain_scenarios
    batch_input[:, 5] = temp_scenarios
    
    # Predict
    predictions = model.predict(batch_input)
    
    # Calculate Risk Metrics
    prob_success = np.mean(predictions >= conditions[8]) * 100 if len(conditions) > 8 else 0 # simple check
    p10 = np.percentile(predictions, 10) # Worst case (optimistic)
    p50 = np.percentile(predictions, 50) # Expected
    p90 = np.percentile(predictions, 90) # Best case
    
    return p10, p50, p90, predictions

def optimize_solution(model, target_yield, optimization_mode="Yield"):
    """
    Reverse Engineering / Optimization Engine.
    Modes:
    - 'Yield': Achieve target yield regardless of cost.
    - 'Profit': Maximize (Yield * Price) - (Input * Cost).
    """
    # Crop prices & Input costs (Hardcoded for demo, normally from DB)
    PRICE_PER_KG = 6000 # selling price
    COST_N = 15000 # per kg N
    COST_P = 20000 
    COST_K = 18000
    
    best_conditions = None
    best_score = -float('inf')
    
    # Grid Search + Random Walk (Simplified Optimization)
    # Start with standard conditions
    current_cond = np.array([200.0, 60.0, 120.0, 6.5, 2000.0, 27.0, 3.0, 0.8])
    
    iterations = 200
    
    for i in range(iterations):
        # Mutate conditions slightly
        test_cond = current_cond + np.random.normal(0, [20, 5, 10, 0.1, 0, 0, 0, 0], 8)
        test_cond = np.clip(test_cond, [0,0,0,4,500,15,1,0], [400,150,300,8,3500,35,5,1])
        
        pred_yield = model.predict(test_cond.reshape(1,-1))[0]
        
        # Calculate Objective Function
        revenue = pred_yield * PRICE_PER_KG
        cost = (test_cond[0] * COST_N) + (test_cond[1] * COST_P) + (test_cond[2] * COST_K)
        profit = revenue - cost
        
        if optimization_mode == "Profit":
            score = profit
        else: # Yield mode: Minimize difference to target, strictly
            diff = abs(pred_yield - target_yield)
            score = -diff # maximize negative error
            
        # Accept if better
        if score > best_score:
            best_score = score
            best_conditions = test_cond
            current_cond = test_cond # Move center of search
            
    # Final prediction on best
    final_yield = model.predict(best_conditions.reshape(1,-1))[0]
    
    return best_conditions, final_yield

# ==========================================
# 🎨 2. UI PRESENTATION LAYER
# ==========================================

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Konfigurasi Perencanaan")
    
    # Crop Selection (FAO Data)
    selected_crop = st.selectbox("Jenis Komoditas", 
        ["Padi (Inpari 32)", "Jagung Hibrida", "Kedelai (Grobogan)", "Cabai Merah", "Bawang Merah"])
    
    st.divider()
    
    # Input Constraints
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        target_yield_input = st.number_input("Target (kg/ha)", 4000, 15000, 8000, step=500)
    with col_t2:
        land_area = st.number_input("Luas (Ha)", 0.1, 100.0, 1.0, step=0.1)
        
    optimization_strategy = st.radio("Strategi Optimasi AI:", 
        ["Max Yield (Kejar Target)", "Max Profit (Ekonomis)"], 
        help="Max Yield akan memaksimalkan hasil tanpa peduli biaya. Max Profit akan mencari keseimbangan biaya & hasil.")
        
    if st.button("🚀 Jalankan Analisis AI", type="primary", use_container_width=True):
        st.session_state['run_analysis'] = True
    
    st.divider()
    st.info("💡 **Tips:** Mode 'Max Profit' biasanya menyarankan dosis pupuk lebih rendah namun lebih efisien secara ROI.")

# Main Dashboard
st.title("🎯 AI Harvest Planner: Global Standard")
st.markdown("Decision Support System (DSS) untuk perencanaan pertanian presisi berbasis data & risiko.")

if 'run_analysis' not in st.session_state:
    # Landing Page State
    st.markdown("""
    <div style='background-color: #f0f9ff; padding: 20px; border-radius: 10px; border-left: 5px solid #0ea5e9;'>
        <h3>👋 Selamat Datang di Perencana Panen Agrikultur Cerdas</h3>
        <p>Sistem ini menggunakan machine learning untuk melakukan <b>Reverse Engineering</b> kondisi lahan:</p>
        <ol>
            <li>Anda tentukan target hasil (ton/ha).</li>
            <li>AI mencari kombinasi nutrisi & lingkungan yang paling optimal.</li>
            <li>Sistem menganalisis profitabilitas & risiko iklim.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
else:
    # 🏃 EXECUTION STATE
    mode_str = "Yield" if "Yield" in optimization_strategy else "Profit"
    
    with st.spinner(f"AI sedang melakukan iterasi optimasi ({mode_str} Mode)..."):
        model = get_ai_model()
        opt_conditions, pred_yield = optimize_solution(model, target_yield_input, mode_str)
        
        # Calculate derived metrics
        sus_score, co2_emission = calculate_sustainability_score(opt_conditions[0], opt_conditions[1], opt_conditions[2], pred_yield)
        p10, p50, p90, risk_dist = run_monte_carlo_simulation(model, opt_conditions)
    
    # --- RENDER RESULTS ---
    
    # 1. KPI Cards (Top Row)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    achievement_rate = (pred_yield / target_yield_input) * 100
    ach_color = "green" if achievement_rate >= 95 else "orange"
    
    kpi1.metric("Prediksi Hasil Panen", f"{pred_yield:.0f} kg/ha", f"{achievement_rate-100:.1f}% vs Target")
    kpi2.metric("Sustainability Score", f"{sus_score}/100", f"{'🌱 Excellent' if sus_score > 80 else '⚠️ Needs Improvement'}")
    
    profit_est = (pred_yield * 6000) - ((opt_conditions[0]*15000) + (opt_conditions[1]*20000) + (opt_conditions[2]*18000))
    kpi3.metric("Estimasi Profit/Ha", f"Rp {profit_est/1000000:.1f} Jt", "Estimasi Kasar")
    
    risk_level = "Rendah" if (p90-p10)/p50 < 0.2 else "Tinggi"
    kpi4.metric("Risiko Iklim", risk_level, "Volatilitas Hasil")

    st.markdown("---")

    # 2. Tabs Interface for Deep Dive
    tab_recipe, tab_sim, tab_risk, tab_financial = st.tabs([
        "📋 Resep Agronomi (AI)", "🎮 Simulasi 'What-If'", "🎲 Analisis Risiko", "💰 Profibilitas"
    ])
    
    # TAB 1: AGRONOMIC RECIPE
    with tab_recipe:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("### 💊 Resep Nutrisi")
            st.dataframe(pd.DataFrame({
                "Parameter": ["Nitrogen (N)", "Fosfor (P2O5)", "Kalium (K2O)", "Target pH"],
                "Recomendasi": [f"{opt_conditions[0]:.1f} kg/ha", f"{opt_conditions[1]:.1f} kg/ha", f"{opt_conditions[2]:.1f} kg/ha", f"{opt_conditions[3]:.1f}"],
                "Peran": ["Pertumbuhan Daun", "Akar & Bunga", "Kualitas Buah", "Ketersediaan Hara"]
            }), hide_index=True, use_container_width=True)
            
            st.info(f"💡 Rekomendasi ini disesuaikan untuk strategi **{optimization_strategy}**.")
            
        with c2:
            st.markdown("### 🕸️ Keseimbangan Hara (Radar Chart)")
            # Radar chart normalization (0-100% of max reasonable dose)
            radar_data = pd.DataFrame({
                'r': [opt_conditions[0]/350*100, opt_conditions[1]/120*100, opt_conditions[2]/250*100, (opt_conditions[3]-4)/4*100, opt_conditions[6]/5*100],
                'theta': ['Nitrogen', 'Fosfor', 'Kalium', 'pH Tanah', 'Bahan Organik']
            })
            fig_radar = px.line_polar(radar_data, r='r', theta='theta', line_close=True, range_r=[0,100], 
                                     title="Profil Nutrisi Lahan Optimal")
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 100])), showlegend=False)
            fig_radar.update_traces(fill='toself')
            st.plotly_chart(fig_radar, use_container_width=True)

    # TAB 2: INTERACTIVE SIMULATION (The "What-If" Feature)
    with tab_sim:
        st.subheader("🎮 Laboratorium Lahan Virtual")
        st.markdown("Geser slider untuk melihat bagaimana perubahan input mempengaruhi hasil secara **Real-Time**.")
        
        cols_slider = st.columns(3)
        sim_n = cols_slider[0].slider("Nitrogen (kg)", 0, 400, int(opt_conditions[0]))
        sim_p = cols_slider[1].slider("Fosfor (kg)", 0, 150, int(opt_conditions[1]))
        sim_k = cols_slider[2].slider("Kalium (kg)", 0, 300, int(opt_conditions[2]))
        
        # Real-time inference
        sim_conditions = opt_conditions.copy()
        sim_conditions[0] = sim_n
        sim_conditions[1] = sim_p
        sim_conditions[2] = sim_k
        
        sim_yield = model.predict(sim_conditions.reshape(1,-1))[0]
        sim_delta = sim_yield - pred_yield
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Hasil Panen (Skenario)", f"{sim_yield:.0f} kg", f"{sim_delta:+.0f} kg vs AI Optimal")
        with col_res2:
            # Bar chart comparison
            df_comp = pd.DataFrame({
                "Skenario": ["AI Optimal", "Skenario Anda"],
                "Yield": [pred_yield, sim_yield],
                "Color": ["#3b82f6", "#f59e0b"]
            })
            fig_comp = px.bar(df_comp, x="Yield", y="Skenario", orientation='h', color="Skenario", text="Yield")
            st.plotly_chart(fig_comp, use_container_width=True, key="sim_chart")

    # TAB 3: RISK ANALYSIS
    with tab_risk:
        st.subheader("🎲 Simulasi Monte Carlo (500 Skenario Cuaca)")
        st.markdown("Analisis ini memprediksi hasil panen jika cuaca **lebih kering/basah** atau **lebih panas/dingin** dari perkiraan.")
        
        fig_hist = px.histogram(risk_dist, nbins=30, title="Distribusi Probabilitas Hasil Panen",
                               labels={"value": "Hasil Panen (kg/ha)"}, color_discrete_sequence=['#10b981'])
        
        # Add vertical lines for p10, p50, p90
        fig_hist.add_vline(x=p10, line_dash="dash", line_color="red", annotation_text=f"Buruk (P10): {p10:.0f}")
        fig_hist.add_vline(x=p50, line_dash="solid", line_color="blue", annotation_text=f"Ekspektasi: {p50:.0f}")
        fig_hist.add_vline(x=p90, line_dash="dash", line_color="green", annotation_text=f"Terbaik (P90): {p90:.0f}")
        
        st.plotly_chart(fig_hist, use_container_width=True)
        
        st.warning(f"📊 **Interpretasi:** Ada 90% peluang hasil panen di atas **{p10:.0f} kg**, namun sangat kecil kemungkinan melebihi **{p90:.0f} kg**.")

    # TAB 4: FINANCIAL
    with tab_financial:
        st.subheader("💰 Analisis Ekonomi & Ekologi")
        
        f1, f2 = st.columns(2)
        
        with f1:
            # Waterfall chart for costs
            cost_n = opt_conditions[0] * 15000
            cost_p = opt_conditions[1] * 20000
            cost_k = opt_conditions[2] * 18000
            gross_rev = pred_yield * 6000
            
            fig_waterfall = go.Figure(go.Waterfall(
                name = "20", orientation = "v",
                measure = ["relative", "relative", "relative", "total", "relative"],
                x = ["Gross Revenue", "Biaya N", "Biaya P", "Operating Profit", "Biaya K"], # Logic correction for waterfall ordering needed normally, simplified here
                textposition = "outside",
                # Simplified representation for demo
                text = [f"+{gross_rev/1e6:.1f}M", f"-{cost_n/1e6:.1f}M", f"-{cost_p/1e6:.1f}M", "...", f"-{cost_k/1e6:.1f}M"],
                y = [gross_rev, -cost_n, -cost_p, 0, -cost_k], # Placeholder logic
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            
            # Simple Bar Stack instead for stablity
            df_fin = pd.DataFrame({
                "Komponen": ["Pendapatan Kotor", "Biaya Pupuk", "Profit Bersih"],
                "Nilai (Rp)": [gross_rev, cost_n+cost_p+cost_k, profit_est],
                "Type": ["In", "Out", "Net"]
            })
            fig_fin = px.bar(df_fin, x="Komponen", y="Nilai (Rp)", color="Type", text_auto='.2s', 
                            title="Struktur Ekonomi")
            st.plotly_chart(fig_fin, use_container_width=True)
            
        with f2:
            st.markdown("#### 🌍 Jejak Karbon (Sustainability)")
            st.success(f"**Total Emisi:** {co2_emission:.1f} kg CO2e/ha")
            st.markdown(f"""
            - Skor Efisiensi: **{sus_score}/100**
            - Emisi per kg Produk: **{co2_emission/pred_yield:.3f} kg CO2/kg Padi**
            
            *Meningkatkan sustainability score akan membuka peluang pasar ekspor premium.*
            """)

# Footer
st.markdown("---")
st.caption("© 2025 AgriSensa Intelligence Systems | Powered by Advanced Random Forest Regressor & Monte Carlo Engine")
