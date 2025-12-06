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
            
            # --- WEATHER CARD ---
            st.info(f"**🌤️ Cuaca Saat Ini**")
            c_w1, c_w2, c_w3 = st.columns(3)
            c_w1.metric("Suhu", f"{temp}°C")
            c_w2.metric("Angin", f"{wind} km/h")
            c_w3.metric("Status", "Siang" if is_day else "Malam")
            
            # --- LAND CARD ---
            st.success(f"**⛰️ Profil Lahan: {climate_zone}**")
            st.caption(f"Zona: {zone}")
            st.metric("Estimasi Ketinggian", f"{elevation} mdpl")
            
            # --- CROP RECOMMENDATION ---
            st.markdown("### 🌱 Rekomendasi Tanaman")
            st.markdown("Berdasarkan data agroklimat lokasi ini, tanaman yang disarankan:")
            
            for crop in rec_crops:
                st.write(f"✅ **{crop}**")
            
            if warnings:
                st.divider()
                st.error("⚠️ **Peringatan Agroklimat:**")
                for w in warnings:
                    st.write(f"- {w}")
                    
    else:
        st.info("👈 **Mulai Analisis:**\n\nKlik dimanapun pada peta di sebelah kiri untuk melihat potensi lahan dan data cuaca.")
        st.markdown("""
        **Fitur:**
        - Deteksi Ketinggian Otomatis
        - Data Cuaca Live
        - Rekomendasi Tanaman Adaptif
        """)
