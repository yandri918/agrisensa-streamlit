# Cuaca Pertanian - Weather for Agriculture
# Module 27 - Comprehensive Weather Information & Agricultural Recommendations
# Version: 1.0.0

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Cuaca Pertanian", page_icon="🌤️", layout="wide")

# ========== WEATHER API CONFIGURATION ==========
# Using OpenWeatherMap API (Free tier)
# You can also use: WeatherAPI, Visual Crossing, or other services

OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "demo_key")  # Add to .streamlit/secrets.toml
WEATHER_API_BASE = "https://api.openweathermap.org/data/2.5"

# ========== HELPER FUNCTIONS ==========

def get_current_weather(lat, lon):
    """Get current weather data from OpenWeatherMap API"""
    try:
        url = f"{WEATHER_API_BASE}/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "id"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("❌ API Key Error: Key tidak valid atau belum aktif. (Code 401)")
            return None
        else:
            st.error(f"❌ Error API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def get_forecast(lat, lon):
    """Get 7-day weather forecast"""
    try:
        url = f"{WEATHER_API_BASE}/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "id"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            # st.error("❌ API Key Error (Forecast): Key tidak valid atau belum aktif.") # Suppress duplicate error
            return None
        else:
            return None
    except Exception as e:
        # st.error(f"Error fetching forecast: {e}")
        return None

def get_weather_icon(icon_code):
    """Get weather icon emoji based on OpenWeatherMap icon code"""
    icon_map = {
        "01d": "☀️", "01n": "🌙",
        "02d": "⛅", "02n": "☁️",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return icon_map.get(icon_code, "🌤️")

def get_agricultural_recommendations(weather_data):
    """Generate agricultural recommendations based on weather"""
    recommendations = []
    
    if not weather_data:
        return ["Data cuaca tidak tersedia"]
    
    temp = weather_data.get('main', {}).get('temp', 0)
    humidity = weather_data.get('main', {}).get('humidity', 0)
    rain = weather_data.get('rain', {}).get('1h', 0)
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    
    # Temperature-based recommendations
    if temp < 15:
        recommendations.append("🌡️ **Suhu Rendah**: Lindungi tanaman sensitif dingin. Pertimbangkan mulsa untuk menjaga suhu tanah.")
    elif temp > 35:
        recommendations.append("🌡️ **Suhu Tinggi**: Tingkatkan frekuensi penyiraman. Hindari aplikasi pestisida siang hari.")
    else:
        recommendations.append("🌡️ **Suhu Optimal**: Kondisi baik untuk sebagian besar aktivitas pertanian.")
    
    # Humidity-based recommendations
    if humidity > 80:
        recommendations.append("💧 **Kelembaban Tinggi**: Risiko penyakit jamur meningkat. Pertimbangkan aplikasi fungisida preventif.")
    elif humidity < 40:
        recommendations.append("💧 **Kelembaban Rendah**: Tingkatkan penyiraman. Pertimbangkan mulsa untuk mengurangi penguapan.")
    
    # Rain-based recommendations
    if rain > 0:
        recommendations.append("🌧️ **Hujan**: Tunda penyemprotan pestisida. Periksa drainase lahan.")
    else:
        recommendations.append("☀️ **Tidak Hujan**: Waktu baik untuk penyemprotan dan pemupukan.")
    
    # Wind-based recommendations
    if wind_speed > 5:
        recommendations.append("💨 **Angin Kencang**: Tunda penyemprotan. Pasang penyangga untuk tanaman tinggi.")
    
    return recommendations

def get_weather_alerts(weather_data):
    """Generate weather alerts for extreme conditions"""
    alerts = []
    
    if not weather_data:
        return alerts
    
    temp = weather_data.get('main', {}).get('temp', 0)
    humidity = weather_data.get('main', {}).get('humidity', 0)
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    
    if temp > 38:
        alerts.append("⚠️ **PERINGATAN PANAS EKSTREM**: Suhu sangat tinggi! Lindungi tanaman dan tingkatkan irigasi.")
    
    if temp < 10:
        alerts.append("⚠️ **PERINGATAN DINGIN**: Suhu rendah! Lindungi tanaman dari frost.")
    
    if wind_speed > 10:
        alerts.append("⚠️ **PERINGATAN ANGIN KENCANG**: Amankan struktur dan tanaman.")
    
    if humidity > 90:
        alerts.append("⚠️ **PERINGATAN KELEMBABAN TINGGI**: Risiko penyakit jamur sangat tinggi!")
    
    return alerts

def get_farming_activity_suitability(weather_data):
    """Determine suitability of farming activities based on weather"""
    if not weather_data:
        return {}
    
    temp = weather_data.get('main', {}).get('temp', 0)
    humidity = weather_data.get('main', {}).get('humidity', 0)
    rain = weather_data.get('rain', {}).get('1h', 0)
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    
    activities = {
        "Penyemprotan Pestisida": "🟢 Cocok" if rain == 0 and wind_speed < 5 else "🔴 Tidak Cocok",
        "Pemupukan": "🟢 Cocok" if rain == 0 else "🟡 Kurang Cocok",
        "Penyiraman": "🔴 Tidak Perlu" if rain > 0 else "🟢 Perlu",
        "Panen": "🟢 Cocok" if rain == 0 and wind_speed < 7 else "🔴 Tidak Cocok",
        "Pengolahan Tanah": "🟢 Cocok" if rain == 0 and humidity < 80 else "🟡 Kurang Cocok",
        "Penanaman": "🟢 Cocok" if 20 < temp < 35 and rain == 0 else "🟡 Kurang Cocok"
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
    }
    .forecast-card {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        margin: 0.5rem 0;
    }
    .alert-box {
        background: #fee2e2;
        border: 2px solid #dc2626;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .recommendation-box {
        background: #d1fae5;
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .activity-suitable {
        color: #059669;
        font-weight: 700;
    }
    .activity-not-suitable {
        color: #dc2626;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
st.markdown('<h1 class="main-header">🌤️ Cuaca Pertanian</h1>', unsafe_allow_html=True)
st.markdown("**Informasi cuaca real-time dan rekomendasi aktivitas pertanian**")

# ========== LOCATION SELECTION ==========
st.markdown("---")
st.subheader("📍 Pilih Lokasi")

tab1, tab2 = st.tabs(["🗺️ Pilih di Peta", "📝 Input Manual"])

# TAB 1: MAP SELECTION
with tab1:
    st.markdown("**Klik pada peta untuk memilih lokasi**")
    
    # Default location (Indonesia center)
    default_lat = -2.5
    default_lon = 118.0
    
    # Create map
    m = folium.Map(
        location=[default_lat, default_lon],
        zoom_start=5,
        tiles="OpenStreetMap"
    )
    
    # Add click functionality
    m.add_child(folium.LatLngPopup())
    
    # Display map
    map_data = st_folium(m, width=700, height=500)
    
    # Get clicked location
    if map_data and map_data.get("last_clicked"):
        selected_lat = map_data["last_clicked"]["lat"]
        selected_lon = map_data["last_clicked"]["lng"]
        st.success(f"📍 Lokasi dipilih: {selected_lat:.4f}, {selected_lon:.4f}")
    else:
        selected_lat = default_lat
        selected_lon = default_lon
        st.info("Klik pada peta untuk memilih lokasi, atau gunakan lokasi default (Indonesia)")

# TAB 2: MANUAL INPUT
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        manual_lat = st.number_input("Latitude", value=-6.2088, format="%.4f", 
                                     help="Contoh: Jakarta = -6.2088")
    with col2:
        manual_lon = st.number_input("Longitude", value=106.8456, format="%.4f",
                                     help="Contoh: Jakarta = 106.8456")
    
    if st.button("🔍 Gunakan Lokasi Manual"):
        selected_lat = manual_lat
        selected_lon = manual_lon
        st.success(f"📍 Lokasi manual: {selected_lat:.4f}, {selected_lon:.4f}")

# ========== FETCH WEATHER DATA ==========
st.markdown("---")

if st.button("🌤️ Dapatkan Data Cuaca", type="primary", use_container_width=True):
    with st.spinner("Mengambil data cuaca..."):
        current_weather = get_current_weather(selected_lat, selected_lon)
        forecast_data = get_forecast(selected_lat, selected_lon)
        
        if current_weather:
            st.session_state['current_weather'] = current_weather
            st.session_state['forecast_data'] = forecast_data
            st.session_state['selected_lat'] = selected_lat
            st.session_state['selected_lon'] = selected_lon
            st.success("✅ Data cuaca berhasil diambil!")
        else:
            st.warning("⚠️ **Gagal mengambil data cuaca.**")
            st.info("""
            **Kemungkinan penyebab:**
            1. **API Key Belum Aktif**: Jika baru dibuat, API key butuh waktu 30-60 menit untuk aktif.
            2. **API Key Salah**: Periksa kembali `secrets.toml`.
            3. **Limit Tercapai**: Kuota harian habis.
            
            Silakan coba lagi dalam beberapa menit.
            """)

# ========== DISPLAY WEATHER DATA ==========
if 'current_weather' in st.session_state:
    weather = st.session_state['current_weather']
    
    # Current Weather
    st.markdown("---")
    st.header("🌡️ Cuaca Saat Ini")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp = weather['main']['temp']
        feels_like = weather['main']['feels_like']
        st.metric("Suhu", f"{temp:.1f}°C", f"Terasa {feels_like:.1f}°C")
    
    with col2:
        humidity = weather['main']['humidity']
        st.metric("Kelembaban", f"{humidity}%")
    
    with col3:
        wind_speed = weather['wind']['speed']
        st.metric("Kecepatan Angin", f"{wind_speed:.1f} m/s")
    
    with col4:
        pressure = weather['main']['pressure']
        st.metric("Tekanan Udara", f"{pressure} hPa")
    
    # Weather Description
    st.markdown(f"""
    <div class="weather-card">
        <h2 style="text-align: center;">{get_weather_icon(weather['weather'][0]['icon'])} {weather['weather'][0]['description'].title()}</h2>
        <p style="text-align: center; font-size: 1.1rem;">
            📍 Lokasi: {weather['name']}<br>
            🌅 Sunrise: {datetime.fromtimestamp(weather['sys']['sunrise']).strftime('%H:%M')}<br>
            🌇 Sunset: {datetime.fromtimestamp(weather['sys']['sunset']).strftime('%H:%M')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Weather Alerts
    alerts = get_weather_alerts(weather)
    if alerts:
        st.markdown("### ⚠️ Peringatan Cuaca")
        for alert in alerts:
            st.markdown(f'<div class="alert-box">{alert}</div>', unsafe_allow_html=True)
    
    # Agricultural Recommendations
    st.markdown("---")
    st.header("🌾 Rekomendasi Aktivitas Pertanian")
    
    recommendations = get_agricultural_recommendations(weather)
    for rec in recommendations:
        st.markdown(f'<div class="recommendation-box">{rec}</div>', unsafe_allow_html=True)
    
    # Activity Suitability
    st.markdown("### 📋 Kesesuaian Aktivitas Pertanian")
    activities = get_farming_activity_suitability(weather)
    
    col1, col2 = st.columns(2)
    for i, (activity, suitability) in enumerate(activities.items()):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"**{activity}**: {suitability}")
    
    # Forecast
    if 'forecast_data' in st.session_state and st.session_state['forecast_data']:
        st.markdown("---")
        st.header("📅 Prakiraan Cuaca 5 Hari")
        
        forecast = st.session_state['forecast_data']
        
        # Process forecast data
        forecast_list = forecast['list']
        daily_forecast = {}
        
        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()
            if date not in daily_forecast:
                daily_forecast[date] = {
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'rain': item.get('rain', {}).get('3h', 0)
                }
            else:
                daily_forecast[date]['temp_min'] = min(daily_forecast[date]['temp_min'], item['main']['temp_min'])
                daily_forecast[date]['temp_max'] = max(daily_forecast[date]['temp_max'], item['main']['temp_max'])
        
        # Display forecast cards
        cols = st.columns(5)
        for i, (date, data) in enumerate(list(daily_forecast.items())[:5]):
            with cols[i]:
                st.markdown(f"""
                <div class="forecast-card">
                    <h4>{date.strftime('%a, %d %b')}</h4>
                    <div style="font-size: 3rem;">{get_weather_icon(data['icon'])}</div>
                    <p><strong>{data['temp_max']:.0f}°C / {data['temp_min']:.0f}°C</strong></p>
                    <p>{data['description'].title()}</p>
                    <p>💧 {data['humidity']}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Temperature Chart
        st.markdown("### 📊 Grafik Suhu 5 Hari")
        
        dates = list(daily_forecast.keys())[:5]
        temp_max = [daily_forecast[d]['temp_max'] for d in dates]
        temp_min = [daily_forecast[d]['temp_min'] for d in dates]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=temp_max,
            name='Suhu Maksimum',
            mode='lines+markers',
            line=dict(color='#dc2626', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=dates, y=temp_min,
            name='Suhu Minimum',
            mode='lines+markers',
            line=dict(color='#0284c7', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Prakiraan Suhu 5 Hari",
            xaxis_title="Tanggal",
            yaxis_title="Suhu (°C)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👆 Pilih lokasi di peta atau input manual, lalu klik tombol 'Dapatkan Data Cuaca' untuk melihat informasi cuaca.")

# ========== ADDITIONAL INFORMATION ==========
st.markdown("---")
st.markdown("""
### 📚 Panduan Interpretasi Cuaca untuk Pertanian

**Suhu:**
- **< 15°C**: Risiko frost, lindungi tanaman sensitif
- **15-30°C**: Optimal untuk sebagian besar tanaman
- **> 35°C**: Stress panas, tingkatkan irigasi

**Kelembaban:**
- **< 40%**: Rendah, tingkatkan penyiraman
- **40-70%**: Optimal
- **> 80%**: Tinggi, risiko penyakit jamur

**Angin:**
- **< 3 m/s**: Tenang, baik untuk semua aktivitas
- **3-5 m/s**: Sedang, hati-hati saat penyemprotan
- **> 5 m/s**: Kencang, tunda penyemprotan

**Hujan:**
- Tunda penyemprotan pestisida 24 jam sebelum dan sesudah hujan
- Periksa drainase saat hujan lebat
- Manfaatkan periode tidak hujan untuk pemupukan
""")

# Footer
st.markdown("---")
st.caption("""
🌤️ **Cuaca Pertanian** - Informasi cuaca real-time untuk optimalisasi aktivitas pertanian.

📡 **Data Source**: OpenWeatherMap API

💡 **Tips**: Selalu periksa cuaca sebelum melakukan aktivitas pertanian penting seperti penyemprotan dan pemupukan.
""")
