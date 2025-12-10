
# Peta Sebaran Harga (Map Visualization)
# Displays Bapanas Map Data (Producer/Geometrik Price)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

# Import Services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.bapanas_service import BapanasService
from utils.bapanas_constants import COMMODITY_MAPPING

st.set_page_config(page_title="Peta Sebaran Harga", page_icon="🗺️", layout="wide")

bapanas_service = BapanasService()

st.title("🗺️ Peta Sebaran Harga Pangan (Nasional)")
st.markdown("""
<div style='background-color: #fffbeb; padding: 1rem; border-radius: 10px; border-left: 5px solid #d97706; margin-bottom: 20px;'>
    <strong>⚠️ Catatan Data:</strong><br>
    Data pada peta ini menggunakan endpoint <strong>Peta Sebaran</strong> Bapanas.
    Nilai harga (Geometrik) mungkin berbeda dengan harga eceran pasar karena seringkali merefleksikan 
    <strong>Harga Produsen/Grosir (Hulu)</strong> atau menggunakan metodologi rata-rata yang berbeda.
</div>
""", unsafe_allow_html=True)

# sidebar
with st.sidebar:
    st.header("⚙️ Konfigurasi Peta")
    
    # Selection
    selected_commodity = st.selectbox("Pilih Komoditas", list(COMMODITY_MAPPING.keys()), index=0)
    commodity_id = COMMODITY_MAPPING[selected_commodity]
    
    # NOTE: Defaulting to Level 3 (as per user finding), but maybe switchable in future
    # level_id = st.radio("Level Harga", [1, 3], format_func=lambda x: "Konsumen (1)" if x==1 else "Produsen/Grosir (3)")
    # Since Level 3 returned logic in debugging, we try that. But debug showed Level 1 in response anyway.
    level_id = 3 

# Main Logic
if st.button("🔄 Muat Peta Harga", type="primary", use_container_width=True):
    with st.spinner(f"Menarik data peta '{selected_commodity}' dari Bapanas..."):
        df_map = bapanas_service.get_price_map_data(commodity_id=commodity_id, level_id=level_id)
        
        if df_map is not None and not df_map.empty:
            st.session_state['map_data'] = df_map
            st.session_state['map_commodity'] = selected_commodity
            st.success(f"Berhasil memuat data dari {len(df_map)} provinsi!")
        else:
            st.error("Gagal memuat data peta. Mungkin data untuk komoditas ini belum tersedia hari ini.")

# Display if data exists
if 'map_data' in st.session_state:
    df = st.session_state['map_data']
    comm_name = st.session_state['map_commodity']
    
    # 1. MAP VISUALIZATION (Plotly Bubble Map)
    st.subheader(f"📍 Sebaran Harga {comm_name}")
    
    # Create size based on price (normalized for visual)
    # Min size 5, Max size 20
    
    fig = px.scatter_mapbox(
        df, 
        lat="lat", 
        lon="lon", 
        hover_name="province", 
        hover_data={"price": ":,.0f", "lat": False, "lon": False},
        color="price",
        size="price",
        color_continuous_scale=px.colors.sequential.Jet,
        size_max=25,
        zoom=3.5,
        center={"lat": -2.5, "lon": 118},
        title=f"Heatmap Harga {comm_name} (Rp/kg)",
        mapbox_style="carto-positron" # or open-street-map
    )
    
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. ANALYSIS (Ranking)
    st.markdown("---")
    st.subheader("📊 Analisis Wilayah")
    
    c1, c2 = st.columns(2)
    
    # Top 5 Cheapest
    cheapest = df.sort_values('price', ascending=True).head(5)
    with c1:
        st.info("📉 5 Provinsi Termurah")
        for i, row in cheapest.iterrows():
            st.markdown(f"**{row['province']}**: Rp {row['price']:,.0f}")
            
    # Top 5 Expensive
    expensive = df.sort_values('price', ascending=False).head(5)
    with c2:
        st.error("📈 5 Provinsi Termahal")
        for i, row in expensive.iterrows():
            st.markdown(f"**{row['province']}**: Rp {row['price']:,.0f}")

    # Data Table
    st.markdown("---")
    with st.expander("📋 Lihat Data Lengkap (Tabel)"):
        st.dataframe(
            df[['province', 'price', 'status']].sort_values('price', ascending=False),
            column_config={
                "province": "Provinsi",
                "price": st.column_config.NumberColumn("Harga (Geometrik)", format="Rp %d"),
                "status": "Status Indikator"
            },
            use_container_width=True
        )

else:
    st.info("👆 Klik tombol 'Muat Peta Harga' untuk melihat visualisasi.")
