import streamlit as st
import cv2
import numpy as np
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="AgriSensa Vision", page_icon="🛸", layout="wide")

# ==========================================
# 🧠 IMAGE PROCESSING ENGINE
# ==========================================

def calculate_vari(image_array):
    """
    VARI (Visible Atmospherically Resistant Index)
    Formula: (Green - Red) / (Green + Red - Blue)
    Used for estimating vegetation fraction/health using only RGB imagery.
    """
    # Normalize to 0-1 float to avoid overflow
    img = image_array.astype(float) / 255.0
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    
    numerator = G - R
    denominator = G + R - B + 0.00001 # Avoid div by zero
    
    vari = numerator / denominator
    return vari

def detect_plants(image_array, sensitivity, min_area):
    """
    Detect green plants using HSV thresholding and contour detection.
    """
    # Convert to HSV
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    
    # Define Green Range based on sensitivity
    # Sensitivity 0-100 scales the breadth of green detected
    lower_green = np.array([30 - (sensitivity/5), 40, 40])
    upper_green = np.array([90 + (sensitivity/5), 255, 255])
    
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Morphological Clean up
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = []
    output_img = image_array.copy()
    
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_area:
            valid_contours.append(c)
            # Draw contour
            cv2.drawContours(output_img, [c], -1, (255, 0, 0), 2) # Red outline
            # Draw center point
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(output_img, (cX, cY), 5, (255, 255, 0), -1)

    return len(valid_contours), output_img, mask

# ==========================================
# 🖥️ UI LAYOUT
# ==========================================

st.title("🛸 AgriSensa Vision")
st.markdown("""
**Analisis Citra Drone & Udara untuk Pertanian Presisi.**
Upload foto kebun Anda (tampak atas) untuk menghitung populasi tanaman dan analisis indeks kesehatan vegetasi (VARI).
""")

# SIDEBAR CONFIG
with st.sidebar:
    st.header("⚙️ Konfigurasi Vision")
    
    st.info("**1. Parameter Deteksi**")
    sens = st.slider("Sensitivitas Warna Hijau", 0, 100, 50, help="Semakin tinggi, semakin toleran terhadap variasi warna hijau.")
    min_area = st.number_input("Min. Area Tanaman (px)", 10, 5000, 100, step=10, help="Filter noise/bintik kecil.")
    
    st.divider()
    
    st.info("**2. Parameter Visualisasi**")
    heatmap_opacity = st.slider("Opasitas Heatmap", 0.1, 1.0, 0.6)

# MAIN UPLOAD
uploaded_file = st.file_uploader("Upload Foto Udara (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Load Image
    image = Image.open(uploaded_file)
    img_array = np.array(image.convert("RGB"))
    
    # RUN ANALYSIS
    with st.spinner("🤖 AI sedang menganalisa citra..."):
        # 1. Counting Logic
        count, contour_img, mask_img = detect_plants(img_array, sens, min_area)
        
        # 2. VARI Logic
        vari_map = calculate_vari(img_array)
        
    st.success("Analisis Selesai!")
    
    # TABS OUTPUT
    tab1, tab2, tab3 = st.tabs(["📊 Plant Counting", "🌡️ Health Heatmap (VARI)", "📝 Laporan & Detail"])
    
    with tab1:
        st.subheader(f"Hasil Deteksi: {count} Tanaman")
        st.caption("Deteksi berdasarkan segmentasi warna kanopi (Green Canopy Segmentation). Garis Merah = Batas Tanaman.")
        
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(image, caption="Gambar Asli", use_column_width=True)
        with col_img2:
            st.image(contour_img, caption=f"Terdeteksi: {count} Pohon", use_column_width=True)
            
    with tab2:
        st.subheader("Analisis Kesehatan Tanaman (VARI Index)")
        st.markdown("**Hijau = Sehat/Rimbun**, **Kuning/Merah = Stres/Jarang/Tanah**")
        
        # Create Heatmap
        # Normalize VARI for display (typically -1 to 1)
        fig = px.imshow(vari_map, color_continuous_scale='RdYlGn', origin='upper')
        fig.update_layout(coloraxis_showscale=True)
        fig.update_traces(opacity=heatmap_opacity)
        st.plotly_chart(fig, use_container_width=True)
        
        avg_vari = np.mean(vari_map)
        st.metric("Rata-rata Indeks Kesehatan (VARI)", f"{avg_vari:.3f}")
        
    with tab3:
        st.subheader("📋 Ringkasan Analisis")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Populasi", f"{count} pohon")
        c2.metric("Kepadatan Hijau", f"{np.count_nonzero(mask_img)/mask_img.size * 100:.1f}%")
        c3.metric("Skor Kesehatan", "Prima" if avg_vari > 0.2 else "Perlu Perhatian")
        
        st.info("""
        **Tentang Algoritma:**
        - **Counting:** Menggunakan algoritma *Contour Detection* pada spektrum warna HSV. Akurasi bergantung pada kejernihan foto dan jarak tanam (tajuk yang menyatu mungkin dihitung satu).
        - **VARI (Visible Atmospherically Resistant Index):** Metrik standar untuk mengukur fraksi vegetasi menggunakan kamera RGB biasa (tanpa sensor inframerah mahal). Indikator klorofil daun.
        """)
        
else:
    # DEMO STATE
    st.info("👈 Silakan upload foto drone/udara. Belum punya foto? Simak demo di bawah.")
    st.markdown("### 💡 Tips Pengambilan Foto")
    c1, c2, c3 = st.columns(3)
    c1.warning("**Sudut Tegak Lurus**\nAmbil foto *Nadir* (90 derjat ke bawah) agar tajuk pohon terlihat bulat sempurna.")
    c2.warning("**Pencahayaan Merata**\nHindari bayangan pohon yang terlalu panjang (ambil jam 10-14 siang).")
    c3.warning("**Resolusi Cukup**\nPastikan setiap pohon terlihat jelas dan tidak blur.")
