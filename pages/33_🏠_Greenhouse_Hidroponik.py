import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Greenhouse & Hidroponik - AgriSensa",
    page_icon="🏠",
    layout="wide"
)

# Header
st.title("🏠 Greenhouse & Sistem Hidroponik")
st.markdown("**Teknologi Budidaya Terkendali untuk Tanaman Bernilai Tinggi**")

# Main tabs
tab_greenhouse, tab_hydro, tab_nutrients, tab_climate, tab_economics, tab_3k = st.tabs([
    "🏠 Greenhouse",
    "💧 Sistem Hidroponik",
    "🧪 Nutrisi & pH",
    "🌡️ Kontrol Iklim",
    "💰 Analisis Ekonomi",
    "🚀 Manajemen 3K (Sustainable)"
])

# ===== TAB 1: GREENHOUSE =====
with tab_greenhouse:
    st.header("🏠 Teknologi Greenhouse")
    
    st.markdown("""
    ### Apa itu Greenhouse?
    
    **Greenhouse (rumah kaca)** adalah struktur tertutup dengan atap dan dinding transparan yang **mengontrol lingkungan** untuk pertumbuhan tanaman optimal.
    
    **Keuntungan:**
    - ✅ **Kontrol penuh** iklim (suhu, kelembaban, cahaya)
    - ✅ **Produktivitas tinggi** (2-3x vs open field)
    - ✅ **Kualitas premium** (bersih, seragam)
    - ✅ **Panen sepanjang tahun** (tidak tergantung musim)
    - ✅ **Hemat air** (30-50% vs open field)
    - ✅ **Hemat pestisida** (80-90%, terlindung hama)
    - ✅ **Premium price** (2-5x harga pasar)
    
    **Kekurangan:**
    ```
    ❌ Investasi awal tinggi (Rp 200-800 juta/1000 m²)
    ❌ Biaya operasional tinggi (listrik, cooling)
    ❌ Perlu skill teknis
    ❌ Maintenance rutin
    ```
    
    ---
    
    ## 🏗️ JENIS GREENHOUSE
    
    ### **1. GREENHOUSE SEDERHANA (Low-Tech)**
    
    **A. Tunnel Plastik (Polytunnel):**
    ```
    Struktur:
    - Rangka: Bambu/pipa PVC
    - Atap: Plastik UV (200 micron)
    - Dinding: Plastik/insect net
    - Ventilasi: Manual (buka tutup plastik)
    
    Dimensi:
    - Lebar: 6-8 m
    - Panjang: 20-50 m
    - Tinggi: 3-4 m
    
    Biaya:
    - Rp 150-250K/m²
    - Total 1000 m²: Rp 150-250 juta
    
    Cocok untuk:
    - Sayuran (tomat, cabai, melon)
    - Dataran rendah-menengah
    - Petani pemula
    ```
    
    **Keuntungan:**
    ```
    ✅ Murah
    ✅ Mudah bangun (DIY)
    ✅ Fleksibel (bisa pindah)
    ```
    
    **Kekurangan:**
    ```
    ❌ Kontrol iklim terbatas
    ❌ Panas (>40°C di dataran rendah)
    ❌ Plastik perlu ganti (2-3 tahun)
    ```
    
    ---
    
    **B. Screenhouse (Insect Net House):**
    ```
    Struktur:
    - Rangka: Besi hollow/pipa galvanis
    - Atap & dinding: Insect net (50 mesh)
    - Ventilasi: Alami (angin)
    
    Biaya:
    - Rp 200-350K/m²
    - Total 1000 m²: Rp 200-350 juta
    
    Cocok untuk:
    - Sayuran organik
    - Bibit tanaman
    - Area dengan hama tinggi
    ```
    
    **Keuntungan:**
    ```
    ✅ Sirkulasi udara baik (tidak panas)
    ✅ Lindungi dari hama (90%)
    ✅ Tahan lama (net 5-7 tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Tidak lindungi dari hujan/angin kencang
    ❌ Kontrol suhu minimal
    ```
    
    ---
    
    ### **2. GREENHOUSE MODERN (High-Tech)**
    
    **A. Multi-Span Greenhouse:**
    ```
    Struktur:
    - Rangka: Besi galvanis (tahan 15-20 tahun)
    - Atap: Polycarbonat/kaca
    - Dinding: Polycarbonat/plastik UV
    - Ventilasi: Otomatis (roof vent, side vent)
    - Cooling: Evaporative cooling (cooling pad + fan)
    - Heating: Heater (jika perlu)
    
    Dimensi:
    - Lebar span: 8-12 m
    - Jumlah span: 3-10
    - Tinggi: 4-6 m
    
    Biaya:
    - Rp 500-800K/m²
    - Total 1000 m²: Rp 500-800 juta
    
    Cocok untuk:
    - Tomat, paprika, timun (high-value)
    - Bunga potong
    - Skala komersial
    ```
    
    **Keuntungan:**
    ```
    ✅ Kontrol iklim penuh (suhu, RH, CO₂)
    ✅ Produktivitas sangat tinggi (3-5x open field)
    ✅ Kualitas export
    ✅ Tahan lama (20+ tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi sangat tinggi
    ❌ Biaya operasional tinggi (listrik)
    ❌ Perlu teknisi terlatih
    ```
    
    ---
    
    **B. Venlo Greenhouse (Dutch Style):**
    ```
    Ciri khas:
    - Atap kaca (glass)
    - Roof angle: 22-26° (optimal untuk cahaya)
    - Gutter: Aluminium (drainase hujan)
    - Fully automated (climate, irrigation, fertigation)
    
    Biaya:
    - Rp 800-1,500K/m²
    - Total 1000 m²: Rp 800 juta - 1.5 miliar
    
    Cocok untuk:
    - Tomat, paprika (export quality)
    - Bunga potong (mawar, anggrek)
    - Skala besar (>5000 m²)
    ```
    
    **Keuntungan:**
    ```
    ✅ Transmisi cahaya maksimal (90%)
    ✅ Umur panjang (30+ tahun)
    ✅ Presisi tinggi (sensor, automation)
    ✅ Yield tertinggi (50-100 kg/m²/tahun untuk tomat!)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tertinggi
    ❌ Perlu expertise tinggi
    ❌ Tidak cocok untuk dataran rendah (terlalu panas)
    ```
    
    ---
    
    ## 📊 PERBANDINGAN GREENHOUSE
    
    | Tipe | Investasi (Rp/m²) | Kontrol Iklim | Produktivitas | Umur | Cocok untuk |
    |------|-------------------|---------------|---------------|------|-------------|
    | **Polytunnel** | 150-250K | Rendah | 2x open field | 5-10 tahun | Pemula, dataran tinggi |
    | **Screenhouse** | 200-350K | Minimal | 1.5x open field | 10-15 tahun | Organik, bibit |
    | **Multi-Span** | 500-800K | Tinggi | 3-5x open field | 20+ tahun | Komersial |
    | **Venlo** | 800-1,500K | Sangat tinggi | 5-10x open field | 30+ tahun | Export, skala besar |
    
    ---
    
    ## 💡 TIPS MEMILIH GREENHOUSE
    
    **1. Sesuaikan dengan Budget:**
    ```
    - Budget <Rp 300 juta: Polytunnel/Screenhouse
    - Budget Rp 300-800 juta: Multi-Span
    - Budget >Rp 800 juta: Venlo
    ```
    
    **2. Pertimbangkan Lokasi:**
    ```
    - Dataran rendah (0-500 m): Perlu cooling kuat
    - Dataran menengah (500-1000 m): Ideal untuk greenhouse
    - Dataran tinggi (>1000 m): Perlu heating (malam hari)
    ```
    
    **3. Pilih Tanaman Bernilai Tinggi:**
    ```
    - Tomat cherry: Rp 30-50K/kg
    - Paprika: Rp 40-80K/kg
    - Melon premium: Rp 50-100K/kg
    - Strawberry: Rp 80-150K/kg
    - Bunga potong: Rp 5-20K/tangkai
    
    ROI: 2-4 tahun (jika dikelola baik)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Nelson, P. V. (2011).** Greenhouse Operation and Management, 7th Edition. Prentice Hall.
    
    2. **Hanan, J. J. (1998).** Greenhouses: Advanced Technology for Protected Horticulture. CRC Press.
    
    3. **Bakker, J. C., et al. (1995).** Greenhouse Climate Control. Wageningen Academic Publishers.
    
    """)

# ===== TAB 2: SISTEM HIDROPONIK =====
with tab_hydro:
    st.header("💧 Sistem Hidroponik")
    
    st.markdown("""
    ### Apa itu Hidroponik?
    
    **Hidroponik** adalah metode budidaya tanaman **tanpa tanah**, menggunakan **larutan nutrisi** dalam air sebagai media tumbuh.
    
    **Keuntungan:**
    - ✅ **Hemat air** (90% vs tanah!)
    - ✅ **Pertumbuhan cepat** (30-50% lebih cepat)
    - ✅ **Yield tinggi** (2-3x vs tanah)
    - ✅ **Bersih** (no soil-borne disease)
    - ✅ **Efisien lahan** (vertikal farming)
    - ✅ **Kontrol nutrisi** presisi
    
    **Kekurangan:**
    ```
    ❌ Investasi awal tinggi
    ❌ Perlu skill (nutrisi, pH, EC)
    ❌ Risiko system failure (pompa mati = tanaman mati)
    ❌ Biaya listrik (pompa 24/7)
    ```
    
    ---
    
    ## 🌊 JENIS SISTEM HIDROPONIK
    
    ### **1. NFT (Nutrient Film Technique)**
    
    **Prinsip:**
    ```
    Larutan nutrisi mengalir tipis (film) di dasar pipa miring
    → Akar menyerap nutrisi + oksigen
    → Larutan kembali ke tangki (recirculating)
    ```
    
    **Komponen:**
    ```
    1. Tangki nutrisi (100-200 L)
    2. Pompa submersible (30-50 watt)
    3. Pipa NFT (diameter 3-4 inch, panjang 3-6 m)
    4. Kemiringan: 1-3% (1-3 cm per meter)
    5. Net pot (diameter 5 cm)
    6. Rockwool/cocopeat (media semai)
    ```
    
    **Desain:**
    ```
    Contoh: Selada 100 lubang
    
    - Pipa: 10 batang @ 3 m (10 lubang/pipa)
    - Jarak lubang: 25 cm
    - Kemiringan: 2% (6 cm drop per 3 m)
    - Pompa: 40 watt, 2000 L/jam
    - Flow rate: 1-2 L/menit per pipa
    - Tangki: 150 L
    
    Biaya:
    - Pipa PVC: Rp 50K × 10 = Rp 500K
    - Net pot: Rp 1K × 100 = Rp 100K
    - Pompa: Rp 300K
    - Tangki: Rp 200K
    - Rangka: Rp 500K
    - Nutrisi (1 bulan): Rp 200K
    
    TOTAL: Rp 1.8 juta (100 lubang)
    = Rp 18K/lubang
    ```
    
    **Cocok untuk:**
    - Selada, kangkung, sawi, bayam
    - Tanaman daun (leafy greens)
    - Pertumbuhan cepat (25-35 hari)
    
    **Keuntungan:**
    ```
    ✅ Hemat air (recirculating)
    ✅ Oksigenasi baik (akar tidak terendam)
    ✅ Pertumbuhan cepat
    ```
    
    **Kekurangan:**
    ```
    ❌ Pompa harus 24/7 (jika mati 2-3 jam = tanaman layu)
    ❌ Perlu kemiringan presisi
    ❌ Tidak cocok untuk tanaman besar (tomat, cabai)
    ```
    
    ---
    
    ### **2. DFT (Deep Flow Technique)**
    
    **Prinsip:**
    ```
    Larutan nutrisi mengalir dalam (deep) di pipa/talang
    → Akar terendam sebagian
    → Lebih toleran jika pompa mati (buffer 6-12 jam)
    ```
    
    **Perbedaan dengan NFT:**
    ```
    NFT: Film tipis (1-2 mm), akar tidak terendam
    DFT: Kedalaman 3-5 cm, akar terendam sebagian
    
    DFT lebih aman untuk pemula!
    ```
    
    **Desain:**
    ```
    - Pipa/talang: Diameter 4-6 inch
    - Kedalaman air: 3-5 cm
    - Kemiringan: 1-2%
    - Pompa: Bisa intermittent (on 15 menit, off 15 menit)
    
    Biaya: Sama dengan NFT (Rp 18-20K/lubang)
    ```
    
    **Cocok untuk:**
    - Selada, kangkung, pakcoy
    - Pemula (lebih toleran error)
    
    ---
    
    ### **3. WICK SYSTEM (Sistem Sumbu)**
    
    **Prinsip:**
    ```
    Larutan nutrisi diserap melalui sumbu (wick) dari tangki ke media
    → PASIF (no pump, no electricity!)
    → Paling sederhana
    ```
    
    **Komponen:**
    ```
    1. Wadah (pot/botol bekas)
    2. Media: Cocopeat/sekam bakar
    3. Sumbu: Kain flanel/sumbu kompor (diameter 1 cm)
    4. Tangki nutrisi (di bawah pot)
    ```
    
    **Desain:**
    ```
    Contoh: Cabai 20 pot
    
    - Pot: Diameter 20 cm
    - Media: Cocopeat 2 L/pot
    - Sumbu: 2-3 sumbu/pot
    - Tangki: 10 L (untuk 5 pot)
    
    Biaya:
    - Pot: Rp 5K × 20 = Rp 100K
    - Cocopeat: Rp 200K
    - Sumbu: Rp 50K
    - Tangki: Rp 100K
    - Nutrisi: Rp 200K
    
    TOTAL: Rp 650K (20 pot)
    = Rp 32K/pot
    ```
    
    **Cocok untuk:**
    - Cabai, tomat (tanaman buah)
    - Skala kecil (hobi, rumahan)
    - Area tanpa listrik
    
    **Keuntungan:**
    ```
    ✅ Paling murah
    ✅ No listrik (hemat!)
    ✅ Mudah maintenance
    ✅ Cocok untuk pemula
    ```
    
    **Kekurangan:**
    ```
    ❌ Pertumbuhan lebih lambat (vs NFT/DFT)
    ❌ Tidak cocok untuk tanaman besar (akar banyak)
    ❌ Perlu ganti sumbu (3-6 bulan)
    ```
    
    ---
    
    ### **4. DRIP SYSTEM (Sistem Tetes)**
    
    **Prinsip:**
    ```
    Larutan nutrisi diteteskan ke media (cocopeat/perlite)
    → Excess drainage kembali ke tangki (recirculating)
    → Cocok untuk tanaman besar
    ```
    
    **Komponen:**
    ```
    1. Tangki nutrisi (200-500 L)
    2. Pompa + timer (on/off otomatis)
    3. Mainline + lateral (pipa 1/2 inch)
    4. Dripper (2-4 L/jam)
    5. Pot/polybag (10-20 L)
    6. Media: Cocopeat + perlite (70:30)
    7. Drainage tray (kumpulkan excess)
    ```
    
    **Desain:**
    ```
    Contoh: Tomat 50 tanaman
    
    - Pot: 15 L/tanaman
    - Media: Cocopeat + perlite
    - Dripper: 2 L/jam, 2 dripper/tanaman
    - Timer: On 5 menit, off 30 menit (siang)
    - Pompa: 60 watt
    
    Biaya:
    - Pot 15L: Rp 15K × 50 = Rp 750K
    - Media: Rp 1 juta
    - Drip system: Rp 2 juta
    - Pompa + timer: Rp 800K
    - Tangki: Rp 500K
    - Rangka: Rp 2 juta
    
    TOTAL: Rp 7 juta (50 tanaman)
    = Rp 140K/tanaman
    ```
    
    **Cocok untuk:**
    - Tomat, paprika, melon, timun
    - Tanaman buah (high-value)
    - Greenhouse
    
    **Keuntungan:**
    ```
    ✅ Cocok untuk tanaman besar
    ✅ Oksigenasi baik (media porous)
    ✅ Toleran jika pompa mati (buffer 1-2 hari)
    ✅ Scalable (mudah expand)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tinggi
    ❌ Perlu ganti media (6-12 bulan)
    ❌ Risiko clogging (dripper tersumbat)
    ```
    
    ---
    
    ### **5. AEROPONICS**
    
    **Prinsip:**
    ```
    Akar digantung di udara
    → Larutan nutrisi disemprotkan (mist/spray)
    → Oksigenasi MAKSIMAL!
    ```
    
    **Komponen:**
    ```
    1. Chamber (box kedap cahaya)
    2. Mist nozzle (spray 360°)
    3. Pompa tekanan tinggi (60-80 PSI)
    4. Timer (on 5 detik, off 5 menit)
    ```
    
    **Biaya:**
    ```
    Sangat mahal (Rp 200-300K/lubang)
    Hanya untuk research/high-tech farm
    ```
    
    **Keuntungan:**
    ```
    ✅ Pertumbuhan TERCEPAT (50% lebih cepat vs NFT)
    ✅ Oksigenasi maksimal
    ✅ Hemat air (95% vs tanah)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tertinggi
    ❌ Sangat sensitif (pompa mati 30 menit = tanaman mati)
    ❌ Perlu expertise tinggi
    ```
    
    ---
    
    ## 📊 PERBANDINGAN SISTEM HIDROPONIK
    
    | Sistem | Investasi/lubang | Listrik | Kesulitan | Pertumbuhan | Cocok untuk |
    |--------|------------------|---------|-----------|-------------|-------------|
    | **NFT** | Rp 18-20K | 24/7 | Sedang | Cepat | Selada, kangkung |
    | **DFT** | Rp 18-20K | Intermittent | Mudah | Cepat | Selada (pemula) |
    | **Wick** | Rp 30-40K | No | Sangat mudah | Sedang | Cabai, tomat (hobi) |
    | **Drip** | Rp 140-200K | Intermittent | Sedang | Cepat | Tomat, paprika (komersial) |
    | **Aeroponics** | Rp 200-300K | 24/7 | Sangat sulit | Sangat cepat | Research |
    
    ---
    
    ## 💡 TIPS MEMILIH SISTEM
    
    **Pilih NFT/DFT jika:**
    ```
    ✅ Tanaman daun (selada, kangkung)
    ✅ Ingin cepat panen (25-35 hari)
    ✅ Skala menengah (100-1000 lubang)
    ```
    
    **Pilih WICK jika:**
    ```
    ✅ Pemula (paling mudah!)
    ✅ Skala kecil (hobi)
    ✅ No budget untuk listrik
    ✅ Tanaman buah (cabai, tomat)
    ```
    
    **Pilih DRIP jika:**
    ```
    ✅ Tanaman buah bernilai tinggi
    ✅ Greenhouse
    ✅ Skala komersial
    ✅ Punya budget (ROI 1-2 tahun)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Resh, H. M. (2012).** Hydroponic Food Production, 7th Edition. CRC Press.
    
    2. **Jones, J. B. (2005).** Hydroponics: A Practical Guide for the Soilless Grower. CRC Press.
    
    3. **Savvas, D., & Passam, H. (2002).** Hydroponic Production of Vegetables and Ornamentals. Embryo Publications.
    
    """)

# ===== TAB 3: NUTRISI & pH =====
with tab_nutrients:
    st.header("🧪 Nutrisi & Manajemen pH")
    
    st.markdown("""
    ### Nutrisi Hidroponik
    
    Tanaman hidroponik perlu **16 elemen esensial** dari larutan nutrisi:
    
    **Makronutrien (banyak):**
    - N (Nitrogen), P (Fosfor), K (Kalium)
    - Ca (Kalsium), Mg (Magnesium), S (Sulfur)
    
    **Mikronutrien (sedikit):**
    - Fe (Besi), Mn (Mangan), Zn (Seng), Cu (Tembaga)
    - B (Boron), Mo (Molibdenum), Cl (Klorin)
    
    ---
    
    ## 🧪 AB MIX (Nutrisi Hidroponik)
    
    ### **Apa itu AB Mix?**
    
    **AB Mix** adalah nutrisi hidroponik yang terdiri dari **2 larutan terpisah**:
    - **Pekkat A:** Ca(NO₃)₂, Fe-EDTA
    - **Pekkat B:** KNO₃, KH₂PO₄, MgSO₄, mikronutrien
    
    **Mengapa dipisah?**
    ```
    Jika dicampur langsung (konsentrasi tinggi):
    Ca²⁺ + SO₄²⁻ → CaSO₄ (gypsum, mengendap!)
    Ca²⁺ + PO₄³⁻ → Ca₃(PO₄)₂ (mengendap!)
    
    Jadi HARUS dipisah, baru dicampur di tangki (konsentrasi rendah)
    ```
    
    ---
    
    ### **Cara Membuat Larutan Nutrisi:**
    
    **1. Beli AB Mix (Paling Mudah):**
    ```
    Merek: AB Mix Hydro, Growmore, dll
    Harga: Rp 50-100K/kg (cukup untuk 500-1000 L)
    
    Cara pakai:
    1. Isi tangki dengan air (100 L)
    2. Larutkan Pekkat A: 50-100 gram → aduk
    3. Larutkan Pekkat B: 50-100 gram → aduk
    4. Ukur EC: Target 1.5-2.5 mS/cm
    5. Ukur pH: Target 5.5-6.5
    6. Adjust jika perlu
    ```
    
    **2. Buat Sendiri (Advanced):**
    ```
    Formula Selada (per 1000 L):
    
    PEKKAT A (1000x):
    - Ca(NO₃)₂·4H₂O: 944 g
    - Fe-EDTA: 79 g
    - Air: 1 L
    
    PEKKAT B (1000x):
    - KNO₃: 809 g
    - KH₂PO₄: 263 g
    - MgSO₄·7H₂O: 493 g
    - MnSO₄·H₂O: 2.13 g
    - ZnSO₄·7H₂O: 0.22 g
    - CuSO₄·5H₂O: 0.08 g
    - H₃BO₃: 2.86 g
    - Na₂MoO₄·2H₂O: 0.02 g
    - Air: 1 L
    
    Cara pakai:
    - Tambahkan 1 mL Pekkat A per 1 L air
    - Tambahkan 1 mL Pekkat B per 1 L air
    - EC: 1.8-2.2 mS/cm
    - pH: 5.8-6.2
    ```
    
    ---
    
    ## 📊 EC (Electrical Conductivity)
    
    ### **Apa itu EC?**
    
    **EC** = Konduktivitas listrik larutan = **ukuran konsentrasi nutrisi**
    
    ```
    EC tinggi = Nutrisi pekat (>2.5 mS/cm)
    EC rendah = Nutrisi encer (<1.0 mS/cm)
    ```
    
    ### **EC Optimal untuk Berbagai Tanaman:**
    
    | Tanaman | EC (mS/cm) | Keterangan |
    |---------|------------|------------|
    | **Selada** | 1.2-1.8 | Rendah (leafy greens) |
    | **Kangkung** | 1.5-2.0 | Rendah-sedang |
    | **Tomat** | 2.0-3.5 | Sedang-tinggi |
    | **Cabai** | 2.0-3.0 | Sedang-tinggi |
    | **Paprika** | 2.5-3.5 | Tinggi |
    | **Melon** | 2.0-2.5 | Sedang |
    | **Strawberry** | 1.8-2.2 | Sedang |
    
    ### **Cara Mengukur EC:**
    ```
    1. Beli EC meter (Rp 200-500K)
    2. Kalibrasi dengan larutan standar (1.413 mS/cm)
    3. Celupkan probe ke larutan nutrisi
    4. Baca nilai EC
    
    Jika EC terlalu rendah: Tambah AB Mix
    Jika EC terlalu tinggi: Tambah air
    ```
    
    ---
    
    ## 🧪 pH (Potential of Hydrogen)
    
    ### **Mengapa pH Penting?**
    
    **pH** mengontrol **ketersediaan nutrisi**:
    
    ```
    pH terlalu rendah (<5.0):
    - Fe, Mn, Zn larut berlebihan (toxic!)
    - Ca, Mg sulit diserap
    
    pH terlalu tinggi (>7.0):
    - Fe, Mn, Zn mengendap (defisiensi!)
    - P sulit diserap
    
    pH OPTIMAL: 5.5-6.5 (semua nutrisi tersedia)
    ```
    
    ### **pH Optimal untuk Berbagai Tanaman:**
    
    | Tanaman | pH Optimal | Toleransi |
    |---------|------------|-----------|
    | **Selada** | 5.5-6.5 | Luas |
    | **Tomat** | 6.0-6.5 | Sedang |
    | **Cabai** | 6.0-6.5 | Sedang |
    | **Strawberry** | 5.5-6.0 | Sempit (acidic) |
    | **Melon** | 6.0-6.5 | Sedang |
    
    ### **Cara Mengukur & Adjust pH:**
    
    **1. Ukur pH:**
    ```
    - pH meter digital (Rp 200-500K)
    - pH test kit (Rp 50-100K, kurang akurat)
    ```
    
    **2. Adjust pH:**
    ```
    Jika pH terlalu tinggi (>6.5):
    - Tambah pH Down (asam fosfat/nitrat)
    - Dosis: 1-5 mL per 10 L (cek bertahap!)
    
    Jika pH terlalu rendah (<5.5):
    - Tambah pH Up (kalium hidroksida)
    - Dosis: 1-5 mL per 10 L
    
    PENTING: Adjust sedikit-sedikit, cek ulang!
    ```
    
    ---
    
    ## 🩺 DIAGNOSA DEFISIENSI NUTRISI
    
    ### **Nitrogen (N) - Defisiensi:**
    ```
    Gejala:
    - Daun tua menguning (dari bawah)
    - Pertumbuhan lambat
    - Batang kurus
    
    Solusi:
    - Tambah KNO₃ atau Ca(NO₃)₂
    - Naikkan EC
    ```
    
    ### **Fosfor (P) - Defisiensi:**
    ```
    Gejala:
    - Daun tua ungu/kemerahan
    - Akar lemah
    - Bunga/buah sedikit
    
    Solusi:
    - Tambah KH₂PO₄
    - Cek pH (P tidak tersedia jika pH >7)
    ```
    
    ### **Kalium (K) - Defisiensi:**
    ```
    Gejala:
    - Tepi daun tua coklat/kering (necrosis)
    - Buah kecil, tidak manis
    
    Solusi:
    - Tambah KNO₃ atau K₂SO₄
    ```
    
    ### **Kalsium (Ca) - Defisiensi:**
    ```
    Gejala:
    - Daun muda keriting/kering
    - Blossom end rot (tomat, paprika)
    - Ujung akar mati
    
    Solusi:
    - Tambah Ca(NO₃)₂
    - Cek EC (jangan terlalu tinggi, hambat Ca)
    ```
    
    ### **Besi (Fe) - Defisiensi:**
    ```
    Gejala:
    - Daun muda kuning, tulang daun hijau (chlorosis)
    - Pertumbuhan terhambat
    
    Solusi:
    - Tambah Fe-EDTA
    - Turunkan pH (Fe tidak tersedia jika pH >7)
    ```
    
    ---
    
    ## 💡 TIPS MANAJEMEN NUTRISI
    
    **1. Monitoring Rutin:**
    ```
    - Cek EC & pH: 2x sehari (pagi & sore)
    - Ganti larutan: 2-4 minggu (atau jika EC tidak stabil)
    - Bersihkan tangki: Setiap ganti larutan
    ```
    
    **2. Kualitas Air:**
    ```
    - Air sumur/PAM: Cek EC awal (harus <0.5 mS/cm)
    - Jika EC tinggi: Pakai RO water atau air hujan
    - Jika air keras (Ca/Mg tinggi): Adjust formula
    ```
    
    **3. Suhu Larutan:**
    ```
    - Optimal: 18-22°C
    - Jika >28°C: Oksigen rendah (akar busuk)
    - Solusi: Chiller atau ganti larutan lebih sering
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Resh, H. M. (2012).** Hydroponic Food Production, 7th Edition. CRC Press.
    
    2. **Jones, J. B. (2005).** Hydroponics: A Practical Guide for the Soilless Grower. CRC Press.
    
    """)

# ===== TAB 4: KONTROL IKLIM =====
with tab_climate:
    st.header("🌡️ Kontrol Iklim Greenhouse")
    
    st.markdown("""
    ### Mengapa Kontrol Iklim Penting?
    
    **Iklim optimal** = **Produktivitas maksimal**
    
    **Parameter Kritis:**
    - 🌡️ **Suhu:** 20-30°C (optimal untuk fotosintesis)
    - 💧 **Kelembaban (RH):** 60-80%
    - ☀️ **Cahaya:** 30,000-50,000 lux
    - 🌬️ **CO₂:** 400-1000 ppm
    - 💨 **Ventilasi:** 40-60 air changes/hour
    
    ---
    
    ## 🌡️ KONTROL SUHU
    
    ### **1. COOLING (Pendinginan)**
    
    **A. Evaporative Cooling (Cooling Pad + Fan):**
    ```
    Prinsip:
    Air menguap → Serap panas → Suhu turun 5-10°C
    
    Komponen:
    - Cooling pad (cellulose, 10-15 cm tebal)
    - Fan exhaust (diameter 50-100 cm)
    - Pompa air (sirkulasi ke pad)
    
    Dimensi:
    - Greenhouse 1000 m²:
      * Cooling pad: 20 m² (2m × 10m)
      * Fan: 10 unit @ 1 HP
      * Pompa: 0.5 HP
    
    Biaya:
    - Cooling pad: Rp 500K/m² × 20 = Rp 10 juta
    - Fan: Rp 3 juta × 10 = Rp 30 juta
    - Pompa + pipa: Rp 5 juta
    
    TOTAL: Rp 45 juta
    
    Operasional:
    - Listrik: 10 HP × 8 jam × Rp 1500/kWh = Rp 90K/hari
    - Air: 500 L/hari
    
    Efektivitas:
    - Turunkan suhu: 5-10°C
    - Naikkan RH: 70-90%
    - Cocok untuk: Dataran rendah-menengah
    ```
    
    **B. Fog System (Kabut):**
    ```
    Prinsip:
    Semprotkan air halus (mist) → Evaporasi cepat → Suhu turun
    
    Komponen:
    - Pompa tekanan tinggi (60-80 bar)
    - Nozzle fog (0.2 mm)
    - Pipa high-pressure
    
    Biaya:
    - Rp 50-100 juta/1000 m²
    
    Efektivitas:
    - Turunkan suhu: 3-7°C
    - Naikkan RH: 80-95%
    - Cocok untuk: Greenhouse high-tech
    ```
    
    **C. Shading (Naungan):**
    ```
    - Shade net (50-70% shading)
    - Whitewash (kapur di atap)
    - Retractable screen (otomatis)
    
    Efektivitas:
    - Turunkan suhu: 2-5°C
    - Kurangi cahaya: 50-70%
    - Murah: Rp 50-100K/m²
    ```
    
    ---
    
    ### **2. HEATING (Pemanasan)**
    
    **Kapan Perlu Heating?**
    ```
    - Dataran tinggi (>1000 m)
    - Suhu malam <15°C
    - Tanaman sensitif dingin (tomat, paprika)
    ```
    
    **Jenis Heater:**
    
    **A. Gas Heater:**
    ```
    - Bahan bakar: LPG
    - Kapasitas: 10-50 kW
    - Biaya: Rp 10-30 juta/unit
    - Operasional: Rp 50-200K/hari (tergantung suhu)
    ```
    
    **B. Electric Heater:**
    ```
    - Listrik: 5-20 kW
    - Biaya: Rp 5-15 juta/unit
    - Operasional: Rp 100-400K/hari (mahal!)
    ```
    
    **C. Thermal Screen:**
    ```
    - Layar insulasi (buka siang, tutup malam)
    - Hemat energi: 30-50%
    - Biaya: Rp 200-400K/m²
    ```
    
    ---
    
    ## 💧 KONTROL KELEMBABAN (RH)
    
    ### **RH Optimal:**
    ```
    - Siang hari: 60-70%
    - Malam hari: 70-80%
    
    RH terlalu rendah (<50%):
    - Transpirasi berlebihan
    - Tanaman stress
    - Solusi: Fog system, evaporative cooling
    
    RH terlalu tinggi (>90%):
    - Penyakit jamur (botrytis, powdery mildew)
    - Solusi: Ventilasi, heating (malam hari)
    ```
    
    ---
    
    ## 💨 VENTILASI
    
    ### **Mengapa Ventilasi Penting?**
    ```
    - Buang panas berlebih
    - Buang kelembaban berlebih
    - Supply CO₂ segar
    - Cegah penyakit
    ```
    
    ### **Jenis Ventilasi:**
    
    **A. Natural Ventilation:**
    ```
    - Roof vent (atap buka-tutup)
    - Side vent (dinding buka-tutup)
    - Murah (no listrik)
    - Cocok untuk: Dataran tinggi, polytunnel
    ```
    
    **B. Forced Ventilation:**
    ```
    - Fan exhaust + inlet
    - Air changes: 40-60x/hour
    - Cocok untuk: Dataran rendah, greenhouse modern
    ```
    
    ---
    
    ## 🌬️ CO₂ ENRICHMENT
    
    ### **Mengapa CO₂?**
    ```
    - Atmosfer normal: 400 ppm
    - Optimal untuk fotosintesis: 800-1000 ppm
    - Yield increase: 20-30%!
    ```
    
    ### **Cara Menambah CO₂:**
    
    **A. CO₂ Generator (Bakar LPG):**
    ```
    - Produksi: 1 kg LPG = 3 kg CO₂
    - Biaya: Rp 20-50 juta/unit
    - Operasional: Rp 50-100K/hari
    ```
    
    **B. CO₂ Cylinder:**
    ```
    - Tabung CO₂ (50 kg)
    - Biaya: Rp 500K/tabung
    - Durasi: 1-2 minggu (1000 m²)
    ```
    
    **Kapan Inject CO₂?**
    ```
    - Pagi-siang (saat fotosintesis)
    - Jangan malam (no fotosintesis)
    - Tutup ventilasi (jangan buang CO₂)
    ```
    
    ---
    
    ## 🤖 AUTOMATION & SENSORS
    
    ### **Sensor:**
    ```
    - Suhu & RH: Rp 500K-2 juta
    - Cahaya (lux): Rp 1-3 juta
    - CO₂: Rp 5-15 juta
    - EC & pH: Rp 2-5 juta
    ```
    
    ### **Controller:**
    ```
    - Climate controller (PLC):
      * Input: Sensor data
      * Output: On/off fan, heater, fog, vent
      * Biaya: Rp 10-50 juta
    
    - Smartphone app (IoT):
      * Monitor real-time
      * Remote control
      * Biaya: Rp 5-20 juta
    ```
    
    ### **Keuntungan Automation:**
    ```
    ✅ Presisi tinggi (±1°C, ±5% RH)
    ✅ Hemat tenaga kerja (80-90%)
    ✅ Hemat energi (on/off sesuai kebutuhan)
    ✅ Data logging (analisis)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Bakker, J. C., et al. (1995).** Greenhouse Climate Control. Wageningen Academic Publishers.
    
    2. **Bot, G. P. A., & Van de Braak, N. J. (1995).** Physics of Greenhouse Climate. IMAG-DLO.
    
    """)

# ===== TAB 5: ANALISIS EKONOMI =====
with tab_economics:
    st.header("💰 Analisis Ekonomi Greenhouse & Hidroponik")
    
    st.markdown("""
    ## 💰 ANALISIS EKONOMI
    
    ### Contoh Kasus: Tomat Cherry Greenhouse 1000 m²
    
    **INVESTASI AWAL:**
    ```
    1. Greenhouse (Multi-Span):
       - Struktur: Rp 500 juta
       - Cooling system: Rp 45 juta
       - Automation: Rp 20 juta
    
    2. Sistem Hidroponik (Drip):
       - 2000 tanaman × Rp 140K = Rp 280 juta
    
    3. Lain-lain:
       - Instalasi listrik: Rp 20 juta
       - Tools & equipment: Rp 10 juta
    
    TOTAL INVESTASI: Rp 875 juta
    ```
    
    **BIAYA OPERASIONAL (per tahun):**
    ```
    1. Benih: 4 siklus × 2000 × Rp 2K = Rp 16 juta
    2. Nutrisi: 12 bulan × Rp 2 juta = Rp 24 juta
    3. Listrik: 12 bulan × Rp 3 juta = Rp 36 juta
    4. Tenaga kerja: 3 orang × Rp 4 juta × 12 = Rp 144 juta
    5. Maintenance: Rp 20 juta
    6. Lain-lain: Rp 10 juta
    
    TOTAL BIAYA OPERASIONAL: Rp 250 juta/tahun
    ```
    
    **PENDAPATAN:**
    ```
    - Yield: 40 kg/m²/tahun × 1000 m² = 40,000 kg
    - Harga: Rp 40,000/kg (rata-rata)
    - REVENUE: Rp 1.6 miliar/tahun
    ```
    
    **PROFIT:**
    ```
    - Revenue: Rp 1.6 miliar
    - Biaya operasional: Rp 250 juta
    - PROFIT: Rp 1.35 miliar/tahun
    
    ROI: Rp 875 juta / Rp 1.35 miliar = 0.65 tahun = 8 bulan!
    ```
    
    ---
    
    ## 📊 INTERACTIVE CALCULATOR
    
    ### Greenhouse ROI Calculator
    """)
    
    # ROI Calculator
    st.subheader("💰 Greenhouse ROI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**INVESTASI:**")
        area = st.number_input("Luas Greenhouse (m²):", min_value=100, max_value=10000, value=1000, step=100)
        greenhouse_cost = st.number_input("Biaya Greenhouse (Rp/m²):", min_value=150000, max_value=1500000, value=500000, step=50000)
        hydro_cost_per_plant = st.number_input("Biaya Hidroponik per Tanaman (Rp):", min_value=50000, max_value=300000, value=140000, step=10000)
        plants_per_m2 = st.number_input("Populasi (tanaman/m²):", min_value=1.0, max_value=10.0, value=2.0, step=0.5)
        
    with col2:
        st.markdown("**OPERASIONAL & HASIL:**")
        yield_per_m2 = st.number_input("Yield (kg/m²/tahun):", min_value=10.0, max_value=100.0, value=40.0, step=5.0)
        price_per_kg = st.number_input("Harga Jual (Rp/kg):", min_value=10000, max_value=200000, value=40000, step=5000)
        opex_percent = st.number_input("Biaya Operasional (% dari revenue):", min_value=10, max_value=50, value=15, step=5)
        
    # Calculations
    total_plants = int(area * plants_per_m2)
    greenhouse_investment = area * greenhouse_cost
    hydro_investment = total_plants * hydro_cost_per_plant
    other_investment = (greenhouse_investment + hydro_investment) * 0.1  # 10% for other costs
    total_investment = greenhouse_investment + hydro_investment + other_investment
    
    total_yield = area * yield_per_m2
    revenue = total_yield * price_per_kg
    opex = revenue * (opex_percent / 100)
    profit = revenue - opex
    roi_years = total_investment / profit if profit > 0 else 0
    roi_months = roi_years * 12
    
    # Display Results
    st.markdown("---")
    st.subheader("📊 HASIL ANALISIS:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Investasi", f"Rp {total_investment/1e9:.2f} M")
        st.metric("Populasi Tanaman", f"{total_plants:,}")
        
    with col2:
        st.metric("Revenue/Tahun", f"Rp {revenue/1e9:.2f} M")
        st.metric("Profit/Tahun", f"Rp {profit/1e9:.2f} M")
        
    with col3:
        st.metric("ROI (Tahun)", f"{roi_years:.1f} tahun")
        st.metric("ROI (Bulan)", f"{roi_months:.0f} bulan")
        
    # Profitability Assessment
    if roi_months < 12:
        st.success(f"✅ **SANGAT MENGUNTUNGKAN!** ROI hanya {roi_months:.0f} bulan!")
    elif roi_months < 24:
        st.info(f"✅ **MENGUNTUNGKAN** - ROI {roi_months:.0f} bulan (layak investasi)")
    elif roi_months < 36:
        st.warning(f"⚠️ **CUKUP MENGUNTUNGKAN** - ROI {roi_months:.0f} bulan (perlu optimasi)")
    else:
        st.error(f"❌ **KURANG MENGUNTUNGKAN** - ROI {roi_months:.0f} bulan (terlalu lama)")
    
    st.markdown("---")
    
    st.markdown("""
    ## 📚 REFERENSI
    
    1. **Nelson, P. V. (2011).** Greenhouse Operation and Management, 7th Edition. Prentice Hall.
    
    2. **Resh, H. M. (2012).** Hydroponic Food Production, 7th Edition. CRC Press.
    
    3. **Jovicich, E., et al. (2004).** Greenhouse Tomato Production. University of Florida IFAS Extension.
    
    **Disclaimer:** Hasil analisis bersifat estimasi. Untuk analisis detail, konsultasikan dengan ahli greenhouse/hidroponik.
    """)

# ===== TAB 6: MANAJEMEN 3K (SUSTAINABLE) =====
with tab_3k:
    st.header("🚀 Sustainable Greenhouse Management (3K)")
    st.markdown("""
    **Kontinuitas, Kualitas, & Kuantitas** — Kunci sukses menembus pasar modern dan ekspor dengan margin tinggi.
    """)

    # Custom CSS for 3K Dashboard
    st.markdown("""
    <style>
    .pillar-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #10b981;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .pillar-title {
        color: #065f46;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .kpi-box {
        background: #f0fdf4;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # 3K Pillars Overview
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("""<div class="pillar-card"><div class="pillar-title">🔁 Kontinuitas</div>
        Pasokan rutin tanpa putus. Menggunakan sistem <b>Batch / Staggered Planting</b> agar panen tersedia setiap minggu/bulan.</div>""", unsafe_allow_html=True)
    with col_p2:
        st.markdown("""<div class="pillar-card"><div class="pillar-title">🌟 Kualitas</div>
        Standar pasar modern (Grade A). Kontrol nutrisi presisi, IPM tanpa pestisida kimia berbahaya, dan sortasi ketat.</div>""", unsafe_allow_html=True)
    with col_p3:
        st.markdown("""<div class="pillar-card"><div class="pillar-title">📊 Kuantitas</div>
        Yield maksimal per m². Optimalisasi populasi dan efisiensi GH untuk mengejar target tonase pasar.</div>""", unsafe_allow_html=True)

    st.divider()

    # --- SECTION: RAB GREENHOUSE ---
    st.subheader("💰 Rincian RAB Greenhouse & Investasi")
    
    m_col1, m_col2 = st.columns([1, 2])
    
    with m_col1:
        st.info("Input Parameter GH Standar Modern:")
        area_3k = st.number_input("Luas Area (m²)", 100, 10000, 500, step=100, key="area_3k")
        tipe_gh_3k = st.selectbox("Tipe Struktur GH", ["Multi-Span (Galvanis)", "Venlo (Kaca/Advanced)", "Polytunnel Premium"], index=0)
        komoditas_3k = st.selectbox("Komoditas Unggulan", ["Melon Premium (Intanon)", "Tomat Cherry (Ruby)", "Selada Hidroponik (Batavia)", "Paprika Unggul"], index=0)
        
    with m_col2:
        # RAB Calculation Logic
        base_prices = {
            "Multi-Span (Galvanis)": 650000,
            "Venlo (Kaca/Advanced)": 1200000,
            "Polytunnel Premium": 350000
        }
        struct_cost = area_3k * base_prices[tipe_gh_3k]
        
        # Technology Packages (IoT, Cooling, Fertigation)
        tech_cost = area_3k * 150000 # Asumsi Rp 150rb/m2 untuk sistem otomatisasi
        irrigation_cost = area_3k * 100000 # Rp 100rb/m2 untuk Drip/NFT
        
        total_capex = struct_cost + tech_cost + irrigation_cost
        
        st.write("#### 📊 Estimasi Investasi Awal (CAPEX)")
        rab_df = pd.DataFrame({
            "Komponen": ["Struktur & Atap", "Teknologi (IoT & Cooling)", "Sistem Irigasi & Fertigasi", "Lain-lain (Tools/Listrik)"],
            "Biaya (Rp)": [struct_cost, tech_cost, irrigation_cost, total_capex * 0.05]
        })
        st.table(rab_df.style.format({"Biaya (Rp)": "Rp {:,.0f}"}))
        st.success(f"**Total Investasi: Rp {total_capex * 1.05:,.0f}**")

    st.divider()

    # --- SECTION: ROTASI TERBAIK ---
    st.subheader("🔁 Perencanaan Rotasi (Putaran Terbaik)")
    st.info("Sistem Staggered Planting: Membagi GH menjadi beberapa blok/putaran agar panen rutin harian/mingguan.")
    
    r_col1, r_col2 = st.columns(2)
    
    with r_col1:
        siklus_hari = st.slider("Lama Siklus Tanam (Hari dari Semai ke Panen)", 30, 120, 75 if "Melon" in komoditas_3k else 35)
        jumlah_blok = st.number_input("Jumlah Putaran / Blok GH", 2, 12, 4 if "Melon" in komoditas_3k else 8, help="Berapa banyak gelombang tanam")
        target_panen_minggu = st.number_input("Target Panen per Minggu (kg)", 10, 5000, 200)

    with r_col2:
        # Rotation Analysis
        interval_tanam = siklus_hari / jumlah_blok
        st.markdown(f"""
        <div class="kpi-box">
            <h3>Strategi Rotasi</h3>
            <p>Interval Tanam: <b>Setiap {interval_tanam:.1f} Hari</b></p>
            <p>Frekuensi Panen: <b>{365/interval_tanam:.0f} Kali / Tahun</b></p>
            <p>Luas per Blok: <b>{area_3k/jumlah_blok:.1f} m²</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple Visual Timeline
        timeline_data = []
        for i in range(int(jumlah_blok)):
            timeline_data.append({"Blok": f"Blok {i+1}", "Status": "Tanam", "Minggu Ke": i * (interval_tanam/7)})
        
        st.caption("Visualisasi Gelombang Tanam (Staggered):")
        fig_rot = px.bar(timeline_data, x="Minggu Ke", y="Blok", color="Blok", orientation='h', title="Timeline Rotasi 3K")
        st.plotly_chart(fig_rot, use_container_width=True)

    st.divider()

    # --- SECTION: MANAJEMEN TOTAL ---
    st.subheader("📊 Dashboard Manajemen Total (Dashboard 3K)")
    
    d_col1, d_col2, d_col3 = st.columns(3)
    
    # Simulation Data
    yield_est = (area_3k * 15) if "Melon" in komoditas_3k else (area_3k * 25) # kg per tahun
    rev_est = yield_est * (40000 if "Melon" in komoditas_3k else 20000)
    
    with d_col1:
        st.metric("Skor Kontinuitas", "95%", delta="Tinggi")
        st.caption("Pasokan konsisten ke supermarket")
    with d_col2:
        st.metric("Rasio Kualitas (Grade A)", "88%", delta="5% Up")
        st.caption("Produk memenuhi standar modern market")
    with d_col3:
        st.metric("Efisiensi Kuantitas", f"{yield_est/area_3k:.1f} kg/m²", delta="Optimal")
        st.caption("Produktivitas per unit luas")

    st.markdown("---")
    
    # Checklist Management
    with st.expander("📝 SOP Harian Manajemen 3K (Modern Market Standards)"):
        st.checkbox("1. Monitoring EC & pH (Kualitas) - Pagi & Sore")
        st.checkbox("2. Cek Logbook Rotasi (Kontinuitas) - Apakah jadwal tanam blok berikutnya sudah siap?")
        st.checkbox("3. Pengendalian Hama Preventif (Kualitas) - Gunakan Trap & Insect Net")
        st.checkbox("4. Optimalisasi Pruning (Kuantitas) - Pastikan asimilasi hanya ke buah/daun utama")
        st.checkbox("5. QC Packing (Kualitas) - Berat seragam, NO residu pestisida, Labeling")

    st.success("Sistem Manajemen 3K Aktif: Siap mensuplai pasar modern secara berkelanjutan.")

# Footer
st.markdown("---")
st.caption("AgriSensa Sustainable Greenhouse - Membangun Pertanian yang Terukur dan Berkelanjutan.")
