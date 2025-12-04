# Perencana Hasil Panen (AI)
# Reverse engineering: Input target yield, AI generates required land conditions

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

st.set_page_config(page_title="Perencana Hasil Panen", page_icon="🎯", layout="wide")

# ========== AI MODEL ==========
def train_yield_model():
    """Train AI model to predict yield based on conditions"""
    np.random.seed(42)
    
    # Generate synthetic training data (in production, use real historical data)
    n_samples = 1000
    
    # Features: N, P, K, pH, rainfall, temp, water_availability (0-1)
    X = np.random.rand(n_samples, 7)
    
    # Scale features to realistic ranges
    X[:, 0] = X[:, 0] * 5000 + 1000  # N: 1000-6000 ppm
    X[:, 1] = X[:, 1] * 40 + 10      # P: 10-50 ppm
    X[:, 2] = X[:, 2] * 4000 + 1000  # K: 1000-5000 ppm
    X[:, 3] = X[:, 3] * 3 + 5        # pH: 5-8
    X[:, 4] = X[:, 4] * 2000 + 800   # Rainfall: 800-2800 mm
    X[:, 5] = X[:, 5] * 15 + 20      # Temp: 20-35°C
    # X[:, 6] already 0-1 for water availability
    
    # Yield formula (simplified but realistic)
    y = (
        X[:, 0] * 0.8 +      # N contribution
        X[:, 1] * 80 +       # P contribution
        X[:, 2] * 0.6 +      # K contribution
        (7 - abs(X[:, 3] - 6.5)) * 500 +  # pH optimum at 6.5
        X[:, 4] * 1.5 +      # Rainfall contribution
        (30 - abs(X[:, 5] - 27)) * 100 +  # Temp optimum at 27°C
        X[:, 6] * 2000 +     # Water availability
        np.random.normal(0, 500, n_samples)  # Noise
    )
    
    # Ensure positive yields
    y = np.maximum(y, 1000)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)
    
    return model

def reverse_engineer_conditions(model, target_yield, crop, current_conditions=None):
    """
    Reverse engineer: Given target yield, find optimal conditions
    Uses optimization to find conditions that achieve target yield
    """
    
    # Crop-specific optimal ranges (expanded to 12 crops)
    crop_optima = {
        # Tanaman Pangan
        "Padi": {
            "N": (3000, 4000), "P": (18, 25), "K": (2500, 3500),
            "pH": (5.5, 7.0), "rainfall": (1500, 2000), "temp": (24, 30)
        },
        "Jagung": {
            "N": (3500, 5000), "P": (20, 30), "K": (3000, 4000),
            "pH": (5.8, 7.0), "rainfall": (1200, 1800), "temp": (21, 30)
        },
        "Kedelai": {
            "N": (2000, 3000), "P": (25, 40), "K": (2000, 3000),
            "pH": (6.0, 7.0), "rainfall": (1000, 1500), "temp": (23, 30)
        },
        
        # Sayuran
        "Cabai Merah": {
            "N": (4000, 5000), "P": (25, 35), "K": (3500, 4500),
            "pH": (6.0, 7.0), "rainfall": (1500, 2500), "temp": (24, 28)
        },
        "Tomat": {
            "N": (3500, 4500), "P": (20, 30), "K": (3000, 4000),
            "pH": (6.0, 6.8), "rainfall": (1200, 2000), "temp": (20, 27)
        },
        "Kentang": {
            "N": (3500, 5000), "P": (25, 35), "K": (3500, 5000),
            "pH": (5.0, 6.5), "rainfall": (1500, 2000), "temp": (15, 20)
        },
        "Bawang Merah": {
            "N": (2500, 4000), "P": (20, 30), "K": (2500, 3500),
            "pH": (6.0, 7.0), "rainfall": (800, 1500), "temp": (25, 32)
        },
        "Kubis": {
            "N": (3000, 4000), "P": (20, 30), "K": (2500, 3500),
            "pH": (6.0, 7.0), "rainfall": (1000, 1500), "temp": (15, 25)
        },
        
        # Buah-buahan
        "Semangka": {
            "N": (3000, 4000), "P": (20, 30), "K": (3000, 4000),
            "pH": (6.0, 7.0), "rainfall": (1000, 1500), "temp": (24, 30)
        },
        "Melon": {
            "N": (3000, 4000), "P": (20, 30), "K": (3000, 4000),
            "pH": (6.0, 7.0), "rainfall": (1000, 1500), "temp": (25, 30)
        },
        
        # Tanaman Perkebunan
        "Tebu": {
            "N": (4000, 6000), "P": (30, 40), "K": (4000, 5000),
            "pH": (6.0, 7.5), "rainfall": (1500, 2500), "temp": (25, 30)
        },
        "Singkong": {
            "N": (1500, 3000), "P": (10, 20), "K": (2000, 3000),
            "pH": (5.5, 7.0), "rainfall": (1000, 1500), "temp": (25, 30)
        }
    }
    
    optima = crop_optima.get(crop, crop_optima["Padi"])
    
    # Start with optimal conditions
    if current_conditions:
        # Adjust from current
        conditions = np.array([
            current_conditions['N'],
            current_conditions['P'],
            current_conditions['K'],
            current_conditions['pH'],
            current_conditions['rainfall'],
            current_conditions['temp'],
            current_conditions['water']
        ])
    else:
        # Start with crop optima midpoints
        conditions = np.array([
            np.mean(optima['N']),
            np.mean(optima['P']),
            np.mean(optima['K']),
            np.mean(optima['pH']),
            np.mean(optima['rainfall']),
            np.mean(optima['temp']),
            0.8  # High water availability
        ])
    
    # Iterative optimization (simplified gradient descent)
    learning_rate = 0.01
    iterations = 100
    
    for i in range(iterations):
        # Predict current yield
        current_yield = model.predict(conditions.reshape(1, -1))[0]
        
        # Calculate error
        error = target_yield - current_yield
        
        # If close enough, stop
        if abs(error) < 100:
            break
        
        # Adjust conditions (simplified)
        if error > 0:  # Need to increase yield
            conditions[0] += learning_rate * 100  # Increase N
            conditions[1] += learning_rate * 1    # Increase P
            conditions[2] += learning_rate * 80   # Increase K
            conditions[6] = min(1.0, conditions[6] + learning_rate * 0.1)  # Increase water
        else:  # Need to decrease (unlikely)
            conditions[0] -= learning_rate * 100
            conditions[1] -= learning_rate * 1
            conditions[2] -= learning_rate * 80
        
        # Keep within realistic bounds
        conditions[0] = np.clip(conditions[0], 1000, 6000)  # N
        conditions[1] = np.clip(conditions[1], 10, 50)      # P
        conditions[2] = np.clip(conditions[2], 1000, 5000)  # K
        conditions[3] = np.clip(conditions[3], 5, 8)        # pH
        conditions[4] = np.clip(conditions[4], 800, 2800)   # Rainfall
        conditions[5] = np.clip(conditions[5], 20, 35)      # Temp
        conditions[6] = np.clip(conditions[6], 0, 1)        # Water
    
    # Final prediction
    predicted_yield = model.predict(conditions.reshape(1, -1))[0]
    
    return {
        'N': conditions[0],
        'P': conditions[1],
        'K': conditions[2],
        'pH': conditions[3],
        'rainfall': conditions[4],
        'temp': conditions[5],
        'water': conditions[6],
        'predicted_yield': predicted_yield,
        'target_yield': target_yield,
        'achievement': (predicted_yield / target_yield) * 100
    }

def calculate_gap_analysis(current, required):
    """Calculate gap between current and required conditions"""
    gaps = {}
    
    for key in ['N', 'P', 'K', 'pH', 'rainfall', 'temp', 'water']:
        if key in current and key in required:
            gap = required[key] - current[key]
            gap_percent = (gap / current[key] * 100) if current[key] > 0 else 0
            
            gaps[key] = {
                'current': current[key],
                'required': required[key],
                'gap': gap,
                'gap_percent': gap_percent,
                'status': 'Cukup' if abs(gap_percent) < 10 else 'Perlu Penyesuaian'
            }
    
    return gaps

def generate_action_plan(gaps, crop):
    """Generate actionable plan to achieve required conditions"""
    actions = []
    
    # NPK adjustments
    if gaps['N']['gap'] > 100:
        urea_needed = (gaps['N']['gap'] * 2 / 1000) / 0.46  # Convert ppm to kg/ha, then to Urea
        actions.append({
            'priority': 'HIGH',
            'category': 'Pemupukan',
            'action': f"Tambahkan Urea {urea_needed:.1f} kg/ha",
            'reason': f"Nitrogen kurang {gaps['N']['gap']:.0f} ppm",
            'timeline': '0-2 minggu',
            'cost_estimate': f"Rp {urea_needed * 2500:,.0f}"
        })
    
    if gaps['P']['gap'] > 2:
        sp36_needed = (gaps['P']['gap'] * 2 / 1000) / 0.36
        actions.append({
            'priority': 'HIGH',
            'category': 'Pemupukan',
            'action': f"Tambahkan SP-36 {sp36_needed:.1f} kg/ha",
            'reason': f"Fosfor kurang {gaps['P']['gap']:.1f} ppm",
            'timeline': '0-2 minggu',
            'cost_estimate': f"Rp {sp36_needed * 3000:,.0f}"
        })
    
    if gaps['K']['gap'] > 100:
        kcl_needed = (gaps['K']['gap'] * 2 / 1000) / 0.60
        actions.append({
            'priority': 'HIGH',
            'category': 'Pemupukan',
            'action': f"Tambahkan KCl {kcl_needed:.1f} kg/ha",
            'reason': f"Kalium kurang {gaps['K']['gap']:.0f} ppm",
            'timeline': '0-2 minggu',
            'cost_estimate': f"Rp {kcl_needed * 3500:,.0f}"
        })
    
    # pH adjustment
    if abs(gaps['pH']['gap']) > 0.5:
        if gaps['pH']['gap'] > 0:
            actions.append({
                'priority': 'MEDIUM',
                'category': 'Perbaikan Tanah',
                'action': f"Aplikasi kapur pertanian 1-2 ton/ha",
                'reason': f"pH terlalu rendah (perlu naik {gaps['pH']['gap']:.1f})",
                'timeline': '2-4 minggu',
                'cost_estimate': "Rp 2,000,000 - 4,000,000"
            })
        else:
            actions.append({
                'priority': 'MEDIUM',
                'category': 'Perbaikan Tanah',
                'action': f"Aplikasi belerang atau pupuk asam",
                'reason': f"pH terlalu tinggi (perlu turun {abs(gaps['pH']['gap']):.1f})",
                'timeline': '2-4 minggu',
                'cost_estimate': "Rp 1,500,000 - 3,000,000"
            })
    
    # Water management
    if gaps['water']['gap'] > 0.2:
        actions.append({
            'priority': 'HIGH',
            'category': 'Irigasi',
            'action': "Tingkatkan sistem irigasi",
            'reason': f"Ketersediaan air kurang {gaps['water']['gap']*100:.0f}%",
            'timeline': '1-2 bulan',
            'cost_estimate': "Rp 5,000,000 - 15,000,000"
        })
    
    # Rainfall (informational)
    if abs(gaps['rainfall']['gap']) > 200:
        if gaps['rainfall']['gap'] > 0:
            actions.append({
                'priority': 'LOW',
                'category': 'Manajemen Air',
                'action': "Pertimbangkan irigasi tambahan atau penyesuaian waktu tanam",
                'reason': f"Curah hujan kurang {gaps['rainfall']['gap']:.0f} mm/tahun",
                'timeline': 'Musim tanam berikutnya',
                'cost_estimate': "Varies"
            })
    
    # Temperature (informational)
    if abs(gaps['temp']['gap']) > 3:
        actions.append({
            'priority': 'LOW',
            'category': 'Adaptasi',
            'action': "Pertimbangkan varietas yang sesuai dengan suhu lokal",
            'reason': f"Suhu rata-rata berbeda {abs(gaps['temp']['gap']):.1f}°C dari optimal",
            'timeline': 'Musim tanam berikutnya',
            'cost_estimate': "N/A"
        })
    
    # Sort by priority
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    actions.sort(key=lambda x: priority_order[x['priority']])
    
    return actions

# ========== MAIN APP ==========
st.title("🎯 Perencana Hasil Panen (AI)")
st.markdown("**Tentukan target hasil panen, AI akan menyusun resep kondisi lahan yang dibutuhkan**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Konsep Reverse Engineering:**
    - Input: Target hasil panen yang diinginkan
    - AI Process: Machine learning model mencari kombinasi kondisi optimal
    - Output: Resep lengkap kondisi lahan + action plan
    
    **Fitur:**
    - 🤖 AI-powered reverse engineering
    - 📊 Gap analysis (kondisi saat ini vs yang dibutuhkan)
    - 📋 Action plan prioritas (HIGH/MEDIUM/LOW)
    - 💰 Estimasi biaya untuk setiap aksi
    - 📅 Timeline implementasi
    - 📈 Visualisasi perbandingan
    
    **Use Case:**
    - Planning produksi untuk kontrak
    - Target panen untuk ekspor
    - Optimasi profit margin
    - Feasibility study
    """)

# Train model
with st.spinner("Memuat AI model..."):
    model = train_yield_model()

st.success("✅ AI Model siap digunakan!")

# Input Section
st.subheader("📝 Input Target & Kondisi")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Target Hasil Panen**")
    
    crop = st.selectbox(
        "Jenis Tanaman",
        [
            "Padi", "Jagung", "Kedelai",  # Tanaman Pangan
            "Cabai Merah", "Tomat", "Kentang", "Bawang Merah", "Kubis",  # Sayuran
            "Semangka", "Melon",  # Buah
            "Tebu", "Singkong"  # Perkebunan
        ],
        help="Pilih tanaman yang akan ditanam"
    )
    
    target_yield = st.number_input(
        "Target Hasil Panen (kg/ha)",
        min_value=1000,
        max_value=50000,
        value=6000,
        step=500,
        help="Masukkan target hasil panen yang diinginkan"
    )
    
    area_ha = st.number_input(
        "Luas Lahan (ha)",
        min_value=0.1,
        max_value=1000.0,
        value=1.0,
        step=0.1
    )

with col2:
    st.markdown("**Kondisi Lahan Saat Ini (Opsional)**")
    
    use_current = st.checkbox("Saya punya data kondisi saat ini")
    
    if use_current:
        current_n = st.number_input("Nitrogen saat ini (ppm)", 0.0, 10000.0, 2500.0, 100.0)
        current_p = st.number_input("Fosfor saat ini (ppm)", 0.0, 100.0, 15.0, 1.0)
        current_k = st.number_input("Kalium saat ini (ppm)", 0.0, 10000.0, 2000.0, 100.0)
        current_ph = st.number_input("pH saat ini", 0.0, 14.0, 6.0, 0.1)
        current_rainfall = st.number_input("Curah hujan (mm/tahun)", 0.0, 5000.0, 1500.0, 100.0)
        current_temp = st.number_input("Suhu rata-rata (°C)", 0.0, 50.0, 27.0, 0.5)
        current_water = st.select_slider(
            "Ketersediaan air",
            options=["Rendah", "Sedang", "Tinggi"],
            value="Sedang"
        )
        
        water_map = {"Rendah": 0.3, "Sedang": 0.6, "Tinggi": 0.9}
        
        current_conditions = {
            'N': current_n,
            'P': current_p,
            'K': current_k,
            'pH': current_ph,
            'rainfall': current_rainfall,
            'temp': current_temp,
            'water': water_map[current_water]
        }
    else:
        current_conditions = None
        st.info("AI akan mulai dari kondisi optimal standar")

# Analyze button
if st.button("🤖 Buat Resep Kondisi Lahan", type="primary", use_container_width=True):
    
    with st.spinner("AI sedang menghitung kondisi optimal..."):
        # Reverse engineer conditions
        required = reverse_engineer_conditions(model, target_yield, crop, current_conditions)
        
        # Calculate gaps if current conditions provided
        if current_conditions:
            gaps = calculate_gap_analysis(current_conditions, required)
            action_plan = generate_action_plan(gaps, crop)
        else:
            gaps = None
            action_plan = None
    
    # Display Results
    st.markdown("---")
    st.subheader("🎯 Hasil Analisis AI")
    
    # Achievement
    achievement_color = "#10b981" if required['achievement'] >= 95 else "#f59e0b" if required['achievement'] >= 85 else "#ef4444"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: {achievement_color}20; padding: 2rem; border-radius: 12px; 
                    border: 2px solid {achievement_color}; text-align: center;">
            <h3 style="color: {achievement_color}; margin: 0;">Target</h3>
            <h1 style="font-size: 2.5rem; margin: 0.5rem 0;">{target_yield:,.0f}</h1>
            <p style="color: #6b7280; margin: 0;">kg/ha</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {achievement_color}20; padding: 2rem; border-radius: 12px; 
                    border: 2px solid {achievement_color}; text-align: center;">
            <h3 style="color: {achievement_color}; margin: 0;">Prediksi AI</h3>
            <h1 style="font-size: 2.5rem; margin: 0.5rem 0;">{required['predicted_yield']:,.0f}</h1>
            <p style="color: #6b7280; margin: 0;">kg/ha</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: {achievement_color}20; padding: 2rem; border-radius: 12px; 
                    border: 2px solid {achievement_color}; text-align: center;">
            <h3 style="color: {achievement_color}; margin: 0;">Achievement</h3>
            <h1 style="font-size: 2.5rem; margin: 0.5rem 0;">{required['achievement']:.1f}%</h1>
            <p style="color: #6b7280; margin: 0;">dari target</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Required Conditions
    st.markdown("---")
    st.subheader("📋 Resep Kondisi Lahan yang Dibutuhkan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Nutrisi Tanah:**")
        st.write(f"- Nitrogen (N): **{required['N']:.0f} ppm**")
        st.write(f"- Fosfor (P): **{required['P']:.1f} ppm**")
        st.write(f"- Kalium (K): **{required['K']:.0f} ppm**")
        st.write(f"- pH Tanah: **{required['pH']:.1f}**")
    
    with col2:
        st.markdown("**Kondisi Lingkungan:**")
        st.write(f"- Curah Hujan: **{required['rainfall']:.0f} mm/tahun**")
        st.write(f"- Suhu Rata-rata: **{required['temp']:.1f}°C**")
        st.write(f"- Ketersediaan Air: **{required['water']*100:.0f}%**")
    
    # Gap Analysis
    if gaps:
        st.markdown("---")
        st.subheader("📊 Gap Analysis")
        
        # Create comparison dataframe
        comparison_data = []
        for key, data in gaps.items():
            comparison_data.append({
                'Parameter': key.upper(),
                'Saat Ini': f"{data['current']:.1f}",
                'Dibutuhkan': f"{data['required']:.1f}",
                'Gap': f"{data['gap']:+.1f}",
                'Gap (%)': f"{data['gap_percent']:+.1f}%",
                'Status': data['status']
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        # Visualization
        fig = go.Figure()
        
        parameters = list(gaps.keys())
        current_values = [gaps[p]['current'] for p in parameters]
        required_values = [gaps[p]['required'] for p in parameters]
        
        fig.add_trace(go.Bar(
            name='Saat Ini',
            x=parameters,
            y=current_values,
            marker_color='#3b82f6'
        ))
        
        fig.add_trace(go.Bar(
            name='Dibutuhkan',
            x=parameters,
            y=required_values,
            marker_color='#10b981'
        ))
        
        fig.update_layout(
            title="Perbandingan Kondisi Saat Ini vs Dibutuhkan",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Action Plan
    if action_plan:
        st.markdown("---")
        st.subheader("📋 Action Plan untuk Mencapai Target")
        
        if action_plan:
            for i, action in enumerate(action_plan, 1):
                priority_colors = {
                    'HIGH': ('#fee2e2', '#dc2626'),
                    'MEDIUM': ('#fef3c7', '#f59e0b'),
                    'LOW': ('#dbeafe', '#3b82f6')
                }
                
                bg_color, border_color = priority_colors[action['priority']]
                
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 1.5rem; border-radius: 8px; 
                            border-left: 4px solid {border_color}; margin: 1rem 0;">
                    <h4 style="margin: 0; color: #1f2937;">
                        {i}. {action['action']}
                        <span style="background: {border_color}; color: white; padding: 0.2rem 0.5rem; 
                                     border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">
                            {action['priority']}
                        </span>
                    </h4>
                    <p style="margin: 0.5rem 0;"><strong>Kategori:</strong> {action['category']}</p>
                    <p style="margin: 0.5rem 0;"><strong>Alasan:</strong> {action['reason']}</p>
                    <p style="margin: 0.5rem 0;"><strong>Timeline:</strong> {action['timeline']}</p>
                    <p style="color: #059669; margin: 0;"><strong>Estimasi Biaya:</strong> {action['cost_estimate']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Kondisi saat ini sudah mendekati optimal!")
    
    # Financial Projection
    st.markdown("---")
    st.subheader("💰 Proyeksi Finansial")
    
    # Price per kg for different crops
    prices = {
        # Tanaman Pangan
        "Padi": 5000,
        "Jagung": 4500,
        "Kedelai": 8000,
        # Sayuran
        "Cabai Merah": 45000,
        "Tomat": 8000,
        "Kentang": 12000,
        "Bawang Merah": 35000,
        "Kubis": 5000,
        # Buah
        "Semangka": 3500,
        "Melon": 8000,
        # Perkebunan
        "Tebu": 800,
        "Singkong": 2000
    }
    
    price_per_kg = prices.get(crop, 5000)
    total_yield = required['predicted_yield'] * area_ha
    revenue = total_yield * price_per_kg
    
    # Calculate total investment from action plan
    total_investment = 0
    if action_plan:
        for action in action_plan:
            # Extract numeric value from cost estimate
            cost_str = action['cost_estimate'].replace('Rp', '').replace(',', '').replace('.', '').strip()
            try:
                # Handle ranges like "2,000,000 - 4,000,000"
                if '-' in cost_str:
                    costs = cost_str.split('-')
                    avg_cost = (float(costs[0].strip()) + float(costs[1].strip())) / 2
                    total_investment += avg_cost
                elif cost_str != 'Varies' and cost_str != 'N/A':
                    total_investment += float(cost_str)
            except:
                pass
    
    profit = revenue - total_investment
    roi = (profit / total_investment * 100) if total_investment > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Hasil", f"{total_yield:,.0f} kg")
    with col2:
        st.metric("Pendapatan", f"Rp {revenue:,.0f}")
    with col3:
        st.metric("Investasi", f"Rp {total_investment:,.0f}")
    with col4:
        st.metric("ROI", f"{roi:.1f}%")
    
    # Download report
    st.markdown("---")
    if action_plan:
        report_data = pd.DataFrame(action_plan)
        csv = report_data.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Action Plan (CSV)",
            data=csv,
            file_name=f"action_plan_{crop}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.caption("""
🎯 **Perencana Hasil Panen (AI)** - Reverse engineering dengan machine learning untuk mencapai target hasil panen.
Model dilatih dengan data sintetis untuk demo. Untuk produksi, gunakan data historical real dari lapangan.
""")
