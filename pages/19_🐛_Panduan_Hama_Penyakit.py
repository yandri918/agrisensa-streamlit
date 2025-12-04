# Panduan Lengkap Hama & Penyakit Tanaman
# Database komprehensif dengan strategi pengendalian terpadu

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Panduan Hama & Penyakit", page_icon="🐛", layout="wide")

# ========== DATABASE HAMA ==========

HAMA_DATABASE = {
    "Ulat Grayak (Spodoptera litura)": {
        "kategori": "Hama Pemakan Daun",
        "nama_latin": "Spodoptera litura",
        "tanaman_inang": ["Padi", "Jagung", "Kedelai", "Cabai", "Tomat", "Kubis", "Bawang"],
        "gejala": [
            "Daun berlubang-lubang",
            "Daun tinggal tulang daun (kerangka)",
            "Kotoran ulat berwarna hitam di daun",
            "Serangan dimulai dari daun muda",
            "Populasi tinggi saat musim hujan"
        ],
        "ciri_hama": {
            "Telur": "Kelompok, ditutupi bulu coklat, 100-300 butir/kelompok",
            "Larva": "Warna hijau-coklat-hitam, garis kuning di punggung, 3-4 cm",
            "Pupa": "Di dalam tanah, coklat kehitaman",
            "Dewasa": "Ngengat coklat, sayap 3-4 cm"
        },
        "siklus_hidup": "28-35 hari (telur 3 hari, larva 14-21 hari, pupa 7-10 hari)",
        "tingkat_kerusakan": "Sangat Tinggi (dapat merusak 100% daun)",
        "ambang_ekonomi": "2 ekor larva/tanaman atau 10% tanaman terserang",
        "pengendalian": {
            "Kultur Teknis": [
                "Sanitasi lahan - bersihkan gulma dan sisa tanaman",
                "Rotasi tanaman dengan non-inang",
                "Tanam serentak untuk memutus siklus",
                "Pengairan berselang untuk mengurangi kelembaban",
                "Pemasangan perangkap feromon seks"
            ],
            "Mekanis": [
                "Kumpulkan dan musnahkan kelompok telur",
                "Tangkap larva secara manual (pagi hari)",
                "Perangkap cahaya untuk ngengat dewasa",
                "Perangkap feromon (1-2 buah/ha)"
            ],
            "Hayati": [
                "Trichogramma spp. (parasitoid telur) - 100.000/ha",
                "Telenomus remus (parasitoid telur)",
                "Bacillus thuringiensis (Bt) - 2-3 g/L",
                "NPV (Nuclear Polyhedrosis Virus) - 2 ml/L",
                "Predator: Laba-laba, kumbang kubah"
            ],
            "Nabati": [
                "Ekstrak daun mimba - semprot 400-500 L/ha",
                "Ekstrak tembakau - encerkan 1:2",
                "Ekstrak daun sirsak - semprot langsung",
                "Formula kombinasi (mimba+bawang putih+cabai)"
            ],
            "Kimia": [
                "Insektisida golongan piretroid (jika populasi tinggi)",
                "Aplikasi sore hari saat larva aktif",
                "Rotasi bahan aktif untuk hindari resistensi",
                "Perhatikan masa tunggu panen"
            ]
        },
        "tips_pengendalian": "Monitoring rutin! Kendalikan saat populasi masih rendah. Kombinasikan kultur teknis + hayati + nabati untuk hasil optimal.",
        "link_pestisida": "Mimba, Tembakau, Sirsak, Mahoni, Suren"
    },
    
    "Kutu Daun (Aphids)": {
        "kategori": "Hama Penghisap",
        "nama_latin": "Aphis spp., Myzus persicae",
        "tanaman_inang": ["Cabai", "Tomat", "Kentang", "Kubis", "Bawang", "Sayuran daun"],
        "gejala": [
            "Daun mengkerut dan menggulung",
            "Daun muda kerdil dan pucat",
            "Embun madu (honeydew) pada daun",
            "Jamur jelaga hitam pada embun madu",
            "Tanaman kerdil dan pertumbuhan terhambat",
            "Vektor virus (mosaik, keriting)"
        ],
        "ciri_hama": {
            "Nimfa": "Hijau muda, tanpa sayap, 1-2 mm",
            "Dewasa": "Hijau/hitam, ada yang bersayap, 2-3 mm",
            "Koloni": "Berkelompok di pucuk dan daun muda"
        },
        "siklus_hidup": "7-10 hari (reproduksi parthenogenesis - tanpa kawin)",
        "tingkat_kerusakan": "Tinggi (vektor virus berbahaya)",
        "ambang_ekonomi": "5-10 ekor/daun atau 25% tanaman terserang",
        "pengendalian": {
            "Kultur Teknis": [
                "Gunakan mulsa plastik perak (reflektif)",
                "Tanam tanaman perangkap (mustard)",
                "Hindari kelebihan nitrogen (daun terlalu lembut)",
                "Sanitasi gulma inang virus",
                "Jarak tanam optimal untuk sirkulasi udara"
            ],
            "Mekanis": [
                "Semprotkan air keras untuk jatuhkan kutu",
                "Pangkas dan musnahkan bagian terserang berat",
                "Perangkap kuning (sticky trap) - 20-40/ha"
            ],
            "Hayati": [
                "Kumbang koksi (Coccinella spp.) - predator alami",
                "Aphidius colemani (parasitoid) - 500-1000/ha",
                "Chrysoperla (lacewing) - predator",
                "Jamur Beauveria bassiana - 2-3 g/L",
                "Tanam bunga untuk menarik musuh alami"
            ],
            "Nabati": [
                "Ekstrak bawang putih - encerkan 1:5",
                "Ekstrak cabai rawit - encerkan 1:3",
                "Sabun insektisida (sabun cuci + air) - 10 ml/L",
                "Minyak nimba - 5 ml/L"
            ],
            "Kimia": [
                "Insektisida sistemik (imidakloprid) - hanya jika berat",
                "Hindari piretroid (bunuh musuh alami)",
                "Aplikasi bergantian dengan hayati"
            ]
        },
        "tips_pengendalian": "Kutu daun berkembang cepat! Kendalikan sejak dini. Mulsa perak sangat efektif. Jangan bunuh musuh alami!",
        "link_pestisida": "Bawang Putih, Cabai Rawit, Mimba, Cengkeh"
    },
    
    "Penggerek Batang (Stem Borer)": {
        "kategori": "Hama Penggerek",
        "nama_latin": "Ostrinia furnacalis, Chilo suppressalis",
        "tanaman_inang": ["Padi", "Jagung", "Tebu"],
        "gejala": [
            "Daun muda mengering (sundep)",
            "Malai hampa (beluk)",
            "Lubang gerek pada batang",
            "Batang mudah patah",
            "Kotoran/frass di lubang gerek"
        ],
        "ciri_hama": {
            "Telur": "Kelompok di daun, pipih, putih kekuningan",
            "Larva": "Putih kecoklatan, kepala coklat, 2-3 cm",
            "Pupa": "Di dalam batang",
            "Dewasa": "Ngengat kuning kecoklatan"
        },
        "siklus_hidup": "30-40 hari",
        "tingkat_kerusakan": "Sangat Tinggi (kehilangan hasil 20-80%)",
        "ambang_ekonomi": "2 kelompok telur/m² atau 5% sundep",
        "pengendalian": {
            "Kultur Teknis": [
                "Tanam varietas tahan (batang keras)",
                "Tanam serentak dalam hamparan luas",
                "Pengairan berselang (larva mati saat kering)",
                "Pemupukan berimbang (jangan over N)",
                "Sanitasi jerami - bakar/benamkan"
            ],
            "Mekanis": [
                "Kumpulkan dan musnahkan kelompok telur",
                "Potong dan bakar tanaman sundep",
                "Perangkap cahaya untuk ngengat",
                "Perangkap feromon"
            ],
            "Hayati": [
                "Trichogramma japonicum (parasitoid telur) - 150.000/ha",
                "Beauveria bassiana - 3-5 g/L",
                "Predator: Laba-laba, kepik"
            ],
            "Nabati": [
                "Ekstrak mimba - aplikasi preventif",
                "Ekstrak mahoni - untuk telur dan larva muda",
                "Ekstrak brotowali - racun perut"
            ],
            "Kimia": [
                "Insektisida granular (karbofuran) - di pucuk",
                "Hanya untuk serangan berat",
                "Aplikasi saat telur menetas"
            ]
        },
        "tips_pengendalian": "Sulit dikendalikan setelah masuk batang! Fokus pada telur dan larva muda. Tanam serentak sangat penting!",
        "link_pestisida": "Mimba, Mahoni, Brotowali, Tembakau"
    },
    
    "Wereng Coklat (Brown Planthopper)": {
        "kategori": "Hama Penghisap",
        "nama_latin": "Nilaparvata lugens",
        "tanaman_inang": ["Padi"],
        "gejala": [
            "Hopperburn - tanaman menguning lalu coklat mengering",
            "Tanaman roboh seperti terbakar",
            "Embun madu pada daun bawah",
            "Vektor virus kerdil (grassy stunt, ragged stunt)"
        ],
        "ciri_hama": {
            "Nimfa": "Putih kecoklatan, tidak bersayap",
            "Dewasa": "Coklat, sayap lebih panjang dari tubuh, 3-4 mm",
            "Koloni": "Di pangkal batang dekat permukaan air"
        },
        "siklus_hidup": "25-30 hari",
        "tingkat_kerusakan": "Sangat Tinggi (dapat gagal panen total)",
        "ambang_ekonomi": "5-10 ekor/rumpun (fase vegetatif), 10-15 ekor/rumpun (generatif)",
        "pengendalian": {
            "Kultur Teknis": [
                "Tanam varietas tahan (IR64, Ciherang, Inpari)",
                "Tanam serentak dalam hamparan luas",
                "Pergiliran varietas untuk hindari resistensi",
                "Pemupukan berimbang (hindari over N)",
                "Pengairan berselang (keringkan berkala)",
                "Jarak tanam optimal (25x25 cm)"
            ],
            "Mekanis": [
                "Gunakan jaring/kain untuk tangkap wereng",
                "Giring wereng ke satu titik lalu musnahkan"
            ],
            "Hayati": [
                "Laba-laba (Lycosa, Pardosa) - predator utama",
                "Mirid bugs (Cyrtorhinus lividipennis) - predator telur",
                "Jamur Metarhizium anisopliae - 5 g/L",
                "Hindari insektisida broad spectrum (bunuh predator)"
            ],
            "Nabati": [
                "Ekstrak mimba - sistemik",
                "Ekstrak brotowali - efektif untuk wereng",
                "Ekstrak tembakau - racun kontak"
            ],
            "Kimia": [
                "HANYA jika populasi >15 ekor/rumpun",
                "Gunakan insektisida selektif (buprofezin, pimetrozin)",
                "HINDARI piretroid dan organofosfat (bunuh predator)",
                "Rotasi bahan aktif"
            ]
        },
        "tips_pengendalian": "Varietas tahan + laba-laba = kunci sukses! Jangan semprotkan insektisida broad spectrum. Monitoring rutin sangat penting!",
        "link_pestisida": "Mimba, Brotowali, Tembakau"
    },
    
    "Keong Mas (Golden Snail)": {
        "kategori": "Mollusca",
        "nama_latin": "Pomacea canaliculata",
        "tanaman_inang": ["Padi (terutama bibit muda)"],
        "gejala": [
            "Bibit padi dimakan habis",
            "Tanaman muda putus di pangkal",
            "Serangan berat saat 0-30 HST",
            "Kelompok telur merah muda di batang/pematang"
        ],
        "ciri_hama": {
            "Telur": "Kelompok, merah muda, di atas permukaan air",
            "Keong": "Cangkang coklat kekuningan, 3-7 cm"
        },
        "siklus_hidup": "60-90 hari",
        "tingkat_kerusakan": "Sangat Tinggi (dapat gagal tanam)",
        "ambang_ekonomi": "1-2 ekor/m² (bibit muda)",
        "pengendalian": {
            "Kultur Teknis": [
                "Tanam bibit umur >21 hari (batang keras)",
                "Keringkan sawah 3-7 hari sebelum tanam",
                "Buat pagar plastik di pematang",
                "Hindari pemindahan keong antar lahan"
            ],
            "Mekanis": [
                "Kumpulkan keong secara manual",
                "Hancurkan kelompok telur",
                "Buat perangkap dari daun pisang/pepaya",
                "Gunakan bebek sebagai predator (10-20 ekor/ha)"
            ],
            "Hayati": [
                "Bebek - predator alami terbaik",
                "Ikan lele, mujair - pemakan keong",
                "Burung - pemakan keong"
            ],
            "Nabati": [
                "Ekstrak akar tuba - moluskisida kuat",
                "Ekstrak biji jarak - beracun untuk keong",
                "Saponin dari biji teh - 50-100 ppm"
            ],
            "Kimia": [
                "Niklosamida (moluskisida) - 3-5 kg/ha",
                "Aplikasi saat air dangkal",
                "Hanya untuk serangan berat"
            ]
        },
        "tips_pengendalian": "Bebek adalah solusi terbaik! Tanam bibit tua. Keringkan sawah sebelum tanam. Hancurkan telur!",
        "link_pestisida": "Akar Tuba, Jarak"
    }
}

# ========== DATABASE PENYAKIT ==========

PENYAKIT_DATABASE = {
    "Busuk Daun (Late Blight)": {
        "kategori": "Penyakit Jamur",
        "nama_latin": "Phytophthora infestans",
        "tanaman_inang": ["Tomat", "Kentang", "Cabai"],
        "gejala": [
            "Bercak coklat kehitaman pada daun",
            "Bercak basah dan berbau busuk",
            "Miselium putih di bawah daun (pagi hari)",
            "Daun cepat mengering dan mati",
            "Buah busuk dengan bercak coklat",
            "Penyebaran sangat cepat saat hujan"
        ],
        "kondisi_ideal": {
            "Suhu": "18-22°C",
            "Kelembaban": ">90%",
            "Cuaca": "Hujan, kabut, embun berat"
        },
        "tingkat_kerusakan": "Sangat Tinggi (dapat merusak 100% dalam 1-2 minggu)",
        "pengendalian": {
            "Kultur Teknis": [
                "Tanam varietas tahan",
                "Jarak tanam lebar untuk sirkulasi udara",
                "Hindari tanam saat musim hujan",
                "Drainase baik - hindari genangan",
                "Mulsa plastik untuk cegah percikan air",
                "Sanitasi - buang tanaman sakit"
            ],
            "Mekanis": [
                "Pangkas daun terserang",
                "Atur kanopi untuk sirkulasi udara",
                "Hindari penyiraman dari atas"
            ],
            "Hayati": [
                "Trichoderma spp. - antagonis jamur",
                "Bacillus subtilis - bakterisida",
                "Pseudomonas fluorescens"
            ],
            "Nabati": [
                "Ekstrak bawang putih - antijamur kuat",
                "Ekstrak kunyit - curcumin antijamur",
                "Ekstrak jahe - gingerol antijamur",
                "Ekstrak lengkuas - galangin",
                "Kombinasi kunyit+jahe+lengkuas sangat efektif"
            ],
            "Kimia": [
                "Fungisida berbahan aktif mankozeb, propineb",
                "Aplikasi preventif sebelum hujan",
                "Interval 5-7 hari saat musim hujan",
                "Rotasi bahan aktif"
            ]
        },
        "tips_pengendalian": "Preventif sangat penting! Aplikasi fungisida sebelum hujan. Kombinasi kunyit+jahe+lengkuas efektif!",
        "link_pestisida": "Bawang Putih, Kunyit, Jahe, Lengkuas, Sirih"
    },
    
    "Layu Bakteri (Bacterial Wilt)": {
        "kategori": "Penyakit Bakteri",
        "nama_latin": "Ralstonia solanacearum",
        "tanaman_inang": ["Tomat", "Cabai", "Kentang", "Terong", "Pisang"],
        "gejala": [
            "Layu mendadak tanpa menguning",
            "Layu siang hari, segar pagi hari (awal)",
            "Layu permanen (lanjut)",
            "Pembuluh berlendir putih kecoklatan",
            "Akar dan batang bawah busuk",
            "Tanaman mati dalam 1-2 minggu"
        ],
        "kondisi_ideal": {
            "Suhu": "25-35°C",
            "Kelembaban": "Tinggi",
            "pH tanah": "6.0-7.0"
        },
        "tingkat_kerusakan": "Sangat Tinggi (tidak ada obat, hanya preventif)",
        "pengendalian": {
            "Kultur Teknis": [
                "Tanam varietas tahan/toleran",
                "Rotasi tanaman dengan non-Solanaceae (3-4 tahun)",
                "Sanitasi alat - celup klorin 10%",
                "Drainase sempurna",
                "pH tanah 5.0-5.5 (bakteri kurang aktif)",
                "Solarisasi tanah (plastik transparan 4-6 minggu)",
                "Hindari luka pada akar"
            ],
            "Mekanis": [
                "Cabut dan bakar tanaman sakit",
                "Jangan komposkan tanaman sakit",
                "Karantina lahan terinfeksi"
            ],
            "Hayati": [
                "Pseudomonas fluorescens - antagonis bakteri",
                "Bacillus subtilis",
                "Trichoderma spp.",
                "Aplikasi saat tanam dan berkala"
            ],
            "Nabati": [
                "Ekstrak bawang putih - antibakteri kuat",
                "Ekstrak lengkuas - galangin antibakteri",
                "Ekstrak sirih - kavikol antibakteri",
                "Ekstrak jahe - antibakteri",
                "Aplikasi preventif sejak tanam"
            ],
            "Kimia": [
                "Bakterisida (streptomisin, oksitetrasiklin)",
                "Hanya efektif untuk preventif",
                "Tidak efektif setelah tanaman sakit",
                "Aplikasi saat tanam dan berkala"
            ]
        },
        "tips_pengendalian": "TIDAK ADA OBAT! Fokus preventif: varietas tahan + rotasi + sanitasi. Bawang putih+lengkuas+sirih untuk preventif!",
        "link_pestisida": "Bawang Putih, Lengkuas, Sirih, Jahe, Kunyit"
    },
    
    "Antraknosa (Anthracnose)": {
        "kategori": "Penyakit Jamur",
        "nama_latin": "Colletotrichum spp.",
        "tanaman_inang": ["Cabai", "Tomat", "Mangga", "Pepaya", "Pisang"],
        "gejala": [
            "Bercak bulat cekung pada buah",
            "Bercak coklat dengan lingkaran konsentris",
            "Titik hitam (acervuli) di tengah bercak",
            "Buah busuk dan rontok",
            "Bercak pada daun dan batang"
        ],
        "kondisi_ideal": {
            "Suhu": "25-30°C",
            "Kelembaban": ">80%",
            "Cuaca": "Hujan, lembab"
        },
        "tingkat_kerusakan": "Tinggi (kehilangan hasil 30-100%)",
        "pengendalian": {
            "Kultur Teknis": [
                "Sanitasi - buang buah busuk",
                "Drainase baik",
                "Jarak tanam optimal",
                "Pemupukan K untuk kulit buah kuat",
                "Panen tepat waktu",
                "Hindari luka pada buah"
            ],
            "Mekanis": [
                "Pangkas cabang sakit",
                "Buang buah terserang",
                "Bungkus buah (untuk mangga)"
            ],
            "Hayati": [
                "Trichoderma harzianum - antagonis",
                "Bacillus subtilis"
            ],
            "Nabati": [
                "Ekstrak kunyit - curcumin antijamur",
                "Ekstrak bawang putih",
                "Ekstrak jahe",
                "Ekstrak sirih"
            ],
            "Kimia": [
                "Fungisida berbahan aktif mankozeb, propineb",
                "Aplikasi preventif saat pembungaan",
                "Interval 7-10 hari"
            ]
        },
        "tips_pengendalian": "Sanitasi buah busuk penting! Pemupukan K untuk kulit buah kuat. Kunyit sangat efektif!",
        "link_pestisida": "Kunyit, Bawang Putih, Jahe, Sirih"
    }
}

# ========== HELPER FUNCTIONS ==========

def get_pestisida_recommendation(hama_penyakit_name):
    """Get pestisida nabati recommendation for specific pest/disease"""
    recommendations = []
    
    if hama_penyakit_name in HAMA_DATABASE:
        data = HAMA_DATABASE[hama_penyakit_name]
        if 'link_pestisida' in data:
            recommendations = data['link_pestisida'].split(", ")
    elif hama_penyakit_name in PENYAKIT_DATABASE:
        data = PENYAKIT_DATABASE[hama_penyakit_name]
        if 'link_pestisida' in data:
            recommendations = data['link_pestisida'].split(", ")
    
    return recommendations

# ========== MAIN APP ==========

st.title("🐛 Panduan Lengkap Hama & Penyakit Tanaman")
st.markdown("**Database komprehensif dengan strategi pengendalian terpadu (PHT)**")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Cari Berdasarkan Tanaman",
    "🐛 Database Hama",
    "🦠 Database Penyakit",
    "📊 Strategi PHT",
    "📖 Panduan Monitoring"
])

# TAB 1: SEARCH BY CROP
with tab1:
    st.header("🔍 Cari Hama & Penyakit Berdasarkan Tanaman")
    
    # Collect all crops
    all_crops = set()
    for data in HAMA_DATABASE.values():
        all_crops.update(data['tanaman_inang'])
    for data in PENYAKIT_DATABASE.values():
        all_crops.update(data['tanaman_inang'])
    
    selected_crop = st.selectbox(
        "Pilih Tanaman:",
        sorted(list(all_crops))
    )
    
    if selected_crop:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🐛 Hama pada {selected_crop}")
            
            hama_matches = []
            for nama, data in HAMA_DATABASE.items():
                if selected_crop in data['tanaman_inang']:
                    hama_matches.append((nama, data))
            
            if hama_matches:
                for nama, data in hama_matches:
                    with st.expander(f"**{nama}** - {data['tingkat_kerusakan']}", expanded=False):
                        st.markdown(f"**Kategori:** {data['kategori']}")
                        st.markdown(f"**Nama Latin:** {data['nama_latin']}")
                        
                        st.markdown("**Gejala Serangan:**")
                        for gejala in data['gejala']:
                            st.markdown(f"- {gejala}")
                        
                        st.markdown(f"**Ambang Ekonomi:** {data['ambang_ekonomi']}")
                        
                        st.markdown("**Pengendalian Terpadu:**")
                        for metode, tindakan in data['pengendalian'].items():
                            with st.expander(f"{metode}"):
                                for item in tindakan:
                                    st.markdown(f"- {item}")
                        
                        st.info(f"💡 **Tips:** {data['tips_pengendalian']}")
                        
                        # Link to pestisida
                        if 'link_pestisida' in data:
                            st.success(f"🌿 **Pestisida Nabati:** {data['link_pestisida']}")
            else:
                st.info("Belum ada data hama untuk tanaman ini")
        
        with col2:
            st.subheader(f"🦠 Penyakit pada {selected_crop}")
            
            penyakit_matches = []
            for nama, data in PENYAKIT_DATABASE.items():
                if selected_crop in data['tanaman_inang']:
                    penyakit_matches.append((nama, data))
            
            if penyakit_matches:
                for nama, data in penyakit_matches:
                    with st.expander(f"**{nama}** - {data['tingkat_kerusakan']}", expanded=False):
                        st.markdown(f"**Kategori:** {data['kategori']}")
                        st.markdown(f"**Nama Latin:** {data['nama_latin']}")
                        
                        st.markdown("**Gejala:**")
                        for gejala in data['gejala']:
                            st.markdown(f"- {gejala}")
                        
                        st.markdown("**Kondisi Ideal Perkembangan:**")
                        for key, value in data['kondisi_ideal'].items():
                            st.markdown(f"- {key}: {value}")
                        
                        st.markdown("**Pengendalian Terpadu:**")
                        for metode, tindakan in data['pengendalian'].items():
                            with st.expander(f"{metode}"):
                                for item in tindakan:
                                    st.markdown(f"- {item}")
                        
                        st.info(f"💡 **Tips:** {data['tips_pengendalian']}")
                        
                        # Link to pestisida
                        if 'link_pestisida' in data:
                            st.success(f"🌿 **Pestisida Nabati:** {data['link_pestisida']}")
            else:
                st.info("Belum ada data penyakit untuk tanaman ini")

# TAB 2: PEST DATABASE
with tab2:
    st.header("🐛 Database Hama Lengkap")
    
    search_hama = st.text_input("🔍 Cari hama...", key="search_hama")
    
    for nama, data in HAMA_DATABASE.items():
        if search_hama.lower() in nama.lower() or search_hama == "":
            with st.expander(f"**{nama}**"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Kategori:** {data['kategori']}")
                    st.markdown(f"**Nama Latin:** *{data['nama_latin']}*")
                    st.markdown(f"**Siklus Hidup:** {data['siklus_hidup']}")
                    st.markdown(f"**Tingkat Kerusakan:** {data['tingkat_kerusakan']}")
                
                with col2:
                    st.markdown("**Tanaman Inang:**")
                    for tanaman in data['tanaman_inang']:
                        st.markdown(f"- {tanaman}")
                    
                    st.markdown(f"**Ambang Ekonomi:**")
                    st.markdown(data['ambang_ekonomi'])
                
                with col3:
                    st.markdown("**Ciri-ciri Hama:**")
                    for stage, ciri in data['ciri_hama'].items():
                        st.markdown(f"- **{stage}:** {ciri}")
                
                st.markdown("---")
                st.markdown("**Gejala Serangan:**")
                for gejala in data['gejala']:
                    st.markdown(f"✓ {gejala}")
                
                st.markdown("---")
                st.markdown("### Strategi Pengendalian Terpadu")
                
                for metode, tindakan in data['pengendalian'].items():
                    with st.expander(f"**{metode}**", expanded=False):
                        for item in tindakan:
                            st.markdown(f"• {item}")
                
                st.info(f"💡 **Tips Pengendalian:** {data['tips_pengendalian']}")
                
                if 'link_pestisida' in data:
                    st.success(f"🌿 **Pestisida Nabati yang Efektif:** {data['link_pestisida']}")
                    st.caption("Klik tab 'Pestisida Nabati' di sidebar untuk detail formula")

# TAB 3: DISEASE DATABASE
with tab3:
    st.header("🦠 Database Penyakit Lengkap")
    
    search_penyakit = st.text_input("🔍 Cari penyakit...", key="search_penyakit")
    
    for nama, data in PENYAKIT_DATABASE.items():
        if search_penyakit.lower() in nama.lower() or search_penyakit == "":
            with st.expander(f"**{nama}**"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Kategori:** {data['kategori']}")
                    st.markdown(f"**Nama Latin:** *{data['nama_latin']}*")
                    st.markdown(f"**Tingkat Kerusakan:** {data['tingkat_kerusakan']}")
                    
                    st.markdown("**Tanaman Inang:**")
                    for tanaman in data['tanaman_inang']:
                        st.markdown(f"- {tanaman}")
                
                with col2:
                    st.markdown("**Kondisi Ideal Perkembangan:**")
                    for key, value in data['kondisi_ideal'].items():
                        st.markdown(f"- **{key}:** {value}")
                
                st.markdown("---")
                st.markdown("**Gejala:**")
                for gejala in data['gejala']:
                    st.markdown(f"✓ {gejala}")
                
                st.markdown("---")
                st.markdown("### Strategi Pengendalian Terpadu")
                
                for metode, tindakan in data['pengendalian'].items():
                    with st.expander(f"**{metode}**", expanded=False):
                        for item in tindakan:
                            st.markdown(f"• {item}")
                
                st.info(f"💡 **Tips Pengendalian:** {data['tips_pengendalian']}")
                
                if 'link_pestisida' in data:
                    st.success(f"🌿 **Pestisida Nabati yang Efektif:** {data['link_pestisida']}")
                    st.caption("Klik tab 'Pestisida Nabati' di sidebar untuk detail formula")

# TAB 4: IPM STRATEGY
with tab4:
    st.header("📊 Strategi Pengendalian Hama Terpadu (PHT)")
    
    st.markdown("""
    ## 🎯 Prinsip Dasar PHT
    
    Pengendalian Hama Terpadu (PHT) adalah pendekatan ekologis untuk mengendalikan hama dengan:
    1. **Meminimalkan** penggunaan pestisida kimia
    2. **Memaksimalkan** pengendalian alami
    3. **Mengintegrasikan** berbagai metode pengendalian
    4. **Berkelanjutan** untuk lingkungan
    
    ---
    
    ## 🔄 Hierarki Pengendalian PHT
    
    ### 1️⃣ Preventif (Prioritas Utama)
    
    **Kultur Teknis:**
    - ✅ Gunakan varietas tahan/toleran
    - ✅ Tanam serentak dalam hamparan luas
    - ✅ Rotasi tanaman
    - ✅ Sanitasi lahan
    - ✅ Pengaturan jarak tanam
    - ✅ Pemupukan berimbang
    - ✅ Pengairan optimal
    
    **Tujuan:** Cegah hama/penyakit sebelum muncul
    
    ---
    
    ### 2️⃣ Monitoring & Ambang Ekonomi
    
    **Monitoring Rutin:**
    - 📅 Cek tanaman 2-3 kali/minggu
    - 📊 Catat populasi hama
    - 📸 Dokumentasi gejala
    - 📈 Bandingkan dengan ambang ekonomi
    
    **Ambang Ekonomi:**
    - Populasi hama yang jika dibiarkan akan menyebabkan kerugian ekonomi
    - **Jangan** kendalikan jika populasi di bawah ambang
    - **Kendalikan** jika populasi mencapai/melebihi ambang
    
    **Contoh Ambang Ekonomi:**
    - Ulat grayak: 2 ekor/tanaman
    - Kutu daun: 5-10 ekor/daun
    - Wereng: 5-10 ekor/rumpun
    
    ---
    
    ### 3️⃣ Pengendalian Non-Kimia (Prioritas Kedua)
    
    **A. Mekanis:**
    - 🖐️ Tangkap manual
    - 🪤 Perangkap (cahaya, feromon, sticky trap)
    - ✂️ Pangkas bagian terserang
    - 🔥 Musnahkan dengan bakar
    
    **B. Hayati:**
    - 🐞 Predator alami (kumbang, laba-laba, lacewing)
    - 🦟 Parasitoid (Trichogramma, Aphidius)
    - 🦠 Patogen serangga (Bt, NPV, Beauveria, Metarhizium)
    - 🌸 Tanaman refugia (bunga untuk musuh alami)
    
    **C. Nabati:**
    - 🌿 Ekstrak tanaman (mimba, bawang putih, cabai, dll)
    - ✅ Aman untuk musuh alami
    - ✅ Tidak meninggalkan residu berbahaya
    - ✅ Murah dan mudah dibuat
    - 📚 Lihat modul "Pestisida Nabati" untuk 29 formula lengkap
    
    ---
    
    ### 4️⃣ Kimia (Pilihan Terakhir)
    
    **Gunakan HANYA jika:**
    - ⚠️ Populasi melebihi ambang ekonomi
    - ⚠️ Metode lain tidak efektif
    - ⚠️ Ancaman gagal panen
    
    **Prinsip Penggunaan:**
    - ✅ Pilih insektisida selektif (tidak bunuh musuh alami)
    - ✅ Gunakan dosis sesuai anjuran
    - ✅ Rotasi bahan aktif (hindari resistensi)
    - ✅ Perhatikan masa tunggu panen
    - ✅ Aplikasi tepat waktu (sore hari)
    - ❌ HINDARI insektisida broad spectrum
    
    ---
    
    ## 🌱 Komponen Penting PHT
    
    ### Tanaman Refugia
    
    Tanaman berbunga untuk menarik dan mempertahankan musuh alami:
    - 🌼 Bunga matahari
    - 🌸 Kenikir (Tagetes)
    - 🌺 Bunga kertas
    - 🌿 Serai wangi
    
    **Cara Tanam:**
    - Di pematang atau tepi lahan
    - Jarak 5-10 meter
    - Kombinasi beberapa jenis
    
    ### Konservasi Musuh Alami
    
    **DO:**
    - ✅ Tanam refugia
    - ✅ Hindari insektisida broad spectrum
    - ✅ Biarkan gulma berbunga di pematang
    - ✅ Sediakan habitat (mulsa, jerami)
    
    **DON'T:**
    - ❌ Semprot insektisida saat tidak perlu
    - ❌ Gunakan piretroid (bunuh semua serangga)
    - ❌ Bersihkan semua gulma
    
    ---
    
    ## 📋 Checklist PHT Harian
    
    **Setiap Hari:**
    - [ ] Keliling lahan pagi/sore
    - [ ] Amati kondisi tanaman
    - [ ] Cari gejala serangan
    
    **2-3 Kali/Minggu:**
    - [ ] Hitung populasi hama
    - [ ] Cek musuh alami
    - [ ] Catat di buku monitoring
    
    **Mingguan:**
    - [ ] Evaluasi perkembangan
    - [ ] Bandingkan dengan ambang ekonomi
    - [ ] Tentukan tindakan
    
    **Bulanan:**
    - [ ] Analisis tren
    - [ ] Evaluasi efektivitas pengendalian
    - [ ] Perbaiki strategi
    
    ---
    
    ## 💡 Tips Sukses PHT
    
    1. **Monitoring adalah Kunci**
       - Kenali hama/penyakit sejak dini
       - Kendalikan saat populasi masih rendah
    
    2. **Preventif Lebih Baik**
       - Varietas tahan + kultur teknis = 70% sukses
       - Lebih murah daripada kuratif
    
    3. **Jangan Bunuh Musuh Alami**
       - Laba-laba, kumbang, lacewing adalah teman
       - Mereka bekerja gratis 24/7
    
    4. **Kombinasi Metode**
       - Kultur teknis + hayati + nabati = optimal
       - Jangan andalkan satu metode saja
    
    5. **Sabar dan Konsisten**
       - PHT butuh waktu untuk stabil
       - Hasil jangka panjang lebih baik
    
    ---
    
    ## 🎓 Sekolah Lapang PHT
    
    **Bergabunglah dengan Sekolah Lapang PHT:**
    - Belajar bersama petani lain
    - Praktik langsung di lapangan
    - Didampingi penyuluh
    - Gratis!
    
    **Hubungi:** Penyuluh Pertanian Lapangan (PPL) di kecamatan Anda
    """)

# TAB 5: MONITORING GUIDE
with tab5:
    st.header("📖 Panduan Monitoring Hama & Penyakit")
    
    st.markdown("""
    ## 🔍 Teknik Monitoring
    
    ### 1. Visual Observation (Pengamatan Visual)
    
    **Cara:**
    - Keliling lahan secara sistematis
    - Amati tanaman dari atas, tengah, bawah
    - Perhatikan daun, batang, buah
    - Cari gejala tidak normal
    
    **Waktu Terbaik:**
    - Pagi (06:00-08:00) - embun masih ada, hama aktif
    - Sore (16:00-18:00) - hama mulai aktif
    
    **Frekuensi:**
    - Fase vegetatif: 2 kali/minggu
    - Fase generatif: 3 kali/minggu
    - Saat wabah: setiap hari
    
    ---
    
    ### 2. Sampling (Pengambilan Sampel)
    
    **Metode Diagonal:**
    ```
    X                   X
        X           X
            X   X
        X           X
    X                   X
    ```
    - Ambil 5-10 titik diagonal
    - Setiap titik: 5-10 tanaman
    - Total: 25-100 tanaman sampel
    
    **Metode Zigzag:**
    ```
    →→→→→
        ↓
    ←←←←←
    ↓
    →→→→→
    ```
    - Jalan zigzag
    - Ambil sampel setiap 10 langkah
    
    ---
    
    ### 3. Perangkap Monitoring
    
    **A. Perangkap Cahaya:**
    - Untuk ngengat (ulat grayak, penggerek)
    - Pasang 1-2 buah/ha
    - Nyalakan malam hari
    - Hitung tangkapan pagi hari
    
    **B. Perangkap Feromon:**
    - Untuk hama spesifik
    - Pasang 2-4 buah/ha
    - Ganti feromon setiap 4-6 minggu
    - Hitung tangkapan mingguan
    
    **C. Sticky Trap (Perangkap Lem):**
    - Kuning: untuk kutu daun, lalat putih
    - Biru: untuk thrips
    - Pasang 20-40 buah/ha
    - Ganti setiap 2 minggu
    
    ---
    
    ## 📊 Pencatatan Data
    
    ### Format Buku Monitoring
    
    | Tanggal | Lokasi | Hama/Penyakit | Populasi | Gejala | Tindakan | Keterangan |
    |---------|--------|---------------|----------|--------|----------|------------|
    | 1/12/24 | Blok A | Ulat grayak   | 1/tanaman| Daun berlubang | Belum | Di bawah AE |
    | 3/12/24 | Blok A | Ulat grayak   | 3/tanaman| Daun rusak 20% | Semprot nabati | Melebihi AE |
    
    **Data yang Dicatat:**
    - Tanggal pengamatan
    - Lokasi (blok/petak)
    - Jenis hama/penyakit
    - Populasi/intensitas
    - Gejala serangan
    - Tindakan yang diambil
    - Hasil tindakan
    
    ---
    
    ## 🎯 Menentukan Tindakan
    
    ### Decision Tree
    
    ```
    Temukan Hama/Penyakit
            ↓
    Hitung Populasi
            ↓
    ┌───────┴───────┐
    ↓               ↓
    < Ambang     ≥ Ambang
    Ekonomi      Ekonomi
    ↓               ↓
    MONITOR      KENDALIKAN
    TERUS           ↓
                Pilih Metode:
                1. Mekanis
                2. Hayati
                3. Nabati
                4. Kimia (terakhir)
    ```
    
    ---
    
    ## 📱 Tools Modern
    
    ### Aplikasi Mobile
    - Plantix - identifikasi penyakit
    - AgriApp - database hama
    - Pest Scout - monitoring digital
    
    ### Teknologi
    - Drone untuk survey lahan luas
    - Sensor IoT untuk monitoring otomatis
    - AI untuk identifikasi otomatis
    
    ---
    
    ## ⚠️ Tanda Bahaya
    
    **Segera Ambil Tindakan jika:**
    - 🚨 Populasi meningkat cepat (2x dalam 3 hari)
    - 🚨 Gejala menyebar ke >25% tanaman
    - 🚨 Tanaman mulai mati
    - 🚨 Fase kritis (pembungaan, pembuahan)
    
    ---
    
    ## 💡 Tips Monitoring Efektif
    
    1. **Konsisten**
       - Jadwal tetap
       - Jangan skip
       - Catat semua
    
    2. **Sistematis**
       - Rute yang sama
       - Metode yang sama
       - Data comparable
    
    3. **Teliti**
       - Periksa semua bagian tanaman
       - Jangan lewatkan gejala awal
       - Cek bawah daun
    
    4. **Dokumentasi**
       - Foto gejala
       - Catat detail
       - Arsip data
    
    5. **Kolaborasi**
       - Diskusi dengan petani lain
       - Konsultasi PPL
       - Ikut kelompok tani
    """)

# Footer
st.markdown("---")
st.caption("""
🐛 **Panduan Hama & Penyakit** - Database komprehensif untuk pengendalian terpadu

💡 **Integrasi dengan Modul Lain:**
- 🌿 **Pestisida Nabati** - 29 formula lengkap untuk pengendalian
- 💧 **Strategi Penyemprotan** - Jadwal dan teknik aplikasi
- 📚 **Pusat Pengetahuan** - Informasi pupuk dan nutrisi

⚠️ **Disclaimer:** Informasi ini bersifat edukatif. Sesuaikan dengan kondisi lokal dan konsultasikan dengan PPL untuk kasus spesifik.

🌱 **Prinsip PHT:** Preventif > Monitoring > Non-Kimia > Kimia (terakhir)

📚 **Referensi:** Balai Penelitian Tanaman, Kementerian Pertanian RI, FAO IPM Guidelines
""")
