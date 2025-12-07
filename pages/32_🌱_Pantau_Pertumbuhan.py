import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 🌱 GROWTH STANDARDS DATABASE (Reference)
# ==========================================
# Ideal Growth Curves (Logistic/Linear Approximations)
# Format: {HST (Day): {Height_cm, Leaves, Stem_mm}}
GROWTH_STANDARDS = {
    "Cabai Merah": {
        "phase_switch": 35, # HST enters Generative
        "targets": {
            10: {"height": 10, "leaves": 5, "stem": 2},
            20: {"height": 25, "leaves": 12, "stem": 4},
            30: {"height": 45, "leaves": 30, "stem": 6},
            40: {"height": 60, "leaves": 80, "stem": 8},
            60: {"height": 90, "leaves": 150, "stem": 12},
            90: {"height": 120, "leaves": 200, "stem": 15}
        }
    },
    "Melon (Premium)": {
        "phase_switch": 25,
        "targets": {
            10: {"height": 15, "leaves": 4, "stem": 3},
            20: {"height": 50, "leaves": 15, "stem": 6},
            30: {"height": 120, "leaves": 25, "stem": 8},
            40: {"height": 180, "leaves": 35, "stem": 10}, # Topping usually at 25-30 leaves
            60: {"height": 200, "leaves": 35, "stem": 12}
        }
    }
}

def get_ideal_value(crop, hst, metric):
    """Interpolate ideal value closest to HST"""
    standards = GROWTH_STANDARDS.get(crop, {}).get("targets", {})
    days = sorted(standards.keys())
    
    if not days: return 0
    
    # Logic Simple: Find closest days (Prev & Next)
    prev_day = days[0]
    next_day = days[-1]
    
    for d in days:
        if d <= hst: prev_day = d
        if d >= hst: 
            next_day = d
            break
            
    val_prev = standards[prev_day].get(metric, 0)
    val_next = standards[next_day].get(metric, 0)
    
    if prev_day == next_day:
        return val_prev
        
    # Linear Interpolation
    slope = (val_next - val_prev) / (next_day - prev_day)
    interpolated = val_prev + slope * (hst - prev_day)
    return interpolated

# ==========================================
# 🧠 AI EVALUATION ENGINE
# ==========================================
def evaluate_growth(crop, hst, height, stem, leaf_color_idx):
    feedback = []
    status = "Normal"
    score = 100
    
    # 1. Height Check
    ideal_h = get_ideal_value(crop, hst, "height")
    if ideal_h > 0:
        dev_h = (height - ideal_h) / ideal_h
        if dev_h < -0.25:
            feedback.append("⚠️ **Kerdil (Stunted):** Tinggi tanaman di bawah standar (-{:.0f}%). Cek kecukupan air dan Nitrogen.".format(abs(dev_h)*100))
            status = "Perlu Perhatian"
            score -= 20
        elif dev_h > 0.30:
            feedback.append("⚠️ **Etiolasi (Kutilang):** Tanaman terlalu tinggi dan kurus. Kemungkinan kurang sinar matahari.")
            status = "Warning"
            score -= 15
        else:
            feedback.append("✅ Tinggi tanaman optimal sesuai umur.")

    # 2. Stem Check (Kekokohan)
    ideal_s = get_ideal_value(crop, hst, "stem")
    if ideal_s > 0 and stem > 0:
        dev_s = (stem - ideal_s) / ideal_s
        if dev_s < -0.20:
             feedback.append("⚠️ **Batang Kecil:** Batang kurang kokoh. Pertimbangkan penambahan Kalium (K) dan Kalsium (Ca).")
             score -= 10
        elif dev_s > 0.20:
             feedback.append("✅ **Batang Kokoh:** Perkembangan vegetatif sangat baik.")
             score += 5

    # 3. Leaf Color (Nitrogen Indicator)
    # Scale 1 (Pale Yellow) to 4 (Dark Green)
    if leaf_color_idx == 1:
        feedback.append("🍂 **Klorosis (Kuning):** Defisiensi Nitrogen parah atau pH tanah bermasalah. Segera aplikasi pupuk daun N tinggi.")
        status = "Kritis"
        score -= 30
    elif leaf_color_idx == 2:
        feedback.append("🍃 **Hijau Muda:** Indikasi kurang Nitrogen. Naikkan dosis pupuk N (Urea/AB Mix).")
        score -= 10
    elif leaf_color_idx == 4:
        feedback.append("🌿 **Hijau Gelap:** Kadar N sangat cukup (mungkin berlebih). Hati-hati serangan hama penghisap.")
    
    return status, score, feedback

# ==========================================
# 🏗️ UI & MAIN PAGE
# ==========================================
st.set_page_config(page_title="Smart Growth Tracker", page_icon="🌱", layout="wide")

def main():
    st.title("🌱 Smart Growth Tracker & AI Evaluator")
    st.markdown("Pantau pertumbuhan tanaman secara presisi dengan analisis AI berdasarkan variabel agronomi komprehensif.")

    # --- SIDEBAR CONFIG ---
    with st.sidebar:
        st.header("⚙️ Konfigurasi Lahan")
        crop_type = st.selectbox("Komoditas", list(GROWTH_STANDARDS.keys()))
        varietas = st.text_input("Varietas", "Misal: Lado F1")
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now() - timedelta(days=20))
        
        hst = (datetime.now().date() - tgl_tanam).days
        st.metric("Umur Tanaman (HST)", f"{hst} Hari")
        
        if st.button("🗑️ Reset Data Log", type="primary"):
            st.session_state.growth_log = []
            st.rerun()

    # --- SESSION STATE ---
    if 'growth_log' not in st.session_state:
        # Dummy Initial Data
        st.session_state.growth_log = [
            {"hst": 10, "height": 12, "leaves": 6, "stem": 2.5, "color": 3, "fruit_qty": 0, "fruit_dia": 0},
            {"hst": 20, "height": 28, "leaves": 14, "stem": 4.2, "color": 3, "fruit_qty": 0, "fruit_dia": 0},
        ]

    # --- TWO COLUMN LAYOUT ---
    col_input, col_viz = st.columns([1, 2])

    with col_input:
        st.container(border=True)
        st.subheader("📝 Input Jurnal Harian")
        
        # 1. Vegetative Metrics
        st.markdown(f"**Fase: {'Generatif 🍓' if hst > GROWTH_STANDARDS[crop_type]['phase_switch'] else 'Vegetatif 🌿'}**")
        
        in_height = st.number_input("Tinggi Tanaman (cm)", 0.0, 500.0, 0.0, step=0.5)
        in_stem = st.number_input("Diameter Batang (mm)", 0.0, 50.0, 0.0, step=0.1, help="Ukur pangkal batang utama dengan jangka sorong")
        in_leaves = st.number_input("Jumlah Daun (Helai)", 0, 500, 0, step=1)
        
        st.markdown("---")
        in_color = st.select_slider(
            "Warna Daun (Indeks BWD)", 
            options=[1, 2, 3, 4], 
            format_func=lambda x: {1: "1 - Kuning Pucat", 2: "2 - Hijau Muda", 3: "3 - Hijau Normal", 4: "4 - Hijau Gelap/Pekat"}[x]
        )
        
        # 2. Generative Metrics
        if hst > 20: # Show only if relevant
            st.markdown("---")
            c_gen1, c_gen2 = st.columns(2)
            in_fruit_qty = c_gen1.number_input("Jml Bunga/Buah", 0, 100, 0)
            in_fruit_dia = c_gen2.number_input("Diameter Buah (cm)", 0.0, 50.0, 0.0)
        else:
            in_fruit_qty = 0
            in_fruit_dia = 0.0

        # 3. Environment & Input Log
        st.markdown("---")
        with st.expander("Log Perawatan (Opsional)"):
            st.number_input("Input Pupuk (ppm/EC)", 0, 5000, 0)
            st.number_input("Input Air (ml/tanaman)", 0, 5000, 0)
            st.slider("Intensitas Hama (%)", 0, 100, 0, help="Estimasi kerusakan daun")

        if st.button("💾 Simpan Log Harian", use_container_width=True):
            new_entry = {
                "hst": hst,
                "height": in_height,
                "leaves": in_leaves,
                "stem": in_stem,
                "color": in_color,
                "fruit_qty": in_fruit_qty,
                "fruit_dia": in_fruit_dia,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            st.session_state.growth_log.append(new_entry)
            st.success("Data berhasil disimpan!")
            st.rerun()

    with col_viz:
        st.subheader("📊 Grafik Pertumbuhan Real-Time")
        
        if len(st.session_state.growth_log) > 0:
            df_log = pd.DataFrame(st.session_state.growth_log)
            
            # --- MAIN CHART: HEIGHT vs STANDARD ---
            # Generate Ideal Curve points
            max_hst_log = df_log['hst'].max()
            x_ideal = list(range(1, max(70, max_hst_log + 10)))
            y_ideal_height = [get_ideal_value(crop_type, d, "height") for d in x_ideal]
            
            fig = go.Figure()
            
            # Ideal Line
            fig.add_trace(go.Scatter(x=x_ideal, y=y_ideal_height, mode='lines', name='Standar Ideal', 
                                    line=dict(color='gray', dash='dash', width=1)))
            
            # Actual Data points
            fig.add_trace(go.Scatter(x=df_log['hst'], y=df_log['height'], mode='lines+markers', name='Realisasi Tinggi (cm)',
                                    line=dict(color='#10b981', width=3)))
            
            # Secondary metric (Stem)
            fig.add_trace(go.Scatter(x=df_log['hst'], y=df_log['stem'], mode='lines+markers', name='Diameter Batang (mm)',
                                    line=dict(color='#3b82f6', width=2), yaxis='y2'))

            fig.update_layout(
                title=f"Kurva Pertumbuhan: {crop_type}",
                xaxis_title="Umur Tanaman (HST)",
                yaxis_title="Tinggi (cm)",
                yaxis2=dict(title="Diameter Batang (mm)", overlaying='y', side='right'),
                legend=dict(orientation="h", y=1.1),
                height=400,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # --- AI EVALUATION CARD ---
            if not df_log.empty:
                last_log = df_log.iloc[-1]
                
                status, score, messages = evaluate_growth(
                    crop_type, last_log['hst'], last_log['height'], last_log['stem'], last_log['color']
                )
                
                st.markdown("### 🤖 Evaluasi Kecerdasan Buatan (AI)")
                
                res_col1, res_col2 = st.columns([1, 2])
                with res_col1:
                    # Score Radial Gauge
                    fig_gau = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        title = {'text': "Skor Kesehatan"},
                        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#10b981" if score > 80 else "#f59e0b"}}
                    ))
                    fig_gau.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
                    st.plotly_chart(fig_gau, use_container_width=True)
                    st.markdown(f"**Status: {status}**")
                
                with res_col2:
                    st.info(f"Analisis untuk data HST {last_log['hst']}:")
                    for msg in messages:
                        st.write(msg)
                        
                    # Specific Advice based on Generative phase
                    if last_log['fruit_qty'] > 0:
                        st.write(f"🍓 **Fase Buah:** Terpantau {last_log['fruit_qty']} buah. Pastikan Kalium cukup untuk pembesaran buah.")

        else:
            st.info("Belum ada data. Silakan input jurnal di sebelah kiri.")

if __name__ == "__main__":
    main()
