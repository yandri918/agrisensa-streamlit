import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Fisiologi Tumbuhan - AgriSensa",
    page_icon="🌱",
    layout="wide"
)

# Header
st.title("🌱 Fisiologi Tumbuhan & Hormon Pertumbuhan")
st.markdown("**Memahami Proses Fisiologis Tanaman untuk Optimasi Produksi**")

# Main tabs
tab_hormone, tab_growth, tab_photosynthesis, tab_stress, tab_practice = st.tabs([
    "🧪 Hormon Tumbuhan",
    "📈 Pertumbuhan & Perkembangan", 
    "☀️ Fotosintesis & Respirasi",
    "⚠️ Stress & Adaptasi",
    "🛠️ Aplikasi Praktis"
])

# ===== TAB 1: HORMON TUMBUHAN =====
with tab_hormone:
    st.header("🧪 Hormon Tumbuhan (Plant Hormones)")
    
    # Sub-tabs for different hormones
    subtab_overview, subtab_auxin, subtab_gibberellin, subtab_cytokinin, subtab_ethylene, subtab_aba, subtab_natural = st.tabs([
        "📚 Overview",
        "🌿 Auksin (Auxin)",
        "🌾 Giberelin (Gibberellin)",
        "🌱 Sitokinin (Cytokinin)",
        "🍎 Etilen (Ethylene)",
        "💧 ABA",
        "🍇 Sumber Alami"
    ])
    
    # Overview
    with subtab_overview:
        st.subheader("Pengantar Hormon Tumbuhan")
        
        st.markdown("""
        ## 🧪 APA ITU HORMON TUMBUHAN?
        
        **Hormon tumbuhan (fitohormon)** adalah senyawa organik yang diproduksi tanaman dalam jumlah kecil 
        dan berfungsi sebagai **sinyal kimia** untuk mengatur pertumbuhan, perkembangan, dan respons terhadap lingkungan.
        
        ### Karakteristik Hormon Tumbuhan:
        
        - ✅ Diproduksi dalam **jumlah sangat kecil** (ppm atau ppb)
        - ✅ Bekerja pada **lokasi berbeda** dari tempat produksi (transportasi)
        - ✅ Mengatur **proses fisiologis** spesifik
        - ✅ Bekerja secara **sinergis atau antagonis** dengan hormon lain
        - ✅ Responsif terhadap **kondisi lingkungan**
        
        ---
        
        ## 🌟 5 HORMON UTAMA TUMBUHAN
        
        ### 1. **Auksin (Auxin)** 🌿
        - **Fungsi Utama:** Pemanjangan sel, dominansi apikal, pembentukan akar
        - **Contoh:** IAA (Indole-3-Acetic Acid)
        - **Aplikasi:** Rooting hormone, parthenocarpy
        
        ### 2. **Giberelin (Gibberellin)** 🌾
        - **Fungsi Utama:** Pemanjangan batang, perkecambahan, pembungaan
        - **Contoh:** GA3, GA7
        - **Aplikasi:** Pembesaran buah (anggur), breaking dormancy
        
        ### 3. **Sitokinin (Cytokinin)** 🌱
        - **Fungsi Utama:** Pembelahan sel, penundaan senescence
        - **Contoh:** Zeatin, Kinetin
        - **Aplikasi:** Kultur jaringan, memperpanjang kesegaran
        
        ### 4. **Etilen (Ethylene)** 🍎
        - **Fungsi Utama:** Pematangan buah, abscission, senescence
        - **Contoh:** C₂H₄ (gas)
        - **Aplikasi:** Ripening control, degreening
        
        ### 5. **Asam Absisat (ABA)** 💧
        - **Fungsi Utama:** Dormansi, penutupan stomata, stress response
        - **Contoh:** ABA
        - **Aplikasi:** Drought tolerance, storage
        
        ---
        
        ## 📊 PERBANDINGAN HORMON
        
        | Hormon | Produksi | Transportasi | Fungsi Utama | Aplikasi Praktis |
        |--------|----------|--------------|--------------|------------------|
        | **Auksin** | Meristem apikal | Basipetal (atas→bawah) | Pemanjangan sel | Stek, parthenocarpy |
        | **Giberelin** | Biji, daun muda | Xylem & phloem | Pemanjangan batang | Anggur seedless |
        | **Sitokinin** | Akar | Xylem (bawah→atas) | Pembelahan sel | Kultur jaringan |
        | **Etilen** | Buah matang | Difusi (gas) | Pematangan | Ripening pisang |
        | **ABA** | Daun, akar | Xylem & phloem | Stress response | Drought tolerance |
        
        ---
        
        ## 🔄 INTERAKSI HORMON
        
        Hormon tumbuhan **TIDAK bekerja sendiri** - mereka berinteraksi!
        
        **Contoh Interaksi:**
        
        **1. Auksin + Sitokinin = Organogenesis**
        ```
        Ratio Tinggi Auksin : Rendah Sitokinin → Pembentukan AKAR
        Ratio Rendah Auksin : Tinggi Sitokinin → Pembentukan TUNAS
        Ratio Seimbang → Pembentukan KALUS
        ```
        
        **2. Giberelin + ABA = Perkecambahan**
        ```
        Giberelin ↑ + ABA ↓ → PERKECAMBAHAN
        Giberelin ↓ + ABA ↑ → DORMANSI
        ```
        
        **3. Auksin + Etilen = Abscission**
        ```
        Auksin ↑ + Etilen ↓ → Buah/Daun TETAP
        Auksin ↓ + Etilen ↑ → Buah/Daun GUGUR
        ```
        
        ---
        
        ## 💡 APLIKASI PRAKTIS
        
        **Untuk Petani:**
        
        1. **Meningkatkan Hasil Panen**
           - Gibberellin untuk pembesaran buah
           - Auksin untuk fruit set
        
        2. **Mempercepat Perkecambahan**
           - Gibberellin untuk breaking dormancy
        
        3. **Kontrol Pematangan**
           - Etilen untuk ripening
           - 1-MCP untuk menunda pematangan
        
        4. **Perbanyakan Tanaman**
           - Auksin untuk rooting
           - Sitokinin untuk kultur jaringan
        
        5. **Manajemen Stress**
           - ABA untuk drought tolerance
        
        """)
    
    # Auxin
    with subtab_auxin:
        st.subheader("🌿 Auksin (Auxin)")
        
        st.markdown("""
        ## 🌿 AUKSIN (AUXIN)
        
        ### Apa itu Auksin?
        
        **Auksin** adalah hormon tumbuhan pertama yang ditemukan (1928) dan paling banyak dipelajari.
        Nama "auxin" berasal dari bahasa Yunani **"auxein"** = tumbuh.
        
        **Jenis Auksin:**
        - **IAA (Indole-3-Acetic Acid)** - Auksin alami utama
        - **IBA (Indole-3-Butyric Acid)** - Sintetik, lebih stabil
        - **NAA (Naphthalene Acetic Acid)** - Sintetik
        - **2,4-D** - Sintetik, herbisida selektif
        
        ---
        
        ## 📍 TEMPAT PRODUKSI
        
        **Diproduksi di:**
        - ✅ Meristem apikal (ujung tunas)
        - ✅ Daun muda
        - ✅ Biji yang berkembang
        - ✅ Buah muda
        
        **Transportasi:**
        - **Basipetal** (dari atas ke bawah)
        - **Polar transport** (satu arah)
        - Melalui **parenchyma cells**
        
        ---
        
        ## 🎯 FUNGSI AUKSIN
        
        ### 1. **Pemanjangan Sel (Cell Elongation)**
        
        **Mekanisme:**
        ```
        Auksin → Aktivasi H⁺-ATPase → Pengasaman dinding sel
        → Pelonggaran dinding sel → Pemanjangan sel
        ```
        
        **Aplikasi:**
        - Pemanjangan batang
        - Pertumbuhan akar
        
        ### 2. **Dominansi Apikal (Apical Dominance)**
        
        **Prinsip:**
        - Tunas apikal (pucuk) **menghambat** pertumbuhan tunas lateral (cabang)
        - Auksin dari apex → Menghambat tunas samping
        
        **Praktis:**
        ```
        Potong pucuk (topping) → Auksin ↓ → Tunas samping tumbuh
        → Tanaman lebih lebat/bercabang
        ```
        
        ### 3. **Pembentukan Akar (Root Initiation)**
        
        **Aplikasi Penting:**
        - **Rooting hormone** untuk stek
        - Konsentrasi: 1000-5000 ppm IBA
        
        **Cara Pakai:**
        ```
        1. Celupkan ujung stek ke rooting hormone
        2. Tanam di media
        3. Akar muncul 7-14 hari
        ```
        
        ### 4. **Parthenocarpy (Buah Tanpa Biji)**
        
        **Prinsip:**
        - Auksin → Stimulasi pembentukan buah tanpa fertilisasi
        
        **Contoh:**
        - Tomat seedless
        - Timun parthenocarpic
        
        ### 5. **Phototropism & Gravitropism**
        
        **Phototropism (Respon terhadap cahaya):**
        ```
        Cahaya dari samping → Auksin terakumulasi di sisi gelap
        → Sisi gelap tumbuh lebih cepat → Batang membengkok ke cahaya
        ```
        
        **Gravitropism (Respon terhadap gravitasi):**
        ```
        Akar: Auksin ke bawah → Menghambat pertumbuhan → Akar tumbuh ke bawah
        Batang: Auksin ke bawah → Menstimulasi pertumbuhan → Batang tumbuh ke atas
        ```
        
        ---
        
        ## 💊 KONSENTRASI & EFEK
        
        **Auksin bersifat DOSE-DEPENDENT:**
        
        | Konsentrasi | Efek pada Batang | Efek pada Akar |
        |-------------|------------------|----------------|
        | **Sangat Rendah** (< 10⁻⁸ M) | Tidak ada efek | Tidak ada efek |
        | **Rendah** (10⁻⁸ - 10⁻⁶ M) | Stimulasi | Stimulasi |
        | **Optimal** (10⁻⁶ - 10⁻⁵ M) | Maksimal | Maksimal |
        | **Tinggi** (10⁻⁵ - 10⁻⁴ M) | Inhibisi | Inhibisi |
        | **Sangat Tinggi** (> 10⁻⁴ M) | Kematian sel | Kematian sel |
        
        **PENTING:**
        - Akar **lebih sensitif** dari batang (10-100x)
        - Konsentrasi optimal untuk batang = Toksik untuk akar!
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Rooting Hormone (Hormon Perakaran)**
        
        **Produk Komersial:**
        - Rootone (IBA 0.1%)
        - Hormodin (IBA 0.1-0.8%)
        
        **Cara Aplikasi:**
        ```
        Stek batang:
        1. Potong batang 10-15 cm
        2. Celupkan ujung 2-3 cm ke rooting powder
        3. Tanam di media (pasir/cocopeat)
        4. Jaga kelembaban
        5. Akar muncul 1-3 minggu
        ```
        
        ### 2. **Fruit Set (Pembentukan Buah)**
        
        **Aplikasi:**
        - Semprot bunga dengan NAA 10-20 ppm
        - Meningkatkan fruit set 20-40%
        
        **Tanaman:**
        - Tomat, cabai, terong
        - Strawberry
        
        ### 3. **Thinning (Penjarangan Buah)**
        
        **Aplikasi:**
        - NAA 10-15 ppm saat buah kecil
        - Buah berlebih gugur → Buah tersisa lebih besar
        
        **Tanaman:**
        - Apel, pir
        - Anggur
        
        ### 4. **Herbisida Selektif**
        
        **2,4-D (Synthetic Auxin):**
        - Membunuh dikotil (broad-leaf weeds)
        - Aman untuk monokotil (padi, jagung)
        
        ---
        
        ## ⚠️ PERINGATAN
        
        1. **Konsentrasi Tepat:**
           - Terlalu rendah → Tidak efektif
           - Terlalu tinggi → Toksik
        
        2. **Waktu Aplikasi:**
           - Pagi/sore (suhu rendah)
           - Hindari siang (degradasi cepat)
        
        3. **Kombinasi:**
           - Auksin + Sitokinin untuk kultur jaringan
           - Auksin + Giberelin untuk fruit set
        
        4. **Storage:**
           - Simpan di tempat gelap, sejuk
           - Hindari panas & cahaya langsung
        
        """)
    
    # Gibberellin
    with subtab_gibberellin:
        st.subheader("🌾 Giberelin (Gibberellin)")
        
        st.markdown("""
        ## 🌾 GIBERELIN (GIBBERELLIN)
        
        ### Apa itu Giberelin?
        
        **Giberelin** adalah kelompok hormon tumbuhan yang ditemukan dari jamur *Gibberella fujikuroi* (1926) 
        yang menyebabkan penyakit "bakanae" pada padi (tanaman tumbuh sangat tinggi lalu roboh).
        
        **Jenis Giberelin:**
        - Lebih dari **130 jenis** giberelin (GA1, GA2, ... GA130+)
        - Yang paling aktif: **GA3 (Gibberellic Acid)**
        - **GA7** juga sangat efektif
        
        ---
        
        ## 📍 TEMPAT PRODUKSI
        
        **Diproduksi di:**
        - ✅ Biji yang berkembang
        - ✅ Daun muda
        - ✅ Ujung akar
        - ✅ Buah muda
        
        **Transportasi:**
        - Melalui **xylem** dan **phloem** (dua arah)
        - **Non-polar** (berbeda dengan auksin)
        
        ---
        
        ## 🎯 FUNGSI GIBERELIN
        
        ### 1. **Pemanjangan Batang (Stem Elongation)**
        
        **Mekanisme:**
        ```
        GA → Aktivasi enzim → Pemanjangan sel + Pembelahan sel
        → Batang memanjang
        ```
        
        **Contoh:**
        - Tanaman dwarf (kerdil) + GA → Tumbuh normal
        - Tanaman rosette + GA → Bolting (pemanjangan batang)
        
        **Aplikasi:**
        ```
        Tanaman hias pendek → Semprot GA3 50-100 ppm
        → Batang memanjang → Lebih menarik
        ```
        
        ### 2. **Perkecambahan Biji (Seed Germination)**
        
        **Mekanisme:**
        ```
        Imbibisi air → Produksi GA → Aktivasi α-amylase
        → Hidrolisis pati → Glukosa → Energi untuk perkecambahan
        ```
        
        **Aplikasi:**
        ```
        Biji dorman → Rendam GA3 100-500 ppm (24 jam)
        → Breaking dormancy → Perkecambahan seragam
        ```
        
        **Tanaman:**
        - Lettuce, celery (light-requiring seeds)
        - Barley, wheat (cereal grains)
        
        ### 3. **Pembungaan (Flowering)**
        
        **Prinsip:**
        - GA → Substitute untuk cold requirement (vernalisasi)
        - GA → Substitute untuk long-day requirement
        
        **Aplikasi:**
        ```
        Tanaman long-day di short-day → Semprot GA3
        → Pembungaan tanpa perlu long-day
        ```
        
        **Contoh:**
        - Strawberry, lettuce
        
        ### 4. **Pembesaran Buah (Fruit Enlargement)**
        
        **Aplikasi PALING TERKENAL:**
        
        **ANGGUR SEEDLESS:**
        ```
        Anggur Thompson Seedless:
        1. Semprot GA3 20-50 ppm saat bunga mekar
        2. Semprot lagi GA3 50-100 ppm saat buah kecil
        
        Hasil:
        - Buah 2-3x lebih besar
        - Tandan lebih panjang
        - Nilai jual 3-5x lebih tinggi!
        ```
        
        **Tanaman Lain:**
        - Apel, pir (pembesaran)
        - Tomat (parthenocarpy)
        - Mandarin (seedless)
        
        ### 5. **Parthenocarpy (Buah Tanpa Biji)**
        
        **Mekanisme:**
        - GA → Stimulasi pertumbuhan ovary tanpa fertilisasi
        
        **Contoh:**
        - Anggur seedless
        - Tomat parthenocarpic
        - Mandarin seedless
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### Dosis GA3 untuk Berbagai Tanaman:
        
        | Tanaman | Tujuan | Konsentrasi | Waktu Aplikasi |
        |---------|--------|-------------|----------------|
        | **Anggur** | Pembesaran buah | 20-100 ppm | Bunga + Buah kecil |
        | **Padi** | Pemanjangan batang | 50-100 ppm | Fase vegetatif |
        | **Lettuce** | Perkecambahan | 100-500 ppm | Rendam biji 24 jam |
        | **Strawberry** | Pembungaan | 10-50 ppm | Sebelum bunga |
        | **Tomat** | Fruit set | 10-20 ppm | Saat bunga |
        | **Apel** | Pembesaran | 10-30 ppm | Buah kecil |
        | **Mandarin** | Seedless | 10-20 ppm | Bunga |
        
        ---
        
        ## 🍇 SUMBER ALAMI GIBERELIN
        
        ### **ANGGUR HIJAU (Green Grapes)**
        
        **Kenapa Anggur Hijau?**
        - Anggur muda mengandung **GA3 dan GA7** tinggi
        - Konsentrasi tertinggi saat buah **2-4 minggu setelah fruit set**
        - Lebih murah dari GA sintetik!
        
        **Cara Membuat Ekstrak GA Alami:**
        
        ```
        BAHAN:
        - 1 kg anggur hijau muda (2-4 minggu setelah fruit set)
        - 2 liter air
        - Blender
        - Kain saring
        
        CARA:
        1. Cuci bersih anggur hijau
        2. Blender dengan 1 liter air (5-10 menit)
        3. Saring dengan kain halus
        4. Tambahkan air hingga 2 liter
        5. Aduk rata
        
        PENGGUNAAN:
        - Semprot langsung (konsentrasi ~50-100 ppm GA equivalent)
        - Atau encerkan 1:1 dengan air (25-50 ppm)
        - Aplikasi pagi/sore hari
        - Ulangi setiap 7-10 hari
        
        PENYIMPANAN:
        - Simpan di kulkas (tahan 3-5 hari)
        - Atau keringkan menjadi powder (tahan lebih lama)
        ```
        
        **Efektivitas:**
        - **70-80%** efektif dibanding GA3 sintetik
        - **Lebih aman** (organik)
        - **Lebih murah** (bisa buat sendiri)
        
        ### **SUMBER ALAMI LAIN:**
        
        **1. Kecambah (Sprouts)**
        - Kecambah kacang hijau, kedelai
        - Tinggi GA saat perkecambahan
        
        **Cara:**
        ```
        1. Rendam kacang 8-12 jam
        2. Kecambahkan 3-5 hari
        3. Blender kecambah dengan air (1:2)
        4. Saring dan aplikasikan
        ```
        
        **2. Rumput Laut (Seaweed)**
        - Mengandung GA alami + sitokinin
        - Produk komersial: Seaweed extract
        
        **3. Kompos Jamur**
        - Jamur produksi GA
        - Kompos jamur → GA residual
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### **Kasus 1: Anggur Seedless**
        
        **Problem:** Anggur seedless ukuran kecil, nilai jual rendah
        
        **Solusi:**
        ```
        Aplikasi GA3:
        1. Saat bunga mekar (bloom): 20-30 ppm
        2. Saat buah kecil (berry set): 50-100 ppm
        3. 2 minggu kemudian: 50-100 ppm (optional)
        
        Atau Ekstrak Anggur Hijau:
        1. Saat bunga mekar: Ekstrak 100% (undiluted)
        2. Saat buah kecil: Ekstrak 100%
        3. Ulangi 7-10 hari kemudian
        
        Hasil:
        - Buah 2-3x lebih besar
        - Tandan lebih panjang
        - Nilai jual naik 200-300%!
        ```
        
        ### **Kasus 2: Breaking Dormancy Biji**
        
        **Problem:** Biji lettuce tidak berkecambah di suhu tinggi
        
        **Solusi:**
        ```
        1. Rendam biji di GA3 100-200 ppm (24 jam)
        2. Atau rendam di ekstrak kecambah (24 jam)
        3. Keringkan sedikit
        4. Tanam normal
        
        Hasil:
        - Perkecambahan 80-90% (vs 20-30% tanpa GA)
        - Lebih seragam
        ```
        
        ### **Kasus 3: Pembesaran Buah Tomat**
        
        **Problem:** Fruit set rendah, buah kecil
        
        **Solusi:**
        ```
        1. Semprot GA3 10-20 ppm saat bunga mekar
        2. Atau semprot ekstrak anggur hijau (encerkan 1:1)
        3. Ulangi setiap minggu selama pembungaan
        
        Hasil:
        - Fruit set naik 30-50%
        - Buah lebih besar
        - Panen lebih awal 5-7 hari
        ```
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### **1. Dosis Berlebihan:**
        ```
        Gejala:
        - Batang terlalu panjang (lodging)
        - Daun pucat (chlorosis)
        - Buah pecah (cracking)
        
        Solusi:
        - Kurangi dosis 50%
        - Perpanjang interval aplikasi
        ```
        
        ### **2. Waktu Aplikasi:**
        ```
        BENAR:
        - Pagi (6-9 AM) atau Sore (4-6 PM)
        - Suhu sejuk, tidak hujan
        
        SALAH:
        - Siang hari (degradasi cepat)
        - Saat hujan (tercuci)
        ```
        
        ### **3. Kombinasi:**
        ```
        BAIK:
        - GA + Auksin (fruit set)
        - GA + Sitokinin (kultur jaringan)
        
        HINDARI:
        - GA + ABA (antagonis!)
        - GA + Retardant (berlawanan)
        ```
        
        ### **4. Tanaman Sensitif:**
        ```
        HATI-HATI:
        - Padi (bisa lodging)
        - Wheat (batang lemah)
        
        AMAN:
        - Anggur, tomat, lettuce
        - Strawberry, apel
        ```
        
        ---
        
        ## 💡 TIPS SUKSES
        
        **1. Mulai Rendah:**
        - Coba dosis terendah dulu
        - Naikkan bertahap jika perlu
        
        **2. Konsistensi:**
        - Aplikasi teratur (7-10 hari)
        - Jangan skip
        
        **3. Monitoring:**
        - Catat respons tanaman
        - Adjust dosis sesuai hasil
        
        **4. Ekonomis:**
        - Buat ekstrak sendiri (anggur hijau, kecambah)
        - Lebih murah, tetap efektif
        
        **5. Dokumentasi:**
        - Foto before-after
        - Ukur pertumbuhan
        - Hitung ROI
        
        """)
    
    # Cytokinin
    with subtab_cytokinin:
        st.subheader("🌱 Sitokinin (Cytokinin)")
        
        st.markdown("""
        ## 🌱 SITOKININ (CYTOKININ)
        
        ### Apa itu Sitokinin?
        
        **Sitokinin** adalah hormon tumbuhan yang merangsang **pembelahan sel (cytokinesis)** dan **penundaan penuaan (anti-senescence)**.
        Nama "cytokinin" berasal dari "cytokinesis" = pembelahan sel.
        
        **Jenis Sitokinin:**
        - **Zeatin** - Sitokinin alami utama (dari jagung)
        - **Kinetin** - Sintetik pertama (dari DNA)
        - **BAP (6-Benzylaminopurine)** - Sintetik, paling umum
        - **TDZ (Thidiazuron)** - Sintetik, sangat kuat
        
        **Sumber:**
        - Taub, D. R., & Goldberg, R. (1996). Plant Physiology, 110(4), 1103-1109
        - Mok, D. W., & Mok, M. C. (2001). Annual Review of Plant Biology, 52, 89-118
        
        ---
        
        ## 📍 TEMPAT PRODUKSI
        
        **Diproduksi di:**
        - ✅ **Akar** (terutama ujung akar)
        - ✅ Biji yang berkembang
        - ✅ Buah muda
        - ✅ Jaringan meristematik
        
        **Transportasi:**
        - Melalui **xylem** (dari akar ke atas)
        - **Acropetal** (dari bawah ke atas)
        - Berlawanan dengan auksin!
        
        **Referensi:**
        - Sakakibara, H. (2006). Annual Review of Plant Biology, 57, 431-449
        
        ---
        
        ## 🎯 FUNGSI SITOKININ
        
        ### 1. **Pembelahan Sel (Cell Division)**
        
        **Mekanisme:**
        ```
        Sitokinin → Aktivasi cyclin-dependent kinases (CDKs)
        → Progresi siklus sel → Pembelahan sel
        ```
        
        **Aplikasi:**
        - Kultur jaringan (kalus formation)
        - Organogenesis (tunas formation)
        - Meristem activation
        
        **Referensi:**
        - Riou-Khamlichi, C., et al. (1999). Science, 283(5407), 1541-1544
        
        ### 2. **Penundaan Senescence (Anti-Aging)**
        
        **Prinsip:**
        - Sitokinin **menunda** penuaan daun
        - Mempertahankan klorofil
        - Mencegah degradasi protein
        
        **Mekanisme:**
        ```
        Sitokinin → Inhibisi degradasi klorofil
        → Daun tetap hijau lebih lama
        → Fotosintesis lebih lama
        ```
        
        **Aplikasi Praktis:**
        ```
        Sayuran potong (lettuce, spinach):
        - Semprot sitokinin 10-50 ppm sebelum panen
        - Kesegaran bertahan 2-3x lebih lama
        - Nilai jual lebih tinggi
        ```
        
        **Referensi:**
        - Gan, S., & Amasino, R. M. (1995). Science, 270(5244), 1986-1988
        
        ### 3. **Pelepasan Dormansi Tunas Lateral**
        
        **Prinsip:**
        - Sitokinin **melawan** dominansi apikal (auksin)
        - Merangsang pertumbuhan tunas samping
        
        **Ratio Auksin:Sitokinin:**
        ```
        Auksin tinggi : Sitokinin rendah → Dominansi apikal
        Auksin rendah : Sitokinin tinggi → Tunas lateral tumbuh
        ```
        
        **Aplikasi:**
        ```
        Tanaman hias (krisan, mawar):
        - Semprot BAP 50-100 ppm
        - Tunas samping tumbuh
        - Tanaman lebih lebat/bushy
        ```
        
        ### 4. **Mobilisasi Nutrisi (Nutrient Sink)**
        
        **Prinsip:**
        - Sitokinin → Jaringan menjadi "sink" (penarik nutrisi)
        - Nutrisi dialihkan ke area dengan sitokinin tinggi
        
        **Contoh:**
        ```
        Buah/biji → Sitokinin tinggi → Nutrisi tertarik ke buah
        Daun tua → Sitokinin rendah → Nutrisi keluar (senescence)
        ```
        
        **Referensi:**
        - Roitsch, T., & Ehneß, R. (2000). Plant Biology, 2(02), 129-138
        
        ### 5. **Pembentukan Kloroplas**
        
        **Mekanisme:**
        - Sitokinin → Diferensiasi kloroplas
        - Meningkatkan kandungan klorofil
        - Daun lebih hijau
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### Dosis Sitokinin untuk Berbagai Aplikasi:
        
        | Aplikasi | Konsentrasi | Metode | Hasil |
        |----------|-------------|--------|-------|
        | **Kultur Jaringan** | 0.5-5 mg/L BAP | Media | Tunas formation |
        | **Anti-Senescence** | 10-50 ppm | Foliar spray | Kesegaran 2-3x |
        | **Tunas Lateral** | 50-100 ppm BAP | Foliar spray | Branching |
        | **Pembesaran Buah** | 5-20 ppm | Spray | Ukuran +20-30% |
        | **Kesegaran Bunga** | 10-30 ppm | Spray/dip | Vase life +50% |
        
        **Referensi:**
        - Skoog, F., & Miller, C. O. (1957). Symposia of the Society for Experimental Biology, 11, 118-130
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Kultur Jaringan (Tissue Culture)**
        
        **Formula MS Medium + Sitokinin:**
        ```
        Media Dasar: MS (Murashige & Skoog)
        Auksin (NAA): 0.1-1 mg/L
        Sitokinin (BAP): 0.5-5 mg/L
        
        Ratio:
        - Auksin > Sitokinin → Akar
        - Auksin < Sitokinin → Tunas
        - Auksin = Sitokinin → Kalus
        ```
        
        **Aplikasi:**
        - Perbanyakan tanaman (micropropagation)
        - Konservasi germplasm
        - Produksi tanaman bebas virus
        
        **Referensi:**
        - Murashige, T., & Skoog, F. (1962). Physiologia Plantarum, 15(3), 473-497
        
        ### 2. **Memperpanjang Kesegaran Sayuran**
        
        **Produk Komersial:**
        - ProFresh (BAP 10 ppm)
        - ReTain (AVG + Cytokinin)
        
        **DIY Formula:**
        ```
        BAHAN:
        - Air kelapa 100 mL (sitokinin alami)
        - Air 900 mL
        - Gula 1 sendok teh (spreader)
        
        APLIKASI:
        - Semprot sayuran 1-2 hari sebelum panen
        - Atau celup setelah panen (30 detik)
        - Kesegaran +2-3 hari
        ```
        
        ### 3. **Meningkatkan Branching (Percabangan)**
        
        **Tanaman Hias:**
        ```
        Krisan, Mawar, Poinsettia:
        - Semprot BAP 50-100 ppm
        - Aplikasi 2-3x (interval 7 hari)
        - Tunas lateral +50-100%
        - Tanaman lebih penuh/bushy
        ```
        
        ### 4. **Pembesaran Buah**
        
        **Aplikasi:**
        ```
        Anggur, Apel, Kiwi:
        - Semprot sitokinin 5-20 ppm saat fruit set
        - Kombinasi dengan GA untuk efek maksimal
        - Ukuran buah +20-30%
        - Cell division meningkat
        ```
        
        **Referensi:**
        - Zhang, C., & Whiting, M. D. (2011). HortScience, 46(6), 865-870
        
        ### 5. **Memperpanjang Vase Life Bunga Potong**
        
        **Formula:**
        ```
        Preservative Solution:
        - Sucrose: 2-4%
        - Citric acid: 200 ppm
        - BAP: 10-30 ppm
        - Silver thiosulfate: 0.2 mM (optional)
        
        Hasil:
        - Vase life +50-100%
        - Daun tetap hijau
        - Bunga segar lebih lama
        ```
        
        **Referensi:**
        - van Doorn, W. G., & Woltering, E. J. (2008). Postharvest Biology and Technology, 50(2-3), 89-99
        
        ---
        
        ## 🥥 SUMBER ALAMI SITOKININ
        
        ### **1. AIR KELAPA (Coconut Water)**
        
        **Kandungan:**
        - **Zeatin:** 10-50 ppm (TINGGI!)
        - **Zeatin riboside:** 5-20 ppm
        - Plus: Gula, mineral, vitamin
        
        **Aplikasi:**
        ```
        Kultur Jaringan:
        - 10-20% air kelapa dalam media MS
        - Meningkatkan shoot formation
        - Lebih ekonomis dari BAP sintetik
        
        Foliar Spray:
        - Encerkan 1:1 dengan air
        - Semprot setiap 7-10 hari
        - Anti-senescence, kesegaran daun
        ```
        
        **Referensi:**
        - Yong, J. W., et al. (2009). Molecules, 14(12), 5144-5164
        
        ### **2. EKSTRAK RUMPUT LAUT (Seaweed Extract)**
        
        **Kandungan:**
        - Sitokinin: 10-50 ppm
        - Betaine, mineral, growth factors
        
        **Produk Komersial:**
        - Maxicrop, Seasol, Kelpak
        
        **DIY:**
        ```
        1 kg rumput laut segar → Rendam 5L air (2-3 minggu)
        → Saring → Encerkan 1:10 untuk aplikasi
        ```
        
        ### **3. EKSTRAK KECAMBAH**
        
        **Kandungan:**
        - Sitokinin: 10-30 ppm
        - Plus GA, auksin
        
        **Cara:**
        ```
        Kecambah alfalfa/kacang hijau (3-5 hari)
        → Blender dengan air (1:2)
        → Saring → Aplikasikan
        ```
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### 1. **Dosis Berlebihan:**
        ```
        Gejala:
        - Daun kecil-kecil (abnormal)
        - Tunas terlalu banyak (kompetisi)
        - Pertumbuhan terhambat
        
        Solusi:
        - Kurangi dosis 50%
        - Perpanjang interval
        ```
        
        ### 2. **Interaksi dengan Auksin:**
        ```
        PENTING:
        - Ratio Auksin:Sitokinin sangat penting!
        - Terlalu banyak sitokinin → Tunas berlebihan
        - Terlalu sedikit → Tidak ada efek
        
        Optimal:
        - Kultur jaringan: 1:1 sampai 1:10 (Auksin:Sitokinin)
        - Foliar spray: Sitokinin saja (atau + GA)
        ```
        
        ### 3. **Waktu Aplikasi:**
        ```
        BENAR:
        - Pagi/sore (suhu sejuk)
        - Fase vegetatif aktif
        - Sebelum stress (panas, kekeringan)
        
        SALAH:
        - Siang hari (degradasi)
        - Saat tanaman stress
        - Terlalu sering (waste)
        ```
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        **1. Untuk Kultur Jaringan:**
        - Start dengan BAP 1 mg/L
        - Adjust berdasarkan respons
        - Combine dengan auksin untuk organogenesis
        
        **2. Untuk Anti-Senescence:**
        - Aplikasi 1-2 hari sebelum panen
        - Atau gunakan air kelapa (ekonomis)
        - Efektif untuk sayuran daun
        
        **3. Untuk Branching:**
        - Aplikasi saat tanaman muda
        - 2-3x aplikasi (interval 7 hari)
        - Combine dengan topping untuk efek maksimal
        
        **4. Ekonomis:**
        - Gunakan air kelapa (alami, murah)
        - Atau seaweed extract
        - Efektivitas 60-80% vs sintetik
        
        **5. Storage:**
        - Sitokinin stabil di suhu rendah
        - Simpan stock solution di freezer
        - Working solution di kulkas (1-2 minggu)
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Mok, D. W., & Mok, M. C. (2001).** Cytokinin metabolism and action. Annual Review of Plant Biology, 52, 89-118.
        
        2. **Sakakibara, H. (2006).** Cytokinins: activity, biosynthesis, and translocation. Annual Review of Plant Biology, 57, 431-449.
        
        3. **Gan, S., & Amasino, R. M. (1995).** Inhibition of leaf senescence by autoregulated production of cytokinin. Science, 270(5244), 1986-1988.
        
        4. **Murashige, T., & Skoog, F. (1962).** A revised medium for rapid growth and bio assays with tobacco tissue cultures. Physiologia Plantarum, 15(3), 473-497.
        
        5. **Yong, J. W., et al. (2009).** The chemical composition and biological properties of coconut (Cocos nucifera L.) water. Molecules, 14(12), 5144-5164.
        
        """)
    
    # Ethylene
    with subtab_ethylene:
        st.subheader("🍎 Etilen (Ethylene)")
        
        st.markdown("""
        ## 🍎 ETILEN (ETHYLENE)
        
        ### Apa itu Etilen?
        
        **Etilen (C₂H₄)** adalah hormon tumbuhan berbentuk **GAS** yang mengatur pematangan buah, penuaan, dan abscission.
        Etilen adalah molekul organik paling sederhana yang berfungsi sebagai hormon.
        
        **Karakteristik Unik:**
        - ✅ Satu-satunya hormon berbentuk **gas**
        - ✅ Dapat berdifusi melalui udara
        - ✅ Sangat potent (aktif pada konsentrasi ppb!)
        - ✅ Diproduksi oleh semua bagian tanaman
        
        **Sumber:**
        - Abeles, F. B., et al. (1992). Ethylene in Plant Biology. Academic Press.
        - Bleecker, A. B., & Kende, H. (2000). Annual Review of Cell and Developmental Biology, 16, 1-18
        
        ---
        
        ## 📍 PRODUKSI & BIOSINTESIS
        
        **Jalur Biosintesis:**
        ```
        Methionine → SAM (S-Adenosyl Methionine)
        → ACC (1-Aminocyclopropane-1-Carboxylic Acid)
        → Ethylene (C₂H₄)
        ```
        
        **Enzim Kunci:**
        - **ACS (ACC Synthase)** - Rate-limiting step
        - **ACO (ACC Oxidase)** - Konversi ACC → Ethylene
        
        **Diproduksi di:**
        - ✅ Buah matang (TINGGI!)
        - ✅ Bunga yang layu
        - ✅ Daun yang menua
        - ✅ Jaringan yang terluka
        - ✅ Akar (saat stress)
        
        **Referensi:**
        - Yang, S. F., & Hoffman, N. E. (1984). Annual Review of Plant Physiology, 35, 155-189
        
        ---
        
        ## 🎯 FUNGSI ETILEN
        
        ### 1. **Pematangan Buah (Fruit Ripening)**
        
        **Mekanisme:**
        ```
        Etilen → Aktivasi enzim:
        - Pectinase → Pelunakan dinding sel
        - Amylase → Konversi pati → gula
        - Chlorophyllase → Degradasi klorofil
        - Carotenoid synthesis → Warna (merah, kuning)
        
        Hasil: Buah matang (lunak, manis, berwarna)
        ```
        
        **Buah Klimakterik vs Non-Klimakterik:**
        
        | Klimakterik | Non-Klimakterik |
        |-------------|-----------------|
        | Produksi etilen ↑↑ saat matang | Produksi etilen rendah |
        | Bisa matang setelah panen | Harus matang di pohon |
        | Contoh: Pisang, tomat, apel, mangga | Contoh: Anggur, jeruk, strawberry |
        
        **Referensi:**
        - Giovannoni, J. J. (2004). Annual Review of Plant Biology, 55, 521-551
        
        ### 2. **Abscission (Gugur Daun/Buah)**
        
        **Mekanisme:**
        ```
        Etilen ↑ + Auksin ↓ → Aktivasi cellulase & polygalacturonase
        → Degradasi dinding sel di abscission zone
        → Daun/buah gugur
        ```
        
        **Aplikasi:**
        - Defoliation (gugurkan daun sebelum panen)
        - Fruit thinning (penjarangan buah)
        
        **Referensi:**
        - Patterson, S. E. (2001). Plant Molecular Biology, 46(1), 1-19
        
        ### 3. **Senescence (Penuaan)**
        
        **Prinsip:**
        - Etilen → Mempercepat penuaan
        - Degradasi klorofil, protein, membran
        - "The death hormone"
        
        **Contoh:**
        - Bunga potong → Etilen tinggi → Cepat layu
        - Sayuran → Etilen → Menguning
        
        ### 4. **Triple Response (Respon Gelap)**
        
        **Pada seedling di gelap + etilen:**
        ```
        1. Inhibisi pemanjangan batang
        2. Penebalan batang
        3. Pertumbuhan horizontal (epinasty)
        
        Fungsi: Membantu seedling menembus tanah
        ```
        
        ### 5. **Sex Expression (Ekspresi Kelamin)**
        
        **Pada tanaman monoecious (timun, melon):**
        ```
        Etilen ↑ → Bunga betina ↑
        Etilen ↓ → Bunga jantan ↑
        
        Aplikasi:
        - Ethephon → Meningkatkan bunga betina
        - Hasil panen lebih tinggi
        ```
        
        **Referensi:**
        - Yamasaki, S., et al. (2003). Plant and Cell Physiology, 44(12), 1350-1358
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### Etilen dalam Berbagai Aplikasi:
        
        | Aplikasi | Konsentrasi | Metode | Hasil |
        |----------|-------------|--------|-------|
        | **Ripening Pisang** | 100-150 ppm | Gas chamber | Matang 3-5 hari |
        | **Degreening Jeruk** | 1-5 ppm | Gas chamber | Warna kuning |
        | **Defoliation Kapas** | Ethephon 500-1000 ppm | Spray | Gugur daun |
        | **Bunga Betina (Timun)** | Ethephon 100-250 ppm | Spray | Bunga betina +50% |
        | **Inhibisi (1-MCP)** | 0.5-1 ppm | Gas chamber | Tunda matang 2-4x |
        
        **Referensi:**
        - Saltveit, M. E. (1999). Postharvest Biology and Technology, 15(3), 279-292
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Ripening Buah (Pematangan)**
        
        **Metode Tradisional:**
        ```
        PISANG MATANG CEPAT:
        1. Masukkan pisang hijau dalam kardus/plastik tertutup
        2. Tambahkan 1-2 buah apel/pisang matang (sumber etilen)
        3. Tutup rapat
        4. Suhu 20-25°C
        5. Matang dalam 2-3 hari
        
        Prinsip: Apel/pisang matang → Etilen → Pisang hijau matang
        ```
        
        **Metode Komersial:**
        ```
        RIPENING ROOM:
        1. Suhu: 18-20°C
        2. Humidity: 90-95%
        3. Etilen gas: 100-150 ppm
        4. Ventilasi: Sirkulasi udara
        5. Durasi: 24-48 jam
        
        Hasil: Matang seragam, kualitas baik
        ```
        
        **Ethephon (Ethrel) - Etilen Cair:**
        ```
        Aplikasi:
        - Ethephon 500-1000 ppm
        - Spray buah hijau
        - Ethephon → Release etilen
        - Matang 3-5 hari
        
        Tanaman: Tomat, pisang, mangga
        ```
        
        ### 2. **Menunda Pematangan (Anti-Ethylene)**
        
        **1-MCP (1-Methylcyclopropene):**
        ```
        Mekanisme:
        - 1-MCP → Blok reseptor etilen
        - Etilen tidak bisa bekerja
        - Pematangan tertunda
        
        Aplikasi:
        - Konsentrasi: 0.5-1 ppm (gas)
        - Durasi: 12-24 jam (sealed chamber)
        - Hasil: Shelf-life +2-4x
        
        Produk Komersial: SmartFresh, RipeLock
        ```
        
        **Referensi:**
        - Watkins, C. B. (2006). Biotechnology Advances, 24(4), 389-409
        
        **Absorber Etilen:**
        ```
        Potassium Permanganate (KMnO₄):
        - Absorb etilen dari udara
        - Sachet dalam packaging
        - Perpanjang kesegaran
        
        Aplikasi: Buah, sayur, bunga potong
        ```
        
        ### 3. **Degreening (Penghijauan → Kuning)**
        
        **Jeruk, Lemon:**
        ```
        Problem: Buah matang tapi masih hijau (suhu tinggi)
        
        Solusi:
        1. Etilen 1-5 ppm (gas chamber)
        2. Suhu: 20-25°C
        3. Humidity: 90-95%
        4. Durasi: 2-5 hari
        
        Hasil:
        - Klorofil degradasi
        - Warna kuning/orange muncul
        - Rasa tidak berubah (sudah matang)
        ```
        
        **Referensi:**
        - Goldschmidt, E. E. (1988). HortScience, 23(1), 42-44
        
        ### 4. **Defoliation (Gugurkan Daun)**
        
        **Kapas:**
        ```
        Tujuan: Gugurkan daun sebelum panen (mekanis)
        
        Aplikasi:
        - Ethephon 500-1000 ppm
        - Spray 7-14 hari sebelum panen
        - Daun gugur 90-100%
        - Panen lebih mudah, bersih
        ```
        
        ### 5. **Meningkatkan Bunga Betina**
        
        **Timun, Melon:**
        ```
        Aplikasi:
        - Ethephon 100-250 ppm
        - Spray saat 2-4 daun sejati
        - Bunga betina +50-100%
        - Hasil panen lebih tinggi
        ```
        
        **Referensi:**
        - Rudich, J., et al. (1972). Plant Physiology, 50(5), 585-590
        
        ---
        
        ## 🍎 SUMBER ETILEN ALAMI
        
        ### **Buah Klimakterik (Penghasil Etilen Tinggi):**
        
        | Buah | Produksi Etilen | Sensitivitas | Aplikasi |
        |------|-----------------|--------------|----------|
        | **Apel** | Tinggi (10-100 ppm) | Tinggi | Ripening agent |
        | **Pisang** | Sangat Tinggi (100-200 ppm) | Sangat Tinggi | Ripening agent |
        | **Tomat** | Tinggi (10-50 ppm) | Tinggi | Ripening |
        | **Alpukat** | Tinggi (50-100 ppm) | Tinggi | Ripening |
        | **Mangga** | Tinggi (20-80 ppm) | Tinggi | Ripening |
        
        **Cara Pakai:**
        ```
        Matangkan buah lain:
        1. Letakkan buah klimakterik matang (apel/pisang)
        2. Bersama buah yang ingin dimatangkan
        3. Dalam wadah tertutup
        4. Suhu ruang (20-25°C)
        5. Cek setiap hari
        ```
        
        ### **Hindari Kombinasi:**
        ```
        JANGAN SIMPAN BERSAMA:
        - Apel + Wortel → Wortel pahit
        - Pisang + Kentang → Kentang cepat berkecambah
        - Tomat + Lettuce → Lettuce cepat busuk
        
        Prinsip: Etilen dari buah klimakterik → Rusak sayuran
        ```
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### 1. **Etilen Berlebihan:**
        ```
        Gejala:
        - Buah terlalu cepat matang → Busuk
        - Daun menguning, gugur
        - Bunga layu prematur
        - Sayuran rusak
        
        Solusi:
        - Ventilasi baik (buang etilen)
        - Pisahkan buah klimakterik
        - Gunakan absorber etilen
        - Suhu rendah (slow down production)
        ```
        
        ### 2. **Storage & Transport:**
        ```
        PENTING:
        - Jangan campur buah klimakterik dengan non-klimakterik
        - Ventilasi baik (buang etilen)
        - Suhu rendah (reduce production)
        - Gunakan 1-MCP untuk long-distance transport
        ```
        
        ### 3. **Timing Aplikasi:**
        ```
        Ethephon:
        - Jangan terlalu dini (buah belum siap)
        - Jangan terlalu lambat (sudah matang)
        - Optimal: Physiological maturity (matang fisiologis)
        ```
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        **1. Ripening di Rumah:**
        - Gunakan apel/pisang matang sebagai sumber etilen
        - Kardus/plastik tertutup (konsentrasi etilen tinggi)
        - Suhu ruang, cek setiap hari
        
        **2. Perpanjang Kesegaran:**
        - Pisahkan buah klimakterik dari sayuran
        - Ventilasi baik di kulkas
        - Gunakan absorber etilen (DIY: arang aktif)
        
        **3. Bunga Potong:**
        - Hindari etilen (jauhkan dari buah)
        - Gunakan STS (Silver Thiosulfate) - blok etilen
        - Suhu rendah (slow down senescence)
        
        **4. Komersial:**
        - Invest in ripening room (kontrol presisi)
        - Gunakan 1-MCP untuk transport jarak jauh
        - Monitor etilen level (sensor)
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Abeles, F. B., et al. (1992).** Ethylene in Plant Biology. Academic Press.
        
        2. **Bleecker, A. B., & Kende, H. (2000).** Ethylene: a gaseous signal molecule in plants. Annual Review of Cell and Developmental Biology, 16, 1-18.
        
        3. **Giovannoni, J. J. (2004).** Genetic regulation of fruit development and ripening. The Plant Cell, 16, S170-S180.
        
        4. **Saltveit, M. E. (1999).** Effect of ethylene on quality of fresh fruits and vegetables. Postharvest Biology and Technology, 15(3), 279-292.
        
        5. **Watkins, C. B. (2006).** The use of 1-methylcyclopropene (1-MCP) on fruits and vegetables. Biotechnology Advances, 24(4), 389-409.
        
        """)
    
    # ABA
    with subtab_aba:
        st.subheader("💧 Asam Absisat (ABA)")
        
        st.markdown("""
        ## 💧 ASAM ABSISAT (ABA - Abscisic Acid)
        
        ### Apa itu ABA?
        
        **ABA (Abscisic Acid)** adalah hormon "stress" yang membantu tanaman bertahan dalam kondisi tidak menguntungkan.
        Awalnya dikira mengatur abscission (gugur), tapi ternyata fungsi utamanya adalah **stress response**.
        
        **Karakteristik:**
        - ✅ "Stress hormone" atau "Growth inhibitor"
        - ✅ Antagonis dari gibberellin & sitokinin
        - ✅ Krusial untuk survival tanaman
        - ✅ Meningkat drastis saat stress
        
        **Sumber:**
        - Finkelstein, R. (2013). Annual Review of Plant Biology, 64, 429-450
        - Cutler, S. R., et al. (2010). Annual Review of Plant Biology, 61, 651-679
        
        ---
        
        ## 📍 PRODUKSI & BIOSINTESIS
        
        **Jalur Biosintesis:**
        ```
        Carotenoids (Zeaxanthin) → Violaxanthin
        → Neoxanthin → Xanthoxin → ABA
        ```
        
        **Diproduksi di:**
        - ✅ **Daun** (saat kekeringan)
        - ✅ **Akar** (saat stress air)
        - ✅ **Biji** (dormansi)
        - ✅ **Buah** (pematangan)
        
        **Transportasi:**
        - Xylem & phloem (dua arah)
        - Signal dari akar → daun (water stress)
        
        **Referensi:**
        - Nambara, E., & Marion-Poll, A. (2005). Annual Review of Plant Biology, 56, 165-185
        
        ---
        
        ## 🎯 FUNGSI ABA
        
        ### 1. **Penutupan Stomata (Drought Response)**
        
        **Mekanisme:**
        ```
        Kekeringan → ABA ↑ di akar
        → ABA transport ke daun
        → Aktivasi ion channels di guard cells
        → K⁺ dan Cl⁻ keluar dari guard cells
        → Air keluar → Guard cells mengempis
        → Stomata MENUTUP
        → Transpirasi ↓ → Konservasi air
        ```
        
        **Kecepatan:**
        - Stomata menutup dalam **10-15 menit** setelah ABA
        - Sangat cepat dan efektif!
        
        **Referensi:**
        - Schroeder, J. I., et al. (2001). Annual Review of Plant Physiology and Plant Molecular Biology, 52, 627-658
        
        ### 2. **Dormansi Biji (Seed Dormancy)**
        
        **Prinsip:**
        ```
        ABA tinggi → Biji dorman (tidak berkecambah)
        ABA rendah → Biji berkecambah
        
        Balance:
        ABA (inhibitor) vs GA (promoter)
        ```
        
        **Fungsi:**
        - Mencegah perkecambahan prematur (di buah)
        - Survival saat kondisi tidak optimal
        - Perkecambahan saat kondisi baik
        
        **Aplikasi:**
        ```
        Breaking Dormancy:
        - Stratifikasi dingin → ABA ↓
        - Gibberellin → Antagonis ABA
        - Perkecambahan seragam
        ```
        
        **Referensi:**
        - Finkelstein, R., et al. (2008). The Plant Cell, 20(12), 2981-2992
        
        ### 3. **Inhibisi Pertumbuhan (Growth Inhibition)**
        
        **Mekanisme:**
        - ABA → Inhibisi pemanjangan sel
        - Antagonis gibberellin
        - "Pause" pertumbuhan saat stress
        
        **Contoh:**
        ```
        Kekeringan → ABA ↑
        → Pertumbuhan berhenti
        → Energi dialihkan untuk survival
        → Setelah hujan → ABA ↓ → Pertumbuhan lanjut
        ```
        
        ### 4. **Toleransi Stress Abiotik**
        
        **Jenis Stress:**
        - **Drought** (kekeringan)
        - **Salinity** (salinitas)
        - **Cold** (dingin)
        - **Heat** (panas)
        
        **Mekanisme:**
        ```
        Stress → ABA ↑
        → Ekspresi stress-responsive genes
        → Produksi:
          - Osmoprotectants (proline, betaine)
          - Antioxidants (SOD, CAT)
          - Heat shock proteins (HSPs)
          - LEA proteins
        → Toleransi meningkat
        ```
        
        **Referensi:**
        - Zhu, J. K. (2002). Annual Review of Plant Biology, 53, 247-273
        
        ### 5. **Senescence & Abscission**
        
        **Prinsip:**
        - ABA → Mempercepat penuaan daun
        - ABA → Promosi abscission (dengan etilen)
        
        **Contoh:**
        - Daun tua → ABA tinggi → Menguning, gugur
        - Stress → ABA tinggi → Premature senescence
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### ABA dalam Berbagai Aplikasi:
        
        | Aplikasi | Konsentrasi | Metode | Hasil |
        |----------|-------------|--------|-------|
        | **Drought Tolerance** | 10-100 μM | Foliar spray | Stomata closure |
        | **Seed Priming** | 1-10 μM | Seed soak | Stress tolerance |
        | **Storage** | 50-100 ppm | Spray | Dormansi, shelf-life |
        | **Transplant** | 10-50 μM | Root dip | Survival rate ↑ |
        | **Fruit Storage** | 100-500 ppm | Spray | Delay ripening |
        
        **Referensi:**
        - Travaglia, C., et al. (2007). Plant Growth Regulation, 53(1), 1-9
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Meningkatkan Drought Tolerance**
        
        **Priming Benih:**
        ```
        CARA:
        1. Rendam benih di ABA 1-10 μM (24 jam)
        2. Keringkan
        3. Tanam normal
        
        HASIL:
        - Toleransi kekeringan +30-50%
        - Survival rate lebih tinggi
        - Yield lebih stabil saat kekeringan
        ```
        
        **Foliar Application:**
        ```
        CARA:
        1. Semprot ABA 10-50 μM
        2. 1-2 hari sebelum stress (kekeringan, transplant)
        3. Atau saat stress ringan
        
        HASIL:
        - Stomata menutup → Transpirasi ↓
        - Water use efficiency ↑
        - Survival saat kekeringan
        ```
        
        **Referensi:**
        - Travaglia, C., et al. (2007). Plant Growth Regulation, 53(1), 1-9
        
        ### 2. **Meningkatkan Transplant Success**
        
        **Aplikasi:**
        ```
        SEEDLING TRANSPLANT:
        1. Rendam akar di ABA 10-50 μM (30 menit)
        2. Atau spray ABA 1 hari sebelum transplant
        3. Transplant
        
        HASIL:
        - Transplant shock ↓
        - Survival rate +20-40%
        - Recovery lebih cepat
        
        Mekanisme:
        - ABA → Stomata menutup
        - Transpirasi ↓ saat akar belum optimal
        - Survival lebih tinggi
        ```
        
        ### 3. **Perpanjang Storage Life**
        
        **Aplikasi:**
        ```
        BUAH & SAYURAN:
        1. Spray ABA 100-500 ppm sebelum panen
        2. Atau celup setelah panen
        
        HASIL:
        - Dormansi meningkat
        - Pematangan tertunda
        - Shelf-life +20-30%
        - Senescence tertunda
        ```
        
        ### 4. **Seed Storage**
        
        **Aplikasi:**
        ```
        BENIH:
        1. Spray ABA 50-100 ppm sebelum panen
        2. Keringkan
        3. Simpan
        
        HASIL:
        - Dormansi terjaga
        - Viabilitas lebih lama
        - Perkecambahan prematur ↓
        ```
        
        ### 5. **Salinity Tolerance**
        
        **Aplikasi:**
        ```
        TANAMAN DI TANAH SALIN:
        1. Seed priming dengan ABA 1-10 μM
        2. Atau foliar spray ABA 10-50 μM
        
        HASIL:
        - Osmotic adjustment
        - Ion homeostasis
        - Toleransi salinitas +30-50%
        ```
        
        **Referensi:**
        - Zhu, J. K. (2002). Annual Review of Plant Biology, 53, 247-273
        
        ---
        
        ## 🌿 SUMBER ABA ALAMI
        
        ### **1. Ekstrak Daun Tua/Stress**
        
        **Prinsip:**
        - Daun tua/stress → ABA tinggi
        - Ekstrak → Aplikasi ke tanaman lain
        
        **Cara:**
        ```
        1. Kumpulkan daun tua/menguning (ABA tinggi)
        2. Blender dengan air (1:2)
        3. Saring
        4. Aplikasikan (spray/siram)
        
        Efektivitas: 30-50% vs ABA sintetik
        ```
        
        ### **2. Stress-Induced ABA**
        
        **Cara:**
        ```
        1. Stress tanaman donor (kekeringan ringan 2-3 hari)
        2. ABA meningkat di daun
        3. Panen daun
        4. Ekstrak
        5. Aplikasi ke tanaman target
        ```
        
        ### **3. Produk Komersial**
        
        **ABA Sintetik:**
        - S-ABA (Active form)
        - ProTone (ABA untuk anggur)
        
        **Harga:**
        - Mahal (Rp 500K-2juta/100g)
        - Tapi sangat potent (μM level)
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### 1. **Dosis Berlebihan:**
        ```
        Gejala:
        - Pertumbuhan terhambat parah
        - Daun kecil, klorosis
        - Yield menurun
        
        Solusi:
        - Gunakan dosis rendah (μM level)
        - Aplikasi targeted (saat perlu)
        - Jangan aplikasi rutin
        ```
        
        ### 2. **Timing:**
        ```
        BENAR:
        - Sebelum stress (priming)
        - Saat stress ringan (protective)
        - Sebelum transplant
        
        SALAH:
        - Saat pertumbuhan aktif (inhibisi)
        - Terlalu sering (growth retardation)
        ```
        
        ### 3. **Interaksi:**
        ```
        ANTAGONIS:
        - ABA vs GA (berlawanan!)
        - ABA vs Sitokinin
        
        JANGAN KOMBINASI:
        - ABA + GA (cancel out)
        - Gunakan terpisah sesuai tujuan
        ```
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        **1. Untuk Drought Tolerance:**
        - Seed priming (1-10 μM, 24 jam)
        - Atau foliar spray sebelum kekeringan
        - Efektif untuk tanaman annual
        
        **2. Untuk Transplant:**
        - Root dip atau foliar spray 1 hari sebelum
        - Konsentrasi rendah (10-50 μM)
        - Kombinasi dengan good watering practice
        
        **3. Untuk Storage:**
        - Aplikasi sebelum panen
        - Konsentrasi tinggi (100-500 ppm)
        - Combine dengan suhu rendah
        
        **4. Ekonomis:**
        - ABA mahal → Gunakan hanya saat perlu
        - Seed priming paling cost-effective
        - Atau gunakan ekstrak alami (daun stress)
        
        **5. Research:**
        - ABA masih area penelitian aktif
        - Banyak aplikasi potensial (climate change)
        - Stay updated dengan literatur terbaru
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Finkelstein, R. (2013).** Abscisic acid synthesis and response. The Arabidopsis Book, 11, e0166.
        
        2. **Cutler, S. R., et al. (2010).** Abscisic acid: emergence of a core signaling network. Annual Review of Plant Biology, 61, 651-679.
        
        3. **Schroeder, J. I., et al. (2001).** Guard cell signal transduction. Annual Review of Plant Physiology and Plant Molecular Biology, 52, 627-658.
        
        4. **Zhu, J. K. (2002).** Salt and drought stress signal transduction in plants. Annual Review of Plant Biology, 53, 247-273.
        
        5. **Travaglia, C., et al. (2007).** Exogenous ABA increases yield in field-grown wheat with moderate water restriction. Journal of Plant Growth Regulation, 53(1), 1-9.
        
        """)
    
    # Natural Sources
    with subtab_natural:
        st.subheader("🍇 Sumber Hormon Alami")
        
        st.markdown("""
        ## 🍇 SUMBER HORMON TUMBUHAN ALAMI
        
        ### Mengapa Gunakan Sumber Alami?
        
        **Keuntungan:**
        - ✅ **Lebih murah** (bisa buat sendiri)
        - ✅ **Organik** (ramah lingkungan)
        - ✅ **Aman** (tidak toksik)
        - ✅ **Multi-hormon** (kombinasi alami)
        - ✅ **Mudah didapat** (bahan lokal)
        
        **Kekurangan:**
        - ⚠️ Konsentrasi tidak presisi
        - ⚠️ Variasi antar batch
        - ⚠️ Shelf-life pendek
        
        ---
        
        ## 🍇 1. ANGGUR HIJAU (Green Grapes)
        
        ### **Kandungan Hormon:**
        - **GA3 (Gibberellic Acid):** 50-200 ppm
        - **GA7:** 20-80 ppm
        - **Auksin (IAA):** 10-30 ppm
        - **Sitokinin:** 5-15 ppm
        
        ### **Waktu Panen Optimal:**
        - **2-4 minggu setelah fruit set**
        - Buah masih hijau, keras
        - Ukuran kecil (diameter 5-10 mm)
        
        ### **RESEP LENGKAP:**
        
        #### **A. Ekstrak Cair (Liquid Extract)**
        
        ```
        BAHAN:
        - 1 kg anggur hijau muda
        - 2 liter air bersih
        - 1 sendok makan gula (optional, sebagai spreader)
        
        ALAT:
        - Blender
        - Kain saring/saringan halus
        - Botol spray
        
        CARA MEMBUAT:
        1. Cuci bersih anggur (buang kotoran, pestisida)
        2. Potong-potong kecil (termasuk biji)
        3. Blender dengan 1 liter air (5-10 menit)
        4. Diamkan 30 menit (ekstraksi)
        5. Saring dengan kain halus (peras)
        6. Tambahkan air hingga 2 liter
        7. Tambahkan gula, aduk rata
        8. Siap digunakan!
        
        KONSENTRASI:
        - Undiluted (100%): ~100-150 ppm GA equivalent
        - Diluted 1:1: ~50-75 ppm
        - Diluted 1:2: ~30-50 ppm
        
        APLIKASI:
        - Semprot pagi/sore
        - Basahi seluruh tanaman
        - Ulangi 7-10 hari
        
        PENYIMPANAN:
        - Kulkas: 3-5 hari
        - Freezer: 1-2 bulan
        ```
        
        #### **B. Powder (Bubuk Kering)**
        
        ```
        CARA MEMBUAT:
        1. Blender anggur hijau (tanpa air)
        2. Sebar tipis di nampan
        3. Keringkan di oven 50-60°C (12-24 jam)
           Atau jemur di bawah sinar matahari (2-3 hari)
        4. Blender kering jadi powder
        5. Simpan di wadah kedap udara
        
        CARA PAKAI:
        - 10-20 gram powder per liter air
        - Rendam 2-4 jam, aduk sesekali
        - Saring, siap semprot
        
        PENYIMPANAN:
        - Tempat gelap, kering
        - Tahan 6-12 bulan
        ```
        
        ### **Target Tanaman:**
        - ✅ Anggur (pembesaran buah)
        - ✅ Tomat (fruit set, pembesaran)
        - ✅ Cabai (fruit set)
        - ✅ Strawberry (pembungaan)
        - ✅ Lettuce (perkecambahan)
        
        ---
        
        ## 🌱 2. KECAMBAH (SPROUTS)
        
        ### **Kandungan Hormon:**
        - **Giberelin (GA):** 100-300 ppm (TINGGI!)
        - **Auksin (IAA):** 20-50 ppm
        - **Sitokinin:** 10-30 ppm
        
        ### **Jenis Kecambah Terbaik:**
        1. **Kacang Hijau** (Mung Bean) - GA tertinggi
        2. **Kedelai** (Soybean) - Balanced hormones
        3. **Alfalfa** - Sitokinin tinggi
        
        ### **RESEP:**
        
        ```
        BAHAN:
        - 500 gram kacang hijau/kedelai
        - 2 liter air
        
        CARA MEMBUAT:
        1. Rendam kacang 8-12 jam
        2. Tiriskan, letakkan di wadah gelap
        3. Siram 2-3x sehari (jaga lembab)
        4. Kecambahkan 3-5 hari (panjang 3-5 cm)
        5. Blender kecambah + 1 liter air
        6. Saring, tambahkan air hingga 2 liter
        7. Siap pakai!
        
        KONSENTRASI:
        - Undiluted: ~150-250 ppm GA
        - Diluted 1:1: ~75-125 ppm
        
        APLIKASI:
        - Breaking dormancy biji
        - Pemanjangan batang
        - Perkecambahan seragam
        
        PENYIMPANAN:
        - Kulkas: 2-3 hari
        - Buat fresh lebih baik
        ```
        
        ---
        
        ## 🥥 3. AIR KELAPA (COCONUT WATER)
        
        ### **Kandungan Hormon:**
        - **Sitokinin (Zeatin):** 10-50 ppm (TINGGI!)
        - **Auksin (IAA):** 5-15 ppm
        - **Giberelin:** 2-10 ppm
        - Plus: Gula, mineral, vitamin
        
        ### **Waktu Panen Optimal:**
        - Kelapa muda (6-8 bulan)
        - Air masih manis, jernih
        
        ### **RESEP:**
        
        ```
        CARA PAKAI LANGSUNG:
        - Air kelapa murni (100%)
        - Atau encerkan 1:1 dengan air
        - Semprot atau siram
        
        APLIKASI:
        1. Kultur Jaringan:
           - 10-20% air kelapa dalam media
           - Stimulasi pembelahan sel
        
        2. Rooting:
           - Rendam stek di air kelapa (24 jam)
           - Atau semprot setelah tanam
        
        3. Foliar Spray:
           - Encerkan 1:2 (1 air kelapa : 2 air)
           - Semprot daun 7-10 hari sekali
        
        TARGET:
        - Kultur jaringan (sitokinin tinggi)
        - Stek (rooting + anti-senescence)
        - Tanaman hias (kesegaran daun)
        ```
        
        ---
        
        ## 🌿 4. EKSTRAK BAWANG (ONION EXTRACT)
        
        ### **Kandungan:**
        - **Auksin:** Tinggi
        - **Antibakteri:** Allicin
        - **Stimulan akar**
        
        ### **RESEP:**
        
        ```
        BAHAN:
        - 3-5 siung bawang merah/putih
        - 1 liter air
        
        CARA:
        1. Kupas dan potong halus bawang
        2. Rendam di air (24 jam)
        3. Saring
        4. Siap pakai
        
        APLIKASI:
        - Rooting hormone alami
        - Rendam stek 2-4 jam
        - Atau siram setelah tanam
        
        EFEKTIVITAS:
        - 60-70% vs rooting hormone sintetik
        - Plus efek antibakteri
        ```
        
        ---
        
        ## 🍌 5. KULIT PISANG (BANANA PEEL)
        
        ### **Kandungan:**
        - **Sitokinin:** Sedang
        - **Auksin:** Rendah
        - **Kalium:** TINGGI (K)
        - **Fosfor:** Sedang (P)
        
        ### **RESEP:**
        
        ```
        A. EKSTRAK CAIR:
        1. Potong kulit pisang 5-10 buah
        2. Rendam di 2 liter air (3-5 hari)
        3. Saring
        4. Encerkan 1:5 dengan air
        5. Siram tanaman
        
        B. KOMPOS:
        1. Potong kecil-kecil
        2. Tanam di sekitar tanaman
        3. Dekomposisi → Release nutrisi
        
        MANFAAT:
        - Nutrisi K tinggi (pembungaan, buah)
        - Hormon sitokinin (anti-aging)
        ```
        
        ---
        
        ## 🌊 6. RUMPUT LAUT (SEAWEED)
        
        ### **Kandungan:**
        - **Sitokinin:** Tinggi
        - **Auksin:** Sedang
        - **Giberelin:** Rendah
        - **Betaine:** Growth stimulant
        - **Mineral:** Lengkap
        
        ### **PRODUK KOMERSIAL:**
        - Maxicrop
        - Seasol
        - Kelpak
        
        ### **DIY EXTRACT:**
        
        ```
        BAHAN:
        - 1 kg rumput laut segar (atau 200g kering)
        - 5 liter air
        
        CARA:
        1. Cuci bersih rumput laut
        2. Potong kecil-kecil
        3. Rendam di air (2-3 minggu)
        4. Aduk setiap 2-3 hari
        5. Saring
        6. Encerkan 1:10 untuk aplikasi
        
        APLIKASI:
        - Foliar spray: 1:20
        - Soil drench: 1:10
        - Frekuensi: 2-4 minggu sekali
        ```
        
        ---
        
        ## 📊 PERBANDINGAN EFEKTIVITAS
        
        | Sumber | GA | Auksin | Sitokinin | Biaya | Efektivitas |
        |--------|----|----|-----------|-------|-------------|
        | **Anggur Hijau** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | Rendah | 70-80% |
        | **Kecambah** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Sangat Rendah | 60-70% |
        | **Air Kelapa** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Rendah | 50-60% |
        | **Bawang** | ⭐ | ⭐⭐⭐⭐ | ⭐ | Sangat Rendah | 60-70% |
        | **Pisang** | ⭐ | ⭐ | ⭐⭐⭐ | Sangat Rendah | 40-50% |
        | **Rumput Laut** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Sedang | 60-70% |
        | **Sintetik** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tinggi | 100% |
        
        ---
        
        ## 💡 TIPS KOMBINASI
        
        ### **Formula 1: Rooting Super (Perakaran)**
        ```
        - 50% Air kelapa
        - 30% Ekstrak bawang
        - 20% Air
        
        Rendam stek 4-6 jam → Tanam
        Efektivitas: 80-90%
        ```
        
        ### **Formula 2: Growth Booster (Pertumbuhan)**
        ```
        - 40% Ekstrak kecambah (GA tinggi)
        - 30% Air kelapa (Sitokinin)
        - 30% Air
        
        Semprot 7-10 hari sekali
        Hasil: Pertumbuhan 30-50% lebih cepat
        ```
        
        ### **Formula 3: Fruit Set (Pembentukan Buah)**
        ```
        - 60% Ekstrak anggur hijau (GA)
        - 20% Air kelapa (Sitokinin)
        - 20% Air
        
        Semprot saat bunga mekar
        Hasil: Fruit set naik 40-60%
        ```
        
        ---
        
        ## ⚠️ PERINGATAN & TIPS
        
        **1. Hygiene:**
        - Cuci bersih semua bahan
        - Gunakan air bersih
        - Sterilkan alat (jika untuk kultur jaringan)
        
        **2. Penyimpanan:**
        - Ekstrak cair: Kulkas (3-5 hari)
        - Powder: Tempat gelap, kering (6-12 bulan)
        - Buat fresh lebih baik!
        
        **3. Aplikasi:**
        - Pagi/sore (suhu sejuk)
        - Jangan saat hujan
        - Basahi seluruh tanaman
        
        **4. Dosis:**
        - Mulai rendah (encerkan lebih banyak)
        - Naikkan bertahap
        - Monitor respons tanaman
        
        **5. Konsistensi:**
        - Aplikasi teratur (7-14 hari)
        - Catat hasil
        - Adjust formula sesuai kebutuhan
        
        ---
        
        ## 🎯 KESIMPULAN
        
        **Hormon alami adalah alternatif:**
        - ✅ **Ekonomis** (hemat 70-90% biaya)
        - ✅ **Organik** (ramah lingkungan)
        - ✅ **Efektif** (60-80% vs sintetik)
        - ✅ **Mudah** (bahan lokal, cara simple)
        
        **Terbaik untuk:**
        - Petani organik
        - Skala kecil-menengah
        - Budget terbatas
        - Eksperimen/trial
        
        **Gunakan sintetik jika:**
        - Butuh presisi tinggi
        - Skala komersial besar
        - Hasil harus konsisten
        - Budget memadai
        
        **ATAU KOMBINASI KEDUANYA!** 🌟
        
        """)

# Save message
st.success("✅ Module Fisiologi Tumbuhan berhasil dibuat!")
st.info("💡 Module ini mencakup hormon tumbuhan lengkap dengan sumber alami seperti anggur hijau untuk GA3/GA7!")
