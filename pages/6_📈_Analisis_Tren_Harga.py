# Analisis Tren Harga
# Prediksi harga komoditas dengan machine learning

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import json
import os

st.set_page_config(page_title="Analisis Tren Harga", page_icon="📈", layout="wide")

# ========== DATA STORAGE ==========
PRICE_DATA_FILE = "data/price_history.json"

# Sample historical price data (1 year)
def generate_sample_data(commodity, days=365):
    """Generate sample price data for demonstration"""
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
    }
    
    base_price = base_prices.get(commodity, 10000)
    dates = [datetime.now() - timedelta(days=days-i) for i in range(days)]
    
    # Generate realistic price pattern with seasonality
    trend = np.linspace(0, 0.2, days)  # Slight upward trend
    seasonal = 0.15 * np.sin(2 * np.pi * np.arange(days) / 365)  # Yearly seasonality
    noise = np.random.normal(0, 0.05, days)  # Random fluctuation
    
    prices = base_price * (1 + trend + seasonal + noise)
    
    return pd.DataFrame({
        'date': dates,
        'price': prices,
        'commodity': commodity
    })

# ========== ML FUNCTIONS ==========
def predict_prices(df, days_ahead=30, model_type='linear'):
    """Predict future prices using ML"""
    # Prepare data
    df = df.sort_values('date')
    df['days'] = (df['date'] - df['date'].min()).dt.days
    
    X = df[['days']].values
    y = df['price'].values
    
    if model_type == 'polynomial':
        # Polynomial regression for better curve fitting
        poly = PolynomialFeatures(degree=3)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        
        # Predict future
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        future_days_poly = poly.transform(future_days)
        predictions = model.predict(future_days_poly)
    else:
        # Simple linear regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict future
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        predictions = model.predict(future_days)
    
    # Create future dates
    last_date = df['date'].max()
    future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
    
    # Calculate confidence interval (simple approach)
    residuals = y - model.predict(X_poly if model_type == 'polynomial' else X)
    std_error = np.std(residuals)
    
    return pd.DataFrame({
        'date': future_dates,
        'predicted_price': predictions,
        'lower_bound': predictions - 1.96 * std_error,
        'upper_bound': predictions + 1.96 * std_error
    })

def calculate_statistics(df):
    """Calculate price statistics"""
    return {
        'current_price': df['price'].iloc[-1],
        'avg_price': df['price'].mean(),
        'min_price': df['price'].min(),
        'max_price': df['price'].max(),
        'volatility': df['price'].std(),
        'trend': 'Naik' if df['price'].iloc[-1] > df['price'].iloc[0] else 'Turun'
    }

# ========== MAIN APP ==========
st.title("📈 Analisis Tren Harga Komoditas")
st.markdown("**Prediksi harga dengan Machine Learning & Visualisasi Tren**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 📊 Visualisasi tren harga historical (1 tahun)
    - 🤖 Prediksi harga 30 hari ke depan dengan ML
    - 📉 Analisis volatilitas dan statistik
    - 💡 Rekomendasi waktu beli/jual
    
    **Cara Menggunakan:**
    1. Pilih komoditas yang ingin dianalisis
    2. Pilih periode historical data
    3. Pilih model prediksi (Linear/Polynomial)
    4. Lihat hasil prediksi dan rekomendasi
    
    **Catatan:**
    - Data ini adalah simulasi untuk demo
    - Untuk produksi, integrate dengan API harga real-time
    - Model akan lebih akurat dengan data real
    """)

# Input Section
st.subheader("⚙️ Konfigurasi Analisis")

col1, col2, col3 = st.columns(3)

with col1:
    commodity = st.selectbox(
        "Pilih Komoditas",
        ["Cabai Merah", "Cabai Rawit", "Tomat", "Kentang", 
         "Bawang Merah", "Bawang Putih", "Padi", "Jagung"],
        help="Pilih komoditas untuk analisis"
    )

with col2:
    historical_days = st.slider(
        "Periode Historical (hari)",
        min_value=30,
        max_value=365,
        value=180,
        step=30,
        help="Jumlah hari data historical untuk analisis"
    )

with col3:
    model_type = st.selectbox(
        "Model Prediksi",
        ["linear", "polynomial"],
        format_func=lambda x: "Linear Regression" if x == "linear" else "Polynomial Regression",
        help="Linear: simple & cepat, Polynomial: lebih akurat untuk pola kompleks"
    )

# Generate and analyze data
if st.button("🔍 Analisis Harga", type="primary", use_container_width=True):
    
    with st.spinner("Menganalisis data harga..."):
        # Generate sample data
        df_historical = generate_sample_data(commodity, historical_days)
        
        # Calculate statistics
        stats = calculate_statistics(df_historical)
        
        # Predict future prices
        df_prediction = predict_prices(df_historical, days_ahead=30, model_type=model_type)
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Hasil Analisis")
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Harga Saat Ini",
            f"Rp {stats['current_price']:,.0f}",
            delta=f"{((stats['current_price'] - stats['avg_price']) / stats['avg_price'] * 100):.1f}% vs avg"
        )
    
    with col2:
        st.metric(
            "Rata-rata",
            f"Rp {stats['avg_price']:,.0f}",
            help="Rata-rata harga dalam periode"
        )
    
    with col3:
        st.metric(
            "Volatilitas",
            f"Rp {stats['volatility']:,.0f}",
            help="Standar deviasi harga (ukuran fluktuasi)"
        )
    
    with col4:
        trend_delta = "📈" if stats['trend'] == 'Naik' else "📉"
        st.metric(
            "Tren",
            stats['trend'],
            delta=trend_delta
        )
    
    # Price chart
    st.markdown("---")
    st.subheader("📈 Grafik Tren Harga")
    
    fig = go.Figure()
    
    # Historical prices
    fig.add_trace(go.Scatter(
        x=df_historical['date'],
        y=df_historical['price'],
        mode='lines',
        name='Harga Historical',
        line=dict(color='#3b82f6', width=2)
    ))
    
    # Predicted prices
    fig.add_trace(go.Scatter(
        x=df_prediction['date'],
        y=df_prediction['predicted_price'],
        mode='lines',
        name='Prediksi Harga',
        line=dict(color='#10b981', width=2, dash='dash')
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
        title=f"Tren Harga {commodity}",
        xaxis_title="Tanggal",
        yaxis_title="Harga (Rp/kg)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Prediction table
    st.markdown("---")
    st.subheader("🔮 Prediksi 30 Hari Ke Depan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Show first 10 days
        display_df = df_prediction.head(10).copy()
        display_df['date'] = display_df['date'].dt.strftime('%d %b %Y')
        display_df['predicted_price'] = display_df['predicted_price'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['lower_bound'] = display_df['lower_bound'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['upper_bound'] = display_df['upper_bound'].apply(lambda x: f"Rp {x:,.0f}")
        
        display_df.columns = ['Tanggal', 'Prediksi Harga', 'Batas Bawah', 'Batas Atas']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        st.caption("Menampilkan 10 hari pertama. Scroll untuk melihat lebih banyak.")
    
    with col2:
        # Summary predictions
        avg_predicted = df_prediction['predicted_price'].mean()
        trend_predicted = "Naik" if df_prediction['predicted_price'].iloc[-1] > df_prediction['predicted_price'].iloc[0] else "Turun"
        
        st.markdown(f"""
        **Ringkasan Prediksi:**
        
        - **Harga Prediksi (30 hari):** Rp {avg_predicted:,.0f}
        - **Tren Prediksi:** {trend_predicted} {"📈" if trend_predicted == "Naik" else "📉"}
        - **Perubahan:** {((avg_predicted - stats['current_price']) / stats['current_price'] * 100):.1f}%
        - **Model:** {model_type.title()}
        """)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi")
    
    # Simple recommendation logic
    price_change = ((avg_predicted - stats['current_price']) / stats['current_price'] * 100)
    
    if price_change > 5:
        st.success(f"""
        **🟢 REKOMENDASI: TAHAN/JUAL NANTI**
        
        Harga diprediksi naik {price_change:.1f}% dalam 30 hari ke depan.
        
        **Untuk Petani:**
        - Tahan hasil panen jika memungkinkan
        - Jual bertahap untuk mitigasi risiko
        - Monitor harga real-time
        
        **Untuk Pembeli:**
        - Beli sekarang sebelum harga naik
        - Stock untuk kebutuhan jangka menengah
        """)
    elif price_change < -5:
        st.warning(f"""
        **🟡 REKOMENDASI: JUAL SEKARANG**
        
        Harga diprediksi turun {abs(price_change):.1f}% dalam 30 hari ke depan.
        
        **Untuk Petani:**
        - Jual hasil panen sekarang
        - Jangan tunda penjualan
        - Pertimbangkan diversifikasi komoditas
        
        **Untuk Pembeli:**
        - Tunggu harga turun
        - Beli dalam jumlah kecil dulu
        """)
    else:
        st.info(f"""
        **🔵 REKOMENDASI: HARGA STABIL**
        
        Harga relatif stabil (perubahan {price_change:.1f}%).
        
        **Untuk Petani:**
        - Jual sesuai kebutuhan cash flow
        - Tidak perlu terburu-buru
        
        **Untuk Pembeli:**
        - Beli sesuai kebutuhan normal
        - Harga tidak akan berubah signifikan
        """)
    
    # Download predictions
    st.markdown("---")
    csv = df_prediction.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Prediksi (CSV)",
        data=csv,
        file_name=f"prediksi_harga_{commodity}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.caption("""
💡 **Disclaimer:** Prediksi harga ini menggunakan machine learning dan data historical. 
Harga aktual dapat berbeda karena faktor eksternal (cuaca, politik, supply-demand, dll). 
Gunakan sebagai referensi, bukan keputusan final.
""")
