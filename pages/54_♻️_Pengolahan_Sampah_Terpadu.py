import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from datetime import datetime

# --- CONFIG & DATA PATHS ---
DATA_DIR = "data"
WASTE_LOG_FILE = os.path.join(DATA_DIR, "waste_log.csv")

def init_waste_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(WASTE_LOG_FILE):
        df = pd.DataFrame(columns=['tanggal', 'tipe', 'berat_kg', 'created_at'])
        df.to_csv(WASTE_LOG_FILE, index=False)

def load_waste_logs():
    if os.path.exists(WASTE_LOG_FILE):
        return pd.read_csv(WASTE_LOG_FILE)
    return pd.DataFrame(columns=['tanggal', 'tipe', 'berat_kg', 'created_at'])

def save_waste_entry(date, waste_type, weight):
    df = load_waste_logs()
    new_entry = {
        'tanggal': date,
        'tipe': waste_type,
        'berat_kg': weight,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(WASTE_LOG_FILE, index=False)
    return df

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

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    st.write("Sesuaikan angka pengali untuk kalkulasi dashboard.")
    
    with st.expander("🌍 Parameter Lingkungan", expanded=True):
        coef_carbon = st.number_input(
            "Koefisien CO2 (kg/kg sampah)", 
            value=0.53, 
            step=0.01,
            help="Jumlah emisi CO2 yang dikurangi per 1kg sampah yang dikelola."
        )
        target_monthly = st.number_input("Target Bulanan (kg)", value=5000, step=500)

    with st.expander("💰 Parameter Ekonomi", expanded=True):
        price_organic = st.number_input(
            "Harga Pupuk (Rp/kg)", 
            value=2500, 
            step=500,
            help="Asumsi nilai ekonomi hasil olahan organik."
        )
        price_filament = st.number_input(
            "Harga Filamen (Rp/kg)", 
            value=150000, 
            step=10000,
            help="Asumsi nilai ekonomi hasil upcycling plastik."
        )
        
    st.divider()
    st.caption("AgriSensa Eco v1.1 - Adjustable Parameters")

# Init Data
init_waste_data()
df_logs = load_waste_logs()

# Navigation Tabs
tabs = st.tabs([
    "📊 Dashboard & KPI",
    "🇯🇵 Sistem Pemilahan", 
    "🍃 Transformasi Organik", 
    "🧵 Upcycling Plastik", 
    "🤝 Kolaborasi & Matriks",
    "🗓️ Roadmap 12 Minggu"
])

# --- TAB 0: DASHBOARD & KPI ---
with tabs[0]:
    st.header("📊 Sustainability Command Center")
    st.write("Metrik konkret untuk mengukur dampak implementasi pengelolaan sampah terpadu.")
    
    # KPI Metrics
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    # Calculation Logic for Dashboard
    total_waste_collected = df_logs['berat_kg'].sum() if not df_logs.empty else 1540 # Default demo value if empty
    organic_processed = df_logs[df_logs['tipe'].str.contains("Organik", na=False)]['berat_kg'].sum() if not df_logs.empty else (total_waste_collected * 0.6)
    plastic_recycled = df_logs[df_logs['tipe'].str.contains("Plastik", na=False)]['berat_kg'].sum() if not df_logs.empty else (total_waste_collected * 0.15)
    
    sustainability_rate = ( (organic_processed + plastic_recycled) / total_waste_collected ) * 100 if total_waste_collected > 0 else 0
    carbon_offset = total_waste_collected * coef_carbon
    money_saved = (organic_processed * price_organic) + (plastic_recycled * price_filament)
    
    kpi_col1.metric("Sustainability Rate", f"{sustainability_rate:.1f}%")
    kpi_col2.metric("Carbon Offset (CO2e)", f"{carbon_offset:,.1f} kg")
    kpi_col3.metric("Economic Value", f"Rp {money_saved/1e6:.2f}M")
    kpi_col4.metric("Instansi Mitra", "12", "+2")
    
    st.markdown("---")
    
    # Daily Log Simulation
    st.subheader("📝 Daily Collection Log")
    log_col1, log_col2 = st.columns([1, 2])
    
    with log_col1:
        log_date = st.date_input("Tanggal Transaksi", datetime.now())
        
        waste_categories = [
            "🍃 Organik (Sisa Makanan)", 
            "🍃 Organik (Ranting/Daun)",
            "🧵 Plastik PET (Botol)", 
            "🧵 Plastik HDPE/LDPE (Kemasan)",
            "📦 Kertas & Kardus",
            "🧴 Kaca & Keramik",
            "🥫 Logam & Kaleng",
            "🔌 Elektronik (E-Waste)",
            "🧤 Tekstil/Kain",
            "⚠️ Limbah B3 (Baterai/Lampu)",
            "➕ Lainnya (Input Manual)"
        ]
        
        selected_cat = st.selectbox("Tipe Sampah", waste_categories)
        
        # Manual Input Logic
        if selected_cat == "➕ Lainnya (Input Manual)":
            waste_type_final = st.text_input("Sebutkan Tipe Sampah", placeholder="Misal: Karet, Kayu Besar, dll")
        else:
            waste_type_final = selected_cat

        weight_in = st.number_input("Berat Masuk (kg)", 0.0, 500.0, 25.0)
        if st.button("Simpan Log Aktivitas"):
            if selected_cat == "➕ Lainnya (Input Manual)" and not waste_type_final:
                st.error("Silakan tulis tipe sampah manual Anda!")
            else:
                save_waste_entry(log_date.strftime("%Y-%m-%d"), waste_type_final, weight_in)
                st.success(f"Berhasil mencatat {weight_in}kg {waste_type_final} ke database!")
                st.rerun()
            
    with log_col2:
        # Mini Chart for Progress
        # (Target taken from sidebar)
        current_progress = total_waste_collected

        if not df_logs.empty:
            st.markdown("**📜 Log Terakhir**")
            st.dataframe(df_logs.tail(5), use_container_width=True)
            st.markdown("---")
        
        fig_progress = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_progress,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Progress Target Bulanan (kg)"},
            delta = {'reference': target_monthly},
            gauge = {
                'axis': {'range': [None, target_monthly]},
                'bar': {'color': "#0fb981"},
                'steps' : [
                    {'range': [0, 2500], 'color': "#ecfdf5"},
                    {'range': [2500, 5000], 'color': "#d1fae5"}]
            }
        ))
        fig_progress.update_layout(height=280, margin=dict(t=50, b=10))
        st.plotly_chart(fig_progress, use_container_width=True)

# --- TAB 1: SISTEM PEMILAHAN ---
with tabs[1]:
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
with tabs[2]:
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
with tabs[3]:
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

# --- TAB 4: KOLABORASI ---
with tabs[4]:
    st.header("🤝 Matriks Kolaborasi & Kemitraan")
    st.write("Pemetaan peran konkret setiap stakeholder dalam ekosistem circular AgriSensa.")
    
    m_data = {
        "Stakeholder": ["Sekolah/Kampus", "Perkantoran", "RT/RW Lingkungan", "UMKM Lokal", "Instansi Pemerintah"],
        "Peran Konkret": ["Suplier Organik Kantin & Edukasi", "Suplier Kertas & Plastik High-Quality", "Suplier Organik Rumah Tangga Terpilah", "Pemanfaat Pupuk untuk Tanaman Hias", "Regulator & Pendanaan Program Green"],
        "Insentif (Reward)": ["Bibit Gratis & Modul Kurikulum", "Sertifikat Carbon Offset & Souvenir 3D", "Pupuk Kompos Gratis Berkala", "Harga Pupuk Subsidi AgriSensa", "Laporan Dampak Keberlanjutan Data-Driven"]
    }
    st.table(pd.DataFrame(m_data))
    
    # ROI Calculator (Moved here)
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

# --- TAB 5: ROADMAP ---
with tabs[5]:
    st.header("🗓️ Roadmap Implementasi (12 Minggu)")
    st.write("Langkah konkret transisi dari perencanaan ke operasional penuh.")
    
    r_col1, r_col2 = st.columns(2)
    
    with r_col1:
        with st.expander("🚀 Fase 1: Setup & Inisiasi (Minggu 1-4)", expanded=True):
            st.markdown("""
            - **W1:** Sosialisasi sistem pemilahan gaya Jepang ke calon mitra.
            - **W2:** Pengadaan bin sampah tersegregasi dan unit shredder plastik.
            - **W3:** Pelatihan SDM operasional (Teknik Composting & 3D Lab).
            - **W4:** Pilot project di 1 instansi (Sekolah/Kantor).
            """)
        
        with st.expander("⚙️ Fase 2: Optimasi Produksi (Minggu 5-8)"):
            st.markdown("""
            - **W5:** Uji lab pertama hasil pupuk organik (Parameter NPK).
            - **W6:** Kalibrasi mesin ekstrusi filamen untuk kualitas pita 3D.
            - **W7:** Peluncuran aplikasi log monitoring harian.
            - **W8:** Evaluasi sistem reward dan barter bibit.
            """)

    with r_col2:
        with st.expander("📈 Fase 3: Scale-up & Komersial (Minggu 9-12)"):
            st.markdown("""
            - **W9:** Ekspansi ke 5-10 instansi mitra baru.
            - **W10:** Integrasi penuh output pupuk ke unit Nursery AgriSensa.
            - **W11:** Penjualan perdana surplus filamen 3D ke komunitas maker.
            - **W12:** Audit dampak lingkungan (Carbon Offset Report).
            """)
            
        st.success("🎯 **Goal Akhir:** Sistem mandiri (Self-Sustaining Eco-System) yang menghasilkan profit dari sampah.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
    <p><b>AgriSensa Eco System v1.0</b> | Zero Waste Farming Model</p>
    <p>Kolaborasi Menghasilkan Keberlanjutan</p>
</div>
""", unsafe_allow_html=True)
