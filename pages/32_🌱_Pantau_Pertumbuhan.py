import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from PIL import Image

# Import Shared Logic
from services.growth_engine import get_ideal_value, evaluate_growth
from services.crop_service import CropService

def analyze_leaf_color_image(image_file):
    """
    Analyze image to determine BWD Index (1-4)
    Logic: Green Chromatic Coordinate (GCC) = G / (R+G+B)
    """
    try:
        img = Image.open(image_file)
        img = img.convert('RGB')
        
        # Resize for speed
        img = img.resize((150, 150))
        
        # Center crop (50%) to avoid background
        w, h = img.size
        left = w * 0.25
        top = h * 0.25
        right = w * 0.75
        bottom = h * 0.75
        img = img.crop((left, top, right, bottom))
        
        # Average Color
        np_img = np.array(img)
        mean_color = np_img.mean(axis=(0, 1))
        r, g, b = mean_color
        
        total = r + g + b
        if total == 0: return 1
        
        gcc = g / total # Green Chromatic Coordinate
        brightness = total / 3
        
        # Heuristic Thresholds (To be calibrated)
        # BWD 1 (Yellowish): gcc low
        # BWD 4 (Dark Green): gcc high + brightness low (dark)
        
        detected_idx = 3 # Default
        
        if gcc < 0.34:
            detected_idx = 1 # Kuning/Pucat
        elif gcc < 0.38:
            detected_idx = 2 # Hijau Muda
        elif gcc < 0.42:
            detected_idx = 3 # Hijau Normal
        else:
            detected_idx = 4 # Hijau Gelap
            
        return detected_idx, (r, g, b)
    except Exception as e:
        return 3, (0,0,0)

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
        crop_type = st.selectbox("Komoditas", CropService.get_all_crops())
        varietas = st.text_input("Varietas", "Misal: Lado F1")
        tgl_tanam = st.date_input("Tanggal Tanam", datetime.now() - timedelta(days=20))
        
        hst = (datetime.now().date() - tgl_tanam).days
        st.metric("Umur Tanaman (HST)", f"{hst} Hari")
        
        st.divider()
        st.subheader("📁 Manajemen Data")
        
        # Bulk Upload
        uploaded_csv = st.file_uploader("Upload Data CSV (Backup)", type=['csv'])
        if uploaded_csv:
            try:
                df_upload = pd.read_csv(uploaded_csv)
                # Basic validation
                if 'hst' in df_upload.columns and 'height' in df_upload.columns:
                    st.session_state.growth_log = df_upload.to_dict('records')
                    st.success(f"✅ Loaded {len(df_upload)} rows!")
            except Exception as e:
                st.error("Format CSV salah.")
        
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
        # Fetch standard to know phase switch
        std = CropService.get_growth_standards(crop_type)
        phase_switch = std.get('phase_switch', 30) if std else 30
        
        st.markdown(f"**Fase: {'Generatif 🍓' if hst > phase_switch else 'Vegetatif 🌿'}**")
        
        in_height = st.number_input("Tinggi Tanaman (cm)", 0.0, 500.0, 0.0, step=0.5)
        in_stem = st.number_input("Diameter Batang (mm)", 0.0, 50.0, 0.0, step=0.1, help="Ukur pangkal batang utama dengan jangka sorong")
        in_leaves = st.number_input("Jumlah Daun (Helai)", 0, 500, 0, step=1)
        
        st.markdown("---")
        st.markdown("**Analisis Warna Daun (BWD)**")
        
        # Smart Camera / Upload for BWD
        bwd_source = st.radio("Sumber Input:", ["Manual Slider", "📸 Kamera / Upload Foto"], horizontal=True, label_visibility="collapsed")
        
        detected_bwd = 3
        
        if bwd_source == "📸 Kamera / Upload Foto":
            img_file = st.camera_input("Ambil Foto Daun (Close up)")
            if not img_file:
                img_file = st.file_uploader("Atau Upload Foto Daun", type=['jpg','png','jpeg'])
                
            if img_file:
                det_idx, rgb_val = analyze_leaf_color_image(img_file)
                detected_bwd = det_idx
                st.info(f"🤖 AI mendeteksi: **BWD Skala {det_idx}** (R:{rgb_val[0]:.0f} G:{rgb_val[1]:.0f})")
        
        in_color = st.select_slider(
            "Warna Daun (Verifikasi)", 
            options=[1, 2, 3, 4], 
            value=detected_bwd if bwd_source != "Manual Slider" else 3,
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
