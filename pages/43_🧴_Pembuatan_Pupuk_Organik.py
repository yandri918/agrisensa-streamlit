import streamlit as st

st.set_page_config(
    page_title="Pembuatan Pupuk Organik - AgriSensa",
    page_icon="🧴",
    layout="wide"
)

st.title("🧴 Laboratorium Pupuk Organik")
st.markdown("**pusat Panduan Pembuatan Pupuk, Bioaktivator, dan Ramuan Organik Tanaman**")

# Tabs
tab_bio, tab_poc, tab_padat, tab_mol = st.tabs([
    "🧪 Bioaktivator & Decomposer",
    "💧 Pupuk Cair (POC)",
    "🍂 Pupuk Padat (Kompos)",
    "🦠 MOL (Mikro Organisme Lokal)"
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
                
    st.markdown("---")
    
    with st.expander("🐐 POC Rumen Kambing (By Ayah Manjel)", expanded=False):
        st.info("Resep alternatif memanfaatkan limbah rumen/usus kambing. Proses cepat (3-7 hari).")
        
        col_pk1, col_pk2 = st.columns(2)
        
        with col_pk1:
            st.markdown("#### 🥬 Bahan-Bahan")
            st.markdown("""
            1.  **Air Bersih:** 5 Liter
            2.  **Gula Kelapa:** 1 kg
            3.  **Kecambah (Tauge):** 1 kg
            4.  **Dedak:** 2 kg
            5.  **Susu Murni:** 1 Liter
            6.  **Rumen/Usus Kambing:** Bagian usus dekat perut besar (kira-kira 12 jari)
            """)
            
        with col_pk2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Sterilisasi:** Cuci wadah (ember/jerigen) dengan air panas.
            2.  **Larutan Gula & Dedak:** Seduh Gula dan Dedak dengan **Air Panas**, aduk rata, saring, dan masukkan airnya ke jerigen.
            3.  **Larutan Susu:** Haluskan/blender Kecambah, campur dengan Susu Murni, saring, dan masukkan ke jerigen.
            4.  **Rumen:** Cincang Rumen/Usus sampai halus, masukkan ke jerigen.
            5.  **Fermentasi:** Tutup rapat (anaerob).
            6.  **Perawatan:** Aduk setiap **Pagi & Sore** (buka sebentar).
            7.  **Waktu:** Cek hari ke-3. Jika harum = JADI. Biarkan maksimal **7 Hari** untuk pematangan.
            """)
            
        st.success("💉 **Dosis Aplikasi:** 250 cc per 14 Liter Air (1 Tangki).")
        st.caption("Aplikasi Pagi (06.00-09.00) atau Sore (15.00-17.00).")

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

# ===== TAB 4: M O L =====
with tab_mol:
    st.header("🦠 MOL (Mikro Organisme Lokal)")
    st.info("Kumpulan resep MOL sederhana menggunakan bahan-bahan lokal.")
    
    mol_choice = st.selectbox("Pilih Jenis MOL:", [
        "MOL Sayuran",
        "MOL Buah",
        "MOL Rebung Bambu",
        "MOL Keong Mas / Bekicot",
        "MOL Bonggol Pisang",
        "MOL Sabut Kelapa",
        "MOL Gedebok / Pelepah Pisang"
    ])
    
    if mol_choice == "MOL Sayuran":
        with st.expander("🥦 MOL Sayuran (Vegetatif)", expanded=True):
            st.markdown("**Fungsi:** Pupuk masa Vegetatif.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Sayur-sayuran (beragam, jangan busuk): 3 kg
                *   Gula Merah: 0.5 kg
                *   Garam: 150 gram
                *   Air Leri (Beras): 3 Liter
                *   Air Kelapa: 2 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Cincang halus/blender sayuran.
                2.  Campur semua bahan, kocok/aduk 3-5 menit.
                3.  Simpan dalam wadah tertutup di tempat teduh.
                4.  Fermentasi: **14 Hari**.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi 2 minggu sekali.")

    elif mol_choice == "MOL Buah":
        with st.expander("🍎 MOL Buah (Generatif)", expanded=True):
            st.markdown("**Fungsi:** Pupuk masa Generatif (Pembuahan) & BOoster Manis.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Buah matang (Pepaya, Mangga, Pisang, Tomat, Nanas, dll): 2 kg
                *   Gula Merah: 0.5 kg
                *   Air Kelapa: 5 Liter
                *   Penyedap Rasa (Opsional): 1 sdt
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Cincang halus/blender buah-buahan.
                2.  Campur semua bahan, kocok/aduk 3-5 menit.
                3.  Simpan wadah tertutup, tempat teduh.
                4.  Fermentasi: **14 Hari**.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi 2 minggu sekali.")
            st.markdown("*Tips: Tambahkan kocokan telur bebek/ayam saat aplikasi agar buah makin manis.*")

    elif mol_choice == "MOL Rebung Bambu":
        with st.expander("🎍 MOL Rebung Bambu (ZPT Gibberellin)", expanded=True):
            st.markdown("**Fungsi:** Perangsang Tumbuh (Gibberellin) & Pengurai Kompos.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Rebung Bambu: 1 kg
                *   Air Leri (Beras): 5 Liter
                *   Gula Merah: 0.5 kg
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Iris tipis atau tumbuk rebung bambu.
                2.  Masukkan ke jerigen bersama Gula Merah dan Air Leri.
                3.  Kocok hingga tercampur.
                4.  Buka tutup sebentar setiap pagi (buang gas).
                5.  Siap pakai setelah **15 Hari**.
                """)
            st.info("""
            **Dosis:**
            *   **Pengomposan:** 1 MOL : 5 Air. Siramkan ke bahan kompos.
            *   **Tanaman:** 1 MOL : 15 Air. Semprot/Kocor.
            """)

    elif mol_choice == "MOL Keong Mas / Bekicot":
        with st.expander("🐌 MOL Keong Mas (Asam Amino Plus)", expanded=True):
            st.markdown("**Fungsi:** Sumber Asam Amino & Dekomposer.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Keong Mas/Bekicot Hidup: 1 kg
                *   Buah Maja (atau Gula Merah 0.5 kg): 1/2 buah
                *   Air Kelapa: 5 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Tumbuk halus Keong Mas (cangkang + daging).
                2.  Tumbuk halus Buah Maja / Gula Merah.
                3.  Campur semua dengan Air Kelapa dalam jerigen.
                4.  Kocok rata. Buka tutup sebentar setiap pagi.
                5.  Siap pakai setelah **15 Hari**.
                """)
            st.info("""
            **Dosis:**
            *   **Pengomposan:** 1 MOL : 5 Air (Plus 1 ons Gula Merah).
            *   **Tanaman:** 1 Liter per Tangki. Semprot pagi/sore.
            """)

    elif mol_choice == "MOL Bonggol Pisang":
        with st.expander("🍌 MOL Bonggol Pisang (ZPT Sitokinin)", expanded=True):
            st.markdown("**Fungsi:** Perangsang akar & tunas (Sitokinin).")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Bonggol Pisang: 1 kg
                *   Gula Merah: 0.5 ons
                *   Air Leri (Beras): 5 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Potong kecil/tumbuk bonggol pisang.
                2.  Larutkan gula merah dengan air leri.
                3.  Campur semua dalam jerigen, tutup rapat.
                4.  Buka tutup setiap 2 hari (buang gas).
                5.  Fermentasi: **14 Hari**.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi Vegetatif (2 minggu sekali).")

    elif mol_choice == "MOL Sabut Kelapa":
        with st.expander("🥥 MOL Sabut Kelapa (Kalium Tinggi)", expanded=True):
            st.markdown("**Fungsi:** Pupuk K (Kalium) untuk pembuahan.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Sabut Kelapa
                *   Air Bersih
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Masukkan sabut kelapa ke drum (jangan penuh).
                2.  Isi air sampai semua terendam.
                3.  Tutup rapat drum.
                4.  **Biarkan 2 Minggu**.
                5.  Air berwarna coklat hitam siap dipakai.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi 2 minggu sekali.")

    elif mol_choice == "MOL Gedebok / Pelepah Pisang":
        with st.expander("🌿 MOL Gedebok Pisang (Fosfat)", expanded=True):
            st.markdown("**Fungsi:** Sumber Fosfat & Penguat batang.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Batang Pisang: 2 kg
                *   Air Nira (atau Gula Jawa 0.5 kg): 1 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Potong-potong batang pisang (jangan ditumbuk).
                2.  Campur dengan 3/4 Air Nira/Gula.
                3.  Masukkan baskom, padatkan.
                4.  Siram sisa nira di atasnya.
                5.  Tutup rapat, biarkan **2 Minggu**.
                6.  Peras airnya (MOL).
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 100 Liter Air (1:100). Semprot pagi/sore.")


