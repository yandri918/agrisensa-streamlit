
import streamlit as st
import pandas as pd
import random

# Page Config
st.set_page_config(
    page_title="Ruang Kerja PPL",
    page_icon="📢",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .card-ppl {
        background-color: #f0f9ff;
        border-left: 5px solid #0284c7;
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .metric-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #1e3a8a; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>📢 Ruang Kerja PPL</h1><p>Sistem Pendukung Keputusan Petugas Penyuluh Lapangan</p></div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🌾 Kalkulator Ubinan Digital", "📋 Simulator Kuota Pupuk (e-RDKK)", "📢 Generator Materi Penyuluhan"])

# --- TAB 1: UBINAN ---
with tab1:
    st.markdown("### 🌾 Kalkulator Ubinan Digital")
    st.info("Alat bantu hitung cepat estimasi produktivitas panen di lapangan.")
    
    col_u1, col_u2 = st.columns(2)
    
    with col_u1:
        st.subheader("📝 Input Lapangan")
        panjang = st.number_input("Panjang Ubinan (m)", value=2.5, step=0.1)
        lebar = st.number_input("Lebar Ubinan (m)", value=2.5, step=0.1)
        berat_ubin = st.number_input("Berat Gabah (GKP) per Ubinan (Kg)", value=6.0, step=0.1, help="Berat bersih setelah dikurangi tarra.")
        jml_rumpun = st.number_input("Jumlah Rumpun dalam Ubinan", value=120, step=10, help="Untuk menghitung populasi per Ha.")
        
    with col_u2:
        st.subheader("📊 Hasil Analisa")
        
        # Logic
        luas_ubin = panjang * lebar
        faktor_konversi = 10000 / luas_ubin
        hasil_gkp_ha = (berat_ubin * faktor_konversi) / 1000 # Ton/Ha
        
        # Konversi BPS
        hasil_gkg = hasil_gkp_ha * 0.8602
        hasil_beras = hasil_gkg * 0.6402
        populasi_ha = jml_rumpun * faktor_konversi
        
        m1, m2 = st.columns(2)
        m1.markdown(f"""<div class="metric-box"><h3>{hasil_gkp_ha:,.2f} Ton/Ha</h3><p>Estimasi GKP</p></div>""", unsafe_allow_html=True)
        m2.markdown(f"""<div class="metric-box"><h3>{hasil_beras:,.2f} Ton/Ha</h3><p>Estimasi Beras</p></div>""", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="card-ppl">
            <b>Detail Teknis:</b><br>
            • Faktor Konversi: {faktor_konversi:,.0f}x<br>
            • Populasi: {populasi_ha:,.0f} rumpun/Ha<br>
            • GKG (Giling): {hasil_gkg:,.2f} Ton/Ha
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: E-RDKK ---
with tab2:
    st.markdown("### 📋 Cek Kuota Pupuk Subsidi (Simulasi)")
    st.info("Berdasarkan aturan Permentan (Maksimal 2 Ha per NIK).")
    
    col_r1, col_r2 = st.columns([1, 2])
    
    with col_r1:
        luas_lahan = st.number_input("Luas Lahan (Ha)", value=1.0, max_value=10.0, step=0.1)
        komoditas = st.selectbox("Komoditas Prioritas", 
                                 ["Padi", "Jagung", "Kedelai", "Cabai", "Bawang Merah", "Bawang Putih", "Tebu Rakyat", "Kopi", "Kakao"])
        mt = st.selectbox("Musim Tanam", ["MT 1", "MT 2", "MT 3"])
        
    with col_r2:
        # Rules logic (simplified quota)
        # Ref: Standar Teknis (Example values)
        quota_ref = {
            "Padi": {"urea": 200, "npk": 250}, # kg/ha
            "Jagung": {"urea": 250, "npk": 300},
            "Kedelai": {"urea": 50, "npk": 150},
            "Cabai": {"urea": 200, "npk": 200},
             # Fallback
        }
        ref = quota_ref.get(komoditas, {"urea": 150, "npk": 150})
        
        # Capping 2 Ha
        luas_valid = min(luas_lahan, 2.0)
        is_capped = luas_lahan > 2.0
        
        quota_urea = ref['urea'] * luas_valid
        quota_npk = ref['npk'] * luas_valid
        
        if is_capped:
            st.warning(f"⚠️ **Perhatian:** Input {luas_lahan} Ha melebihi batas subsidi. Perhitungan otomatis dibatasi max 2.0 Ha.")
        
        st.success(f"✅ **Alokasi Subsidi untuk {komoditas} ({mt}):**")
        
        q1, q2 = st.columns(2)
        q1.metric("UREA (Subsidi)", f"{quota_urea:,.0f} Kg")
        q2.metric("NPK FORMULA (Subsidi)", f"{quota_npk:,.0f} Kg")
        
        st.caption("*Angka ini adalah simulasi sesuai rekomendasi teknis umum. Realisasi tergantung e-Alokasi daerah.*")

# --- TAB 3: MATERI PENYULUHAN ---
with tab3:
    st.markdown("### 📢 Generator Materi Penyuluhan Instan")
    st.markdown("Buat outline materi penyuluhan dalam hitungan detik untuk pertemuan poktan.")
    
    topik = st.text_input("Topik Penyuluhan:", placeholder="Contoh: Pengendalian Hama Wereng Batang Coklat")
    audiens = st.selectbox("Target Audiens:", ["Kelompok Tani Pemula", "Kelompok Tani Lanjut/Madya", "Petani Milenial"])
    
    if st.button("🤖 Buat Materi"):
        if topik:
            st.markdown("---")
            st.markdown(f"#### 🎙️ Modul Penyuluhan: {topik}")
            st.caption(f"Audiens: {audiens}")
            
            # Simple Templating logic
            intro_style = "Santai & Motivasi" if "Pemula" in audiens else "Teknis & Data"
            
            st.markdown(f"""
            **1. Pembukaan ({intro_style})**
            - Salam & Apersepsi: Tanyakan kabar lahan bapak/ibu.
            - "Bapak/Ibu sekalian, hari ini kita bahas masalah {topik} yang sedang hangat."
            
            **2. Isi Materi (Poin Kunci)**
            - **Identifikasi Masalah**: Ciri-ciri serangan/kendala di lapangan.
            - **Solusi Praktis**: Langkah 1, 2, 3 yang bisa dikerjakan besok.
            - **Analisa Biaya**: Tekankan efisiensi biaya vs hasil.
            
            **3. Sesi Diskusi**
            - Pancing pertanyaan: "Siapa yang lahannya sudah kena?"
            - Beri hadiah kecil untuk penanya aktif.
            
            **4. Kesimpulan & Rencana Tindak Lanjut**
            - Sepakati jadwal praktek lapangan minggu depan.
            - Salam penutup & yel-yel pertanian.
            """)
            
            st.info("💡 **Tips PPL:** Gunakan bahasa daerah setempat agar lebih mengena!")
        else:
            st.error("Mohon isi topik penyuluhan terlebih dulu.")

# Footer
st.markdown("---")
st.caption("Agrisensa PPL Tools v1.0 - Dedikasi untuk Pahlawan Pangan Indonesia 🇮🇩")
