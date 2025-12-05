# Cuaca Pertanian - Weather for Agriculture (Open-Meteo Version)
# Module 27 - Comprehensive Weather Information & Agricultural Recommendations
# Version: 2.0.0 (Migrated to Open-Meteo)

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cuaca Pertanian", page_icon="🌤️", layout="wide")

# ========== HELPER FUNCTIONS ==========

def get_elevation(lat, lon):
    """Get elevation data from Open-Meteo Elevation API"""
    try:
        url = "https://api.open-meteo.com/v1/elevation"
        params = {
            "latitude": lat,
            "longitude": lon
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('elevation', [0])[0]
    except:
        pass
    return 0

def get_weather_data(lat, lon):
    """Get weather data from Open-Meteo API (No Key Needed)"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,rain,weather_code,wind_speed_10m,surface_pressure",
            "hourly": "temperature_2m,relative_humidity_2m,rain,soil_temperature_0cm,soil_moisture_0_to_1cm,shortwave_radiation,vapor_pressure_deficit",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,rain_sum,precipitation_probability_max,et0_fao_evapotranspiration",
            "timezone": "auto"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def get_weather_icon(code):
    """Get weather icon based on WMO code"""
    # WMO Weather interpretation codes (WW)
    # https://open-meteo.com/en/docs
    if code == 0: return "☀️", "Cerah"
    if code in [1, 2, 3]: return "⛅", "Berawan"
    if code in [45, 48]: return "🌫️", "Kabut"
    if code in [51, 53, 55]: return "🌦️", "Gerimis"
    if code in [61, 63, 65]: return "🌧️", "Hujan"
    if code in [80, 81, 82]: return "🌧️", "Hujan Lebat"
    if code in [95, 96, 99]: return "⛈️", "Badai Petir"
    return "🌤️", "Cerah Berawan"

def get_climate_season(lat):
    """Detect climate zone and current season based on latitude and month"""
    month = datetime.now().month
    
    # 1. Tentukan Zona Iklim
    if abs(lat) <= 23.5:
        zone = "Tropis"
    elif 23.5 < abs(lat) <= 40:
        zone = "Sub-Tropis"
    elif 40 < abs(lat) <= 60:
        zone = "Sedang (Temperate)"
    else:
        zone = "Kutub/Dingin"
        
    # 2. Tentukan Musim (Season)
    season = ""
    icon = ""
    
    if zone == "Tropis":
        # Pendekatan sederhana untuk tropis (ID)
        if 4 <= month <= 9:
            season = "Musim Kemarau"
            icon = "☀️"
        else:
            season = "Musim Hujan"
            icon = "🌧️"
    else:
        # Negara 4 Musim (Utara vs Selatan)
        is_north = lat > 0
        
        if is_north: # Jepang, Eropa, US
            if 3 <= month <= 5: 
                season = "Musim Semi (Spring)"
                icon = "🌸"
            elif 6 <= month <= 8: 
                season = "Musim Panas (Summer)"
                icon = "☀️"
            elif 9 <= month <= 11: 
                season = "Musim Gugur (Autumn)"
                icon = "🍂"
            else: 
                season = "Musim Dingin (Winter)"
                icon = "❄️"
        else: # Australia, NZ
            if 3 <= month <= 5: 
                season = "Musim Gugur (Autumn)"
                icon = "🍂"
            elif 6 <= month <= 8: 
                season = "Musim Dingin (Winter)"
                icon = "❄️"
            elif 9 <= month <= 11: 
                season = "Musim Semi (Spring)"
                icon = "🌸"
            else: 
                season = "Musim Panas (Summer)"
                icon = "☀️"
                
    return zone, season, icon

def get_seasonal_insight(season, temp):
    """Get specific insights based on season"""
    insights = []
    
    if "Winter" in season or "Dingin" in season:
        insights.append("❄️ **Winter Strategy:** Fokus pada tanaman root vegetables (lobak, wortel) atau leafy greens tahan dingin (bayam, kale).")
        if temp < 5:
            insights.append("⚠️ **Frost Warning:** Suhu mendekati beku! Gunakan greenhouse, tunnel, atau mulsa jerami tebal.")
            insights.append("🏠 **Indoor Farming:** Pertimbangkan menanam microgreens atau hidroponik indoor.")
    
    elif "Spring" in season or "Semi" in season:
        insights.append("🌸 **Spring Planting:** Waktu terbaik untuk menyemai benih. Tanah mulai menghangat.")
        insights.append("🌱 **Soil Prep:** Lakukan pengolahan tanah dan penambahan kompos setelah musim dingin.")
    
    elif "Summer" in season or "Panas" in season:
        insights.append("☀️ **Heat Mgmt:** Waspada stress panas. Pastikan irigasi cukup, terutama di siang hari.")
        if temp > 30:
            insights.append("🌡️ **High Temp:** Gunakan naungan (shade net) untuk tanaman sensitif (selada, pakchoy).")
    
    elif "Autumn" in season or "Gugur" in season:
        insights.append("🍂 **Harvest Time:** Periode panen raya untuk tanaman musim panas.")
        insights.append("🌾 **Cover Crops:** Tanam penutup tanah (cover crops) untuk melindungi tanah selama winter.")
    
    elif "Kemarau" in season:
        insights.append("☀️ **Musim Kemarau:** Fokus pada efisiensi air. Gunakan irigasi tetes atau mulsa.")
    
    elif "Hujan" in season:
        insights.append("🌧️ **Musim Hujan:** Waspada serangan jamur dan pembusukan akar. Perbaiki drainase.")

    return insights

def get_agricultural_recommendations(weather_data, elevation, lat):
    """Generate agricultural recommendations based on weather, elevation, and season"""
    recommendations = []
    
    if not weather_data:
        return ["Data tidak tersedia"]
    
    current = weather_data.get('current', {})
    daily = weather_data.get('daily', {})
    
    temp = current.get('temperature_2m', 0)
    humidity = current.get('relative_humidity_2m', 0)
    rain = current.get('rain', 0)
    wind = current.get('wind_speed_10m', 0)
    
    # Get Seasonal Data
    zone, season, season_icon = get_climate_season(lat)
    
    # 1. Seasonal Insights (PRIORITY)
    recommendations.append(f"🌍 **Zona Iklim:** {zone} | {season_icon} **{season}**")
    seasonal_tips = get_seasonal_insight(season, temp)
    recommendations.extend(seasonal_tips)

    # 2. Elevation Recommendations
    if elevation < 100:
        recommendations.append("🏔️ **Dataran Rendah:** Cocok untuk Padi, Jagung, Kelapa (Tropis) atau Gandum (Sub-tropis).")
    elif 100 <= elevation <= 700:
        recommendations.append("🏔️ **Dataran Menengah:** Cocok untuk Karet, Kopi Robusta, Buah-buahan.")
    else:
        recommendations.append("🏔️ **Dataran Tinggi (>700m):** Cocok untuk Teh, Kopi Arabika, Apel, Strawberry, Wasabi.")

    # 3. Rain & Irrigation
    if rain > 0 or daily.get('rain_sum', [0])[0] > 5:
        recommendations.append("🌧️ **Hujan Terdeteksi:** Tunda penyemprotan. Risiko pencucian pupuk tinggi.")
    else:
        recommendations.append("💧 **Tidak Ada Hujan:** Cek kelembaban tanah. Aman untuk pemupukan dan penyemprotan.")
        
    # 4. Wind
    if wind > 15:
        recommendations.append("💨 **Angin Kencang (>15 km/h):** Hindari penyemprotan pestisida (drift hazard).")

    return recommendations

def get_farming_suitability(weather_data, soil_moisture=None):
    """Determine suitability of farming activities"""
    if not weather_data:
        return {}
    
    current = weather_data.get('current', {})
    rain = current.get('rain', 0)
    wind = current.get('wind_speed_10m', 0)
    
    activities = {
        "Penyemprotan": "🟢 Cocok" if rain == 0 and wind < 10 else "🔴 Tidak Cocok",
        "Pemupukan Padat": "🟢 Cocok" if rain < 5 else "🟡 Hati-hati (Hanyut)",
        "Pemupukan Cair": "🟢 Cocok" if rain == 0 else "🔴 Tidak Cocok",
        "Panen": "🟢 Cocok" if rain == 0 else "🔴 Berisiko (Kadar Air Tinggi)",
        "Olah Tanah": "🟢 Cocok" if rain == 0 else "🟡 Berlumpur/Lengket"
    }
    
    return activities

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0284c7;
        text-align: center;
        margin-bottom: 1rem;
    }
    .weather-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #0284c7;
        margin: 1rem 0;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .forecast-card {
        background: white;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin: 5px;
    }
    .rec-box {
        background: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 1rem;
        margin-bottom: 0.5rem;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
st.markdown('<h1 class="main-header">🌤️ Cuaca Pertanian & Altimeter</h1>', unsafe_allow_html=True)
st.markdown("**Data Cuaca Presisi, Curah Hujan, & Ketinggian Lahan (Powered by Open-Meteo)**")

# ========== LOCATION ==========
st.sidebar.header("📍 Lokasi Lahan")
tabs = st.tabs(["🗺️ Pilih di Peta", "📝 Input Manual"])

with tabs[0]:
    # Default: Central Java (Agricultural center)
    default_lat, default_lon = -7.150975, 110.140259 
    
    m = folium.Map(location=[default_lat, default_lon], zoom_start=8)
    m.add_child(folium.LatLngPopup())
    
    map_data = st_folium(m, height=400, width=700)
    
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        st.success(f"📍 Terpilih: {lat:.5f}, {lon:.5f}")
    else:
        lat, lon = default_lat, default_lon

with tabs[1]:
    # Initialize session state for manual inputs if not exists
    if 'manual_lat' not in st.session_state: st.session_state['manual_lat'] = lat
    if 'manual_lon' not in st.session_state: st.session_state['manual_lon'] = lon

    col_preset1, col_preset2 = st.columns(2)
    with col_preset1:
        if st.button("📍 Set Lokasi: Tokyo, Jepang (4 Musim)"):
            st.session_state['manual_lat'] = 35.6762
            st.session_state['manual_lon'] = 139.6503
            
    with col_preset2:
        if st.button("📍 Set Lokasi: Jakarta, ID (Tropis)"):
            st.session_state['manual_lat'] = -6.2088
            st.session_state['manual_lon'] = 106.8456

    col1, col2 = st.columns(2)
    with col1: 
        lat_input = st.number_input("Latitude", value=st.session_state['manual_lat'], format="%.5f", key="input_lat")
    with col2: 
        lon_input = st.number_input("Longitude", value=st.session_state['manual_lon'], format="%.5f", key="input_lon")
            
    if st.button("Update Lokasi Manual", type="primary"):
        lat, lon = lat_input, lon_input

# ========== GET DATA ==========
if st.button("🔍 Analisis Cuaca & Lahan", type="primary", use_container_width=True):
    with st.spinner("Mengambil data satelit & cuaca..."):
        weather = get_weather_data(lat, lon)
        elevation = get_elevation(lat, lon)
        
        if weather:
            st.session_state['weather_data'] = weather
            st.session_state['elevation'] = elevation
            st.session_state['data_lat'] = lat
            st.session_state['data_lon'] = lon
            st.success("✅ Data berhasil diambil!")

# ========== DISPLAY DASHBOARD ==========
if 'weather_data' in st.session_state:
    data = st.session_state['weather_data']
    elev = st.session_state['elevation']
    current = data['current']
    
    icon, desc = get_weather_icon(current['weather_code'])
    
    # 1. Main Weather Card
    col_main, col_info = st.columns([1, 2])
    
    with col_main:
        st.markdown(f"""
        <div class="weather-card">
            <h1 style="font-size: 4rem; margin:0;">{icon}</h1>
            <h2 style="margin:0;">{current['temperature_2m']}°C</h2>
            <p style="font-size: 1.2rem; font-weight:bold;">{desc}</p>
            <hr>
            <p>⛰️ Elevasi: <b>{elev:.0f} mdpl</b></p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info:
        st.subheader("📊 Parameter Lahan Real-time")
        c1, c2, c3 = st.columns(3)
        c1.markdown(f"""<div class="metric-card">🌧️ <b>Hujan</b><br><h2>{current['rain']} mm</h2></div>""", unsafe_allow_html=True)
        c2.markdown(f"""<div class="metric-card">💧 <b>Kelembaban</b><br><h2>{current['relative_humidity_2m']}%</h2></div>""", unsafe_allow_html=True)
        c3.markdown(f"""<div class="metric-card">💨 <b>Angin</b><br><h2>{current['wind_speed_10m']} km/h</h2></div>""", unsafe_allow_html=True)
        
        st.markdown("")
        # Soil Data (Approximation from hourly[0])
        hourly = data.get('hourly', {})
        soil_temp = hourly.get('soil_temperature_0cm', [0])[0] if hourly.get('soil_temperature_0cm') else "-"
        soil_moist = hourly.get('soil_moisture_0_to_1cm', [0])[0] if hourly.get('soil_moisture_0_to_1cm') else "-"
        
        c4, c5, c6 = st.columns(3)
        c4.markdown(f"""<div class="metric-card">🌱 <b>Suhu Tanah</b><br><h2>{soil_temp}°C</h2></div>""", unsafe_allow_html=True)
        c5.markdown(f"""<div class="metric-card">🏜️ <b>Emb. Tanah</b><br><h2>{soil_moist} m³/m³</h2></div>""", unsafe_allow_html=True)
        c6.markdown(f"""<div class="metric-card">⏱️ <b>Tekanan</b><br><h2>{current['surface_pressure']} hPa</h2></div>""", unsafe_allow_html=True)

    # 2. Recommendations & Suitability
    st.markdown("---")
    col_rec, col_suit = st.columns([3, 2])
    
    with col_rec:
        st.subheader("🌾 Rekomendasi Agronomi")
        recs = get_agricultural_recommendations(data, elev, st.session_state['data_lat'])
        for rec in recs:
            st.markdown(f'<div class="rec-box">{rec}</div>', unsafe_allow_html=True)
            
    with col_suit:
        st.subheader("📋 Kesesuaian Aktivitas")
        suits = get_farming_suitability(data)
        for act, status in suits.items():
            st.markdown(f"**{act}**: {status}")

    # 3. Forecast 7 Days
    st.markdown("---")
    st.subheader("📅 Prakiraan 7 Hari Kedepan")
    
    daily = data.get('daily', {})
    dates = daily.get('time', [])
    codes = daily.get('weather_code', [])
    t_max = daily.get('temperature_2m_max', [])
    t_min = daily.get('temperature_2m_min', [])
    rain_sum = daily.get('rain_sum', [])
    
    cols = st.columns(7)
    for i in range(min(7, len(dates))):
        d_icon, d_desc = get_weather_icon(codes[i])
        day_date = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%d/%m")
        
        with cols[i]:
            st.markdown(f"""
            <div class="forecast-card">
                <b>{day_date}</b><br>
                <span style="font-size:2rem">{d_icon}</span><br>
                <span style="font-size:0.8rem">{d_desc}</span><br>
                <b>{t_max[i]}°</b> <span style="color:gray">/ {t_min[i]}°</span><br>
                <span style="color:#2563eb; font-size:0.8rem">🌧️ {rain_sum[i]}mm</span>
            </div>
            """, unsafe_allow_html=True)
            
    # 4. Advanced Metrics (New Tab)
    st.markdown("---")
    tab_basic, tab_adv, tab_chart = st.tabs(["📊 Metrik Dasar", "🔬 Metrik Lanjutan (Agronomi)", "📈 Grafik Tren"])
    
    with tab_basic:
        st.info("Pilih tab 'Metrik Lanjutan' untuk data profesional (ET0, VPD, Radiasi).")

    with tab_adv:
        st.subheader("🔬 Metrik Agronomi Presisi")
        st.markdown("Data tingkat lanjut untuk manajemen pertanian presisi.")
        
        # Get hourly data for current time approximation
        hourly = data.get('hourly', {})
        current_hour_idx = datetime.now().hour
        
        et0 = daily.get('et0_fao_evapotranspiration', [0])[0] # Daily ET0
        solar_rad = hourly.get('shortwave_radiation', [0])[current_hour_idx] if hourly.get('shortwave_radiation') else 0
        vpd = hourly.get('vapor_pressure_deficit', [0])[current_hour_idx] if hourly.get('vapor_pressure_deficit') else 0
        
        col_et, col_rad, col_vpd = st.columns(3)
        
        with col_et:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #3b82f6;">
                <h3>💧 Evapotranspirasi (ET₀)</h3>
                <h1>{et0} mm/hari</h1>
                <p>Kebutuhan Air Tanaman Referensi</p>
                <div style="font-size:0.8rem; color:gray; text-align:left;">
                <b>Tips:</b> Gunakan nilai ini untuk menghitung kebutuhan irigasi harian.
                (ETc = ET₀ × Kc Tanaman)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_rad:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #f59e0b;">
                <h3>☀️ Radiasi Matahari</h3>
                <h1>{solar_rad} W/m²</h1>
                <p>Intensitas Energi Matahari (Saat Ini)</p>
                <div style="font-size:0.8rem; color:gray; text-align:left;">
                <b>Info:</b> Penting untuk fotosintesis.
                <br>> 500 W/m²: Radiasi tinggi (Siang cerah).
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_vpd:
            vpd_status = "Optimal 🟢" if 0.4 <= vpd <= 1.6 else ("Rendah (Lembab) 🔵" if vpd < 0.4 else "Tinggi (Kering) 🔴")
            st.markdown(f"""
            <div class="metric-card" style="border-left: 5px solid #10b981;">
                <h3>🍃 VPD (Stress Tanaman)</h3>
                <h1>{vpd} kPa</h1>
                <p>Status: <b>{vpd_status}</b></p>
                <div style="font-size:0.8rem; color:gray; text-align:left;">
                <b>Vapor Pressure Deficit:</b>
                <br>Optimal (0.4-1.6 kPa): Stomata terbuka maksimal.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with tab_chart:
        chart_df = pd.DataFrame({
            "Tanggal": dates,
            "Suhu Max": t_max,
            "Suhu Min": t_min,
            "Curah Hujan (mm)": rain_sum,
            "ET0 (mm)": daily.get('et0_fao_evapotranspiration', [])
        })
        
        subtab1, subtab2, subtab3 = st.tabs(["🌡️ Suhu", "🌧️ Hujan & ET0", "💧 Water Balance"])
        
        with subtab1:
            fig_temp = px.line(chart_df, x="Tanggal", y=["Suhu Max", "Suhu Min"], markers=True, 
                              color_discrete_map={"Suhu Max": "#ef4444", "Suhu Min": "#3b82f6"})
            st.plotly_chart(fig_temp, use_container_width=True)
            
        with subtab2:
            fig_rain = go.Figure()
            fig_rain.add_trace(go.Bar(x=chart_df['Tanggal'], y=chart_df['Curah Hujan (mm)'], name='Curah Hujan (Input)', marker_color='#3b82f6'))
            fig_rain.add_trace(go.Bar(x=chart_df['Tanggal'], y=chart_df['ET0 (mm)'], name='Evapotranspirasi (Output)', marker_color='#ef4444'))
            fig_rain.update_layout(barmode='group', title="Input Air (Hujan) vs Output Air (ET0)")
            st.plotly_chart(fig_rain, use_container_width=True)
            
        with subtab3:
            chart_df['Water Balance'] = chart_df['Curah Hujan (mm)'] - chart_df['ET0 (mm)']
            fig_bal = px.bar(chart_df, x="Tanggal", y="Water Balance", color="Water Balance",
                            color_continuous_scale="RdBu", title="Neraca Air Harian (Hujan - ET0)")
            st.plotly_chart(fig_bal, use_container_width=True)

else:
    st.info("👆 Silakan pilih lokasi di peta lalu klik tombol 'Analisis Cuaca & Lahan'")

# Footer
st.markdown("---")
st.caption("Powered by **Open-Meteo API** (Free, Open Source Data) | Tanpa API Key")
