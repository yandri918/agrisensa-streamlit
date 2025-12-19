import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="AgriSensa Eco - Pengolahan Sampah Terpadu",
    page_icon="♻️",
    layout="wide"
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    .main {
        background-color: #f0fdf4;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .jap-sorting-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-top: 8px solid #059669;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .transformation-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }
    .highlight-text {
        color: #059669;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.title("♻️ Pengolahan Sampah Terpadu (Circular Economy)")
st.markdown("""
**Transformasi Limbah Menjadi Emas Hijau & Bahan Baku Presisi.** 
Modul ini mengadopsi disiplin pengelolaan sampah ala Jepang untuk mendukung ekosistem AgriSensa.
""")

st.markdown("---")

# Navigation Tabs
tabs = st.tabs([
    "🇯🇵 Sistem Pemilahan (Gomi Hiroi)", 
    "🍃 Transformasi Organik", 
    "🧵 Upcycling Plastik (3D Filament)", 
    "🤝 Kolaborasi & ROI"
])

# --- TAB 1: SISTEM PEMILAHAN ---
with tabs[0]:
    st.header("🇯🇵 Pola Pemilahan Gaya Jepang (Gomi Hiroi)")
    st.info("Kunci keberhasilan pengolahan adalah pada **Disiplin Pemilahan di Sumber**.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="jap-sorting-card">', unsafe_allow_html=True)
        st.subheader("🗑️ Kategori Pemilahan Utama")
        st.markdown("""
        1. **Moeru Gomi (Combustible):** Sampah sisa makanan, kertas tisu, sampah organik dapur. -> *Output: Pupuk Cair/Kompos.*
        2. **Moenai Gomi (Non-Combustible):** Kaca, keramik, logam kecil. -> *Output: Bank Sampah.*
        3. **Shigen Gomi (Recyclable):** Botol PET, kaleng, koran/kardus. -> *Output: Bahan Baku 3D / Industri.*
        4. **Plastic Spesifik:** LDPE/HDPE bersih. -> *Output: Filamen Pita 3D.*
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.subheader("📅 Jadwal Pengumpulan Kolektif")
        schedule = {
            "Hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],
            "Kategori": ["Organik Basah", "Plastik (Filamen)", "Organik Basah", "Kertas/Kardus", "Organik Basah", "Sampah Spesial/B3"],
            "Tujuan": ["Unit Kompos", "Unit Shredding", "Unit Kompos", "Bank Sampah", "Unit Kompos", "Karantina B3"]
        }
        st.table(pd.DataFrame(schedule))

# --- TAB 2: TRANSFORMASI ORGANIK ---
with tabs[1]:
    st.header("🍃 Transformasi Limbah ke Pupuk Organik")
    st.write("Mengubah sisa dapur instansi menjadi nutrisi premium untuk AgriSensa Nursery.")
    
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        st.subheader("⚙️ Parameter Kompos")
        waste_input = st.number_input("Input Sampah Organik (kg/hari)", 10, 1000, 100)
        method = st.selectbox("Metode Pengolahan", ["Takakura (Cepat)", "Bokashi (Anaerob)", "Vermikompos (Cacing)"])
        
        # Calculation Logic
        reduction_rate = 0.4 # 40% yield
        fertilizer_output = waste_input * reduction_rate
        
        st.metric("Estimasi Pupuk/Hari", f"{fertilizer_output:.1f} kg")
        st.success(f"Dapat menyuplai nutrisi untuk **{(fertilizer_output/0.5):.0f} bibit** di Nursery.")

    with col_t2:
        st.subheader("📊 Potensi Kandungan Hara (NPK Lab Simulation)")
        st.caption("Hasil olahan sampah organik terpilah dibandingkan standar industri.")
        
        hara_data = {
            "Unsur": ["Nitrogen (N)", "Phosphate (P)", "Kalium (K)", "C/N Ratio"],
            "Hasil Olahan (%)": [2.5, 1.8, 2.1, 15],
            "Standar Minimum (%)": [2.0, 1.5, 1.5, 20]
        }
        df_hara = pd.DataFrame(hara_data)
        
        fig_hara = go.Figure()
        fig_hara.add_trace(go.Bar(x=df_hara["Unsur"], y=df_hara["Hasil Olahan (%)"], name="Hasil AgriSensa Eco", marker_color="#10b981"))
        fig_hara.add_trace(go.Bar(x=df_hara["Unsur"], y=df_hara["Standar Minimum (%)"], name="Standar SNI", marker_color="#94a3b8"))
        fig_hara.update_layout(barmode='group', height=300, margin=dict(t=20))
        st.plotly_chart(fig_hara, use_container_width=True)

# --- TAB 3: UPCYCLING PLASTIK ---
with tabs[2]:
    st.header("🧵 Upcycling Plastik ke Filamen 3D (Pita 3D)")
    st.warning("Eksperimental: Fokus pada sampah botol plastik (PET) dan tutup botol (HDPE).")
    
    col_p1, col_p2 = st.columns([1, 1])
    
    with col_p1:
        st.markdown('<div class="transformation-card">', unsafe_allow_html=True)
        st.subheader("🛠️ Alur Produksi Filamen")
        st.markdown("""
        1. **Cleaning:** Pencucian botol dari residu gula/label.
        2. **Shredding:** Pencacahan plastik menjadi serpihan kecil (flakes).
        3. **Extrusion:** Pemanasan flakes dan penarikan menjadi benang/pita filamen 1.75mm.
        4. **Spooling:** Mengulung filamen ke rol untuk siap digunakan.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_p2:
        st.subheader("📐 Penggunaan di Ekosistem AgriSensa")
        st.write("Hasil pita 3D digunakan untuk mencetak komponen operasional mandiri:")
        cols_app = st.columns(3)
        cols_app[0].image("https://img.icons8.com/isometric/100/3D-Printer.png", caption="Label Nursery")
        cols_app[1].image("https://img.icons8.com/isometric/100/Water-Pipe.png", caption="Konektor Irigasi")
        cols_app[2].image("https://img.icons8.com/isometric/100/Marker.png", caption="Patok Lahan")

# --- TAB 4: KOLABORASI & ROI ---
with tabs[3]:
    st.header("🤝 Model Kolaborasi & Analisis Bisnis")
    
    # Collaborative Model
    st.subheader("🏛️ Skema Kemitraan Instansi (Sekolah/Kantor/RT)")
    with st.expander("Lihat Detail Alur Kerjasama", expanded=True):
        st.markdown("""
        1. **Penyediaan Drop-box:** AgriSensa menyediakan bin sampah terpilah di instansi mitra.
        2. **Koleksi Terjadwal:** Mitra menyetor sampah Moeru Gomi (Organik) & Plastik bersih.
        3. **Reward System (Barter Value):**
            - Setiap 10kg sampah organik = **1 Paket Bibit Sayuran + 1kg Pupuk Olahan.**
            - Setiap 5kg botol plastik = **Voucher Masuk Agrowisata / Souvenir 3D Lab.**
        """)
    
    # ROI Calculator
    st.markdown("---")
    st.subheader("💰 ROI Kalkulator Pengolahan Sampah")
    col_roi1, col_roi2 = st.columns(2)
    
    with col_roi1:
        invest_mesin = st.number_input("Investasi Mesin (Shredder & Extruder) - Rp", 5000000, 100000000, 15000000)
        opex_listrik = st.number_input("Biaya Operasional Bulanan (Listrik/Labor) - Rp", 500000, 10000000, 1500000)
        
    with col_roi2:
        harga_pupuk_pasar = st.number_input("Harga Pupuk Organik Pasar (Rp/kg)", 1000, 5000, 2500)
        harga_filamen_pasar = st.number_input("Harga Filamen 3D Pasar (Rp/kg)", 50000, 500000, 150000)
        
    # Result Calculation
    total_rev_pupuk = (fertilizer_output * 30) * harga_pupuk_pasar
    total_rev_filament = (waste_input * 0.1 * 30) * harga_filamen_pasar # Assume 10% plastic from total waste
    total_revenue_month = total_rev_pupuk + total_rev_filament
    profit_month = total_revenue_month - opex_listrik
    
    st.markdown("---")
    res1, res2, res3 = st.columns(3)
    res1.metric("Revenue Bulanan", f"Rp {total_revenue_month:,.0f}")
    res2.metric("Laba Bersih", f"Rp {profit_month:,.0f}")
    
    if profit_month > 0:
        res3.metric("Break Even Point", f"{(invest_mesin / profit_month):.1f} Bulan")
    else:
        st.error("Biaya operasional lebih besar dari potensi income. Tingkatkan volume input sampah!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
    <p><b>AgriSensa Eco System v1.0</b> | Zero Waste Farming Model</p>
    <p>Kolaborasi Menghasilkan Keberlanjutan</p>
</div>
""", unsafe_allow_html=True)
