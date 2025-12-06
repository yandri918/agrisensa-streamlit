import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Panduan Budidaya Buah", page_icon="🍎", layout="wide")

# ==========================================
# 🌳 DATABASE BUAH TROPIS
# ==========================================
fruit_data = {
    "Durian (Si Raja Buah)": {
        "icon": "🧀",
        "desc": "Durian (*Durio zibethinus*) adalah komoditas buah premium dengan nilai ekonomi tinggi.",
        "syarat": {
            "Iklim": "Curah hujan 1500-2500 mm/tahun, Suhu 23-30°C",
            "Fase Kering": "Butuh 1-3 bulan kering (<60 mm hujan) untuk memicu pembungaan",
            "Ketinggian": "100 - 800 mdpl (Optimal 400-600 mdpl)",
            "Tanah": "Lempung berpasir, subur, gembur, pH 6.0-7.0, Drainase baik (tidak tahan tergenang)"
        },
        "tanam": {
            "Jarak Tanam": "8x8 m (Populasi ~156 pohon/ha) atau 10x10 m (Populasi ~100 pohon/ha)",
            "Lubang Tanam": "60x60x60 cm atau 80x80x80 cm. Biarkan terbuka 2 minggu, campur pupuk kandang 20kg + Dolomit 0.5kg",
            "Bibit": "Gunakan bibit okulasi/sambung pucuk tinggi >80cm, bebas penyakit, daun hijau tua mengkilap"
        },
        "pupuk": {
            "TBM (1-3 th)": "NPK 16-16-16: 200g - 1kg per pohon/tahun (dibagi 4x aplikasi)",
            "TM (>4 th)": "Awal musim hujan (NPK Tinggi N), Menjelang bunga (Tinggi P & K), Pasca Panen (Organik + NPK seimbang)",
            "Boost Buah": "KNO3 Putih saat pentil buah seukuran kelereng"
        },
        "hama": [
            {"nama": "Penggerek Buah", "gejala": "Lubang pada buah, kotoran ulat", "solusi": "Sanitasi buah rontok, Perangkap feromon, Insektisida Deltamethrin"},
            {"nama": "Kanker Batang", "gejala": "Kulit batang mengeluarkan lendir/gumosis", "solusi": "Kerok kulit sakit, olesi fungisida berbahan aktif Tembaga/Mankozeb"}
        ],
        "panen": "Jatuh sendiri (matang fisiologis sempurna) atau petik tua (tangkai mengeras, duri renggang) untuk kiriman jauh. Durasi matang 115-125 hari setelah bunga mekar (tergantung varietas)."
    },
    "Mangga (Export Quality)": {
        "icon": "🥭",
        "desc": "Mangga (*Mangifera indica*) sangat potensial untuk pasar lokal dan ekspor, terutama varietas Gedong Gincu dan Arumanis.",
        "syarat": {
            "Iklim": "Bulan kering 3-4 bulan sangat penting untuk pembungaan. Curah hujan <1500 mm/tahun optimal.",
            "Ketinggian": "0 - 500 mdpl (Dataran Rendah)",
            "Tanah": "Tanah aluvial/latosol, solum dalam (>1m), pH 5.5-7.5"
        },
        "tanam": {
            "Jarak Tanam": "8x8 m atau 10x10 m (Tanpa pangkas), 4x5 m (High Density Planting dengan manajemen tajuk intensif)",
            "Lubang Tanam": "60x60x60 cm. Campurkan 20kg kompos matang.",
            "Waktu": "Awal musim hujan"
        },
        "pupuk": {
            "TBM": "Urea:SP36:KCl (1:1:1) mulai 200g/pohon umur 1 th, naik bertahap.",
            "Induksi Bunga": "ZPT Paklobutrazol (aplikasi siram tanah) pada tanaman sehat umur >3-4 tahun saat daun tua (dorman).",
            "Pembesaran": "Pupuk K tinggi (KNO3) saat buah sebesar telur ayam."
        },
        "hama": [
            {"nama": "Lalat Buah", "gejala": "Buah busuk, ada belatung di dalam", "solusi": "Bungkus buah (brongsong) sejak dini, Perangkap Metil Eugenol"},
            {"nama": "Wereng Mangga", "gejala": "Bunga kering dan rontok, embun jelaga", "solusi": "Insektisida Imidakloprid sebelum bunga mekar sempurna"}
        ],
        "panen": "Petik saat pangkal buah membengkak rata, lekukan ujung hilang, dan kulit mulai berbedak. 85-95% tingkat kematangan untuk pasar jauh."
    },
    "Alpukat (Superfood)": {
        "icon": "🥑",
        "desc": "Alpukat (*Persea americana*) kini menjadi primadona karena tren hidup sehat. Varietas mentega dan aligator sangat diminati.",
        "syarat": {
            "Iklim": "Suhu optimal 20-28°C. Angin kencang dapat merusak percabangan lunak.",
            "Ketinggian": "200 - 1000 mdpl (Tergantung ras: Ras Meksiko tahan dingin, Ras Hindia Barat dataran rendah)",
            "Tanah": "Wajib gembur dan TIDAK BOLEH TERGENANG air sama sekali. pH 6.0-7.0."
        },
        "tanam": {
            "Jarak Tanam": "6x7 m atau 8x8 m",
            "Persiapan": "Buat guludan/busut jika tanah datar untuk hindari genangan air hujan (drainase adalah kunci).",
            "Bibit": "Sambung pucuk, umur >6 bulan di polybag."
        },
        "pupuk": {
            "TBM": "NPK 15-15-15, 4x setahun. Dosis 50g (th 1) naik ke 200g (th 2).",
            "TM": "NPK 12-12-17 + TE saat berbunga dan berbuah. Tambahan Boron penting untuk cegah buah bengkok.",
            "Organik": "Mutlak perlu 20kg/pohon setiap tahun."
        },
        "hama": [
            {"nama": "Ulat Kipat", "gejala": "Daun habis dimakan ulat besar", "solusi": "Kutif manual kepompong, Insektisida kontak"},
            {"nama": "Busuk Akar (Phytophthora)", "gejala": "Daun layu mendadak, akar membusuk", "solusi": "Drainase diperbaiki, Trichoderma pada tanah, Bubur Bordeaux"}
        ],
        "panen": "Warna kulit buah tua (kusam/tidak mengkilap), jika diguncang biji berbunyi (pada beberapa varietas). Petik dengan gunting, sisakan tangkai cm."
    },
    "Manggis (Queen of Fruits)": {
        "icon": "👸",
        "desc": "Manggis (*Garcinia mangostana*) adalah tanaman asli nusantara dengan pertumbuhan lambat namun umur produktif sangat panjang.",
        "syarat": {
            "Iklim": "Lembab tinggi, curah hujan merata >2000 mm/th. Tidak tahan kering ekstrem.",
            "Ketinggian": "100 - 600 mdpl",
            "Naungan": "WAJIB ada naungan (pisang/waru) pada 2-3 tahun pertama karena tidak tahan terik matahari langsung."
        },
        "tanam": {
            "Jarak Tanam": "10x10 m",
            "Lubang Tanam": "Ukuran besar 100x100x50 cm karena perakaran manggis sedikit dan lambat.",
            "Naungan": "Siapkan naungan buatan (paraneti) atau tanaman sela sebelum tanam."
        },
        "pupuk": {
            "Slow Release": "Gunakan pupuk lepas lambat atau organik tinggi karena serapan akar lambat.",
            "Fase": "TBM fokus N untuk daun. TM butuh KCl tinggi untuk kualitas daging buah."
        },
        "hama": [
            {"nama": "Getah Kuning", "gejala": "Getah kuning pada kulit dan daging buah (buah pahit/keras)", "solusi": "Hindari benturan, jaga ketersediaan air tanah stabil, pemupukan Ca dan B"},
            {"nama": "Burik Buah", "gejala": "Kulit buah kasar kecoklatan", "solusi": "Kendalikan Thrips dengan insektisida abamektin saat berbunga"}
        ],
        "panen": "Warna kulit ungu kemerahan (indeks warna 2-3) untuk ekspor. Ungu pekat (indeks 5-6) untuk konsumsi langsung."
    },
     "Jeruk (High Demand)": {
        "icon": "🍊",
        "desc": "Jeruk (Siam, Keprok, Pamelo) adalah buah paling banyak dikonsumsi harian.",
        "syarat": {
            "Iklim": "Suhu 25-30°C. Perbedaan suhu siang-malam membantu warna kulit cerah.",
            "Ketinggian": "0 - 1200 mdpl (Siam dataran rendah, Keprok dataran tinggi)",
            "Tanah": "Andosol atau Latosol. pH 5.5 - 6.5. Tidak tahan genangan."
        },
        "tanam": {
            "Jarak Tanam": "3x4 m atau 5x5 m",
            "Lubang Tanam": "60x60x60 cm.",
            "Sistem": "Tanam di atas gundukan/bedengan jika lahan datar (sistem surjan)."
        },
        "pupuk": {
            "Berimbang": "Jeruk sangat responsif terhadap pupuk kandang dan mikro (Zn, Fe, Mn).",
            "Defisiensi": "Perhatikan gejala kuning daun (kurang N/Mg/Fe) yang sering muncul."
        },
        "hama": [
            {"nama": "CVPD (Huanglongbing)", "gejala": "Daun belang kuning, tulang daun hijau, buah kecil asimetris", "solusi": "TIDAK ADA OBAT. Cegah kutu loncat (Diaphorina citri) sebagai vektor. Gunakan bibit bebas penyakit."},
            {"nama": "Lalat Buah", "gejala": "Buah busuk gugur", "solusi": "Perangkap, Petik bubur sanitasi, Insektisida sistemik terbatas"}
        ],
        "panen": "Buah mulai menguning >30-50%, rasio gula:asam optimal. Panen dengan gunting, jangan ditarik."
    }
}

# ==========================================
# 🏗️ UI LAYOUT
# ==========================================

# Sidebar
st.sidebar.header("Pilih Komoditas")
selected_fruit = st.sidebar.selectbox("Jenis Tanaman Buah", list(fruit_data.keys()))

# DATA LOAD
data = fruit_data[selected_fruit]

# MAIN HEADER
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{data['icon']}</h1>", unsafe_allow_html=True)
with col_header2:
    st.title(f"{selected_fruit}")
    st.markdown(data['desc'])
    
st.divider()

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌱 Syarat Tumbuh", "🚜 Teknis Penanaman", "🧪 Pemupukan & Perawatan", "🛡️ Hama & Penyakit", "💰 Analisis Singkat"])

# TAB 1: SYARAT TUMBUH
with tab1:
    st.subheader("Kondisi Lingkungan Optimal")
    col_env1, col_env2 = st.columns(2)
    
    with col_env1:
        st.info(f"**🌡️ Iklim & Curah Hujan**\n\n{data['syarat']['Iklim']}")
        st.warning(f"**⛰️ Ketinggian Tempat (mdpl)**\n\n{data['syarat']['Ketinggian']}")
        
    with col_env2:
        st.success(f"**🏞️ Kondisi Tanah**\n\n{data['syarat']['Tanah']}")
        if "Fase Kering" in data['syarat']:
            st.error(f"**☀️ Catatan Khusus**\n\n{data['syarat']['Fase Kering']}")

# TAB 2: TEKNIS TANAM
with tab2:
    st.subheader("Standar Operasional Penanaman")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 📏 Jarak Tanam")
        st.write(data['tanam']['Jarak Tanam'])
    with c2:
        st.markdown("### 🕳️ Lubang Tanam")
        st.write(data['tanam']['Lubang Tanam'])
    with c3:
        st.markdown("### 🌱 Bibit & Waktu")
        st.write(data['tanam'].get('Bibit', data['tanam'].get('Waktu', '-')))
        
    st.caption("💡 *Tips: Sebaiknya lubang tanam disiapkan 2-4 minggu sebelum penanaman agar gas racun tanah hilang dan pupuk kandang matang.*")

# TAB 3: PEMUPUKAN
with tab3:
    st.subheader("Manajemen Nutrisi")
    st.markdown("Pupuk adalah kunci produksi buah. Berikan berimbang Organik dan Kimia.")
    
    col_p1, col_p2 = st.columns([2, 1])
    
    with col_p1:
        st.markdown("#### 📅 Jadwal & Dosis Referensi")
        for fase, desc in data['pupuk'].items():
            st.success(f"**{fase}**: {desc}")
            
    with col_p2:
        st.markdown("#### 🧮 Kalkulator Pupuk NPK")
        st.caption("Hitung estimasi kebutuhan per tahun")
        umur = st.number_input("Umur Tanaman (Tahun)", 1, 30, 5)
        jml_pohon = st.number_input("Jumlah Pohon", 1, 1000, 10)
        
        # Simple Logic Estimation
        if umur <= 3:
            perpohon = 0.5 * umur # approx kg/th
        else:
            perpohon = 2.0 + ((umur-3)*0.5) # naik 0.5kg tiap tahun produktif
            if perpohon > 6: perpohon = 6 # max cap
            
        total_kebutuhan = perpohon * jml_pohon
        
        st.metric("Estimasi NPK/Pohon/Th", f"{perpohon:.1f} kg")
        st.metric("Total Pupuk 1 Kebun", f"{total_kebutuhan:.1f} kg")
        st.caption("*Ini adalah estimasi kasar. Sesuaikan dengan kondisi tanah.*")

# TAB 4: HAMA PENYAKIT
with tab4:
    st.subheader("Musuh Alami & Pengendaliannya")
    
    for h in data['hama']:
        with st.expander(f"🔴 {h['nama']}"):
            c_h1, c_h2 = st.columns([1, 2])
            with c_h1:
                st.markdown("**Gejala Serangan:**")
                st.write(h['gejala'])
            with c_h2:
                st.markdown("**Pengendalian Efektif:**")
                st.write(h['solusi'])

# TAB 5: ANALISIS DAN PANEN
with tab5:
    col_end1, col_end2 = st.columns(2)
    with col_end1:
        st.subheader("🧺 Kriteria Panen")
        st.info(data['panen'])
        
    with col_end2:
        st.subheader("📈 Potensi Ekonomi")
        st.write("Simulasi sederhana hasil panen per musim.")
        
        harga = st.number_input("Harga Jual per Kg (Rp)", 5000, 200000, 25000, step=1000)
        hasil_pohon = st.slider("Estimasi Hasil per Pohon (kg)", 10, 200, 50)
        total_populasi = st.number_input("Populasi Tanaman", 1, 10000, 100)
        
        omzet = harga * hasil_pohon * total_populasi
        st.metric("Potensi Omzet/Musim", f"Rp {omzet:,.0f}")
