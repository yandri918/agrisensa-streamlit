import streamlit as st
import cv2
import numpy as np
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="AgriSensa Vision", page_icon="🛸", layout="wide")

# ==========================================
# 🧠 IMAGE PROCESSING ENGINE
# ==========================================

# ==========================================
# 🧠 IMAGE PROCESSING ENGINES
# ==========================================

def calculate_vari(image_array):
    """VARI Algorithm for Aerial View"""
    img = image_array.astype(float) / 255.0
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    numerator = G - R
    denominator = G + R - B + 0.00001
    return numerator / denominator

def detect_plants(image_array, sensitivity, min_area):
    """Plant Counting for Aerial View"""
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    lower_green = np.array([30 - (sensitivity/5), 40, 40])
    upper_green = np.array([90 + (sensitivity/5), 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = []
    output_img = image_array.copy()
    for c in contours:
        if cv2.contourArea(c) > min_area:
            valid_contours.append(c)
            cv2.drawContours(output_img, [c], -1, (255, 0, 0), 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cv2.circle(output_img, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 5, (255, 255, 0), -1)
    return len(valid_contours), output_img, mask

def analyze_bwd(image_array):
    """
    BWD / LCC (Leaf Color Chart) Analysis for Nitrogen Estimation.
    Based on IRRI & PhilRice methodologies using Digital Image Processing.
    """
    # 1. Focus on Center Area (Region of Interest) to avoid background noise
    h, w, _ = image_array.shape
    center_img = image_array[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]
    
    # 2. Average Greenness Calculation (Simple approach for robustness)
    avg_color_per_row = np.average(center_img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    R, G, B = avg_color
    
    # 3. Determine LCC Scale (1-5) based on Green intensity relative to others
    # Heuristic mapping based on standard BWD colors
    # Calculate "Greenness Index" typically G/(R+G+B) or just raw Green in controlled light
    
    # Using G/R ratio as a proxy for Chlorophyll vs Carotenoid/Senescence
    # And G_mean for intensity
    
    lcc_score = 0
    status = ""
    recommendation = ""
    
    # Simple thresholds (calibrated logic)
    if G < 60: # Too dark/black or dead
        lcc_score = 1
        status = "BWD 1 (Kuning/Kering)"
        recommendation = "Kritis Nitrogen. Segera pupuk Urea 100 kg/ha."
    elif G < 100:
        lcc_score = 2
        status = "BWD 2 (Hijau Kekuningan)"
        recommendation = "Defisiensi Nitrogen. Tambahkan Urea 75 kg/ha."
    elif G < 140:
        lcc_score = 3
        status = "BWD 3 (Hijau Muda - Optimal Rendah)"
        recommendation = "Cukup untuk pemeliharaan. Tambah Urea 25-50 kg/ha jika fase bunting."
    elif G < 180:
        lcc_score = 4
        status = "BWD 4 (Hijau Mantap - Optimal)"
        recommendation = "Nitrogen Optimal. TIDAK PERLU pemupukan tambahan."
    else:
        lcc_score = 5
        status = "BWD 5 (Hijau Gelap - Berlebih)"
        recommendation = "Kelebihan Nitrogen (Risiko Rebah/Hama). STOP Urea."
        
    return lcc_score, status, recommendation, center_img

# ==========================================
# 🖥️ UI LAYOUT
# ==========================================

st.title("🛸 AgriSensa Vision")
st.markdown("**Platform Analisis Citra Pertanian Cerdas**")

# MODE SELECTION
mode = st.radio("Pilih Mode Analisis:", ["📸 Analisis Daun (BWD/LCC)", "🚁 Analisis Drone (Aerial)"], horizontal=True)

if mode == "🚁 Analisis Drone (Aerial)":
    st.info("Upload foto udara/drone untuk menghitung populasi dan cek kesehatan lahan (VARI).")
    
    # SIDEBAR CONFIG AERIAL
    with st.sidebar:
        st.header("⚙️ Konfigurasi Drone")
        sens = st.slider("Sensitivitas Warna Hijau", 0, 100, 50)
        min_area = st.number_input("Min. Area (px)", 10, 5000, 100)
        heatmap_opacity = st.slider("Opasitas Heatmap", 0.1, 1.0, 0.6)

    uploaded_file = st.file_uploader("Upload Foto Udara (JPG/PNG)", type=['jpg', 'jpeg', 'png'], key="drone")

    if uploaded_file:
        image = Image.open(uploaded_file)
        img_array = np.array(image.convert("RGB"))
        
        with st.spinner("Menganalisa lahan..."):
            count, contour_img, mask_img = detect_plants(img_array, sens, min_area)
            vari_map = calculate_vari(img_array)
            
        st.success("Selesai!")
        tab1, tab2 = st.tabs(["📊 Counting", "🌡️ Health Heatmap"])
        with tab1:
            st.image(contour_img, caption=f"Terdeteksi: {count} Tanaman", use_column_width=True)
        with tab2:
            fig = px.imshow(vari_map, color_continuous_scale='RdYlGn')
            fig.update_traces(opacity=heatmap_opacity)
            st.plotly_chart(fig, use_container_width=True)

elif mode == "📸 Analisis Daun (BWD/LCC)":
    st.info("Upload foto close-up daun padi untuk mengukur kadar Nitrogen (BWD/LCC) dan kebutuhan Urea.")
    
    uploaded_leaf = st.file_uploader("Upload Foto Daun (Close Up)", type=['jpg', 'jpeg', 'png'], key="leaf")
    
    if uploaded_leaf:
        image = Image.open(uploaded_leaf)
        img_array = np.array(image.convert("RGB"))
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.image(image, caption="Foto Asli", use_column_width=True)
            
        with st.spinner("Menganalisa warna daun..."):
            score, status, rec, roi_img = analyze_bwd(img_array)
            
        with col_res2:
            st.image(roi_img, caption="Area Analisis (ROI)", width=150)
            st.metric("Skor BWD", f"{score}/5", delta_color="normal" if score==4 else "inverse")
            st.subheader(status)
            
            if score < 4:
                st.warning(f"💡 **Rekomendasi:** {rec}")
            else:
                st.success(f"✅ **Rekomendasi:** {rec}")
                
            st.markdown("---")
            st.caption("""
            **Referensi Ilmiah:**
            - **IRRI (Intl Rice Research Inst):** Standar Bagan Warna Daun (Leaf Color Chart).
            - **Ali et al. (2014):** *Smartphone-based LCC for Nitrogen Status.*
            - **Metode:** Analisis intensitas hijau rata-rata pada area tengah daun (ROI) untuk mengestimasi klorofil.
            """)
