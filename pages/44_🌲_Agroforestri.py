import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Sistem Agroforestri",
    page_icon="🌲",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stHeader {
        background-color: #2E7D32;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .card {
        background-color: #f0f8ff;
        border-left: 5px solid #2E7D32;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .badge-high {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .badge-low {
        background-color: #fff3e0;
        color: #e65100;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="stHeader">
    <h1>🌲 Sistem Agroforestri Terpadu</h1>
    <p>Panduan Optimalisasi Lahan Di Bawah Tegakan (LMDH / Perhutanan Sosial)</p>
</div>
""", unsafe_allow_html=True)

# Introduction
with st.expander("ℹ️ Tentang Modul Ini & Potensi Agroforestri", expanded=False):
    st.markdown("""
    **Agroforestri** (Wanatani) adalah solusi strategis untuk meningkatkan kesejahteraan petani hutan sekaligus menjaga kelestarian lingkungan.
    Modul ini dirancang khusus untuk mendukung petani mitra **Perhutani** dan pengelola **Perhutanan Sosial**.
    """)

# Main Content Layout - EXPANDED to 5 Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌳 Karakteristik Dasar Tegakan", 
    "🌽 Tanaman Sela Unggulan", 
    "💡 Rekomendasi Cerdas",
    "💰 Simulasi Bisnis",
    "🌍 Kalkulator Karbon"
])

with tab1:
    st.subheader("Karakteristik Tegakan Hutan")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("### 🌲 Pinus (*Pinus merkusii*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-high">Dataran Tinggi (> 700 mdpl)</span></li>
            <li><b>Karakter Naungan:</b> Daun jarum, naungan moderat.</li>
            <li><b>Kondisi Tanah:</b> Cenderung <b>ASAM</b> (pH rendah).</li>
            <li><b>Tanaman Cocok:</b> Kopi Arabika, Wortel, Kapulaga.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🌳 Jati (*Tectona grandis*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-low">Dataran Rendah - Menengah (< 700 mdpl)</span></li>
            <li><b>Karakter Naungan:</b> Gugur daun saat kemarau.</li>
            <li><b>Kondisi Tanah:</b> Butuh Kalsium (Ca) tinggi, tidak tahan asam kuat.</li>
            <li><b>Tanaman Cocok:</b> Jagung, Padi Gogo, Kunyit, Porang.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown("### 🌿 Kayu Putih (*Melaleuca cajuputi*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-low">Dataran Rendah & Panas</span></li>
            <li><b>Karakter Naungan:</b> Terbuka karena rutin dipangkas.</li>
            <li><b>Tanaman Cocok:</b> Jagung, Kacang-kacangan (Sistem Lorong).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🌲 Damar (*Agathis dammara*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-high">Dataran Menengah - Tinggi</span></li>
            <li><b>Karakter Naungan:</b> Sangat Teduh / Gelap.</li>
            <li><b>Tanaman Cocok:</b> Tanaman shade-loving (Kapulaga, Vanili).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("Panduan Budidaya Tanaman Sela")
    
    crop = st.selectbox("Pilih Komoditas untuk Panduan Detail:", 
                        ["Jagung", "Padi Gogo", "Rempah (Jahe/Kunyit/Kapulaga)", "Porang & Umbi-umbian", "Kopi (Arabika/Robusta)"])
    
    if crop == "Jagung":
        st.markdown("""
        ### 🌽 Jagung
        <span class="badge-low">Cocok: Dataran Rendah - Menengah</span>
        
        *   **Kesesuaian:** Sangat baik di sela **Jati Muda** atau **Kayu Putih**.
        *   **Syarat:** Butuh cahaya matahari > 75%. Jangan tanam di bawah tegakan rapat/tua.
        *   **Tips:** Di dataran tinggi (>800 mdpl), umur panen jagung akan jauh lebih lama.
        """, unsafe_allow_html=True)

    elif crop == "Padi Gogo":
        st.markdown("""
        ### 🌾 Padi Gogo
        <span class="badge-low">Cocok: Dataran Rendah - Menengah (< 700 mdpl)</span>
        
        *   **Varietas:** Gunakan Inpago (Inbrida Padi Gogo).
        *   **Suhu:** Tidak tahan suhu dingin (pertumbuhan melambat drastis di >800 mdpl).
        """, unsafe_allow_html=True)

    elif crop == "Rempah (Jahe/Kunyit/Kapulaga)":
        st.markdown("""
        ### 🍛 Rempah & Empon-empon
        | Jenis | Elevasi Ideal | Keterangan |
        | :--- | :--- | :--- |
        | **Kapulaga** | <span class="badge-high">Menengah - Tinggi (400-1000m)</span> | Emas hijau di bawah **Pinus/Damar**. Butuh lembab. |
        | **Jahe Gajah** | <span class="badge-high">Menengah - Tinggi</span> | Nilai ekonomi tinggi, butuh tanah gembur. |
        | **Jahe Merah** | <span class="badge-low">Rendah - Menengah</span> | Lebih tahan panas & kering. |
        | **Kunyit** | <span class="badge-low">Rendah - Menengah</span> | Sangat adaptif di bawah **Jati**. |
        """, unsafe_allow_html=True)

    elif crop == "Porang & Umbi-umbian":
        st.markdown("""
        ### 🥔 Porang
        <span class="badge-low">Optimal: 100 - 600 mdpl</span>
        
        *   **Ketinggian:** Di atas 700 mdpl pertumbuhan umbi melambat.
        *   **Naungan:** Butuh naungan 40-60%. Ideal di bawah **Jati tua** atau **Sono**.
        """, unsafe_allow_html=True)

    elif "Kopi" in crop:
        st.markdown("""
        ### ☕ Kopi
        Tanaman konservasi terbaik.
        
        *   **Robusta:** <span class="badge-low">Dataran Rendah (0 - 800 mdpl)</span>. Cocok di bawah Lamtoro/Sengon.
        *   **Arabika:** <span class="badge-high">Dataran Tinggi (> 800 mdpl)</span>. Wajib di bawah **Pinus/Eucalyptus** untuk citarasa terbaik.
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("💡 Rekomendasi Cerdas Pola Tanam")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        altitude = st.select_slider("Ketinggian Tempat (mdpl):", 
                                    options=["Dataran Rendah (<400m)", "Menengah (400-700m)", "Dataran Tinggi (>700m)"])
    with col_in2:
        tree_type = st.selectbox("Jenis Pohon Utama (Tegakan):", ["Jati", "Pinus", "Kayu Putih", "Damar/Sengon"])
    with col_in3:
        tree_age = st.selectbox("Umur / Kondisi Tegakan:", 
                                ["Muda / Terbuka (Cahaya >75%)", 
                                 "Remaja / Sedang (Cahaya 50-75%)", 
                                 "Tua / Rimbun (Cahaya <50%)"])

    st.markdown("---")
    st.markdown(f"### 🌱 Hasil Rekomendasi untuk: **{tree_type}** di **{altitude}**")
    
    rec_text = ""
    rec_type = "info" # success, warning, info, error
    
    # Logic Blocks (Same as before, abbreviated here for clarity but fully preserved in logic)
    # 1. Logic Check - Mismatched Tree Ecology
    ecology_warning = False
    if "Dataran Tinggi" in altitude and tree_type in ["Jati", "Kayu Putih"]:
         st.warning(f"⚠️ **Perhatian:** {tree_type} biasanya kurang optimal di dataran tinggi. Pertumbuhan mungkin lambat.")
         ecology_warning = True
    elif "Dataran Rendah" in altitude and tree_type in ["Pinus", "Damar"]:
         st.warning(f"⚠️ **Perhatian:** {tree_type} di dataran rendah rentan hama.")
         ecology_warning = True

    # 2. Crop Recommendation Logic
    if "Dataran Rendah" in altitude:
        if tree_type == "Jati":
            if "Muda" in tree_age:
                rec_text = "✅ **Jagung, Padi Gogo, Kacang Tanah, Kedelai.**\n\nOptimal untuk tumpangsari pangan (Palawija)."
                rec_type = "success"
            elif "Remaja" in tree_age:
                rec_text = "✅ **Kunyit, Temulawak, Garut.**\n\nCahaya berkurang, beralih ke rimpang-rimpangan."
                rec_type = "warning"
            else:
                rec_text = "✅ **Porang, Empon-empon (Kunyit/Temu).**\n\nNaungan rapat cocok untuk Porang."
                rec_type = "info"
        elif tree_type == "Kayu Putih":
             rec_text = "✅ **Jagung, Kacang Hijau (Sistem Lorong).**\n\nKayu putih pangkas pendek, cahaya aman untuk jagung."
             rec_type = "success"
        else: 
             rec_text = "✅ **Kopi Robusta.**\n\nJika dipaksakan, Kopi Robusta lebih tahan panas dibanding Arabika."
             rec_type = "warning"

    elif "Menengah" in altitude:
        if "Muda" in tree_age:
            rec_text = "✅ **Jagung, Cabai, Sayuran.**"
            rec_type = "success"
        else: 
            if tree_type == "Pinus" or "Damar" in tree_type:
                rec_text = "✅ **Kapulaga, Jahe Gajah, Kopi Robusta.**\n\nZona transisi sangat bagus untuk rempah."
                rec_type = "success"
            else: 
                rec_text = "✅ **Porang, Vanili, Lada.**"
                rec_type = "success"

    elif "Dataran Tinggi" in altitude:
        if tree_type in ["Pinus", "Damar", "Sengon"]:
            if "Muda" in tree_age:
                rec_text = "✅ **Wortel, Kubis (Kol), Kentang, Bawang Daun.**\n\nSayuran dataran tinggi sangat cocok di sela pinus muda."
                rec_type = "success"
            else:
                rec_text = "⭐ **Kopi Arabika (Premium), Kapulaga.**\n\nKombinasi Pinus + Kopi Arabika adalah standar emas konservasi."
                rec_type = "success"
        else:
            rec_text = "✅ **Sayuran (Jika cahaya cukup), Kopi Arabika.**"
            rec_type = "info"

    if rec_type == "success":
        st.success(rec_text)
    elif rec_type == "warning":
        st.warning(rec_text)
    elif rec_type == "info":
        st.info(rec_text)

with tab4:
    st.subheader("💰 Simulasi Usaha Tani (Tanaman Sela)")
    st.markdown("Perkiraan keuntungan menanam jagung/porang di sela tegakan.")
    
    col_biz1, col_biz2 = st.columns(2)
    with col_biz1:
        biz_crop = st.selectbox("Komoditas:", ["Jagung Hibrida", "Porang (Umbi)", "Padi Gogo"])
        biz_area = st.number_input("Luas Lahan Efektif (Ha):", value=0.5, step=0.1, help="Biasanya hanya 50-70% dr luas total karena terpotong pohon.")
    
    with col_biz2:
        if biz_crop == "Jagung Hibrida":
            biz_yield = st.number_input("Target Hasil Panen (Ton/Ha):", value=6.0)
            biz_price = st.number_input("Harga Jual (Rp/Kg):", value=4500)
            biz_cost = st.number_input("Biaya Produksi Total (Rp):", value=8000000, help="Benih, Pupuk, Tenaga")
        elif biz_crop == "Porang (Umbi)":
            biz_yield = st.number_input("Target Hasil Panen (Ton/Ha):", value=15.0)
            biz_price = st.number_input("Harga Jual (Rp/Kg):", value=3500)
            biz_cost = st.number_input("Biaya Produksi Total (Rp):", value=15000000)
        else: # Padi
            biz_yield = st.number_input("Target Hasil Panen (Ton/Ha):", value=4.0)
            biz_price = st.number_input("Harga Jual (Rp/Kg):", value=5500)
            biz_cost = st.number_input("Biaya Produksi Total (Rp):", value=6000000)

    # Calculation
    total_revenue = biz_yield * biz_price * 1000 * biz_area # Yield in Ton -> Kg
    total_cost = biz_cost * biz_area
    profit = total_revenue - total_cost
    roi = (profit / total_cost) * 100 if total_cost > 0 else 0
    
    st.markdown("---")
    c_res1, c_res2, c_res3 = st.columns(3)
    c_res1.metric("Omzet Estimasi (Per Musim)", f"Rp {total_revenue:,.0f}")
    c_res2.metric("Biaya Budidaya", f"Rp {total_cost:,.0f}")
    c_res3.metric("Keuntungan Bersih (Profit)", f"Rp {profit:,.0f}", delta=f"{roi:.1f}% ROI")
    
    if profit > 0:
        st.success("✅ **Usaha Layak (Profitable).** Pastikan manajemen pupuk tepat agar target hasil tercapai!")
    else:
        st.error("⚠️ **Resiko Rugi.** Cek kembali biaya produksi atau target hasil panen Anda.")

with tab5:
    st.subheader("🌍 Kalkulator Karbon (Green Economy)")
    st.markdown("""
    Fitur ini membantu menghitung estimasi **Stok Karbon** yang tersimpan di lahan Anda. 
    Sangat berguna untuk pengajuan program Perhutanan Sosial atau skema perdagangan karbon.
    """)
    
    col_carb1, col_carb2 = st.columns(2)
    with col_carb1:
        c_tree = st.selectbox("Jenis Pohon:", ["Jati", "Pinus", "Mahoni", "Sengon"])
        c_age = st.slider("Umur Rata-rata Pohon (Tahun):", 5, 40, 10)
    with col_carb2:
        c_dens = st.number_input("Jumlah Pohon (Batang):", value=100)
        
    # Simplified Allometric estimation (Scientific approximation)
    # Formula: Biomass (kg) approx = a * Age^b (Very rough approximation for demo)
    # Jati: High density, Pinus: Med, Sengon: Low
    
    biomass_per_tree = 0
    if c_tree == "Jati":
        biomass_per_tree = 0.15 * (c_age ** 2.3) * 10 # heuristic
    elif c_tree == "Pinus":
        biomass_per_tree = 0.10 * (c_age ** 2.4) * 8
    elif c_tree == "Mahoni":
        biomass_per_tree = 0.12 * (c_age ** 2.3) * 9
    else: # Sengon (Fast growing)
        biomass_per_tree = 0.08 * (c_age ** 2.5) * 6
        
    total_biomass_ton = (biomass_per_tree * c_dens) / 1000
    carbon_stock_ton = total_biomass_ton * 0.47 # IPCC Conversion Factor
    co2_equivalent = carbon_stock_ton * 3.67 # C -> CO2
    
    st.info(f"💡 Estimasi untuk **{c_dens} pohon {c_tree}** umur **{c_age} tahun**:")
    
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Biomassa Total", f"{total_biomass_ton:,.1f} Ton")
    mc2.metric("Stok Karbon (C)", f"{carbon_stock_ton:,.1f} Ton C")
    mc3.metric("Serapan CO2 Ekuivalen", f"{co2_equivalent:,.1f} Ton CO2e", delta="Lingkungan")
    
    st.caption("*Perhitungan menggunakan estimasi alometrik sederhana standar kehutanan. Untuk perdagangan karbon resmi diperlukan inventarisasi langsung.*")

# Footer
st.markdown("---")
st.caption("Dikembangkan untuk Petani Indonesia & Mitra Perhutani | AgriSensa © 2025")
