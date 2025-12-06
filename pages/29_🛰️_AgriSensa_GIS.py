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

def analyze_suitability(elevation, temp):
    """Simple Rule-Based Suitability Engine"""
    recommendations = []
    warnings = []
    
    # Kategori Dataran
    if elevation < 400:
        zone = "Dataran Rendah"
        suitable = ["Bawang Merah", "Cabai", "Padi", "Mangga", "Jagung", "Semangka"]
        if temp > 33: warnings.append("Suhu cukup ekstrem, perhatikan irigasi.")
    elif 400 <= elevation <= 800:
        zone = "Dataran Menengah"
        suitable = ["Durian", "Alpukat", "Kopi Robusta", "Tomat", "Terong"]
    else:
        zone = "Dataran Tinggi"
        suitable = ["Kubis", "Kentang", "Wortel", "Kopi Arabika", "Teh", "Stroberi"]
        if temp > 28: warnings.append("Anomali suhu panas untuk dataran tinggi.")

    return zone, suitable, warnings

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
            zone, rec_crops, warnings = analyze_suitability(elevation, temp)
            
            # 3. DISPLAY RESULTS
            
            # --- WEATHER CARD ---
            st.info(f"**🌤️ Cuaca Saat Ini**")
            c_w1, c_w2, c_w3 = st.columns(3)
            c_w1.metric("Suhu", f"{temp}°C")
            c_w2.metric("Angin", f"{wind} km/h")
            c_w3.metric("Status", "Siang" if is_day else "Malam")
            
            # --- LAND CARD ---
            st.success(f"**⛰️ Profil Lahan: {zone}**")
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
