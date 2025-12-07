import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import requests
import time

st.set_page_config(page_title="AgriSensa GIS", page_icon="🛰️", layout="wide")

# ==========================================
# 🔧 UTILITIES & API HANDLERS
# ==========================================

@st.cache_data(ttl=3600)
def get_elevation(lat, lon):
    """Fetch elevation from Open-Elevation API"""
    try:
        url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()['results'][0]['elevation']
    except:
        return None # Fallback logic handled in UI
    return None

@st.cache_data(ttl=300)
def get_weather(lat, lon):
    """Fetch current weather from Open-Meteo"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=precipitation_sum&timezone=auto"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

def analyze_suitability(elevation, temp, lat):
    """Advanced Rule-Based Suitability Engine with Climate Zones"""
    recommendations = []
    warnings = []
    zone_info = ""
    
    # 1. TENTUKAN ZONA IKLIM (Berdasarkan Latitude)
    abs_lat = abs(lat)
    if abs_lat < 23.5:
        climate_zone = "Tropis"
        season = "Sepanjang Tahun (Cek Hujan)"
    elif 23.5 <= abs_lat < 40:
        climate_zone = "Sub-Tropis"
        # Simple season logic
        month = time.localtime().tm_mon
        is_north = lat > 0
        if (month >= 4 and month <= 9):
            season = "Musim Panas" if is_north else "Musim Dingin"
        else:
            season = "Musim Dingin" if is_north else "Musim Panas"
    else:
        climate_zone = "Iklim Sedang/Dingin"
        season = "Variatif (4 Musim)"

    # 2. LOGIKA REKOMENDASI BERDASARKAN ZONA
    if climate_zone == "Tropis":
        # Logika Elevasi (Indonesia Style)
        if elevation < 400:
            zone_info = "Dataran Rendah Tropis"
            suitable = ["Bawang Merah", "Cabai", "Padi Sawah", "Mangga", "Jagung", "Semangka", "Melon", "Pisang"]
            if temp > 33: warnings.append("⚠️ Suhu tinggi ekstrem. Perhatikan stres air.")
        elif 400 <= elevation <= 800:
            zone_info = "Dataran Menengah Tropis"
            suitable = ["Durian", "Alpukat", "Kopi Robusta", "Tomat", "Terong", "Salak", "Lada"]
        else: # > 800
            zone_info = "Dataran Tinggi Tropis"
            suitable = ["Kubis", "Kentang", "Wortel", "Kopi Arabika", "Teh", "Stroberi", "Brokoli"]
    
    elif climate_zone == "Sub-Tropis":
        # Logika Musiman (Jepang, China, Mediterania)
        zone_info = f"Sub-Tropis ({season})"
        
        if "Panas" in season:
            suitable = ["Padi Japonica", "Kedelai", "Teh Hijau", "Jeruk Satsuma", "Sayuran Daun", "Apel (Fase Buah)"]
        else: # Musim Dingin/Sejuk
            suitable = ["Gandum (Winter Wheat)", "Barley", "Bawang Putih", "Bayam", "Komatsuna", "Lobak"]
            if temp < 5: warnings.append("❄️ Risiko beku (frost). Butuh Greenhouse untuk sayuran lunak.")
            
        if elevation > 1000:
            warnings.append("🏔️ Area pegunungan tinggi sub-tropis. Musim tanam sangat pendek.")

    else: # Iklim Sedang/Dingin
        zone_info = "Iklim Sedang (Temperate)"
        suitable = ["Gandum", "Kentang", "Apel", "Anggur", "Bit Gula"]
        if temp < 10: warnings.append("❄️ Suhu terlalu rendah untuk sebagian besar tanaman pangan terbuka.")

    # 3. ANALISIS SUHU LOKAL (Cross-check)
    if temp > 35: warnings.append("🔥 Heat Stress Alert: Bahaya bagi serbuk sari (polinasi).")
    if temp < 15 and climate_zone == "Tropis": warnings.append("❄️ Chilling Injury: Tanaman tropis mungkin melambat pertumbuhannya.")

    return climate_zone, zone_info, suitable, warnings

# ==========================================
# 🖥️ UI LAYOUT
# ==========================================

st.title("🛰️ AgriSensa GIS Intelligence")
st.markdown("Analisis presisi berbasis lokasi: **Klik pada peta** untuk mendapatkan analisis kesesuaian lahan dan data cuaca real-time.")

# SPLIT VIEW
col_map, col_analysis = st.columns([2, 1])

with col_map:
    # BASE MAP
    m = folium.Map(location=[-2.5489, 118.0149], zoom_start=5, tiles="OpenStreetMap") # Centered Indonesia
    
    # ADD MARKER IF CLICKED
    last_click = st.session_state.get("last_click", None)
    if 'clicked_coords' not in st.session_state:
        st.session_state.clicked_coords = None

    # Render Map
    map_data = st_folium(m, height=600, width="100%", returned_objects=["last_clicked"])

# PROCESS CLICK
if map_data and map_data['last_clicked']:
    lat = map_data['last_clicked']['lat']
    lon = map_data['last_clicked']['lng']
    
    # Store in session to persist reload
    st.session_state.clicked_coords = (lat, lon)

# DISPLAY ANALYSIS
with col_analysis:
    if st.session_state.clicked_coords:
        lat, lon = st.session_state.clicked_coords
        
        st.subheader("📍 Analisis Lokasi")
        st.write(f"Koordinat: `{lat:.4f}, {lon:.4f}`")
        
        with st.spinner("Mengambil data satelit..."):
            # 1. FETCH DATA
            elevation = get_elevation(lat, lon)
            weather_data = get_weather(lat, lon)
            
            # Simulated Elevation fallback if API fails
            if elevation is None:
                elevation = 0 # Default low
                st.warning("Gagal mengambil data ketinggian real-time. Menggunakan asumsi dataran rendah.")
            
            # Weather parsers
            temp = 30 # Default
            wind = 0
            is_day = 1
            if weather_data and 'current_weather' in weather_data:
                temp = weather_data['current_weather']['temperature']
                wind = weather_data['current_weather']['windspeed']
                is_day = weather_data['current_weather']['is_day']

            # 2. RUN ENGINE
            climate_zone, zone, rec_crops, warnings = analyze_suitability(elevation, temp, lat)
            
            # 3. DISPLAY RESULTS
            
            # 3. DISPLAY RESULTS & MULTI-DIMENSION ANALYSIS
            
            tab_cuaca, tab_tanah, tab_pasar = st.tabs(["🌤️ Cuaca & Iklim", "🟤 Potensi Tanah", "🏪 Akses Pasar"])
            
            with tab_cuaca:
                # --- WEATHER CARD ---
                st.info(f"**Data Agroklimat Real-time**")
                c_w1, c_w2, c_w3 = st.columns(3)
                c_w1.metric("Suhu", f"{temp}°C")
                c_w2.metric("Angin", f"{wind} km/h")
                c_w3.metric("Elevasi", f"{elevation} mdpl")
                
                st.markdown("### 🌱 Rekomendasi Tanaman")
                st.markdown(f"**Zona: {zone}**")
                
                # Group recommendations for better readability
                col_r1, col_r2 = st.columns(2)
                mid_idx = (len(rec_crops) + 1) // 2
                with col_r1:
                    for crop in rec_crops[:mid_idx]:
                        st.write(f"✅ **{crop}**")
                with col_r2:
                    for crop in rec_crops[mid_idx:]:
                        st.write(f"✅ **{crop}**")
                
                if warnings:
                    st.divider()
                    st.error("⚠️ **Peringatan Agroklimat:**")
                    for w in warnings:
                        st.write(f"- {w}")

            with tab_tanah:
                st.markdown("### 🟤 Estimasi Bio-Fisik Lahan")
                st.caption("Analisis heuristik berdasarkan topografi dan iklim.")
                
                # Heuristic Soil Logic
                soil_ph_est = "5.5 - 6.5"
                soil_tex_est = "Lempung Liat Berpasir"
                moisture_est = "Sedang"
                
                if elevation < 200:
                    soil_tex_est = "Lempung Liat (Alluvial)"
                    moisture_est = "Tinggi (Basah)"
                    if temp > 30: soil_ph_est = "5.0 - 6.0 (Cenderung Asam)"
                elif elevation > 800:
                    soil_tex_est = "Andosol / Vulkanik"
                    moisture_est = "Tinggi (Lembab)"
                    soil_ph_est = "6.0 - 7.0 (Netral)"
                elif temp > 32 and wind > 10:
                    moisture_est = "Rendah (Kering)"
                
                t1, t2, t3 = st.columns(3)
                t1.metric("Prediksi pH", soil_ph_est, help="Perlu koreksi kapur jika < 5.5")
                t2.metric("Est. Tekstur", soil_tex_est)
                t3.metric("Kelembaban", moisture_est)
                
                st.info("ℹ️ **Tips Pengolahan:** Lakukan uji tanah fisik untuk akurasi 100%. Data di atas adalah estimasi geospasial umum.")

            with tab_pasar:
                st.markdown("### 🚛 Analisis Akses & Logistik")
                st.markdown("Simulasi jarak ke infrastruktur pendukung pertanian:")
                
                # Simulated Distance Logic
                dist_market = max(2, int((abs(lat) + abs(lon)) % 15)) # Deterministic simulation
                dist_road = max(0.5, dist_market / 3)
                cost_transport = dist_market * 500 # Rp 500/kg assumption
                
                p1, p2 = st.columns(2)
                p1.metric("Jarak ke Pasar Utama", f"{dist_market} km")
                p1.metric("Jarak ke Jalan Raya", f"{dist_road:.1f} km")
                
                p2.metric("Est. Biaya Angkut", f"Rp {cost_transport:,.0f} /kg")
                p2.metric("Ketersediaan Buruh Tani", "Sedang" if dist_market < 10 else "Terbatas")
                
                if dist_market > 20:
                    st.warning("⚠️ Lokasi cukup terpencil. Disarankan komoditas tahan simpan (Kopi/Lada/Jagung) daripada sayuran segar.")
                else:
                    st.success("✅ Lokasi strategis. Sangat cocok untuk hortikultura segar (Sayur/Buah).")
                    
    else:
        st.info("👈 **Mulai Analisis:**\n\nKlik dimanapun pada peta di sebelah kiri untuk melihat potensi lahan dan data cuaca.")
        st.markdown("""
        **Fitur:**
        - Deteksi Ketinggian Otomatis
        - Data Cuaca Live
        - Rekomendasi Tanaman Adaptif
        """)
