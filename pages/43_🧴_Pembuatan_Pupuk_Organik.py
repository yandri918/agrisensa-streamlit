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
    st.info("Pilih menu resep di bawah ini (Akan segera ditambahkan).")
    # Placeholder for future POC recipes

# ===== TAB 3: PADAT =====
with tab_padat:
    st.header("🍂 Pupuk Organik Padat (Kompos)")
    st.info("Pilih menu resep di bawah ini (Akan segera ditambahkan).")
    # Placeholder for future Solid Fertilizer recipes
