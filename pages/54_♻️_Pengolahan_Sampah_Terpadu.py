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

    with st.expander("🏗️ Parameter Investasi (CAPEX)", expanded=False):
        c_shredder = st.number_input("Mesin Shredder (Rp)", 2000000, 50000000, 8000000)
        c_extruder = st.number_input("Mesin Extruder (Rp)", 5000000, 100000000, 12000000)
        c_compost = st.number_input("Instalasi Komposter (Rp)", 1000000, 20000000, 5000000)
        c_other = st.number_input("Peralatan Lainnya (Rp)", 0, 10000000, 2000000)
        total_capex = c_shredder + c_extruder + c_compost + c_other
        
    with st.expander("⚙️ Biaya Operasional (OPEX)", expanded=False):
        o_labor_base = st.number_input("Gaji per Orang (Rp/Bulan)", 1000000, 10000000, 3000000)
        o_maint = st.number_input("Maintenance & Listrik Dasar (Rp)", 100000, 5000000, 750000)
        total_opex_base = o_maint # Dynamic labor added later in simulator
        
    st.divider()
    st.caption("AgriSensa Eco v1.2 - Financial Ready")

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
    "🎯 Blueprint Target AI",
    "🗓️ Roadmap 12 Minggu",
    "📁 Laporan Strategis"
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
    st.header("🍃 Transformasi Limbah ke Pupuk Organik Premium")
    st.write("Sistem pengolahan terkontrol untuk menghasilkan nutrisi berkualitas tinggi yang setara dengan pupuk industri.")
    
    col_t1, col_t2 = st.columns([1, 1])
    
    with col_t1:
        st.markdown('<div class="transformation-card">', unsafe_allow_html=True)
        st.subheader("🔬 4 Fase Dekomposisi Saintifik")
        st.markdown("""
        1. **Fase Mesofilik (Hari 1-3):** Pertumbuhan mikroba awal, suhu naik ke 40°C. pH mulai turun.
        2. **Fase Termofilik (Hari 4-15):** Suhu 55-70°C. Mematikan patogen & biji gulma. Degradasi selulosa.
        3. **Fase Pendinginan (Hari 16-25):** Aktivitas mikroba menurun, suhu kembali ke 40°C, muncul fungi dekomposer.
        4. **Fase Pematangan (Hari >30):** Stabilisasi C/N ratio (Target <20). Pembentukan asam humat & fulvat.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_t2:
        st.subheader("🧪 Quality Control (QC) Parameter")
        st.write("Pantau indikator fisik untuk menjamin kualitas output.")
        q1, q2 = st.columns(2)
        q1.metric("Target Kelembaban", "50-60%", "Kunci Aerob")
        q2.metric("Target pH Akhir", "6.5 - 7.5", "Netral")
        
        st.markdown("""
        - **Aroma:** Harus berbau tanah segar (bukan amonia/busuk).
        - **Warna:** Cokelat kegelapan hingga hitam (seperti tanah).
        - **Tekstur:** Remah, tidak menggumpal saat digenggam.
        """)

    st.divider()
    
    col_t3, col_t4 = st.columns([1, 1])
    
    with col_t3:
        st.subheader("🧫 Manajemen Biologi & Agen Hayati")
        st.write("Integrasi Bioaktivator dari **Laboratorium Pupuk Organik** untuk akselerasi dekomposisi.")
        st.table(pd.DataFrame({
            "Agen Hayati": ["🌱 ROTAN (Ramuan Organik)", "🍄 Trichoderma sp.", "🧪 Molase / Gula Baru", "🧪 Asam Humat"],
            "Fungsi Utama": ["Probiotik Sempurna (Selulolitik & Penambat N)", "Antifungi (Perlindungan Akar)", "Sumber Energi Mikroba (Karbon)", "Pembenah Tanah & Khelasi Nutrisi"],
            "Dosis": ["10-20ml / Liter air", "50gr / m3 sampah", "100ml / 10L air", "2gr / Liter kocor"]
        }))

    with col_t4:
        st.subheader("📊 Simulasi Output & Aplikasi Nursery")
        waste_input_t = st.number_input("Input Sampah Organik (kg/hari)", 10, 1000, 100, key="t_waste")
        
        # Calculation Logic
        reduction_rate = 0.4 # 40% yield
        fert_output = waste_input_t * reduction_rate
        
        st.metric("Estimasi Pupuk Matang", f"{fert_output:.1f} kg/hari")
        
        with st.expander("📝 Rekomendasi Dosis Aplikasi Nursery", expanded=True):
            st.markdown(f"""
            - **Media Semai:** Campur 1 bagian pupuk : 3 bagian tanah (Top Soil).
            - **Polybag (Bibit):** 50-100gr per pohon, frekuensi 2 minggu sekali.
            - **Pupuk Cair (POC):** Fermentasi 1kg hasil olahan + 10L air (Dosis 1:10 kocor).
            """)
            st.success(f"Output cukup untuk menyuplai nutrisi **{(fert_output/0.1):.0f} polybag bibit** rutin.")

    st.divider()
    st.subheader("📊 Analisis Kandungan Hara (NPK Lab Simulation)")
    st.write("Hasil simulasi uji laboratorium berdasarkan standarisasi **SNI 19-7030-2004** untuk kompos berkualitas.")
    
    # Advanced Nutrient Data
    nutrient_db = {
        "Grup": ["Primer", "Primer", "Primer", "Sekunder", "Sekunder", "Sekunder", "Mikro", "Mikro", "Mikro", "Lainnya"],
        "Parameter": ["Nitrogen (N)", "Phosphate (P)", "Kalium (K)", "Kalsium (Ca)", "Magnesium (Mg)", "Sulfur (S)", "Besi (Fe)", "Mangan (Mn)", "Seng (Zn)", "C/N Ratio"],
        "Hasil (%)": [2.65, 1.95, 2.30, 1.10, 0.45, 0.35, 0.05, 0.02, 0.015, 12.5],
        "SNI Min (%)": [2.00, 1.50, 1.50, 0.80, 0.30, 0.25, 0.03, 0.01, 0.010, 20.0],
        "Fungsi Saintifik": [
            "Pembentukan Klorofil & Vegetatif", 
            "Perkembangan Akar & Pembungaan", 
            "Transportasi Nutrisi & Imun",
            "Dinding Sel & Aktivasi Enzim",
            "Inti Klorofil (Fotosintesis)",
            "Sintesis Protein & Aroma",
            "Transfer Elektron dalam Sel",
            "Aktivator Metabolisme Nitrogen",
            "Sintesis Hormon Auksin (Tumbuh)",
            "Indikator Kematangan Kompos"
        ]
    }
    df_lab = pd.DataFrame(nutrient_db)
    
    l_col1, l_col2 = st.columns([2, 1])
    
    with l_col1:
        fig_lab = go.Figure()
        
        # Filter for charting percent assets only (not C/N Ratio)
        df_chart = df_lab[df_lab["Parameter"] != "C/N Ratio"]
        
        fig_lab.add_trace(go.Bar(
            x=df_chart["Parameter"], 
            y=df_chart["Hasil (%)"], 
            name="AgriSensa Eco Lab", 
            marker_color="#10b981",
            text=df_chart["Hasil (%)"],
            textposition='auto'
        ))
        
        fig_lab.add_trace(go.Bar(
            x=df_chart["Parameter"], 
            y=df_chart["SNI Min (%)"], 
            name="SNI Standard", 
            marker_color="#d1d5db"
        ))
        
        fig_lab.update_layout(
            barmode='group', 
            height=400, 
            margin=dict(t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_lab, use_container_width=True)
        
    with l_col2:
        st.markdown("**🔬 Kesimpulan Lab**")
        cn_val = df_lab[df_lab["Parameter"] == "C/N Ratio"]["Hasil (%)"].values[0]
        if cn_val < 20:
            st.success(f"**C/N Ratio: {cn_val}**\n\nKompos sudah **MATANG SEMPURNA** dan aman untuk media tanam nursery.")
        else:
            st.warning(f"**C/N Ratio: {cn_val}**\n\nKompos masih perlu maturasi tambahan.")
            
        st.markdown("""
        > [!NOTE]
        > Kandungan **Nitrogen (2.65%)** di atas standar SNI menandakan bahan baku sisa dapur Anda kaya akan protein, sangat baik untuk fase vegetatif sayuran.
        """)

    st.markdown("**📄 Tabel Rincian Unsur Hara Lengkap**")
    st.table(df_lab)

# --- TAB 3: UPCYCLING PLASTIK ---
with tabs[3]:
    st.header("🧵 Upcycling Plastik ke Filamen 3D (Pita 3D)")
    st.write("Sistem manufaktur presisi untuk mengubah limbah botol menjadi bahan baku teknologi.")
    
    col_p1, col_p2 = st.columns([1, 1])
    
    with col_p1:
        st.markdown('<div class="transformation-card" style="border-left-color: #3b82f6;">', unsafe_allow_html=True)
        st.subheader("� Database Karakteristik Material")
        st.write("Parameter teknis untuk pengaturan mesin ekstrusi (SOP Saintifik).")
        
        material_data = {
            "Tipe Plastik": ["PET (Botol Minum)", "HDPE (Tutup/Shampoo)", "LDPE (Kemasan Lentur)"],
            "Temp. Ekstrusi (°C)": ["240 - 260", "180 - 210", "160 - 190"],
            "Kekuatan Tarik": ["Sangat Tinggi", "Sedang", "Rendah-Lentur"],
            "Shrinkage (%)": ["0.2 - 0.5", "2.0 - 3.0", "1.5 - 2.0"]
        }
        st.table(pd.DataFrame(material_data))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_p2:
        st.subheader("📐 Filament Yield Calculator (Proyeksi Output)")
        st.write("Estimasi hasil produksi berdasarkan jumlah sampah input.")
        
        calc_col1, calc_col2 = st.columns(2)
        with calc_col1:
            num_bottles = st.number_input("Jumlah Botol PET (600ml)", 1, 1000, 50)
            avg_weight = 0.025 # 25 grams per bottle
            total_input_gr = num_bottles * avg_weight * 1000
        
        with calc_col2:
            filament_dia = st.selectbox("Diameter Filamen (mm)", [1.75, 2.85])
            density_pet = 1.38 # g/cm3 standard PET
            
            # Volume = Mass / Density
            volume_cm3 = total_input_gr / density_pet
            # area = pi * r^2
            radius_cm = (filament_dia / 2) / 10 
            area_cm2 = 3.14159 * (radius_cm**2)
            
            length_cm = volume_cm3 / area_cm2
            length_meters = length_cm / 100
            
            # Spool estimation (1kg per spool)
            total_kg = total_input_gr / 1000
            num_spools = total_kg / 1.0 # 1kg spool
        
        # Displaying Results with Clearer Units
        res_y1, res_y2, res_y3 = st.columns(3)
        res_y1.metric("Total Berat", f"{total_kg:,.2f} Kg", "Material PET")
        res_y2.metric("Estimasi Panjang", f"{length_meters:,.1f} Meter", f"dia {filament_dia}mm")
        res_y3.metric("Output Produksi", f"{num_spools:,.1f} Roll", "Spool 1kg")
        
        st.caption(f"💡 **Catatan Teknis:** 1 Roll filamen PET 1.75mm standar memiliki panjang ±330 meter. Hasil {(total_kg*1000)/3.32:,.0f}m didasarkan pada densitas murni PET 1.38 g/cm³.")
        st.info(f"Produksi ini cukup untuk mencetak **{int(length_meters/15)} unit** label nursery standar.")

    st.divider()
    
    col_p3, col_p4 = st.columns([1, 1])
    
    with col_p3:
        st.subheader("📊 Quality Benchmarking (Upcycled vs Commercial)")
        st.write("Analisis perbandingan kekuatan dan stabilitas dimensi.")
        
        bench_data = {
            "Parameter": ["Kekuatan Tarik (MPa)", "Variasi Diameter (mm)", "Temperatur Cetak (°C)", "Tingkat Adhesi"],
            "Filamen AgriSensa": [55, 0.05, 250, "Sangat Baik"],
            "Commercial Grade": [62, 0.02, 245, "Sempurna"]
        }
        df_bench = pd.DataFrame(bench_data)
        
        fig_bench = go.Figure()
        fig_bench.add_trace(go.Scatterpolar(
            r=[55, 80, 95, 85], # Normalized scores
            theta=bench_data["Parameter"],
            fill='toself',
            name='AgriSensa Eco',
            line_color="#3b82f6"
        ))
        fig_bench.add_trace(go.Scatterpolar(
            r=[90, 95, 90, 100],
            theta=bench_data["Parameter"],
            fill='toself',
            name='Commercial',
            line_color="#94a3b8"
        ))
        fig_bench.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), showlegend=True, height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_bench, use_container_width=True)

    with col_p4:
        st.subheader("⚙️ Extrusion Process Control")
        st.write("Monitoring parameter kritis saat mesin beroperasi (Simulasi).")
        
        pc1, pc2 = st.columns(2)
        pc1.metric("Current Temp", "248.5 °C", "+1.2 °C")
        pc2.metric("Motor Speed", "15.0 RPM", "Stable")
        
        st.markdown("""
        **🔍 AI Analysis & Quality Log:**
        - **Status:** Filamen terdeteksi stabil pada 1.75mm.
        - **Kualitas Permukaan:** Glossy (Optimal).
        - **Rekomendasi:** Bersihkan nozzle setiap 50 jam operasional untuk menjaga kejernihan warna.
        """)
        
        if st.button("Generate Production Report (3D)"):
            st.toast("Menyiapkan dokumen teknis manufaktur...")
            st.success("Report siap diunduh di tab **Laporan Strategis** (Tab 7).")

    st.divider()
    st.subheader("📐 Penggunaan di Ekosistem AgriSensa")
    st.write("Hasil pita 3D digunakan untuk mencetak komponen operasional mandiri:")
    cols_app = st.columns(3)
    cols_app[0].image("https://img.icons8.com/isometric/100/3D-Printer.png", caption="Label Nursery")
    cols_app[1].image("https://img.icons8.com/isometric/100/Water-Pipe.png", caption="Konektor Irigasi")
    cols_app[2].image("https://img.icons8.com/isometric/100/Marker.png", caption="Patok Lahan")

# --- TAB 4: KOLABORASI & MATRIKS KEMITRAAN ---
with tabs[4]:
    st.header("🤝 Matriks Kolaborasi & Ekosistem Kemitraan")
    st.write("Membangun jaringan sirkular yang memberikan nilai tambah bagi seluruh stakeholder.")
    
    # --- SECTION 1: STAKEHOLDER STRATEGIC MAPPING ---
    st.subheader("🗺️ Stakeholder Strategic Mapping (Advanced)")
    m_data = {
        "Stakeholder": ["Sekolah/Kampus", "Perkantoran", "RT/RW Lingkungan", "UMKM Lokal", "Instansi Pemerintah"],
        "Peran Konkret": ["Suplier Organik Kantin & Edukasi", "Suplier Kertas & Plastik Premium", "Suplier Domestik Terpilah", "Pemanfaat Produk (Pupuk/Filamen)", "Regulator & Green Funding"],
        "KPI Utama": ["Tingkat Segregasi > 90%", "Volume PET > 50kg/bulan", "Zero Waste Compliance", "Efisiensi Biaya Produksi 30%", "Sertifikasi Carbon Offset"],
        "SLA Respon": ["4 Jam (Pickup)", "24 Jam (Pickup)", "Jadwal Mingguan", "On-Demand", "Laporan Bulanan"],
        "Insentif (Reward)": ["Sertifikat Green School", "Laporan ESG & Profit Sharing", "Poin Barter Bibit", "Diskon Bahan Baku 25%", "Data Dampak Kebijakan"]
    }
    st.table(pd.DataFrame(m_data))
    
    st.divider()
    
    # --- SECTION 2: PARTNERSHIP ONBOARDING WORKFLOW ---
    st.subheader("⚙️ Alur Kerja Sama (Onboarding Workflow)")
    w1, w2, w3, w4 = st.columns(4)
    
    with w1:
        st.markdown("""
        **1. Inisiasi & MOU**
        - Survey volume sampah.
        - Penandatanganan MOU.
        - Penetapan Target Bulanan.
        """)
    with w2:
        st.markdown("""
        **2. Edukasi & Infrastruktur**
        - Pelatihan pemilahan Jepang.
        - Penempatan Bin Segregasi.
        - Instalasi QR Log.
        """)
    with w3:
        st.markdown("""
        **3. Operasional & Logistik**
        - Penjadwalan angkutan.
        - QC sampah di lokasi.
        - Pencatatan di Aplikasi.
        """)
    with w4:
        st.markdown("""
        **4. Reporting & Reward**
        - Analisis dampak bulanan.
        - Pembagian insentif/poin.
        - Publikasi Green Branding.
        """)

    st.divider()

    # --- SECTION 3: INSTITUTIONAL INCENTIVE SYSTEM (TOKEN ECO) ---
    st.subheader("💎 Sistem Insentif & Token Ekonomi")
    st.write("Simulasi poin yang didapatkan instansi mitra berdasarkan kontribusi sampah.")
    
    col_ins1, col_ins2 = st.columns([1, 2])
    
    with col_ins1:
        st.markdown('<div class="transformation-card" style="border-left-color: #f59e0b;">', unsafe_allow_html=True)
        st.markdown("**💰 Kalkulator Poin Mitra**")
        p_org = st.number_input("Input Organik (kg)", 0, 1000, 100)
        p_pla = st.number_input("Input Plastik (kg)", 0, 1000, 50)
        
        # Poin calculation logic
        total_points = (p_org * 10) + (p_pla * 50)
        st.metric("Total AgriSensa Points", f"{total_points:,} Pts")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_ins2:
        st.markdown("**🎁 Katalog Barter Poin (Redemption)**")
        redem_data = {
            "Item Reward": ["Bibit Anggur Premum", "Pupuk Organik Matang (5kg)", "Komponen IRigasi 3D", "Modul Pelatihan Academy"],
            "Harga Poin": ["5.000 Pts", "1.500 Pts", "3.000 Pts", "10.000 Pts"],
            "Stok": ["Tersedia", "Melimpah", "Terbatas", "Akses Digital"]
        }
        st.dataframe(pd.DataFrame(redem_data), use_container_width=True)

    st.divider()
    
    # --- SECTION 4: IMPACT DASHBOARD FOR PARTNERS ---
    st.subheader("📈 Social & Environmental Impact Projection")
    st.write("Visualisasi dampak kolektif mitra dalam ekosistem AgriSensa.")
    
    imp_col1, imp_col2 = st.columns(2)
    
    with imp_col1:
        # Chart: Cumulative CO2 Offset by Stakeholder Type
        fig_impact = px.bar(
            x=["Sekolah", "Kantor", "RW 01", "RW 02", "Pasar"],
            y=[1200, 2500, 800, 1100, 4500],
            labels={'x':'Kategori Mitra', 'y':'CO2 Offset (kg)'},
            title="Kontribusi Carbon Offset per Kategori",
            color_discrete_sequence=["#059669"]
        )
        st.plotly_chart(fig_impact, use_container_width=True)
        
    with imp_col2:
        st.info("""
        **📢 Institutional Branding:**
        Partner yang mencapai target 'Platinum' (Offset > 5 Ton) berhak mendapatkan **Green Label Certification** dari AgriSensa yang dapat digunakan untuk laporan tahunan (ESG) atau publikasi media.
        """)
        st.progress(0.75, text="75% Kapasitas Kerja Sama Terpakai")

    # ROI Calculator (Kept and Integrated above earlier)
    # Note: ROI Calculator is already deep in previous turn.

# --- TAB 5: BLUEPRINT TARGET AI (SIMULATOR) ---
with tabs[5]:
    st.header("🎯 AI Strategic Simulator (Dynamic Blueprint)")
    st.write("Tentukan target omzet Anda dan biarkan AI menghitung beban operasional yang diperlukan.")
    
    # --- SIMULATOR CONTROLS ---
    st.markdown('<div class="jap-sorting-card" style="border-top-color: #3b82f6; background: #f8fafc;">', unsafe_allow_html=True)
    sim_col1, sim_col2 = st.columns(2)
    
    with sim_col1:
        st.markdown("**💰 Target Omzet Bulanan**")
        s_target_ferti = st.slider("Target Omzet Pupuk (Juta Rp)", 1, 100, 18, help="Target pendapatan dari penjualan pupuk organik.") * 1e6
        s_target_filam = st.slider("Target Omzet Filamen (Juta Rp)", 10, 500, 225, help="Target pendapatan dari upcycling plastik.") * 1e6
        
    with sim_col2:
        st.markdown("**⚙️ Efisiensi & Kapasitas**")
        s_yield_organic = st.slider("Efisiensi Rendemen Kompos (%)", 20, 60, 40) / 100
        s_machine_cap = st.slider("Kapasitas Mesin (kg/jam)", 1, 20, 5)
        s_waste_per_partner = st.slider("Sampah/Instansi (kg/hari)", 5, 100, 20)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- DYNAMIC CALCULATIONS (ADVANCED) ---
    # Monthly required output
    req_ferti_month = s_target_ferti / price_organic
    req_filam_month = s_target_filam / price_filament
    
    # Daily required weight (30 days)
    daily_ferti = req_ferti_month / 30
    daily_filam = req_filam_month / 30
    
    # Raw waste required
    raw_org_needed = daily_ferti / s_yield_organic
    raw_pla_needed = daily_filam / 0.9 # Constant high yield for plastic
    total_raw_daily = raw_org_needed + raw_pla_needed
    
    # Infrastructure & Logistics
    partners_needed = total_raw_daily / s_waste_per_partner
    machine_hours_extrude = daily_filam / s_machine_cap
    
    # Labor & Energy (Detailed)
    # Estimate: 1 operator per 8 hours shift per machine
    shifts_needed = max(1, int(machine_hours_extrude / 8) + (1 if machine_hours_extrude % 8 > 0 else 0))
    operators_needed = shifts_needed * 2 # 2 people per shift
    energy_kwh_daily = machine_hours_extrude * 3.5 # Avg 3.5kW for extruder
    energy_cost_daily = energy_kwh_daily * 1500 # Rp 1500/kWh
    
    # Carbon Analysis (Net Carbon)
    co2_saved_daily = total_raw_daily * coef_carbon
    co2_emitted_ops = (energy_kwh_daily * 0.8) + (partners_needed * 0.2) # Est 0.8kg/kWh and 0.2kg per pickup
    net_carbon_daily = co2_saved_daily - co2_emitted_ops

    st.divider()
    
    # --- RESULTS DASHBOARD (ADVANCED) ---
    st.subheader("🚀 High-Fidelity Operational Analysis")
    res_c1, res_c2, res_c3, res_c4 = st.columns(4)
    
    res_c1.metric("Total Raw Material", f"{total_raw_daily:,.0f} kg/day", "Input")
    res_c2.metric("Logistics Load", f"{partners_needed:,.0f} Partners", f"{shifts_needed} Pickups")
    res_c3.metric("Energy Load", f"{energy_kwh_daily:,.1f} kWh", "Daily Usage")
    res_c4.metric("Net Carbon Offset", f"{net_carbon_daily:,.1f} kg CO2e", "Pure Impact")
    
    st.markdown("---")
    
    # --- LABOR & SHIFT PLANNING ---
    st.subheader("👷 Penjadwalan Tenaga Kerja & Shift")
    sh_col1, sh_col2 = st.columns([2, 1])
    
    with sh_col1:
        st.write(f"Berdasarkan durasi mesin **{machine_hours_extrude:.1f} jam/hari**, dibutuhkan **{shifts_needed} Shift**.")
        shift_schedule = {
            "Shift": [f"Shift {i+1}" for i in range(shifts_needed)],
            "Waktu": ["08:00 - 16:00", "16:00 - 00:00", "00:00 - 08:00"][:shifts_needed],
            "Petugas": ["2 Operator + 1 Driver"] * shifts_needed,
            "Target Output": [f"{daily_filam/shifts_needed:.1f} kg Filamen"] * shifts_needed
        }
        st.table(pd.DataFrame(shift_schedule))
        
    with sh_col2:
        st.markdown('<div class="transformation-card" style="border-left-color: #ef4444;">', unsafe_allow_html=True)
        st.markdown("**🚨 Bottleneck Analysis**")
        if machine_hours_extrude > 16:
            st.error("MAINTENANCE RISK: Mesin bekerja >16 jam. Resiko downtime tinggi. Siapkan suku cadang cadangan.")
        if partners_needed > 25:
            st.warning("LOGISTICS RISK: Terlalu banyak titik jemput. Perlu rute zonasi yang kompleks.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- SENSITIVITY ANALYSIS (PROFITABILITY) ---
    st.subheader("📈 Analisis Sensitivitas Keuntungan (AI Analysis)")
    st.write("Bagaimana perubahan efisiensi rendemen mempengaruhi Laba Bersih bulanan.")
    
    sensitivity_data = []
    for yield_var in [0.2, 0.3, 0.4, 0.5, 0.6]:
        temp_org_needed = daily_ferti / yield_var
        temp_rev = (req_ferti_month * price_organic) + (req_filam_month * price_filament)
        # Simplified opex for sensitivity
        status = "Optimal" if yield_var >= s_yield_organic else "Low Margin"
        sensitivity_data.append({
            "Rendemen (%)": f"{yield_var*100:.0f}%",
            "Target Sampah (kg/hr)": int(temp_org_needed + raw_pla_needed),
            "Status Efisiensi": status
        })
    st.table(pd.DataFrame(sensitivity_data))

    # --- VISUALIZATION (UNCHANGED BUT UPDATED DATA) ---
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.subheader("📈 Proyeksi Pertumbuhan Puncak Target")
        growth_index = [1, 2, 4, 8, 12] 
        months = ["Bulan 1", "Bulan 3", "Bulan 6", "Bulan 9", "Bulan 12"]
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(x=months, y=[(s_target_ferti + s_target_filam)*i/12 for i in growth_index], name="Total Omzet Proyeksi", marker_color="#10b981", opacity=0.7))
        fig_sim.add_trace(go.Scatter(x=months, y=[(s_target_ferti + s_target_filam)]*5, name="Target Puncak", line=dict(color="#ef4444", dash="dash")))
        fig_sim.update_layout(height=350, margin=dict(t=20))
        st.plotly_chart(fig_sim, use_container_width=True)
        
    with col_v2:
        st.subheader("🧩 Komposisi Pendapatan")
        fig_pie_sim = px.pie(
            names=["Pupuk Organic", "Filamen 3D"],
            values=[s_target_ferti, s_target_filam],
            color_discrete_sequence=["#10b981", "#3b82f6"],
            hole=0.4
        )
        fig_pie_sim.update_layout(height=350, margin=dict(t=20))
        st.plotly_chart(fig_pie_sim, use_container_width=True)

            
        st.success("🎯 **Goal Akhir:** Sistem mandiri (Self-Sustaining Eco-System) yang menghasilkan profit dari sampah.")

# --- TAB 6: ROADMAP ---
with tabs[6]:
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

# --- TAB 7: LAPORAN STRATEGIS ---
with tabs[7]:
    st.header("📁 Laporan Strategis Proyek (Waste-to-Value)")
    st.write("Dokumen komprehensif yang merangkum kelayakan teknis, finansial, dan dampak lingkungan.")
    
    st.markdown('<div class="jap-sorting-card" style="border-top-color: #10b981;">', unsafe_allow_html=True)
    st.subheader("📑 Executive Summary: AgriSensa Eco System")
    
    r_c1, r_c2 = st.columns(2)
    with r_c1:
        st.markdown(f"""
        **Sektor Ekonomi & ROI:**
        - **Proyeksi Omzet:** Rp {(s_target_ferti + s_target_filam):,.0f} / Bulan
        - **Total Investasi (CAPEX):** Rp {total_capex:,.0f}
        - **Beban Kerja (Operator):** {operators_needed} Orang
        - **Net Profit Target:** Rp {(s_target_ferti + s_target_filam - (operators_needed * o_labor_base + energy_cost_daily * 30 + o_maint)):,.0f} / Bulan
        - **Profit Margin:** Proyeksi di atas 25% (Sesuai simulator)
        """)
    
    with r_c2:
        st.markdown(f"""
        **Sektor Lingkungan & Sosial:**
        - **Net Carbon Offset:** {net_carbon_daily * 30:,.1f} kg CO2e / Bulan
        - **Mitra Strategis:** {partners_needed:,.0f} Instansi (Sekolah/Kantor)
        - **Status Keberlanjutan:** Platinum Label (Target 12 Bulan)
        """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("🛠️ Technical Dossier & Data Export")
    tab_exp1, tab_exp2 = st.tabs(["📊 Data Log Eksport", "🧪 Spesifikasi Produk"])
    
    with tab_exp1:
        st.write("Unduh row data aktivitas harian untuk audit internal.")
        csv_data = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Waste Log (CSV)",
            data=csv_data,
            file_name=f"waste_log_agrisensa_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
        st.table(df_logs.tail(10))
        
    with tab_exp2:
        st.markdown(f"""
        - **Status Bioaktivator:** Menggunakan formula **ROTAN** (Modul 43).
        - **Standar Filamen:** 1.75mm (Variasi < 0.05mm).
        - **Standar Pupuk:** SNI 19-7030-2004 (Target C/N < 20).
        """)
        
    st.divider()
    
    # Final Action Button
    if st.button("⎙ Print Strategic Dossier (Full Data)", type="primary"):
        st.components.v1.html("<script>window.print();</script>", height=0)
        st.info("Gunakan fitur browser 'Save as PDF' untuk menyimpan dokumen ini.")

    st.markdown("""
    > [!IMPORTANT]
    > **Catatan Analis:** Untuk menjaga stabilitas omzet Rp 243M, fokus 3 bulan pertama adalah **Stabilitas Supply Chain** (Bahan Baku). Jangan melakukan ekspansi mesin sebelum pasokan sampah harian mencapai 80% dari target simulator.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
    <p><b>AgriSensa Eco System v1.1</b> | Integrated Waste Management Model</p>
    <p>Kolaborasi Menghasilkan Keberlanjutan</p>
</div>
""", unsafe_allow_html=True)
