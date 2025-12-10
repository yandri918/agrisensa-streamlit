
# Analisis Tren Harga (Bapanas API Integrated)
# Real-time price analysis dengan data dari Badan Pangan Nasional

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# Import Services
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.bapanas_service import BapanasService
from utils.bapanas_constants import PROVINCE_MAPPING, COMMODITY_MAPPING

st.set_page_config(page_title="Analisis Tren Harga", page_icon="📈", layout="wide")

# Initialize Service
bapanas_service = BapanasService()

# ========== ML FUNCTIONS ==========
def predict_prices_advanced(df, days_ahead=30, model_type='random_forest'):
    """Advanced price prediction with multiple models"""
    if len(df) < 3: # Not enough data for prediction
        # Return dummy prediction for visual if data is too scarce
        last_price = df['price'].iloc[-1]
        future_dates = [df['date'].max() + timedelta(days=i) for i in range(1, days_ahead + 1)]
        return pd.DataFrame({
            'date': future_dates,
            'predicted_price': [last_price] * days_ahead,
            'lower_bound': [last_price * 0.95] * days_ahead,
            'upper_bound': [last_price * 1.05] * days_ahead
        })
        
    df = df.sort_values('date')
    df['days'] = (df['date'] - df['date'].min()).dt.days
    
    X = df[['days']].values
    y = df['price'].values
    
    # Simple logic for scarce data (linear fallback)
    if len(df) < 10 or model_type == 'linear':
        model = LinearRegression()
        model.fit(X, y)
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        predictions = model.predict(future_days)
        std_error = np.std(y - model.predict(X)) if len(y) > 1 else y[0] * 0.05
        
    elif model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        future_days = np.array([[df['days'].max() + i] for i in range(1, days_ahead + 1)])
        predictions = model.predict(future_days)
        std_error = np.std(y - model.predict(X))
    
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
    if df.empty:
        return {}
        
    current_price = df['price'].iloc[-1]
    prev_price = df['price'].iloc[0] if len(df) > 1 else current_price
    
    change_pct = ((current_price - prev_price) / prev_price * 100) if prev_price != 0 else 0
    
    return {
        'current_price': current_price,
        'avg_price': df['price'].mean(),
        'min_price': df['price'].min(),
        'max_price': df['price'].max(),
        'volatility': df['price'].std() if len(df) > 1 else 0,
        'trend': 'Naik 📈' if change_pct > 0.5 else ('Turun 📉' if change_pct < -0.5 else 'Stabil ➖'),
        'change_pct': change_pct
    }

# ========== MAIN APP ==========
st.title("📈 Analisis Tren Harga Pangan (Bapanas Official)")
st.markdown("""
    <div style='background-color: #f0fdf4; padding: 1rem; border-radius: 10px; border-left: 5px solid #10b981; margin-bottom: 20px;'>
        <strong>✅ Official Data Source</strong><br>
        Menggunakan data real-time dari <strong>Badan Pangan Nasional (Bapanas)</strong> - Panel Harga Pangan.
        Data ini adalah acuan resmi pemerintah untuk harga tingkat konsumen/retail di seluruh Indonesia.
    </div>
""", unsafe_allow_html=True)

# Sidebar Config
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    
    # Province Selector
    selected_province_name = st.selectbox(
        "Pilih Provinsi",
        list(PROVINCE_MAPPING.keys()),
        index=0 # Nasional default
    )
    province_id = PROVINCE_MAPPING[selected_province_name]
    
    # Model Selector
    model_type = st.selectbox(
        "Model Prediksi AI",
        ["linear", "random_forest"],
        format_func=lambda x: "Linear Regression (Cepat)" if x == "linear" else "Random Forest (Akurat)",
        index=1
    )
    
    prediction_days = st.slider("Prediksi Hari ke Depan", 7, 60, 30)

# Main Logic
if st.button("🔄 Segarkan Data Harga", type="primary", use_container_width=True):
    with st.spinner(f"Mengambil data resmi Bapanas untuk {selected_province_name}..."):
        try:
            # Fetch Data
            df = bapanas_service.get_latest_prices(province_id=province_id)
            
            if df is not None and not df.empty:
                st.session_state['price_data'] = df
                st.session_state['data_source'] = "Bapanas API v2"
                # Correct message to count unique commodities
                comm_count = df['commodity'].nunique()
                st.success(f"Berhasil memuat {comm_count} jenis komoditas! (Total {len(df)} data poin hari ini & kemarin)")
            else:
                st.error("Gagal mengambil data. Server Bapanas mungkin sibuk atau API Key expired.")
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# Display Data if available
if 'price_data' in st.session_state:
    df_all = st.session_state['price_data']
    
    # 1. Commodity Selector for Detail View
    commodity_list = df_all['commodity'].unique().tolist()
    
    # Filter valid commodities only
    valid_commodities = [c for c in commodity_list if c is not None]
    
    selected_commodity = st.selectbox("🔍 Pilih Komoditas untuk Analisis Detail:", valid_commodities)
    
    if selected_commodity:
        # Filter data specific to commodity
        # Since API currently returns snapshot (today/yesterday), we simulate a small history trend
        # for visualization purposes based on the 'gap' trend if real history is not available
        df_comm = df_all[df_all['commodity'] == selected_commodity].sort_values('date')
        
        stats = calculate_statistics(df_comm)
        
        # Display Stats Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Harga Hari Ini", f"Rp {stats['current_price']:,.0f}", f"{stats['change_pct']:.2f}%")
        with col2:
            st.metric("Tren Harga", stats['trend'])
        with col3:
            st.metric("Volatilitas", f"Rp {stats['volatility']:,.0f}")
        with col4:
            st.metric("Status Data", "Official ✅", "Real-time")
            
        # Prediction & Chart
        df_pred = predict_prices_advanced(df_comm, days_ahead=prediction_days, model_type=model_type)
        
        st.subheader("📊 Grafik Tren & Prediksi")
        
        fig = go.Figure()
        
        # Plot actual data points
        fig.add_trace(go.Scatter(
            x=df_comm['date'], y=df_comm['price'],
            mode='lines+markers', name='Data Aktual (Bapanas)',
            line=dict(color='#0ea5e9', width=3),
            marker=dict(size=8)
        ))
        
        # Plot prediction
        fig.add_trace(go.Scatter(
            x=df_pred['date'], y=df_pred['predicted_price'],
            mode='lines', name=f'Prediksi AI ({model_type})',
            line=dict(color='#10b981', dash='dash')
        ))
        
        fig.update_layout(
            title=f"Dinamika Harga {selected_commodity} - {selected_province_name}",
            xaxis_title="Tanggal", yaxis_title="Harga (Rp)",
            hovermode="x unified",
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Recommendation Section
        st.info(f"""
        💡 **Insight AgriSensa:**
        Harga **{selected_commodity}** saat ini adalah **Rp {stats['current_price']:,.0f}**.
        Berdasarkan data hari ini vs kemarin, tren terlihat **{stats['trend']}**.
        
        *Rekomendasi Petani:* {"Jual Segera" if "Turun" in stats['trend'] else "Bisa Tahan Stok"}
        *Rekomendasi Pembeli:* {"Beli Sekarang" if "Naik" in stats['trend'] else "Tunggu Harga Turun"}
        """)

    # 2. Daily Price Table (Ranked)
    st.markdown("---")
    st.subheader("📋 Daftar Harga Pangan Hari Ini")
    
    # Clean table for display
    display_df = df_all[df_all['date'] == df_all['date'].max()].copy()
    display_df = display_df[['commodity', 'price', 'unit']].sort_values('price', ascending=False)
    display_df['price'] = display_df['price'].apply(lambda x: f"Rp {x:,.0f}")
    display_df.columns = ['Komoditas', 'Harga Konsumen', 'Satuan']
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Harga Konsumen": st.column_config.TextColumn(
                "Harga (Rp)",
                help="Harga tingkat konsumen berdasarkan data Bapanas"
            )
        }
    )

else:
    st.info("👋 Silakan klik tombol 'Segarkan Data Harga' untuk menarik data terbaru dari server Bapanas.")

# Footer with Attribution
st.markdown("---")
st.caption(f"""
    **Sumber Data:** Badan Pangan Nasional (Bapanas) via API Public Endpoint.
    **Last Check:** {datetime.now().strftime('%d-%m-%Y %H:%M')}
    
    *Data ini diambil langsung dari server panelharga.badanpangan.go.id dan diolah oleh AI AgriSensa.*
""")
