import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Agrowisata Petik Langsung Pro",
    page_icon="🍓",
    layout="wide"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        background-color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🍓 Agrowisata Petik Langsung Premium V2")
st.markdown("""
**Transformasi Lahan Menjadi Destinasi Wisata Bernilai Tinggi!**
Modul ini menggabungkan konsep *Experience Economy* dengan *High-Precision Agriculture*. 
Fokus pada integrasi: **Tourism, Production, and Nursery (Yamasa Style).**
""")

st.markdown("---")

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📍 Analisis Kelayakan",
    "🍇 Panduan Komoditas", 
    "💰 Bisnis & ROI",
    "📋 Manajemen & SOP",
    "📅 Kalender Ops",
    "🌱 Yamasa Nursery"
])

# --- TAB 1: ANALISIS KELAYAKAN ---
with tab1:
    st.header("📍 Cek Kesesuaian & Skor Kelayakan")
    st.caption("Gunakan data presisi untuk meminimalkan risiko investasi.")
    
    col_loc1, col_loc2 = st.columns([1, 2])
    
    with col_loc1:
        st.subheader("🛠️ Parameter Lingkungan")
        altitude = st.number_input("Ketinggian Lokasi (mdpl)", 0, 3000, 500, step=50)
        temp_avg = st.slider("Rata-rata Suhu Harian (°C)", 10, 40, 25)
        soil_ph = st.slider("pH Tanah", 3.0, 9.0, 6.0, 0.1)
        humidity = st.slider("Kelembaban Rata-rata (%)", 30, 100, 70)
        
    with col_loc2:
        st.subheader("📊 Hasil Analisis Spesifik")
        
        # Scoring Logic (Simplified)
        score_strawberry = 0
        if altitude >= 1000: score_strawberry += 40
        elif 700 <= altitude < 1000: score_strawberry += 20
        
        if 15 <= temp_avg <= 22: score_strawberry += 30
        if 5.5 <= soil_ph <= 6.5: score_strawberry += 20
        if humidity >= 70: score_strawberry += 10
        
        score_melon = 0
        if altitude < 700: score_melon += 30
        if 25 <= temp_avg <= 32: score_melon += 40
        if 6.0 <= soil_ph <= 7.0: score_melon += 20
        if humidity <= 75: score_melon += 10

        score_grapes = 0
        if altitude < 1000: score_grapes += 30
        if 25 <= temp_avg <= 35: score_grapes += 40
        if 6.0 <= soil_ph <= 7.5: score_grapes += 20
        if humidity <= 70: score_grapes += 10

        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Strawberry Suitability", f"{score_strawberry}%")
        m2.metric("Melon Suitability", f"{score_melon}%")
        m3.metric("Grapes Suitability", f"{score_grapes}%")

        # Gauge Chart
        fig_score = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = max(score_strawberry, score_melon, score_grapes),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Highest Feasibility Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "limegreen"}],
            }
        ))
        fig_score.update_layout(height=300)
        st.plotly_chart(fig_score, use_container_width=True)

        if max(score_strawberry, score_melon, score_grapes) < 50:
            st.error("⚠️ Lokasi ini memiliki tantangan tinggi. Disarankan menggunakan Greenhouse dengan kontrol iklim total.")
        elif max(score_strawberry, score_melon, score_grapes) < 80:
            st.warning("✅ Lokasi cukup baik, namun perlu penyesuaian teknis di beberapa parameter.")
        else:
            st.success("⭐ LOKASI PRIMA! Potensi hasil maksimal dengan input minimal.")

# --- TAB 2: PANDUAN TANAMAN ---
with tab2:
    st.header("🍇 Panduan Komoditas Agrowisata")
    
    # 1. Anggur
    with st.expander("🍇 Anggur Import (Table Grapes)", expanded=True):
        st.markdown("""
        **Kenapa Anggur?** Estetika "Lorong Buah" sangat menjual untuk foto. Buah tahan lama di pohon.
        
        *   **Varietas Manis:** Jupiter (Aroma mangga), Transfiguration (Buah besar), Ninel (Tahan banting/pemula), Julian.
        *   **Sistem Tanam:** Para-para (Datar di atas kepala) untuk *Experience* berjalan di bawah buah.
        *   **Kunci Sukses:**
            *   **Naungan UV:** Wajib pakai plastik UV untuk cegah jamur karena hujan.
            *   **Pruning (Pemangkasan):** Mengatur jadwal berbuah agar bisa panen *saat liburan*.
        """)
        
    # 2. Melon
    with st.expander("🍈 Melon Premium (Eksklusif)", expanded=False):
        st.markdown("""
        **Kenapa Melon?** Kesan mewah, panen serentak, rasa sangat manis (Honey Globe/Golden).
        
        *   **Varietas:** Intanon (Kulit kuning net), Fujisawa, Golden Aroma.
        *   **Sistem Tanam:** Hidroponik Fertigasi (Drip) di Polybag.
        *   **Kaya Visual:** Sistem *Single Stem* (satu pohon satu buah) yang digantung rapi sangat indah difoto.
        *   **Kunci Sukses:** Greenhouse steril (Insect Net) untuk cegah lalat buah.
        """)
        
    # 3. Strawberry
    with st.expander("🍓 Strawberry (Everlasting Favorite)", expanded=False):
        st.markdown("""
        **Kenapa Strawberry?** Ikon agrowisata keluarga. Anak-anak sangat suka memetiknya.
        
        *   **Varietas:** Mencir (Tahan agak panas), California (Besar), Sweet Charlie (Manis).
        *   **Sistem Tanam:** 
            *   *Polybag Bertingkat (Gunungan):* Hemat tempat, estetik.
            *   *Gantung (Hanging):* Unik, buah tidak kotor kena tanah.
        *   **Kunci Sukses:** Pupuk Kalium tinggi saat berbunga, buang sulur (runner) agar fokus ke buah.
        """)
        
    # 4. Bunga & Refugia
    with st.expander("🌻 Bunga Estetik & Refugia (Wajib Ada!)", expanded=False):
        st.markdown("""
        **Fungsi Ganda:** Spot Selfie (Daya tarik visual) + Rumah Predator Alami (Pengendali Hama).
        
        *   **Bunga Matahari (Helianthus):**
            *   *Estetika:* Sangat megah untuk background foto.
            *   *Fungsi:* Menarik lebah (polinator) untuk membantu penyerbukan Melon/Strawberry.
        *   **Marigold (Tagetes):**
            *   *Estetika:* Warna oranye/kuning mencolok, hamparan indah.
            *   *Fungsi:* **Anti-Nematoda** tanah dan mengalihkan perhatian kutu kebul dari tanaman utama.
        *   **Zinnia (Bunga Kertas):**
            *   *Estetika:* Warni-warni ceria.
            *   *Fungsi:* Mengundang musuh alami (kumbang/laba-laba) yang memakan hama ulat.
            
        **Tips Tata Letak:** Tanam bunga di PINGGIR green house atau di sela-sela bedengan sebagai pagar hidup.
        """)

# --- TAB 3: BISNIS & ROI ---
with tab3:
    st.header("💰 Simulasi Investasi & Keuntungan")
    st.info("Agrowisata adalah bisnis padat modal di awal, namun memiliki margin tinggi karena menjual 'pengalaman'.")
    
    # Simulation Mode
    sim_mode = st.radio("Skenario Simulasi", ["Konservatif", "Moderat", "Optimis"], horizontal=True)
    multiplier = {"Konservatif": 0.8, "Moderat": 1.0, "Optimis": 1.3}
    
    col_biz1, col_biz2 = st.columns(2)
    
    with col_biz1:
        st.subheader("🏗️ Investasi Awal (CAPEX)")
        gh_size = st.number_input("Luas Greenhouse (m2)", 0, 10000, 500)
        gh_cost_m2 = st.number_input("Biaya Bangun GH (Rp/m2)", 0, 1000000, 350000)
        system_cost = st.number_input("Sistem Irigasi & Media (Total Rp)", 0, 500000000, 50000000)
        legal_marketing = st.number_input("Legalitas & Branding (Rp)", 0, 100000000, 25000000)
        
        capex_total = (gh_size * gh_cost_m2) + system_cost + legal_marketing
        st.markdown(f"**Total CAPEX: Rp {capex_total:,.0f}**")

    with col_biz2:
        st.subheader("🎟️ Target Operasional (Bulanan)")
        htm_price = st.number_input("Harga Tiket Masuk (Rp)", 0, 100000, 20000)
        visitors_month = st.number_input("Target Pengunjung / Bulan", 0, 10000, 1000) * multiplier[sim_mode]
        fruit_sales_kg = st.number_input("Rata-rata Beli Buah (kg/orang)", 0.0, 5.0, 0.7)
        fruit_price = st.number_input("Harga Jual Buah (Rp/kg)", 0, 200000, 100000)
        
        st.subheader("💸 Biaya Operasional (OPEX/Bulan)")
        labor_cost = st.number_input("Tenaga Kerja (Rp/Bulan)", 0, 100000000, 15000000)
        utility_fert = st.number_input("Listrik & Pupuk (Rp/Bulan)", 0, 50000000, 7000000)
        opex_total = labor_cost + utility_fert
        
    # Financial Analysis
    st.markdown("---")
    rev_ticket = visitors_month * htm_price
    rev_fruit = visitors_month * fruit_sales_kg * fruit_price
    revenue_month = rev_ticket + rev_fruit
    profit_month = revenue_month - opex_total
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue/Bulan", f"Rp {revenue_month:,.0f}")
    m2.metric("Profit/Bulan", f"Rp {profit_month:,.0f}")
    
    # Payback Period Calculation
    if profit_month > 0:
        payback_months = capex_total / profit_month
        m3.metric("Payback Period", f"{payback_months:.1f} Bulan")
        m4.metric("ROI (1 Thn)", f"{(profit_month * 12 / capex_total * 100):.1f}%")
    else:
        st.error("⚠️ Operasional masih defisit. Perlu menaikkan harga tiket atau target pengunjung.")

    # Chart Profit Projection
    months = np.arange(1, 25)
    cumulative_profit = (profit_month * months) - capex_total
    
    fig_roi = go.Figure()
    fig_roi.add_trace(go.Scatter(x=months, y=cumulative_profit, mode='lines+markers', name='Arus Kas Kumulatif'))
    fig_roi.add_trace(go.Scatter(x=months, y=[0]*24, mode='lines', name='Break Even Point', line=dict(color='red', dash='dash')))
    fig_roi.update_layout(title="Proyeksi Break Even Point (2 Tahun)", xaxis_title="Bulan", yaxis_title="Saldo Kas (Rp)")
    st.plotly_chart(fig_roi, use_container_width=True)

# --- TAB 4: MANAJEMEN & SOP ---
with tab4:
    st.header("📋 Standard Operating Procedure (SOP)")
    st.markdown("""
    Bisnis Agrowisata yang sukses bergantung pada **Disiplin Eksekusi** dan **Kenyamanan Wisatawan**.
    """)
    
    col_sop1, col_sop2 = st.columns(2)
    
    with col_sop1:
        with st.expander("🛡️ Protokol Biosecurity (Wajib)", expanded=True):
            st.markdown("""
            1. **Footbath:** Wisatawan wajib menginjak karpet desinfektan sebelum masuk Greenhouse.
            2. **Hand Sanitizer:** Cegah penularan virus dari tangan manusia ke tanaman (terutama Melon/Tomat).
            3. **No Smoking:** Area Greenhouse wajib bebas rokok (asap merusak stomata & residu nikotin beracun).
            4. **Jalur Satu Arah:** Atur alur jalan agar tidak terjadi penumpukan massa di satu titik.
            """)
            
        with st.expander("🧺 Teknik Petik & Penanganan"):
            st.markdown("""
            1. **Gunting Steril:** Jangan memetik dengan menarik paksa. Gunakan gunting kecil yang disediakan.
            2. **Leave No Trace:** Pastikan pengunjung tidak membuang sisa tangkai atau buah rusak di dalam bedengan.
            3. **Sorting di Kasir:** Berikan edukasi cara memilih buah yang benar-benar matang (Brix tinggi).
            """)

    with col_sop2:
        with st.expander("🤳 Strategi Digital Marketing"):
            st.markdown("""
            1. **TikTok/Reels Spots:** Sediakan 3 titik dengan pencahayaan terbaik (Golden Hour) dan background 'lorong buah'.
            2. **User Generated Content (UGC):** Diskon 5% bagi pengunjung yang tag lokasi di Instagram Story.
            3. **Google Maps SEO:** Pastikan titik lokasi akurat dan foto terbaru diupload setiap minggu.
            """)
            
        with st.expander("🎟️ Strategi Pricing & Tiket"):
            st.markdown("""
            1. **Sistem Voucher:** Tiket masuk Rp 20rb dapat ditukar dengan 1 pack bibit atau potongan harga beli buah.
            2. **Paket Edukasi:** Tiket + Panduan Budidaya Singkat + Jus Buah Segar.
            3. **Early Bird:** Diskon untuk kunjungan hari kerja (Weekdays).
            """)

# --- TAB 5: KALENDER OPERASIONAL ---
with tab5:
    st.header("📅 Kalender Budidaya & Liburan")
    st.caption("Penyelarasan masa panen dengan puncak musim liburan nasional (High Season).")
    
    # Simple Calendar Data
    cal_data = {
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nop", "Des"],
        "Status Tanaman": ["Vegetatif", "Vegetatif", "Generatif (Pruning)", "Masa Panen", "Masa Panen", "Masa Istirahat", 
                           "Vegetatif", "Vegetatif", "Generatif", "Masa Panen", "Masa Panen", "Peak Season (Des)"],
        "Level Pengunjung": ["Low", "Low", "Medium (Puasa)", "High (Lebaran)", "Medium", "High (Sekolah)", 
                             "High", "Medium", "Low", "Medium", "High", "Extreme (Nataru)"]
    }
    df_cal = pd.DataFrame(cal_data)
    
    # Highlight Peak Seasons
    def highlight_peak(s):
        return ['background-color: #ffcccc' if v in ['High', 'Extreme'] else '' for v in s]
    
    st.table(df_cal.style.apply(highlight_peak, subset=['Level Pengunjung']))
    
    st.info("""
    **💡 Tip Strategis:**
    *Lakukan Pruning (pemangkasan pembuahan) Anggur 100-110 hari SEBELUM Idul Fitri atau Libur Natal agar buah matang sempurna tepat saat ribuan orang mencari tempat wisata.*
    """)

# --- TAB 6: YAMASA NURSERY ---
with tab6:
    st.header("🌱 Yamasa Seedling Business Simulation")
    st.markdown("""
    **Inspirasi: Yamasa No Niwa, Japan.** 
    Pusat pembibitan yang menggabungkan presisi produksi dengan estetika ruang pajang.
    """)
    
    col_nur1, col_nur2 = st.columns([1, 1])
    
    with col_nur1:
        st.subheader("🏭 Kapasitas Produksi")
        tray_type = st.selectbox("Jenis Tray Semai", ["105 Holes", "128 Holes", "200 Holes"])
        num_trays = st.number_input("Jumlah Tray per Batch", 1, 5000, 100)
        seed_cost_item = st.number_input("Harga Benih per Butir (Rp)", 10, 5000, 500)
        maintenance_cost_tray = st.number_input("Biaya Rawat per Tray (Rp)", 0, 50000, 15000)
        
        total_seeds = int(tray_type.split()[0]) * num_trays
        total_prod_cost = (total_seeds * seed_cost_item) + (num_trays * maintenance_cost_tray)
        
        st.markdown(f"**Total Kapasitas: {total_seeds:,.0f} Bibit**")
        st.markdown(f"**Total Biaya Produksi: Rp {total_prod_cost:,.0f}**")

    with col_nur2:
        st.subheader("📈 Simulasi Penjualan (Dual Stream)")
        
        # Stream 1: Retail Merchandise
        st.markdown("**1. Penjualan Souvenir (Wisatawan)**")
        retail_percent = st.slider("% Bibit Terjual ke Wisatawan", 0, 100, 20)
        retail_price = st.number_input("Harga Jual Wisata (Rp/Pohon)", 5000, 50000, 15000, help="Dalam pot estetik")
        
        # Stream 2: B2B / Farm Supply
        st.markdown("**2. Penjualan B2B (Petani/Mitra)**")
        b2b_percent = st.slider("% Bibit Terjual ke Petani", 0, (100-retail_percent), 60)
        b2b_price = st.number_input("Harga Jual B2B (Rp/Pohon)", 500, 10000, 2500)
        
        # Calculation
        qty_retail = (retail_percent/100) * total_seeds
        qty_b2b = (b2b_percent/100) * total_seeds
        
        rev_nursery = (qty_retail * retail_price) + (qty_b2b * b2b_price)
        profit_nursery = rev_nursery - total_prod_cost
        
    st.markdown("---")
    res_n1, res_n2, res_n3 = st.columns(3)
    res_n1.metric("Total Omzet Nursery", f"Rp {rev_nursery:,.0f}")
    res_n2.metric("Laba Bersih Nursery", f"Rp {profit_nursery:,.0f}")
    res_n3.metric("Margin Keuntungan", f"{(profit_nursery/rev_nursery*100):.1f}%" if rev_nursery > 0 else "0%")

    with st.expander("🇯🇵 Yamasa Standards Checklist (Japan Quality)"):
        st.checkbox("Kebersihan Lantai: Bebas lumut, tanah, dan genangan air.", value=True)
        st.checkbox("Pencahayaan: Minimal 30.000 Lux untuk bibit melon/cabai.", value=True)
        st.checkbox("Pelabelan: Nama varietas, tgl semai, dan tgl siap tanam di setiap tray.", value=True)
        st.checkbox("Uniformity: Tinggi tanaman dalam satu tray harus seragam >95%.", value=True)
        st.success("✅ Memenuhi Standar Yamasa No Niwa")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p><b>Advanced Agrowisata & Nursery Control System</b></p>
    <p>© 2025 AgriSensa - Terinspirasi oleh Inovasi Pertanian Global</p>
</div>
""", unsafe_allow_html=True)
