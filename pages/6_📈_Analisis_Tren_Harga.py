# Analisis Tren Harga (BigView API Integration)
# Real-time price analysis dengan data dari BigView API

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
import requests
import json

st.set_page_config(page_title="Analisis Tren Harga", page_icon="📈", layout="wide")

# ========== PANEL HARGA PANGAN API INTEGRATION ==========
PANEL_HARGA_API = "https://panelharga.badanpangan.go.id/api"

# Commodity mapping for Panel Harga Pangan
COMMODITY_MAPPING = {
    "Beras Premium": "beras_premium",
    "Beras Medium": "beras_medium",
    "Cabai Merah Besar": "cabai_merah_besar",
    "Cabai Merah Keriting": "cabai_merah_keriting",
    "Cabai Rawit Hijau": "cabai_rawit_hijau",
    "Cabai Rawit Merah": "cabai_rawit_merah",
    "Bawang Merah": "bawang_merah",
    "Bawang Putih": "bawang_putih",
    "Gula Pasir Premium": "gula_pasir_premium",
    "Gula Pasir Lokal": "gula_pasir_lokal",
    "Minyak Goreng Curah": "minyak_goreng_curah",
    "Minyak Goreng Kemasan": "minyak_goreng_kemasan",
    "Daging Ayam Ras": "daging_ayam_ras",
    "Daging Sapi Murni": "daging_sapi_murni",
    "Telur Ayam Ras": "telur_ayam_ras",
    "Tomat": "tomat",
    "Kentang": "kentang"
}

# Province mapping
PROVINCE_MAPPING = {
    "Semua Provinsi": None,
    "DKI Jakarta": "jakarta",
    "Jawa Barat": "jawa_barat",
    "Jawa Tengah": "jawa_tengah",
    "Jawa Timur": "jawa_timur",
    "Banten": "banten",
    "Sumatera Utara": "sumatera_utara",
    "Sulawesi Selatan": "sulawesi_selatan",
    "Bali": "bali"
}

def fetch_panel_harga_data(commodity_key=None, province_key=None, limit=100):
    """
    Fetch real-time price data from Panel Harga Pangan API
    
    Try multiple endpoint variations:
    1. /api/harga
    2. /harga
    3. /data/harga
    """
    endpoints = [
        f"{PANEL_HARGA_API}/harga",
        "https://panelharga.badanpangan.go.id/harga",
        "https://hargapangan.id/api/harga",  # Old endpoint
    ]
    
    params = {}
    if commodity_key:
        params["komoditas"] = commodity_key
    if province_key:
        params["provinsi"] = province_key
    if limit:
        params["limit"] = limit
    
    # Try each endpoint
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and ('data' in data or isinstance(data, list)):
                    return data
        except Exception as e:
            continue
    
    return None

def parse_panel_harga_data(api_response):
    """Parse Panel Harga Pangan API response into DataFrame"""
    if not api_response:
        return None
    
    # Handle different response formats
    if isinstance(api_response, dict) and 'data' in api_response:
        records = api_response['data']
    elif isinstance(api_response, list):
        records = api_response
    else:
        return None
    
    parsed_data = []
    for item in records:
        try:
            parsed_data.append({
                'date': pd.to_datetime(item.get('tanggal', item.get('date', datetime.now()))),
                'price': float(item.get('harga', item.get('price', 0))),
                'commodity': item.get('komoditas', item.get('commodity', 'Unknown')),
                'province': item.get('provinsi', item.get('province', 'Unknown')),
                'market': item.get('pasar', item.get('market', 'Unknown'))
            })
        except:
            continue
    
    return pd.DataFrame(parsed_data) if parsed_data else None

# ========== SAMPLE DATA (FALLBACK) ==========
def generate_sample_data(commodity, days=90):
    """Generate sample data if API fails"""
    np.random.seed(42)
    
    base_prices = {
        "Cabai Merah": 45000,
        "Cabai Rawit": 55000,
        "Tomat": 8000,
        "Kentang": 12000,
        "Bawang Merah": 35000,
        "Bawang Putih": 40000,
        "Padi": 5000,
        "Jagung": 4500,
        "Kedelai": 8000,
        "Gula Pasir": 15000,
        "Minyak Goreng": 18000,
        "Daging Ayam": 35000,
        "Daging Sapi": 130000,
        "Telur Ayam": 28000
    }
    
    base_price = base_prices.get(commodity, 10000)
    dates = [datetime.now() - timedelta(days=days-i) for i in range(days)]
    
    # Realistic price pattern
    trend = np.linspace(0, 0.15, days)
    seasonal = 0.1 * np.sin(2 * np.pi * np.arange(days) / 30)
    noise = np.random.normal(0, 0.05, days)
    
    prices = base_price * (1 + trend + seasonal + noise)
    
    return pd.DataFrame({
        'date': dates,
        'price': prices,
        'commodity': commodity
    })

# ========== ML FUNCTIONS ==========
def predict_prices_advanced(df, days_ahead=30, model_type='random_forest'):
    """Advanced price prediction with multiple models"""
    df = df.sort_values('date')
    df['days'] = (df['date'] - df['date'].min()).dt.days
    
    X = df[['days']].values
    y = df['price'].values
    
    if model_type == 'random_forest':
        # Random Forest for better accuracy
        model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
        model.fit(X, y)
        
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        predictions = model.predict(future_days)
        
    elif model_type == 'polynomial':
        # Polynomial regression
        poly = PolynomialFeatures(degree=3)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        future_days_poly = poly.transform(future_days)
        predictions = model.predict(future_days_poly)
        
    else:  # linear
        model = LinearRegression()
        model.fit(X, y)
        
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        predictions = model.predict(future_days)
    
    # Calculate confidence interval
    if model_type == 'polynomial':
        residuals = y - model.predict(X_poly)
    else:
        residuals = y - model.predict(X)
    
    std_error = np.std(residuals)
    
    last_date = df['date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
    
    return pd.DataFrame({
        'date': future_dates,
        'predicted_price': predictions,
        'lower_bound': predictions - 1.96 * std_error,
        'upper_bound': predictions + 1.96 * std_error
    })

def calculate_statistics(df):
    """Calculate comprehensive price statistics"""
    recent_7d = df.tail(7)
    recent_30d = df.tail(30)
    
    return {
        'current_price': df['price'].iloc[-1],
        'avg_price': df['price'].mean(),
        'avg_7d': recent_7d['price'].mean(),
        'avg_30d': recent_30d['price'].mean(),
        'min_price': df['price'].min(),
        'max_price': df['price'].max(),
        'volatility': df['price'].std(),
        'trend': 'Naik' if df['price'].iloc[-1] > df['price'].iloc[0] else 'Turun',
        'change_7d': ((recent_7d['price'].iloc[-1] - recent_7d['price'].iloc[0]) / recent_7d['price'].iloc[0] * 100) if len(recent_7d) > 0 else 0,
        'change_30d': ((recent_30d['price'].iloc[-1] - recent_30d['price'].iloc[0]) / recent_30d['price'].iloc[0] * 100) if len(recent_30d) > 0 else 0
    }

# ========== MAIN APP ==========
st.title("📈 Analisis Tren Harga Komoditas (Panel Harga Pangan)")
st.markdown("**Real-time price analysis dengan data dari Panel Harga Pangan + Machine Learning**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 🌐 Data real-time dari Panel Harga Pangan (Badan Pangan Nasional)
    - 📊 Analisis tren harga multi-periode
    - 🤖 Prediksi dengan 3 model ML (Linear, Polynomial, Random Forest)
    - 📉 Volatilitas dan statistik lengkap
    - 💡 Rekomendasi buy/sell/hold
    - 📥 Export data & prediksi
    
    **Data Source:**
    - Panel Harga Pangan: https://panelharga.badanpangan.go.id
    - Update real-time setiap 2 jam (10:00 - 13:00 WIB)
    - Coverage: 17 komoditas strategis
    - Fallback: Data simulasi jika API tidak tersedia
    
    **Model ML:**
    - **Linear:** Simple & cepat
    - **Polynomial:** Untuk pola non-linear
    - **Random Forest:** Paling akurat untuk data kompleks
    """)

# Input Section
st.subheader("⚙️ Konfigurasi Analisis")

col1, col2, col3 = st.columns(3)

with col1:
    commodity = st.selectbox(
        "Pilih Komoditas",
        list(COMMODITY_MAPPING.keys()),
        help="Pilih komoditas untuk analisis"
    )

with col2:
    province = st.selectbox(
        "Pilih Provinsi",
        list(PROVINCE_MAPPING.keys()),
        help="Filter berdasarkan provinsi (opsional)"
    )

with col3:
    model_type = st.selectbox(
        "Model Prediksi",
        ["random_forest", "polynomial", "linear"],
        format_func=lambda x: {
            "random_forest": "Random Forest (Recommended)",
            "polynomial": "Polynomial Regression",
            "linear": "Linear Regression"
        }[x],
        help="Pilih model ML untuk prediksi"
    )

# Advanced options
with st.expander("⚙️ Opsi Lanjutan"):
    col1, col2 = st.columns(2)
    
    with col1:
        data_limit = st.slider(
            "Jumlah Data Historical",
            min_value=30,
            max_value=365,
            value=90,
            step=10,
            help="Jumlah hari data untuk analisis"
        )
    
    with col2:
        prediction_days = st.slider(
            "Prediksi (hari ke depan)",
            min_value=7,
            max_value=60,
            value=30,
            step=7
        )

# Analyze button
if st.button("🔍 Analisis Harga Real-Time", type="primary", use_container_width=True):
    
    with st.spinner("Mengambil data dari Panel Harga Pangan..."):
        # Get commodity and province keys
        commodity_key = COMMODITY_MAPPING.get(commodity)
        province_key = PROVINCE_MAPPING.get(province)
        
        # Fetch data from Panel Harga Pangan API
        api_response = fetch_panel_harga_data(commodity_key, province_key, data_limit)
        
        if api_response:
            df_historical = parse_panel_harga_data(api_response)
            
            if df_historical is not None and len(df_historical) > 0:
                data_source = "Panel Harga Pangan (Real-time)"
            else:
                st.warning("⚠️ Data dari API kosong, menggunakan data simulasi")
                df_historical = generate_sample_data(commodity, data_limit)
                data_source = "Data Simulasi"
        else:
            st.warning("⚠️ Panel Harga Pangan API tidak tersedia, menggunakan data simulasi")
            df_historical = generate_sample_data(commodity, data_limit)
            data_source = "Data Simulasi"
        
        if df_historical is None or len(df_historical) == 0:
            st.error("Tidak ada data tersedia untuk komoditas dan provinsi ini")
            st.stop()
        
        # Calculate statistics
        stats = calculate_statistics(df_historical)
        
        # Predict future prices
        df_prediction = predict_prices_advanced(df_historical, prediction_days, model_type)
    
    # Display results
    st.markdown("---")
    st.subheader(f"📊 Hasil Analisis - {commodity}")
    st.caption(f"Data source: {data_source} | Total data points: {len(df_historical)}")
    
    # Statistics cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Harga Saat Ini",
            f"Rp {stats['current_price']:,.0f}",
            delta=f"{stats['change_7d']:.1f}% (7d)"
        )
    
    with col2:
        st.metric(
            "Rata-rata 30d",
            f"Rp {stats['avg_30d']:,.0f}",
            help="Rata-rata harga 30 hari terakhir"
        )
    
    with col3:
        st.metric(
            "Min - Max",
            f"Rp {stats['min_price']:,.0f}",
            delta=f"Max: Rp {stats['max_price']:,.0f}"
        )
    
    with col4:
        st.metric(
            "Volatilitas",
            f"Rp {stats['volatility']:,.0f}",
            help="Standar deviasi (ukuran fluktuasi)"
        )
    
    with col5:
        trend_icon = "📈" if stats['trend'] == 'Naik' else "📉"
        st.metric(
            "Tren",
            stats['trend'],
            delta=trend_icon
        )
    
    # Price chart
    st.markdown("---")
    st.subheader("📈 Grafik Tren Harga")
    
    fig = go.Figure()
    
    # Historical prices
    fig.add_trace(go.Scatter(
        x=df_historical['date'],
        y=df_historical['price'],
        mode='lines+markers',
        name='Harga Historical',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=4)
    ))
    
    # Predicted prices
    fig.add_trace(go.Scatter(
        x=df_prediction['date'],
        y=df_prediction['predicted_price'],
        mode='lines',
        name='Prediksi Harga',
        line=dict(color='#10b981', width=3, dash='dash')
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=df_prediction['date'].tolist() + df_prediction['date'].tolist()[::-1],
        y=df_prediction['upper_bound'].tolist() + df_prediction['lower_bound'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(16, 185, 129, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval (95%)',
        showlegend=True
    ))
    
    fig.update_layout(
        title=f"Tren Harga {commodity} - {province}",
        xaxis_title="Tanggal",
        yaxis_title="Harga (Rp/kg)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Prediction table
    st.markdown("---")
    st.subheader(f"🔮 Prediksi {prediction_days} Hari Ke Depan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show predictions
        display_df = df_prediction.copy()
        display_df['date'] = display_df['date'].dt.strftime('%d %b %Y')
        display_df['predicted_price'] = display_df['predicted_price'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['lower_bound'] = display_df['lower_bound'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['upper_bound'] = display_df['upper_bound'].apply(lambda x: f"Rp {x:,.0f}")
        
        display_df.columns = ['Tanggal', 'Prediksi Harga', 'Batas Bawah', 'Batas Atas']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
    
    with col2:
        # Summary predictions
        avg_predicted = df_prediction['predicted_price'].mean()
        final_predicted = df_prediction['predicted_price'].iloc[-1]
        trend_predicted = "Naik" if final_predicted > stats['current_price'] else "Turun"
        change_predicted = ((final_predicted - stats['current_price']) / stats['current_price'] * 100)
        
        st.markdown(f"""
        **Ringkasan Prediksi:**
        
        - **Harga Akhir ({prediction_days}d):** Rp {final_predicted:,.0f}
        - **Rata-rata Prediksi:** Rp {avg_predicted:,.0f}
        - **Tren Prediksi:** {trend_predicted} {" 📈" if trend_predicted == "Naik" else "📉"}
        - **Perubahan:** {change_predicted:+.1f}%
        - **Model:** {model_type.replace('_', ' ').title()}
        - **Confidence:** {(1 - stats['volatility']/stats['avg_price'])*100:.0f}%
        """)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi Trading")
    
    price_change = change_predicted
    
    if price_change > 10:
        st.success(f"""
        **🟢 STRONG BUY / HOLD**
        
        Harga diprediksi naik signifikan **{price_change:.1f}%** dalam {prediction_days} hari.
        
        **Untuk Petani/Supplier:**
        - ✅ TAHAN stok jika memungkinkan
        - ✅ Jual bertahap untuk maximize profit
        - ✅ Monitor harga harian
        
        **Untuk Pembeli/Trader:**
        - ✅ BUY sekarang sebelum harga naik
        - ✅ Stock untuk jangka menengah
        - ✅ Consider futures contract
        """)
    elif price_change > 5:
        st.info(f"""
        **🔵 MODERATE BUY / HOLD**
        
        Harga diprediksi naik moderat **{price_change:.1f}%**.
        
        **Untuk Petani:**
        - Tahan 1-2 minggu untuk harga lebih baik
        - Jual bertahap
        
        **Untuk Pembeli:**
        - Beli untuk kebutuhan normal
        - Tidak perlu panic buying
        """)
    elif price_change < -10:
        st.error(f"""
        **🔴 STRONG SELL**
        
        Harga diprediksi turun signifikan **{abs(price_change):.1f}%**.
        
        **Untuk Petani:**
        - ⚠️ JUAL SEGERA untuk minimize loss
        - ⚠️ Jangan tunda penjualan
        - ⚠️ Diversifikasi ke komoditas lain
        
        **Untuk Pembeli:**
        - ✅ TUNGGU harga turun
        - ✅ Beli minimal sekarang
        - ✅ Stock buying opportunity nanti
        """)
    elif price_change < -5:
        st.warning(f"""
        **🟡 MODERATE SELL**
        
        Harga diprediksi turun **{abs(price_change):.1f}%**.
        
        **Untuk Petani:**
        - Jual dalam 1 minggu
        - Monitor daily price
        
        **Untuk Pembeli:**
        - Tunggu beberapa hari
        - Beli sedikit demi sedikit
        """)
    else:
        st.info(f"""
        **🔵 HOLD / NEUTRAL**
        
        Harga relatif stabil (perubahan {price_change:+.1f}%).
        
        **Untuk Petani:**
        - Jual sesuai cash flow needs
        - Tidak urgent
        
        **Untuk Pembeli:**
        - Beli sesuai kebutuhan normal
        - Harga tidak akan berubah signifikan
        """)
    
    # Download options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Download historical
        csv_historical = df_historical.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Data Historical (CSV)",
            data=csv_historical,
            file_name=f"historical_{commodity}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Download predictions
        csv_prediction = df_prediction.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Prediksi (CSV)",
            data=csv_prediction,
            file_name=f"prediksi_{commodity}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.caption("""
💡 **Data Source:** Panel Harga Pangan - Badan Pangan Nasional (https://panelharga.badanpangan.go.id)

⚠️ **Disclaimer:** Prediksi harga menggunakan machine learning dan data historical. 
Harga aktual dapat berbeda karena faktor eksternal (cuaca, politik, supply-demand, dll). 
Gunakan sebagai referensi, bukan keputusan final. DYOR (Do Your Own Research).
""")
