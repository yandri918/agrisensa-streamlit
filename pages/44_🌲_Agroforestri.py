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
with st.expander("ℹ️ Tentang Modul Ini & Potensi Agroforestri", expanded=True):
    st.markdown("""
    **Agroforestri** (Wanatani) adalah solusi strategis untuk meningkatkan kesejahteraan petani hutan sekaligus menjaga kelestarian lingkungan.
    Modul ini dirancang khusus untuk mendukung petani mitra **Perhutani** dan pengelola **Perhutanan Sosial**.
    """)

# Main Content Layout
tab1, tab2, tab3 = st.tabs(["🌳 Karakteristik Dasar Tegakan", "🌽 Tanaman Sela Unggulan", "💡 Rekomendasi Cerdas"])

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
        *   **Tips:** Di dataran tinggi (>800 mdpl), umur panen jagung akan jauh lebih lama, dan resiko serangan bule (bulai) meningkat jika lembab.
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
    
    # 1. Logic Check - Mismatched Tree Ecology
    ecology_warning = False
    if "Dataran Tinggi" in altitude and tree_type in ["Jati", "Kayu Putih"]:
         st.warning(f"⚠️ **Perhatian:** {tree_type} biasanya kurang optimal di dataran tinggi yang dingin. Pertumbuhan mungkin lambat.")
         ecology_warning = True
    elif "Dataran Rendah" in altitude and tree_type in ["Pinus", "Damar"]:
         st.warning(f"⚠️ **Perhatian:** {tree_type} di dataran rendah rentan hama dan kualitas getah/kayu mungkin berbeda.")
         ecology_warning = True

    # 2. Crop Recommendation Logic
    if "Dataran Rendah" in altitude:
        # LOWLAND LOGIC
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
        else: # Pinus/Damar in Lowland
             rec_text = "✅ **Kopi Robusta.**\n\nJika dipaksakan, Kopi Robusta lebih tahan panas dibanding Arabika."
             rec_type = "warning"

    elif "Menengah" in altitude:
        # MIDLAND LOGIC (The Sweet Spot)
        if "Muda" in tree_age:
            rec_text = "✅ **Jagung, Cabai, Sayuran.**"
            rec_type = "success"
        else: # Shaded
            if tree_type == "Pinus" or "Damar" in tree_type:
                rec_text = "✅ **Kapulaga, Jahe Gajah, Kopi Robusta.**\n\nZona transisi sangat bagus untuk rempah."
                rec_type = "success"
            else: # Jati/Sengon
                rec_text = "✅ **Porang, Vanili, Lada.**"
                rec_type = "success"

    elif "Dataran Tinggi" in altitude:
        # HIGHLAND LOGIC
        if tree_type in ["Pinus", "Damar", "Sengon"]:
            if "Muda" in tree_age:
                rec_text = "✅ **Wortel, Kubis (Kol), Kentang, Bawang Daun.**\n\nSayuran dataran tinggi sangat cocok di sela pinus muda."
                rec_type = "success"
            else: # Shaded Highlander
                rec_text = "⭐ **Kopi Arabika (Premium), Kapulaga.**\n\nKombinasi Pinus + Kopi Arabika adalah standar emas konservasi (Kopi Naungan)."
                rec_type = "success"
        else:
            rec_text = "✅ **Sayuran (Jika cahaya cukup), Kopi Arabika.**"
            rec_type = "info"

    # Display Result
    if rec_type == "success":
        st.success(rec_text)
    elif rec_type == "warning":
        st.warning(rec_text)
    elif rec_type == "info":
        st.info(rec_text)
    
    st.markdown("""
    > **Tips:** Di dataran tinggi, perhatikan drainase agar akar tidak busuk. 
    > Di dataran rendah, perhatikan ketersediaan air saat kemarau.
    """)

# Footer
st.markdown("---")
st.caption("Dikembangkan untuk Petani Indonesia & Mitra Perhutani | AgriSensa © 2025")
