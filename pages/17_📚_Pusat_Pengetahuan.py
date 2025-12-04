# Pusat Pengetahuan Pertanian
# Ensiklopedia lengkap nutrisi tanaman, pupuk, dan pengendalian hama alami

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Pusat Pengetahuan", page_icon="📚", layout="wide")

# ========== KNOWLEDGE DATABASE ==========

# PUPUK MAKRO
PUPUK_MAKRO = {
    "Urea (46% N)": {
        "kandungan": {"N": 46, "P": 0, "K": 0},
        "fungsi": "Pertumbuhan vegetatif (daun, batang)",
        "dosis": "200-300 kg/ha untuk padi, 250-350 kg/ha untuk jagung",
        "cara_aplikasi": "Tabur/kocor, 2-3 kali aplikasi",
        "waktu_aplikasi": "7-10 HST, 21-25 HST, 35-40 HST",
        "kelebihan": ["Kadar N tinggi", "Mudah larut", "Harga terjangkau"],
        "kekurangan": ["Mudah menguap", "Perlu aplikasi bertahap", "Dapat menurunkan pH tanah"],
        "tips": "Aplikasi pagi/sore, hindari siang hari. Campur dengan tanah untuk mengurangi penguapan."
    },
    "ZA (21% N, 24% S)": {
        "kandungan": {"N": 21, "P": 0, "K": 0, "S": 24},
        "fungsi": "Pertumbuhan + tambahan Sulfur",
        "dosis": "100-200 kg/ha",
        "cara_aplikasi": "Tabur/kocor",
        "waktu_aplikasi": "Fase vegetatif",
        "kelebihan": ["Mengandung S", "Tidak mudah menguap", "Cocok untuk tanah alkalin"],
        "kekurangan": ["Kadar N lebih rendah", "Dapat menurunkan pH"],
        "tips": "Baik untuk tanaman yang butuh sulfur (bawang, kubis)"
    },
    "SP-36 (36% P2O5)": {
        "kandungan": {"N": 0, "P": 36, "K": 0},
        "fungsi": "Pertumbuhan akar, bunga, buah",
        "dosis": "100-150 kg/ha",
        "cara_aplikasi": "Tabur saat tanam, kocor saat berbunga",
        "waktu_aplikasi": "Saat tanam + fase generatif",
        "kelebihan": ["Kadar P tinggi", "Efek jangka panjang", "Merangsang pembungaan"],
        "kekurangan": ["Tidak larut air", "Perlu waktu untuk tersedia"],
        "tips": "Aplikasi saat tanam untuk hasil maksimal. Campur dengan pupuk kandang."
    },
    "TSP (46% P2O5)": {
        "kandungan": {"N": 0, "P": 46, "K": 0},
        "fungsi": "Pertumbuhan akar dan buah",
        "dosis": "75-125 kg/ha",
        "cara_aplikasi": "Tabur saat tanam",
        "waktu_aplikasi": "Saat tanam",
        "kelebihan": ["Kadar P sangat tinggi", "Efisien"],
        "kekurangan": ["Harga lebih mahal", "Tidak larut air"],
        "tips": "Lebih efisien dari SP-36, cocok untuk lahan intensif"
    },
    "KCl (60% K2O)": {
        "kandungan": {"N": 0, "P": 0, "K": 60},
        "fungsi": "Kualitas hasil, ketahanan penyakit",
        "dosis": "100-200 kg/ha",
        "cara_aplikasi": "Tabur/kocor",
        "waktu_aplikasi": "Fase generatif",
        "kelebihan": ["Kadar K tinggi", "Mudah larut", "Meningkatkan kualitas"],
        "kekurangan": ["Mengandung Cl (tidak cocok untuk tembakau)"],
        "tips": "Aplikasi saat pembentukan buah untuk kualitas optimal"
    },
    "NPK 15-15-15": {
        "kandungan": {"N": 15, "P": 15, "K": 15},
        "fungsi": "Nutrisi seimbang untuk semua fase",
        "dosis": "200-400 kg/ha",
        "cara_aplikasi": "Tabur/kocor, 2-3 kali",
        "waktu_aplikasi": "Sepanjang musim tanam",
        "kelebihan": ["Praktis", "Seimbang", "Cocok untuk semua tanaman"],
        "kekurangan": ["Kurang spesifik", "Harga lebih mahal"],
        "tips": "Cocok untuk petani pemula, aplikasi mudah"
    },
    "NPK 16-16-16 (Phonska)": {
        "kandungan": {"N": 16, "P": 16, "K": 16},
        "fungsi": "Nutrisi lengkap untuk tanaman pangan",
        "dosis": "250-350 kg/ha",
        "cara_aplikasi": "Tabur, 2-3 kali",
        "waktu_aplikasi": "10 HST, 25 HST, 40 HST",
        "kelebihan": ["Subsidi pemerintah", "Lengkap", "Terjangkau"],
        "kekurangan": ["Stok terbatas", "Perlu kartu tani"],
        "tips": "Pupuk subsidi terbaik untuk padi dan palawija"
    }
}

# PUPUK MIKRO
PUPUK_MIKRO = {
    "Boron (B)": {
        "fungsi": "Pembentukan bunga, buah, dan biji",
        "defisiensi": "Bunga rontok, buah kecil, pertumbuhan terhambat",
        "sumber": "Borax, Asam borat",
        "dosis": "0.5-1 kg/ha atau 2-3 g/L (semprot)",
        "tanaman_peka": ["Kubis", "Brokoli", "Apel", "Anggur"],
        "tips": "Sangat penting untuk tanaman buah dan sayuran"
    },
    "Zinc (Zn)": {
        "fungsi": "Pembentukan klorofil, hormon pertumbuhan",
        "defisiensi": "Daun kecil, klorosis, pertumbuhan kerdil",
        "sumber": "ZnSO4 (Zinc Sulfat)",
        "dosis": "5-10 kg/ha atau 2-3 g/L (semprot)",
        "tanaman_peka": ["Padi", "Jagung", "Kedelai"],
        "tips": "Penting untuk tanah alkalin dan berpasir"
    },
    "Mangan (Mn)": {
        "fungsi": "Fotosintesis, metabolisme nitrogen",
        "defisiensi": "Klorosis interveinal, bercak nekrotik",
        "sumber": "MnSO4 (Mangan Sulfat)",
        "dosis": "2-5 kg/ha atau 1-2 g/L (semprot)",
        "tanaman_peka": ["Kedelai", "Gandum", "Kentang"],
        "tips": "Defisiensi umum pada tanah alkalin"
    },
    "Tembaga (Cu)": {
        "fungsi": "Fotosintesis, pembentukan protein",
        "defisiensi": "Daun layu, ujung daun mati",
        "sumber": "CuSO4 (Tembaga Sulfat)",
        "dosis": "2-5 kg/ha atau 0.5-1 g/L (semprot)",
        "tanaman_peka": ["Jeruk", "Tomat", "Gandum"],
        "tips": "Hati-hati overdosis, bersifat toksik"
    },
    "Besi (Fe)": {
        "fungsi": "Pembentukan klorofil",
        "defisiensi": "Klorosis pada daun muda",
        "sumber": "FeSO4, Fe-EDTA",
        "dosis": "5-10 kg/ha atau 2-3 g/L (semprot)",
        "tanaman_peka": ["Padi", "Kedelai", "Buah-buahan"],
        "tips": "Gunakan Fe-EDTA untuk tanah alkalin"
    },
    "Molibdenum (Mo)": {
        "fungsi": "Fiksasi nitrogen, metabolisme N",
        "defisiensi": "Daun kuning, pertumbuhan terhambat",
        "sumber": "Sodium molybdate",
        "dosis": "0.1-0.5 kg/ha",
        "tanaman_peka": ["Kedelai", "Kacang-kacangan", "Kubis"],
        "tips": "Penting untuk legum dan tanah asam"
    }
}

# PUPUK ORGANIK & HAYATI
PUPUK_ORGANIK = {
    "Kompos": {
        "kandungan": "N: 1-2%, P: 0.5-1%, K: 1-2%, C-Organik: 15-25%",
        "fungsi": "Memperbaiki struktur tanah, meningkatkan mikroba",
        "dosis": "5-10 ton/ha",
        "cara_buat": [
            "1. Kumpulkan bahan organik (jerami, daun, kotoran)",
            "2. Cacah bahan ukuran 2-5 cm",
            "3. Susun berlapis, siram EM4/MOL",
            "4. Tutup dengan terpal, balik setiap minggu",
            "5. Matang 4-6 minggu (warna hitam, tidak bau)"
        ],
        "kelebihan": ["Murah", "Ramah lingkungan", "Memperbaiki tanah jangka panjang"],
        "tips": "Campurkan berbagai bahan untuk kompos berkualitas"
    },
    "Pupuk Kandang": {
        "jenis": {
            "Ayam": "N: 3%, P: 2%, K: 1.5% (paling kaya nutrisi)",
            "Sapi": "N: 2%, P: 1%, K: 1.5% (paling aman)",
            "Kambing": "N: 2.5%, P: 1.5%, K: 2% (cocok untuk sayuran)"
        },
        "dosis": "10-20 ton/ha",
        "cara_aplikasi": "Fermentasi 2-4 minggu, tabur saat olah tanah",
        "kelebihan": ["Nutrisi lengkap", "Memperbaiki struktur tanah"],
        "tips": "Harus difermentasi dulu, jangan gunakan segar!"
    },
    "Kascing (Vermikompos)": {
        "kandungan": "N: 2%, P: 1.5%, K: 1.5%, Hormon pertumbuhan",
        "fungsi": "Nutrisi + hormon + mikroba menguntungkan",
        "dosis": "2-5 ton/ha",
        "cara_buat": [
            "1. Siapkan cacing tanah (Lumbricus rubellus)",
            "2. Buat media dari kotoran ternak + jerami",
            "3. Masukkan cacing, tutup dengan karung basah",
            "4. Siram setiap 2 hari",
            "5. Panen setelah 1-2 bulan"
        ],
        "kelebihan": ["Kualitas tinggi", "Mengandung hormon", "Mikroba aktif"],
        "tips": "Kascing adalah pupuk organik terbaik!"
    },
    "Biochar (Arang Hayati)": {
        "fungsi": "Meningkatkan retensi air dan nutrisi",
        "dosis": "1-3 ton/ha",
        "cara_buat": "Bakar biomassa dengan oksigen terbatas",
        "kelebihan": ["Efek jangka panjang (>100 tahun)", "Sekuestrasi karbon"],
        "tips": "Campur dengan kompos sebelum aplikasi"
    },
    "Pupuk Hijau": {
        "tanaman": ["Kacang-kacangan", "Orok-orok", "Mucuna"],
        "fungsi": "Fiksasi N, biomassa organik",
        "cara_aplikasi": "Tanam → Potong saat berbunga → Benamkan ke tanah",
        "kelebihan": ["Gratis", "Fiksasi N alami", "Memperbaiki tanah"],
        "tips": "Ideal untuk rotasi tanaman"
    }
}

# POC, MOL & ZPT
POC_MOL_ZPT = {
    "POC (Pupuk Organik Cair)": {
        "bahan": "Kotoran ternak, urine, daun-daunan",
        "cara_buat": [
            "1. Campurkan kotoran + air (1:3)",
            "2. Tambahkan gula merah 1 kg/20L",
            "3. Tambahkan EM4 atau MOL",
            "4. Tutup rapat, buka setiap 3 hari",
            "5. Fermentasi 14 hari"
        ],
        "dosis": "5-10 L/ha (diencerkan 1:10)",
        "aplikasi": "Semprot daun atau kocor",
        "kelebihan": ["Cepat diserap", "Mudah dibuat", "Murah"],
        "tips": "Aplikasi pagi/sore untuk hasil maksimal"
    },
    "MOL (Mikroorganisme Lokal)": {
        "jenis": {
            "MOL Bonggol Pisang": {
                "bahan": "Bonggol pisang, gula merah, air",
                "fungsi": "Hormon pertumbuhan (auksin, giberelin)",
                "cara": "Cacah bonggol + gula + air, fermentasi 7-14 hari"
            },
            "MOL Rebung Bambu": {
                "bahan": "Rebung bambu, gula merah, air",
                "fungsi": "Pertumbuhan tunas dan akar",
                "cara": "Cacah rebung + gula + air, fermentasi 7 hari"
            },
            "MOL Buah-buahan": {
                "bahan": "Buah busuk, gula, air",
                "fungsi": "Mikroba pengurai, nutrisi",
                "cara": "Hancurkan buah + gula + air, fermentasi 14 hari"
            }
        },
        "dosis": "100-200 ml/L air",
        "aplikasi": "Semprot/kocor setiap 7-10 hari",
        "tips": "MOL bonggol pisang terbaik untuk pertumbuhan!"
    },
    "ZPT Alami (Zat Pengatur Tumbuh)": {
        "Air Kelapa": {
            "kandungan": "Sitokinin, auksin, giberelin",
            "fungsi": "Pertumbuhan akar, tunas, buah",
            "dosis": "100-200 ml/L air",
            "aplikasi": "Rendam benih, semprot tanaman muda"
        },
        "Bawang Merah": {
            "kandungan": "Auksin, vitamin B1",
            "fungsi": "Perakaran kuat",
            "cara": "Haluskan 250g bawang + 1L air, saring",
            "aplikasi": "Rendam stek/benih 30 menit"
        },
        "Kecambah Kacang Hijau": {
            "kandungan": "Giberelin tinggi",
            "fungsi": "Pertumbuhan tinggi, pembungaan",
            "cara": "Haluskan kecambah + air, saring",
            "aplikasi": "Semprot saat fase vegetatif"
        }
    }
}

# PESTISIDA NABATI
PESTISIDA_NABATI = {
    "Ekstrak Daun Mimba (Neem)": {
        "target": ["Ulat", "Kutu daun", "Thrips", "Tungau"],
        "bahan_aktif": "Azadirachtin",
        "cara_buat": [
            "1. Tumbuk 1 kg daun mimba segar",
            "2. Rendam dalam 10 L air + 10 ml detergen",
            "3. Diamkan 24 jam, aduk sesekali",
            "4. Saring, siap digunakan"
        ],
        "dosis": "Semprot langsung (tidak perlu diencerkan)",
        "interval": "Setiap 5-7 hari",
        "kelebihan": ["Sistemik", "Aman untuk manusia", "Efek jangka panjang"],
        "tips": "Aplikasi sore hari, mimba sangat efektif!"
    },
    "Ekstrak Bawang Putih": {
        "target": ["Bakteri", "Jamur", "Serangga penghisap"],
        "bahan_aktif": "Allicin (antibakteri kuat)",
        "cara_buat": [
            "1. Haluskan 500g bawang putih",
            "2. Rendam dalam 10 L air + 50 ml minyak goreng",
            "3. Diamkan 24 jam",
            "4. Saring, encerkan 1:5"
        ],
        "dosis": "Semprot 1:5 dengan air",
        "interval": "Setiap 3-5 hari",
        "kelebihan": ["Antibakteri kuat", "Antijamur", "Mudah didapat"],
        "tips": "Kombinasi dengan cabai untuk efek maksimal"
    },
    "Ekstrak Cabai Rawit": {
        "target": ["Ulat", "Belalang", "Kutu daun"],
        "bahan_aktif": "Capsaicin (iritan kuat)",
        "cara_buat": [
            "1. Haluskan 500g cabai rawit",
            "2. Rebus dengan 5 L air selama 30 menit",
            "3. Dinginkan, saring",
            "4. Tambahkan 50 ml detergen"
        ],
        "dosis": "Encerkan 1:3 dengan air",
        "interval": "Setiap 5 hari",
        "kelebihan": ["Efek repellent kuat", "Murah", "Mudah dibuat"],
        "tips": "Gunakan sarung tangan saat membuat!"
    },
    "Ekstrak Tembakau": {
        "target": ["Ulat", "Kutu", "Thrips"],
        "bahan_aktif": "Nikotin",
        "cara_buat": [
            "1. Rendam 200g tembakau kering dalam 5 L air",
            "2. Diamkan 48 jam",
            "3. Saring, tambahkan detergen"
        ],
        "dosis": "Encerkan 1:2",
        "interval": "Setiap 7 hari",
        "kelebihan": ["Sangat efektif", "Kontak dan sistemik"],
        "peringatan": "⚠️ Beracun! Gunakan APD, jangan untuk sayuran menjelang panen"
    },
    "Pestisida Nabati Kombinasi (Super Formula)": {
        "target": "Hama & penyakit umum",
        "bahan": [
            "500g daun mimba",
            "250g bawang putih",
            "250g cabai rawit",
            "100g lengkuas",
            "100g jahe",
            "50 ml minyak goreng",
            "50 ml detergen",
            "10 L air"
        ],
        "cara_buat": [
            "1. Haluskan semua bahan (kecuali air, minyak, detergen)",
            "2. Rendam dalam air 24 jam",
            "3. Saring, tambahkan minyak + detergen",
            "4. Aduk rata"
        ],
        "dosis": "Encerkan 1:3",
        "interval": "Setiap 5-7 hari",
        "kelebihan": ["Spektrum luas", "Sangat efektif", "Tahan lama"],
        "tips": "Formula terbaik untuk pengendalian terpadu!"
    },
    "Fermentasi Urine Sapi + Daun Pepaya": {
        "target": ["Ulat", "Penggerek", "Kutu"],
        "cara_buat": [
            "1. Campurkan 5 L urine sapi segar",
            "2. Tambahkan 1 kg daun pepaya yang dihaluskan",
            "3. Tambahkan 100g gula merah",
            "4. Fermentasi 7 hari dalam wadah tertutup"
        ],
        "dosis": "Encerkan 1:10",
        "interval": "Setiap 7 hari",
        "kelebihan": ["Murah", "Efektif", "Bonus nutrisi"],
        "tips": "Urine sapi juga mengandung nutrisi!"
    }
}

# ========== MAIN APP ==========
st.title("📚 Pusat Pengetahuan Pertanian")
st.markdown("**Ensiklopedia lengkap nutrisi tanaman, pupuk, dan pengendalian hama alami**")

# Category tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌾 Pupuk Makro",
    "⚗️ Pupuk Mikro",
    "🌱 Pupuk Organik & Hayati",
    "💧 POC, MOL & ZPT",
    "🌿 Pestisida Nabati"
])

# TAB 1: PUPUK MAKRO
with tab1:
    st.header("🌾 Pupuk Makro")
    st.markdown("Pupuk dengan kandungan NPK tinggi untuk pertumbuhan optimal")
    
    # Search
    search_makro = st.text_input("🔍 Cari pupuk makro...", key="search_makro")
    
    # Filter
    filtered_makro = {k: v for k, v in PUPUK_MAKRO.items() 
                      if search_makro.lower() in k.lower()}
    
    for nama, data in filtered_makro.items():
        with st.expander(f"**{nama}**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Kandungan:**
                - N: {data['kandungan']['N']}%
                - P: {data['kandungan']['P']}%
                - K: {data['kandungan']['K']}%
                
                **Fungsi:** {data['fungsi']}
                
                **Dosis:** {data['dosis']}
                
                **Cara Aplikasi:** {data['cara_aplikasi']}
                
                **Waktu Aplikasi:** {data['waktu_aplikasi']}
                """)
            
            with col2:
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
                st.warning("**Kekurangan:**\n" + "\n".join([f"⚠️ {k}" for k in data['kekurangan']]))
                st.info(f"💡 **Tips:** {data['tips']}")

# TAB 2: PUPUK MIKRO
with tab2:
    st.header("⚗️ Pupuk Mikro")
    st.markdown("Unsur hara mikro penting untuk pertumbuhan optimal")
    
    for nama, data in PUPUK_MIKRO.items():
        with st.expander(f"**{nama}**"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Fungsi:** {data['fungsi']}
                
                **Gejala Defisiensi:**
                {data['defisiensi']}
                
                **Sumber:** {data['sumber']}
                """)
            
            with col2:
                st.markdown(f"""
                **Dosis:** {data['dosis']}
                
                **Tanaman Peka:**
                {', '.join(data['tanaman_peka'])}
                """)
                
                st.info(f"💡 {data['tips']}")

# TAB 3: PUPUK ORGANIK
with tab3:
    st.header("🌱 Pupuk Organik & Hayati")
    st.markdown("Pupuk alami untuk kesehatan tanah jangka panjang")
    
    for nama, data in PUPUK_ORGANIK.items():
        with st.expander(f"**{nama}**", expanded=False):
            if "kandungan" in data:
                st.markdown(f"**Kandungan:** {data['kandungan']}")
            
            if "jenis" in data:
                st.markdown("**Jenis:**")
                for jenis, desc in data['jenis'].items():
                    st.markdown(f"- **{jenis}:** {desc}")
            
            st.markdown(f"**Fungsi:** {data['fungsi']}")
            st.markdown(f"**Dosis:** {data['dosis']}")
            
            if "cara_buat" in data:
                st.markdown("**Cara Membuat:**")
                for step in data['cara_buat']:
                    st.markdown(f"{step}")
            
            if "cara_aplikasi" in data:
                st.markdown(f"**Cara Aplikasi:** {data['cara_aplikasi']}")
            
            if "kelebihan" in data:
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
            
            st.info(f"💡 **Tips:** {data['tips']}")

# TAB 4: POC, MOL & ZPT
with tab4:
    st.header("💧 POC, MOL & ZPT Alami")
    st.markdown("Pupuk cair dan zat pengatur tumbuh alami")
    
    for kategori, items in POC_MOL_ZPT.items():
        st.subheader(kategori)
        
        if kategori == "MOL (Mikroorganisme Lokal)":
            for jenis_mol, data_mol in items['jenis'].items():
                with st.expander(jenis_mol):
                    st.markdown(f"**Bahan:** {data_mol['bahan']}")
                    st.markdown(f"**Fungsi:** {data_mol['fungsi']}")
                    st.markdown(f"**Cara:** {data_mol['cara']}")
            
            st.markdown(f"**Dosis Umum:** {items['dosis']}")
            st.markdown(f"**Aplikasi:** {items['aplikasi']}")
            st.info(f"💡 {items['tips']}")
            
        elif kategori == "ZPT Alami (Zat Pengatur Tumbuh)":
            for zpt_name, zpt_data in items.items():
                with st.expander(zpt_name):
                    st.markdown(f"**Kandungan:** {zpt_data['kandungan']}")
                    st.markdown(f"**Fungsi:** {zpt_data['fungsi']}")
                    if 'cara' in zpt_data:
                        st.markdown(f"**Cara:** {zpt_data['cara']}")
                    if 'dosis' in zpt_data:
                        st.markdown(f"**Dosis:** {zpt_data['dosis']}")
                    st.markdown(f"**Aplikasi:** {zpt_data['aplikasi']}")
        else:
            with st.expander("Detail"):
                st.markdown(f"**Bahan:** {items['bahan']}")
                st.markdown("**Cara Membuat:**")
                for step in items['cara_buat']:
                    st.markdown(step)
                st.markdown(f"**Dosis:** {items['dosis']}")
                st.markdown(f"**Aplikasi:** {items['aplikasi']}")
                st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in items['kelebihan']]))
                st.info(f"💡 {items['tips']}")

# TAB 5: PESTISIDA NABATI
with tab5:
    st.header("🌿 Pestisida Nabati")
    st.markdown("Pengendalian hama & penyakit dengan bahan alami")
    
    st.warning("""
    **⚠️ Penting:**
    - Gunakan APD (masker, sarung tangan)
    - Aplikasi pagi/sore hari
    - Hindari saat hujan
    - Simpan di tempat aman
    - Jauhkan dari jangkauan anak-anak
    """)
    
    for nama, data in PESTISIDA_NABATI.items():
        with st.expander(f"**{nama}**", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Target Hama:**")
                if isinstance(data['target'], list):
                    for target in data['target']:
                        st.markdown(f"- {target}")
                else:
                    st.markdown(data['target'])
                
                if 'bahan_aktif' in data:
                    st.markdown(f"\n**Bahan Aktif:** {data['bahan_aktif']}")
                
                if 'bahan' in data:
                    st.markdown("\n**Bahan:**")
                    for bahan in data['bahan']:
                        st.markdown(f"- {bahan}")
            
            with col2:
                st.markdown(f"**Dosis:** {data['dosis']}")
                st.markdown(f"**Interval:** {data['interval']}")
                
                if 'kelebihan' in data:
                    st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
            
            st.markdown("**Cara Membuat:**")
            for i, step in enumerate(data['cara_buat'], 1):
                st.markdown(step)
            
            if 'tips' in data:
                st.info(f"💡 **Tips:** {data['tips']}")
            
            if 'peringatan' in data:
                st.error(data['peringatan'])

# Footer
st.markdown("---")
st.caption("""
📚 **Pusat Pengetahuan Pertanian** - Ensiklopedia lengkap untuk pertanian berkelanjutan.

💡 **Disclaimer:** Informasi ini bersifat edukatif. Sesuaikan dengan kondisi lokal dan konsultasikan dengan ahli untuk kasus spesifik.

🌱 **Tips:** Kombinasikan pupuk organik dan anorganik untuk hasil optimal dan kesehatan tanah jangka panjang!
""")
