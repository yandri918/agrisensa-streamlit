import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="Agrowisata Petik Langsung",
    page_icon="🍓",
    layout="wide"
)

# Header
st.title("🍓 Agrowisata Petik Langsung Premium")
st.markdown("""
**Transformasi Lahan Menjadi Destinasi Wisata!**
Modul ini membantu Anda merencanakan kebun buah komersial dengan konsep *"Pick Your Own"* (Petik Sendiri).
Fokus pada komoditas bernilai tinggi dan *Instagrammable*: **Strawberry, Anggur Import, dan Melon Premium.**
""")

st.markdown("---")

# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Analisis Lokasi",
    "🍇 Panduan Tanaman", 
    "💰 Kalkulator Bisnis",
    "📸 Desain Visual"
])

# --- TAB 1: ANALISIS LOKASI ---
with tab1:
    st.header("📍 Cek Kesesuaian Lokasi")
    st.caption("Tanaman premium butuh iklim yang spesifik. Jangan memaksakan tanaman di lokasi yang salah!")
    
    col_loc1, col_loc2 = st.columns([1, 2])
    
    with col_loc1:
        altitude = st.number_input("Ketinggian Lokasi (mdpl)", 0, 3000, 500, step=50, help="Meter di atas permukaan laut")
        temp_avg = st.slider("Rata-rata Suhu Harian (°C)", 10, 40, 25)
        
    with col_loc2:
        st.subheader("📋 Rekomendasi Komoditas")
        
        # Logic Analisis
        if altitude >= 1000:
            st.success("✅ **Sangat Cocok untuk STRAWBERRY!**")
            st.info("Suhu dingin memacu rasa manis dan warna merah merona.")
            st.warning("⚠️ Kurang cocok untuk Melon/Anggur (kecuali pakai Green House dengan pemanas/UV filter yang sangat baik untuk menjaga suhu).")
            rec_crop = "Strawberry"
        elif 500 <= altitude < 1000:
            st.success("✅ **Zona Transisi: Bisa Semua (Dengan Catatan)**")
            st.markdown("""
            - **Strawberry:** Bisa, tapi varietas panas (Mencir/California). Rasa mungkin sedikit asam.
            - **Anggur:** Cukup bagus.
            - **Melon:** Sangat bagus.
            """)
            rec_crop = "Anggur / Melon"
        else: # < 500 mdpl (Dataran Rendah)
            st.success("✅ **Surga untuk ANGGUR & MELON!**")
            st.info("Suhu panas membuat gula buah maksimal (Brix tinggi).")
            st.error("⛔ **JANGAN tanam Strawberry!** Buah akan kecil, masam, dan tanaman mudah mati kepanasan.")
            rec_crop = "Anggur / Melon"

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

# --- TAB 3: KALKULATOR BISNIS ---
with tab3:
    st.header("💰 Kalkulator Potensi Bisnis")
    st.info("Agrowisata punya 2 sumber uang: **Tiket Masuk (Experience)** & **Penjualan Buah (Product)**.")
    
    # Inputs
    col_biz1, col_biz2 = st.columns(2)
    
    with col_biz1:
        st.markdown("### 🎟️ Pendapatan Tiket")
        htm_price = st.number_input("Harga Tiket Masuk (Rp)", 0, 100000, 15000, step=1000)
        visitors_week = st.number_input("Target Pengunjung per Minggu", 0, 5000, 200)
        
    with col_biz2:
        st.markdown("### 🧺 Pendapatan Buah")
        avg_spend_kg = st.number_input("Rata-rata Belanja Buah per Orang (kg)", 0.0, 5.0, 0.5)
        fruit_price = st.number_input("Harga Jual Petik (Rp/kg)", 10000, 200000, 80000, help="Biasanya 2x lipat harga pasar")
        
    # Calculations per Month
    visitors_month = visitors_week * 4
    
    revenue_ticket = visitors_month * htm_price
    revenue_fruit = visitors_month * avg_spend_kg * fruit_price
    total_revenue = revenue_ticket + revenue_fruit
    
    # Display Results
    st.markdown("---")
    st.subheader("📊 Estimasi Omzet Bulanan")
    
    met1, met2, met3 = st.columns(3)
    with met1:
        st.metric("Total Omzet", f"Rp {total_revenue:,.0f}")
    with met2:
        st.metric("Dari Tiket", f"Rp {revenue_ticket:,.0f}", f"{(revenue_ticket/total_revenue)*100:.1f}%")
    with met3:
        st.metric("Dari Buah", f"Rp {revenue_fruit:,.0f}", f"{(revenue_fruit/total_revenue)*100:.1f}%")
        
    st.progress(revenue_ticket/total_revenue)
    st.caption("Bar: Proporsi Pendapatan Tiket vs Buah")
    
    if revenue_ticket > revenue_fruit:
        st.info("💡 **Insight:** Bisnis Anda didominasi **Jasa Wisata**. Fokus pada fasilitas (toilet, spot foto, kenyamanan) agar orang betah.")
    else:
        st.info("💡 **Insight:** Bisnis Anda didominasi **Penjualan Produk**. Fokus pada kualitas & rasa buah agar orang beli banyak.")

# --- TAB 4: DESAIN VISUAL ---
with tab4:
    st.header("📸 Konsep Visual & Fasilitas")
    st.markdown("""
    Agar viral dan menarik pengunjung, kebun TIDAK BOLEH hanya sekedar kebun. Harus ada unsur **Estetika**.
    
    ### 1. Spot Wajib "Instagrammable"
    - **Lorong Anggur (Grape Tunnel):** Buat para-para berbentuk melengkung (tunnel). Saat berbuah, pengunjung berjalan di bawah ribuan buah anggur yang menggantung.
    - **Pyramid Strawberry:** Susun polybag strawberry mengerucut ke atas seperti piramida/tumpeng. Hemat tempat & cantik.
    - **Melon Catwalk:** Barisan melon kiri-kanan yang rapi, lantai dialasi *Weedmat* hitam atau batu koral putih agar bersih (tidak becek).
    
    ### 2. Fasilitas Pendukung (Crucial!)
    - **Topi Caping Lukis:** Sediakan topi caping warna-warni gratis dipinjam untuk properti foto.
    - **Keranjang Rotan:** Jangan pakai kantong kresek! Pakai keranjang rotan estetik untuk wadah petik.
    - **Hanging Tag:** Beri label nama varietas di pohon (misal: "Jupiter - Rasa Mangga") agar pengunjung belajar.
    
    ### 3. Layout Kebun
    - Jangan tanam terlalu rapat. Beri jarak antar bedengan minimal **1 - 1.5 meter** agar pengunjung leluasa selfie tanpa merusak tanaman.
    """)

# Footer
st.markdown("---")
st.caption("(c) 2025 AgriSensa - Modul Agrowisata Petik Langsung")
