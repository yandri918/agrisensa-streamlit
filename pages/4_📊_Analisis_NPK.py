# Analisis NPK Manual
# Input dan analisis data NPK tanah dengan rekomendasi pupuk

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os
from datetime import datetime
import uuid

st.set_page_config(page_title="Analisis NPK", page_icon="📊", layout="wide")

# ========== DATA STORAGE ==========
NPK_ANALYSIS_FILE = "data/npk_analysis_records.json"

def load_records():
    if os.path.exists(NPK_ANALYSIS_FILE):
        with open(NPK_ANALYSIS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_records(records):
    os.makedirs(os.path.dirname(NPK_ANALYSIS_FILE), exist_ok=True)
    with open(NPK_ANALYSIS_FILE, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# ========== ANALYSIS FUNCTIONS ==========
def analyze_npk(n, p, k):
    """Analyze NPK values (all in ppm)"""
    def classify_value(value, low, high):
        if value < low:
            return "Rendah", "🔴", "#ef4444"
        elif value <= high:
            return "Sedang", "🟡", "#f59e0b"
        else:
            return "Tinggi", "🟢", "#10b981"
    
    # Thresholds in ppm
    n_status, n_icon, n_color = classify_value(n, 2000, 5000)
    p_status, p_icon, p_color = classify_value(p, 10, 25)
    k_status, k_icon, k_color = classify_value(k, 2000, 4000)
    
    return {
        'n': {'value': n, 'status': n_status, 'icon': n_icon, 'color': n_color},
        'p': {'value': p, 'status': p_status, 'icon': p_icon, 'color': p_color},
        'k': {'value': k, 'status': k_status, 'icon': k_icon, 'color': k_color}
    }

def get_fertilizer_recommendation(n, p, k, area_ha=1.0):
    """Get fertilizer recommendations based on NPK deficiency"""
    recommendations = []
    fertilizer_needs = {}
    
    # Calculate deficiency (target - current, converted to kg/ha)
    # Assumption: 1 ppm ≈ 2 kg/ha for top 20cm soil
    n_kg_ha = (n * 2) / 1000
    p_kg_ha = (p * 2) / 1000
    k_kg_ha = (k * 2) / 1000
    
    # Target levels (kg/ha)
    target_n = 3.5  # 3500 ppm * 2 / 1000
    target_p = 0.035  # 17.5 ppm * 2 / 1000
    target_k = 3.0  # 3000 ppm * 2 / 1000
    
    # Calculate needs
    n_deficit = max(0, target_n - n_kg_ha) * area_ha
    p_deficit = max(0, target_p - p_kg_ha) * area_ha
    k_deficit = max(0, target_k - k_kg_ha) * area_ha
    
    if n < 2000:
        urea_needed = (n_deficit / 0.46) * 100  # Urea 46% N
        recommendations.append(f"🔹 **Nitrogen Rendah**: Tambahkan {urea_needed:.1f} kg Urea (46% N)")
        fertilizer_needs['Urea'] = urea_needed
    
    if p < 10:
        sp36_needed = (p_deficit / 0.36) * 100  # SP-36 36% P
        recommendations.append(f"🔹 **Fosfor Rendah**: Tambahkan {sp36_needed:.1f} kg SP-36 (36% P)")
        fertilizer_needs['SP-36'] = sp36_needed
    
    if k < 2000:
        kcl_needed = (k_deficit / 0.60) * 100  # KCl 60% K
        recommendations.append(f"🔹 **Kalium Rendah**: Tambahkan {kcl_needed:.1f} kg KCl (60% K)")
        fertilizer_needs['KCl'] = kcl_needed
    
    if not recommendations:
        recommendations.append("✅ **Kandungan NPK sudah baik!** Lakukan pemeliharaan rutin dengan pupuk organik.")
    
    return recommendations, fertilizer_needs

# ========== MAIN APP ==========
st.title("📊 Analisis NPK Manual")
st.markdown("**Input dan analisis data NPK tanah dengan rekomendasi pupuk otomatis**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Langkah-langkah:**
    1. Input hasil uji lab tanah (N, P, K dalam ppm)
    2. Masukkan pH tanah dan jenis tanah
    3. (Opsional) Masukkan luas lahan untuk perhitungan kebutuhan pupuk
    4. Klik "Analisis NPK" untuk melihat hasil
    5. Lihat status NPK dan rekomendasi pupuk
    6. Simpan data untuk tracking historical
    
    **Interpretasi Hasil:**
    - 🔴 **Rendah**: Perlu penambahan pupuk segera
    - 🟡 **Sedang**: Kondisi cukup baik, pemeliharaan rutin
    - 🟢 **Tinggi**: Kondisi sangat baik, hati-hati over-fertilization
    """)

# Input Section
st.subheader("📝 Input Data NPK")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Data NPK Tanah (ppm)**")
    st.caption("Semua nilai dalam satuan ppm (mg/kg) sesuai hasil uji lab")
    
    n_value = st.number_input(
        "Nitrogen (N) ppm",
        min_value=0.0,
        max_value=10000.0,
        value=3000.0,
        step=100.0,
        help="Range normal: 2000-5000 ppm"
    )
    
    p_value = st.number_input(
        "Fosfor (P) ppm",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=1.0,
        help="Range normal: 10-25 ppm"
    )
    
    k_value = st.number_input(
        "Kalium (K) ppm",
        min_value=0.0,
        max_value=10000.0,
        value=2500.0,
        step=100.0,
        help="Range normal: 2000-4000 ppm"
    )

with col2:
    st.markdown("**Informasi Tambahan**")
    
    ph_value = st.number_input(
        "pH Tanah",
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1,
        help="Range ideal: 6.0-7.0"
    )
    
    soil_type = st.selectbox(
        "Jenis Tanah",
        ["Lempung", "Pasir", "Liat", "Humus", "Gambut", "Lempung Berpasir"]
    )
    
    location = st.text_input(
        "Lokasi Lahan",
        placeholder="Contoh: Desa Sukamaju, Kec. Cianjur"
    )
    
    area_ha = st.number_input(
        "Luas Lahan (ha) - untuk rekomendasi pupuk",
        min_value=0.01,
        value=1.0,
        step=0.1,
        format="%.2f"
    )

# Analyze Button
if st.button("🔍 Analisis NPK", type="primary", use_container_width=True):
    
    # Perform analysis
    analysis = analyze_npk(n_value, p_value, k_value)
    recommendations, fertilizer_needs = get_fertilizer_recommendation(n_value, p_value, k_value, area_ha)
    
    st.markdown("---")
    st.subheader("📊 Hasil Analisis NPK")
    
    # NPK Status Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 2px solid {analysis['n']['color']};">
            <div style="font-size: 2rem; text-align: center;">{analysis['n']['icon']}</div>
            <h3 style="text-align: center; color: #1e40af;">Nitrogen (N)</h3>
            <p style="text-align: center; font-size: 2rem; font-weight: 700; color: {analysis['n']['color']};">
                {analysis['n']['value']:.0f} ppm
            </p>
            <p style="text-align: center; color: #6b7280;">Status: <strong>{analysis['n']['status']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 2px solid {analysis['p']['color']};">
            <div style="font-size: 2rem; text-align: center;">{analysis['p']['icon']}</div>
            <h3 style="text-align: center; color: #065f46;">Fosfor (P)</h3>
            <p style="text-align: center; font-size: 2rem; font-weight: 700; color: {analysis['p']['color']};">
                {analysis['p']['value']:.1f} ppm
            </p>
            <p style="text-align: center; color: #6b7280;">Status: <strong>{analysis['p']['status']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                    padding: 1.5rem; border-radius: 12px; border: 2px solid {analysis['k']['color']};">
            <div style="font-size: 2rem; text-align: center;">{analysis['k']['icon']}</div>
            <h3 style="text-align: center; color: #92400e;">Kalium (K)</h3>
            <p style="text-align: center; font-size: 2rem; font-weight: 700; color: {analysis['k']['color']};">
                {analysis['k']['value']:.0f} ppm
            </p>
            <p style="text-align: center; color: #6b7280;">Status: <strong>{analysis['k']['status']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💊 Rekomendasi Pupuk")
    
    for rec in recommendations:
        st.markdown(rec)
    
    if fertilizer_needs:
        st.markdown("---")
        st.subheader("📦 Kebutuhan Pupuk Detail")
        
        total_cost = 0
        for fertilizer, amount in fertilizer_needs.items():
            bags = amount / 50  # Assuming 50kg bags
            
            # Price per kg (approximate)
            prices = {'Urea': 2500, 'SP-36': 3000, 'KCl': 3500}
            cost = amount * prices.get(fertilizer, 3000)
            total_cost += cost
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{fertilizer}", f"{amount:.1f} kg")
            with col2:
                st.metric("Karung (50kg)", f"{bags:.1f} karung")
            with col3:
                st.metric("Estimasi Biaya", f"Rp {cost:,.0f}")
        
        st.success(f"💰 **Total Estimasi Biaya: Rp {total_cost:,.0f}**")

        # Integration Button
        if st.button("🚀 Lanjut ke RAB (Analisis Usaha Tani)", type="primary"):
            st.session_state['rab_context'] = {
                'source': 'Analisis NPK Manual',
                'ph': float(ph_value),
                'texture': soil_type,
                'fertilizer_needs': fertilizer_needs, # {'Urea': 150, ...}
                'area_ha': float(area_ha)
            }
            st.switch_page("pages/28_💰_Analisis_Usaha_Tani.py")
    
    # Visualization
    st.markdown("---")
    st.subheader("📈 Visualisasi NPK")
    
    # Create gauge charts
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Nitrogen', 'Fosfor', 'Kalium'],
        y=[n_value, p_value, k_value],
        marker_color=[analysis['n']['color'], analysis['p']['color'], analysis['k']['color']],
        text=[f"{n_value:.0f} ppm", f"{p_value:.1f} ppm", f"{k_value:.0f} ppm"],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Status NPK Tanah",
        yaxis_title="Nilai (ppm)",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Save option
    st.markdown("---")
    if st.button("💾 Simpan Data Analisis", use_container_width=True):
        record = {
            'id': str(uuid.uuid4()),
            'date': datetime.now().isoformat(),
            'location': location,
            'n_value': n_value,
            'p_value': p_value,
            'k_value': k_value,
            'ph': ph_value,
            'soil_type': soil_type,
            'area_ha': area_ha,
            'analysis': {
                'n_status': analysis['n']['status'],
                'p_status': analysis['p']['status'],
                'k_status': analysis['k']['status']
            },
            'recommendations': recommendations
        }
        
        records = load_records()
        records.append(record)
        save_records(records)
        
        st.success("✅ Data berhasil disimpan!")
        st.balloons()

# Historical Data
st.markdown("---")
st.subheader("📜 Riwayat Analisis")

records = load_records()

if records:
    st.write(f"**Total {len(records)} analisis tersimpan**")
    
    for record in reversed(records[-5:]):  # Show last 5
        with st.expander(f"📊 {record['date'][:10]} - {record.get('location', 'Unknown')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**N:** {record['n_value']:.0f} ppm ({record['analysis']['n_status']})")
                st.write(f"**P:** {record['p_value']:.1f} ppm ({record['analysis']['p_status']})")
                st.write(f"**K:** {record['k_value']:.0f} ppm ({record['analysis']['k_status']})")
            with col2:
                st.write(f"**pH:** {record['ph']}")
                st.write(f"**Jenis Tanah:** {record['soil_type']}")
                st.write(f"**Luas:** {record['area_ha']} ha")
else:
    st.info("Belum ada riwayat analisis. Lakukan analisis dan simpan untuk tracking.")

# Footer
st.markdown("---")
st.caption("💡 Analisis ini berdasarkan standar umum. Untuk rekomendasi spesifik, konsultasikan dengan ahli agronomi.")
