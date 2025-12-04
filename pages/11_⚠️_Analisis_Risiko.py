# Analisis Risiko Keberhasilan (AI)
# Logistic Regression model untuk prediksi probabilitas keberhasilan tanam

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Analisis Risiko", page_icon="⚠️", layout="wide")

# ========== ML MODEL ==========
def train_success_model():
    """Train a simple logistic regression model for success prediction"""
    # Synthetic training data (in production, use real historical data)
    np.random.seed(42)
    
    # Features: NPK adequacy (0-1), pH suitability (0-1), water availability (0-1),
    #           weather suitability (0-1), pest control (0-1), experience (years)
    X_train = np.random.rand(1000, 6)
    
    # Success probability based on weighted features
    success_prob = (
        X_train[:, 0] * 0.25 +  # NPK adequacy
        X_train[:, 1] * 0.20 +  # pH suitability
        X_train[:, 2] * 0.20 +  # Water availability
        X_train[:, 3] * 0.15 +  # Weather suitability
        X_train[:, 4] * 0.10 +  # Pest control
        X_train[:, 5] * 0.10    # Experience
    )
    
    # Add some noise
    success_prob += np.random.normal(0, 0.1, 1000)
    success_prob = np.clip(success_prob, 0, 1)
    
    # Binary outcome (1 = success, 0 = failure)
    y_train = (success_prob > 0.6).astype(int)
    
    # Train model
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)
    
    model = LogisticRegression(random_state=42)
    model.fit(X_scaled, y_train)
    
    return model, scaler

def calculate_risk_factors(n_ppm, p_ppm, k_ppm, ph, rainfall, temp, 
                          water_avail, pest_control, experience, crop):
    """Calculate risk factors for the model"""
    
    # NPK adequacy (0-1 scale)
    optimal_npk = {
        "Padi": {"N": 3500, "P": 20, "K": 3000},
        "Jagung": {"N": 4000, "P": 25, "K": 3500},
        "Cabai Merah": {"N": 4500, "P": 30, "K": 4000},
        "Tomat": {"N": 4000, "P": 25, "K": 3500},
    }
    
    opt = optimal_npk.get(crop, {"N": 3500, "P": 20, "K": 3000})
    
    n_adequacy = min(n_ppm / opt["N"], 1.0)
    p_adequacy = min(p_ppm / opt["P"], 1.0)
    k_adequacy = min(k_ppm / opt["K"], 1.0)
    npk_adequacy = (n_adequacy + p_adequacy + k_adequacy) / 3
    
    # pH suitability (0-1 scale)
    if 6.0 <= ph <= 7.0:
        ph_suitability = 1.0
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        ph_suitability = 0.7
    else:
        ph_suitability = 0.4
    
    # Water availability (already 0-1)
    water_map = {"Rendah": 0.3, "Sedang": 0.6, "Tinggi": 1.0}
    water_score = water_map[water_avail]
    
    # Weather suitability (0-1 scale)
    optimal_weather = {
        "Padi": {"rain": 1800, "temp": 27},
        "Jagung": {"rain": 1500, "temp": 26},
        "Cabai Merah": {"rain": 2000, "temp": 26},
        "Tomat": {"rain": 1600, "temp": 24},
    }
    
    opt_weather = optimal_weather.get(crop, {"rain": 1800, "temp": 27})
    
    rain_diff = abs(rainfall - opt_weather["rain"]) / opt_weather["rain"]
    temp_diff = abs(temp - opt_weather["temp"]) / opt_weather["temp"]
    
    weather_suitability = max(0, 1 - (rain_diff + temp_diff) / 2)
    
    # Pest control (already 0-1)
    pest_map = {"Tidak Ada": 0.2, "Minimal": 0.5, "Sedang": 0.7, "Intensif": 1.0}
    pest_score = pest_map[pest_control]
    
    # Experience (0-1 scale, normalized to 10 years max)
    experience_score = min(experience / 10, 1.0)
    
    return np.array([
        npk_adequacy,
        ph_suitability,
        water_score,
        weather_suitability,
        pest_score,
        experience_score
    ])

def get_risk_level(probability):
    """Determine risk level based on success probability"""
    if probability >= 0.8:
        return "Sangat Rendah", "🟢", "#10b981"
    elif probability >= 0.6:
        return "Rendah", "🟡", "#f59e0b"
    elif probability >= 0.4:
        return "Sedang", "🟠", "#f97316"
    else:
        return "Tinggi", "🔴", "#ef4444"

# ========== MAIN APP ==========
st.title("⚠️ Analisis Risiko Keberhasilan (AI)")
st.markdown("**Masukkan parameter rencana tanam untuk mendapatkan analisis probabilitas keberhasilan**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 🤖 Model AI Logistic Regression
    - 📊 Analisis 6 faktor risiko utama
    - 🎯 Probabilitas keberhasilan (0-100%)
    - 💡 Rekomendasi mitigasi risiko
    
    **Parameter yang Dianalisis:**
    1. Kecukupan NPK tanah
    2. Kesesuaian pH
    3. Ketersediaan air/irigasi
    4. Kesesuaian cuaca
    5. Pengendalian hama/penyakit
    6. Pengalaman petani
    
    **Output:**
    - Probabilitas keberhasilan (%)
    - Level risiko (Rendah → Tinggi)
    - Breakdown kontribusi setiap faktor
    - Rekomendasi mitigasi
    """)

# Train model
with st.spinner("Memuat model AI..."):
    model, scaler = train_success_model()

st.success("✅ Model AI siap digunakan!")

# Input Section
st.subheader("📝 Input Parameter Rencana Tanam")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Data Tanah & Lahan**")
    
    crop = st.selectbox(
        "Jenis Tanaman",
        ["Padi", "Jagung", "Cabai Merah", "Tomat"],
        help="Pilih tanaman yang akan ditanam"
    )
    
    n_ppm = st.number_input(
        "Nitrogen Tanah (ppm)",
        min_value=0.0,
        max_value=10000.0,
        value=3000.0,
        step=100.0
    )
    
    p_ppm = st.number_input(
        "Fosfor Tanah (ppm)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )
    
    k_ppm = st.number_input(
        "Kalium Tanah (ppm)",
        min_value=0.0,
        max_value=10000.0,
        value=2500.0,
        step=100.0
    )
    
    ph = st.number_input(
        "pH Tanah",
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1
    )

with col2:
    st.markdown("**Kondisi Lingkungan & Manajemen**")
    
    rainfall = st.number_input(
        "Curah Hujan Tahunan (mm)",
        min_value=0.0,
        max_value=5000.0,
        value=1800.0,
        step=100.0
    )
    
    temp = st.number_input(
        "Suhu Rata-rata (°C)",
        min_value=0.0,
        max_value=50.0,
        value=27.0,
        step=0.5
    )
    
    water_avail = st.selectbox(
        "Ketersediaan Air/Irigasi",
        ["Rendah", "Sedang", "Tinggi"],
        index=1
    )
    
    pest_control = st.selectbox(
        "Tingkat Pengendalian Hama",
        ["Tidak Ada", "Minimal", "Sedang", "Intensif"],
        index=2
    )
    
    experience = st.slider(
        "Pengalaman Bertani (tahun)",
        min_value=0,
        max_value=30,
        value=5,
        step=1
    )

# Analyze button
if st.button("🔍 Analisis Risiko", type="primary", use_container_width=True):
    
    with st.spinner("Menganalisis dengan AI..."):
        # Calculate risk factors
        features = calculate_risk_factors(
            n_ppm, p_ppm, k_ppm, ph, rainfall, temp,
            water_avail, pest_control, experience, crop
        )
        
        # Scale features
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # Predict
        success_prob = model.predict_proba(features_scaled)[0][1]
        success_percentage = success_prob * 100
        
        # Get risk level
        risk_level, risk_icon, risk_color = get_risk_level(success_prob)
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Hasil Analisis AI")
    
    # Main result
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {risk_color}20 0%, {risk_color}40 100%); 
                    padding: 2rem; border-radius: 12px; border: 2px solid {risk_color}; text-align: center;">
            <div style="font-size: 4rem;">{risk_icon}</div>
            <h2 style="color: {risk_color}; margin: 0.5rem 0;">Probabilitas Keberhasilan</h2>
            <h1 style="font-size: 3.5rem; margin: 0.5rem 0; color: {risk_color};">{success_percentage:.1f}%</h1>
            <p style="font-size: 1.2rem; color: #6b7280; margin: 0;">Risiko: {risk_level}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "Prediksi Model",
            "Berhasil" if success_prob >= 0.5 else "Berisiko",
            delta=f"{success_percentage:.1f}%"
        )
    
    with col3:
        confidence = min(abs(success_prob - 0.5) * 200, 100)
        st.metric(
            "Confidence",
            f"{confidence:.0f}%",
            help="Tingkat kepercayaan model terhadap prediksi"
        )
    
    # Factor breakdown
    st.markdown("---")
    st.subheader("📈 Breakdown Faktor Risiko")
    
    factor_names = [
        "Kecukupan NPK",
        "Kesesuaian pH",
        "Ketersediaan Air",
        "Kesesuaian Cuaca",
        "Pengendalian Hama",
        "Pengalaman Petani"
    ]
    
    factor_values = features * 100  # Convert to percentage
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    colors = ['#3b82f6', '#10b981', '#06b6d4', '#f59e0b', '#8b5cf6', '#ec4899']
    
    for i, (name, value, color) in enumerate(zip(factor_names, factor_values, colors)):
        fig.add_trace(go.Bar(
            y=[name],
            x=[value],
            orientation='h',
            marker_color=color,
            text=f"{value:.1f}%",
            textposition='auto',
            name=name
        ))
    
    fig.update_layout(
        title="Kontribusi Setiap Faktor terhadap Keberhasilan",
        xaxis_title="Skor (%)",
        xaxis_range=[0, 105],
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis
    st.markdown("---")
    st.subheader("🔍 Analisis Detail")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Faktor Kuat (>70%):**")
        strong_factors = [(name, val) for name, val in zip(factor_names, factor_values) if val > 70]
        
        if strong_factors:
            for name, val in strong_factors:
                st.success(f"✅ {name}: {val:.1f}%")
        else:
            st.info("Tidak ada faktor dengan skor >70%")
    
    with col2:
        st.markdown("**Faktor Lemah (<50%):**")
        weak_factors = [(name, val) for name, val in zip(factor_names, factor_values) if val < 50]
        
        if weak_factors:
            for name, val in weak_factors:
                st.error(f"⚠️ {name}: {val:.1f}%")
        else:
            st.success("Semua faktor di atas 50%!")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi Mitigasi Risiko")
    
    recommendations = []
    
    # NPK adequacy
    if features[0] < 0.7:
        recommendations.append({
            "priority": "HIGH",
            "factor": "Kecukupan NPK",
            "issue": f"Skor NPK rendah ({features[0]*100:.1f}%)",
            "action": "Aplikasikan pupuk sesuai rekomendasi Kalkulator Pupuk",
            "impact": "Meningkatkan probabilitas +15-20%"
        })
    
    # pH suitability
    if features[1] < 0.7:
        recommendations.append({
            "priority": "MEDIUM",
            "factor": "Kesesuaian pH",
            "issue": f"pH tidak optimal ({features[1]*100:.1f}%)",
            "action": "Lakukan pengapuran atau penambahan bahan organik",
            "impact": "Meningkatkan probabilitas +10-15%"
        })
    
    # Water availability
    if features[2] < 0.6:
        recommendations.append({
            "priority": "HIGH",
            "factor": "Ketersediaan Air",
            "issue": f"Irigasi kurang memadai ({features[2]*100:.1f}%)",
            "action": "Tingkatkan sistem irigasi atau pilih tanaman tahan kering",
            "impact": "Meningkatkan probabilitas +15-25%"
        })
    
    # Weather suitability
    if features[3] < 0.6:
        recommendations.append({
            "priority": "MEDIUM",
            "factor": "Kesesuaian Cuaca",
            "issue": f"Cuaca kurang sesuai ({features[3]*100:.1f}%)",
            "action": "Sesuaikan waktu tanam dengan musim yang tepat",
            "impact": "Meningkatkan probabilitas +10-15%"
        })
    
    # Pest control
    if features[4] < 0.5:
        recommendations.append({
            "priority": "HIGH",
            "factor": "Pengendalian Hama",
            "issue": f"Pengendalian hama lemah ({features[4]*100:.1f}%)",
            "action": "Implementasikan IPM (Integrated Pest Management)",
            "impact": "Meningkatkan probabilitas +10-15%"
        })
    
    # Experience
    if features[5] < 0.5:
        recommendations.append({
            "priority": "LOW",
            "factor": "Pengalaman",
            "issue": f"Pengalaman terbatas ({features[5]*100:.1f}%)",
            "action": "Konsultasi dengan petani berpengalaman atau penyuluh",
            "impact": "Meningkatkan probabilitas +5-10%"
        })
    
    if recommendations:
        # Sort by priority
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        recommendations.sort(key=lambda x: priority_order[x["priority"]])
        
        for rec in recommendations:
            priority_colors = {
                "HIGH": ("#fee2e2", "#dc2626"),
                "MEDIUM": ("#fef3c7", "#f59e0b"),
                "LOW": ("#dbeafe", "#3b82f6")
            }
            
            bg_color, border_color = priority_colors[rec["priority"]]
            
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid {border_color}; margin: 0.5rem 0;">
                <h4 style="margin: 0; color: #1f2937;">
                    {rec["factor"]}
                    <span style="background: {border_color}; color: white; padding: 0.2rem 0.5rem; 
                                 border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">
                        {rec["priority"]}
                    </span>
                </h4>
                <p style="margin: 0.5rem 0;"><strong>Masalah:</strong> {rec["issue"]}</p>
                <p style="margin: 0.5rem 0;"><strong>Aksi:</strong> {rec["action"]}</p>
                <p style="color: #059669; margin: 0;"><strong>Dampak:</strong> {rec["impact"]}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Semua faktor sudah optimal! Lanjutkan dengan rencana tanam Anda.")
    
    # Potential improvement
    st.markdown("---")
    st.subheader("🚀 Potensi Peningkatan")
    
    # Calculate potential if all factors optimal
    optimal_features = np.ones(6)
    optimal_scaled = scaler.transform(optimal_features.reshape(1, -1))
    optimal_prob = model.predict_proba(optimal_scaled)[0][1] * 100
    
    potential_increase = optimal_prob - success_percentage
    
    if potential_increase > 5:
        st.info(f"""
        **Jika semua faktor dioptimalkan:**
        - Probabilitas keberhasilan dapat meningkat menjadi **{optimal_prob:.1f}%**
        - Peningkatan: **+{potential_increase:.1f}%**
        - Implementasikan rekomendasi di atas untuk mencapai potensi maksimal
        """)
    else:
        st.success("✅ Rencana tanam Anda sudah mendekati optimal!")

# Footer
st.markdown("---")
st.caption("""
⚠️ **Disclaimer:** Model AI ini menggunakan Logistic Regression yang dilatih dengan data sintetis untuk demo.
Untuk produksi, model harus dilatih dengan data historical real dari lapangan. Gunakan hasil analisis ini
sebagai referensi, bukan keputusan final. Konsultasikan dengan ahli agronomi untuk keputusan penting.
""")
