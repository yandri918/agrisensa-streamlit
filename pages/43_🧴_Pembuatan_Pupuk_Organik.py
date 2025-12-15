import streamlit as st

st.set_page_config(
    page_title="Pembuatan Pupuk Organik - AgriSensa",
    page_icon="🧴",
    layout="wide"
)

st.title("🧴 Laboratorium Pupuk Organik")
st.markdown("**pusat Panduan Pembuatan Pupuk, Bioaktivator, dan Ramuan Organik Tanaman**")

# Tabs
tab_bio, tab_poc, tab_padat = st.tabs([
    "🧪 Bioaktivator & Decomposer",
    "💧 Pupuk Cair (POC)",
    "🍂 Pupuk Padat (Kompos)"
])

# ===== TAB 1: BIOAKTIVATOR =====
with tab_bio:
    st.subheader("🧪 Bioaktivator & Decomposer")
    st.info("Bioaktivator berfungsi mempercepat proses pengomposan dan meningkatkan kesuburan tanah dengan mikroorganisme menguntungkan.")
    
    with st.expander("🐮 ROTAN (Ramuan Organik Tanaman) - Cairan Rumen Sapi", expanded=True):
        st.markdown("""
        **Bioaktivator Super (Probiotik Sempurna)** yang kaya akan mikroorganisme selulolitik dan penambat N. Sangat efektif untuk decomposer maupun pupuk dasar.
        """)
        
        col_bahan, col_cara = st.columns([1, 1.2])
        
        with col_bahan:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.warning("**Bahan Utama:**")
            st.markdown("""
            1.  **Cairan Rumen Sapi** (Isi usus halus/perasan isi usus besar) = **2 Liter**
            2.  **Molase** (Tetes Tebu/Air Gula/Air Tebu) = **2 Liter**
            3.  **Air Rebusan Dedak/Katul** = **4 Liter**
            """)
            
            st.success("**Bahan Tambahan:**")
            st.markdown("""
            1.  **Ragi Tape** = 2-3 butir
            2.  **Terasi** = ½ - 1 ons
            3.  **Buah Nanas** = 1 buah
            4.  **Urine Ternak** (Sapi/Kambing/kelinci) yg sudah diendapkan 1 minggu = **4 Liter**
            """)
            
        with col_cara:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Siapkan Air Dedak:** Campur 1 kg dedak dengan 5 liter air. Rebus hingga mendidih, dinginkan, lalu saring. Ambil airnya sebanyak **4 liter**.
            2.  **Campur Utama:** Masukkan **2 liter Cairan Rumen** dan **2 liter Molase** ke dalam wadah. Aduk rata.
            3.  **Campur Dedak:** Masukkan air rebusan dedak (4 liter) ke dalam campuran rumen dan molase tadi.
            4.  **Haluskan Tambahan:** Parut/blender **1 buah nanas** dan encerkan **Terasi** dengan sedikit air. Masukkan ke dalam wadah.
            5.  **Ragi:** Hancurkan **2-3 butir ragi tape**, masukkan.
            6.  **Urine:** Tambahkan **4 liter Urine ternak**.
            7.  **Fermentasi:** Masukkan semua larutan ke dalam jerigen/tong plastik. Tutup rapat (anaerob).
            8.  **Waktu:** Simpan selama **2 Minggu**.
            9.  **Finishing:** Jika sudah jadi, bioaktivator ini siap digunakan atau dicampur dengan ROTAN lain.
            """)
            
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("✅ **Ciri-Ciri Berhasil:**")
            st.markdown("""
            *   Berbau khas fermentasi (harum/asam segar).
            *   Berwarna kuning kecoklatan.
            *   Tidak keruh.
            *   Tidak ada jamur hitam/abu-abu (jamur putih/krem boleh).
            """)
            
        with c2:
            st.error("❌ **Ciri-Ciri Gagal:**")
            st.markdown("""
            *   Berbau busuk (seperti got/bangkai).
            *   Berwarna coklat kehitaman/keruh.
            *   Terdapat banyak jamur berwarna coklat/hitam/abu-abu.
            """)
            
        with st.chat_message("assistant"):
            st.markdown("""
            **🧬 Kandungan Mikroba Super:**
            *   **Selulolitik (Pengurai Serat):** *Bacteriodes succinogenes, Cillobacterium cellulosolvens, Lactobacillus sp.*
            *   **Hemiselulolitik:** *Butyrivibrio fibriosolven, Bacteriodes ruminicola*
            *   **Amilolitik:** *Bacteriodes amylophilus, Streptococcus bovis*
            *   **Penambat N (Penyubur N):** *Azotobacter, Azospirillum, Nitrosococcus, Nitrosomonas*
            *   **Pelarut P (Phosphate):** *Aspergillus niger, Bacillus subtilis, Bacillus polymixa, Bacillus megatherium*
            *   **ZPT (Hormon Tumbuh):** *Acetobacter sp, Actinomycetes sp*
            *   **Pembenah Tanah:** *Bacillus mojavensis* (meningkatkan kemampuan memegang air).
            
            *InsyaAllah menjadi Probiotik "SEMPURNA" untuk POC, POP, dan Decomposer.*
            """)

# ===== TAB 2: POC =====
with tab_poc:
    st.header("💧 Pupuk Organik Cair (POC)")
    st.markdown("Kumpulan resep POC kualitas tinggi (Premium)")
    
    with st.expander("🥣 POC ROTAN (Premium Quality)", expanded=True):
        st.info("POC ini memiliki kandungan mikroba lengkap: *Azotobacter sp., Azospirillium sp., Pseudomonas sp., Lactobacillus sp., Rhizobium sp., dan Streptomyces sp.*")
        
        tab_buat, tab_banyak, tab_upgrade, tab_dosis = st.tabs(["🥣 Cara Buat", "📈 Cara Memperbanyak", "🚀 Upgrade ZPT", "💉 Dosis Aplikasi"])
        
        with tab_buat:
            col_b, col_c = st.columns([1, 1.2])
            
            with col_b:
                st.markdown("#### 🥦 Bahan-Bahan")
                st.markdown("""
                1.  **Buah Pisang:** 5 buah
                2.  **Buah Pepaya:** 1 buah
                3.  **Buah Nanas:** 1 buah
                4.  **Buah Mangga:** 2 buah
                5.  **Buah Melon/Semangka:** 1 buah
                6.  **Kangkung Air:** 3 ikat
                7.  **Kacang Panjang:** 3 ikat
                8.  **Jagung Muda:** 2 buah
                9.  **Ragi:** 3 butir
                10. **Air Kelapa:** 5 Liter
                11. **Air Leri (Cucian Beras):** 3 Liter
                12. **Gula Kelapa:** 1 kg
                13. **Usus Ikan:** 2 ons
                """)
                
            with col_c:
                st.markdown("#### 🥣 Cara Pembuatan")
                st.markdown("""
                1.  **Blender Halus:** Blender bahan no 1 sampai 8 (Buah-buahan, sayuran, jagung) sampai seperti jus.
                2.  **Rebus Gula:** Didihkan gula kelapa dengan 1 liter air, biarkan sampai **benar-benar dingin**.
                3.  **Pencampuran:** Campurkan semua bahan (Jus, Gula cair dingin, Air kelapa, Air leri, Usus ikan, Ragi) menjadi satu. Aduk sampai benar-benar merata.
                4.  **Wadah:** Simpan dalam wadah **Tembikar** atau **Plastik**.
                5.  **PENTING:** Jangan gunakan wadah LOGAM.
                6.  **Fermentasi:** Tutup rapat, fermentasi selama **10-14 Hari**.
                7.  **Perawatan:** Setiap **2 hari sekali**, buka tutup dan aduk selama 5 menit, lalu tutup kembali rapat-rapat.
                """)
                
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.success("✅ **Ciri-Ciri Berhasil:**")
                st.markdown("* Campuran berbau **Asam** dan **Harum Tape**.")
                st.markdown("* Fermentasi selesai jika **sudah tidak ada gas**.")
            with c2:
                st.warning("⚠️ **Tips:**")
                st.markdown("* Saring hasil fermentasi.")
                st.markdown("* **Ampas jangan dibuang!** Masih mengandung semua mikroba super di atas.")

        with tab_banyak:
            st.subheader("📈 Cara Memperbanyak (Perbanyakan Masal)")
            st.markdown("Anda bisa membuat 100 Liter POC ROTAN dengan kualitas SAMA dari 1 Liter biang POC ROTAN.")
            
            st.markdown("#### Bahan:")
            st.markdown("""
            1.  **Air Jernih** (Sumur/Mata air): 100 Liter
            2.  **Dedak:** 10 kg
            3.  **Gula Kelapa:** 5 kg
            4.  **Air Kelapa:** 10 liter
            5.  **Biang POC ROTAN:** 1 Liter
            """)
            
            st.markdown("#### Cara Buat:")
            st.markdown("""
            1.  Panaskan/Rebus bahan **Air Jernih (sebagian), Dedak, dan Gula Kelapa**.
            2.  Setelah larut dan matang, biarkan sampai **Benar-benar Dingin**.
            3.  Campurkan dengan sisa Air Jernih, Air Kelapa, dan **1 Liter POC ROTAN**.
            4.  Masukkan ke dalam drum plastik, tutup rapat (anaerob).
            5.  Diamkan selama **7 Hari**.
            6.  **Selesai!** Anda punya 100 Liter POC ROTAN kualitas super.
            """)
            
        with tab_upgrade:
            st.subheader("🚀 Upgrade Kualitas Nomor Wahid (Plus ZPT)")
            st.markdown("Tambahkan ZPT (Zat Pengatur Tumbuh) ke dalam **100 Liter** POC ROTAN tadi sesuai fase tanaman.")
            
            col_veg, col_gen = st.columns(2)
            
            with col_veg:
                st.success("🌱 **Fase Vegetatif (Pertumbuhan)**")
                st.markdown("""
                Tambahkan:
                *   **ZPT Auxin:** 1 Liter
                *   **ZPT Sitokinin:** 1 Liter
                """)
                
            with col_gen:
                st.warning("🌺 **Fase Generatif (Pembuahan)**")
                st.markdown("""
                Tambahkan:
                *   **ZPT Sitokinin:** ½ Liter
                *   **ZPT Giberelin:** 1.5 Liter
                """)
                
        with tab_dosis:
            st.subheader("💉 Dosis Aplikasi")
            
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.info("🌾 **Tanaman Padi**")
                st.markdown("""
                *   **Dosis:** 250 ml per 14 Liter air (per tangki).
                *   **Interval:** 1 Minggu sekali.
                """)
                
            with col_d2:
                st.info("🌽 **Palawija / Sayuran**")
                st.markdown("""
                *   **Dosis:** 100 ml per 14 Liter air.
                *   **Interval:** 1 Minggu sekali.
                """)

# ===== TAB 3: PADAT =====
with tab_padat:
    st.header("🍂 Pupuk Organik Padat (Kompos/Bokashi)")
    
    with st.expander("💩 Bokashi Padat ROTAN (1 Hektar)", expanded=True):
        st.info("Resep ini mencukupi kebutuhan 16 Unsur Hara Makro & Mikro untuk lahan 1 Hektar.")
        
        col_pb, col_pc = st.columns(2)
        
        with col_pb:
            st.markdown("#### 🧱 Bahan-Bahan")
            st.markdown("""
            1.  **Kohe Domba/Kambing:** 1 Ton
            2.  **Dolomit (Kapur Pertanian):** 100 kg
            3.  **Dedak/Katul:** 50 kg
            4.  **Sekam Padi:** 300 kg
            5.  **Jerami Padi:** 1 Ton
            6.  **Bioaktivator ROTAN:** 4 Liter
            7.  **Air Kelapa:** Secukupnya (untuk kelembaban)
            """)
            
        with col_pc:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Pencampuran:** Campur semua bahan padat (Kohe, Dolomit, Dedak, Sekam, Jerami (cacah)) hingga merata.
            2.  **Larutan:** Campurkan 4 Liter Bioaktivator ROTAN dengan Air Kelapa secukupnya.
            3.  **Penyiraman:** Siramkan larutan ke tumpukan bahan padat sambil diaduk.
            4.  **Kelembaban:** Pastikan kelembaban sekitar **30-40%** (Mamel: Bila digenggam menggumpal, bila disentuh hancur, tidak meneteskan air).
            5.  **Fermentasi:** Tutup tumpukan dengan terpal.
            6.  **Waktu:** Fermentasi selama **5 - 7 Hari**.
            7.  **Panen:** Pupuk siap digunakan jika suhu sudah turun/dingin dan berbau harum fermentasi.
            """)
