# Pestisida Nabati - Database Lengkap
# Referensi: M-48 Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Pestisida Nabati", page_icon="🌿", layout="wide")

# ========== DATABASE PESTISIDA NABATI ==========

PESTISIDA_DATABASE = {
    # INSEKTISIDA NABATI
    "Ekstrak Daun Mimba (Neem)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat grayak", "Kutu daun", "Thrips", "Tungau", "Wereng", "Penggerek batang"],
        "target_tanaman": ["Padi", "Jagung", "Cabai", "Tomat", "Kubis", "Sayuran"],
        "bahan_aktif": "Azadirachtin",
        "mekanisme": "Sistemik - mengganggu hormon pertumbuhan serangga",
        "bahan": {
            "Daun mimba segar": "1 kg",
            "Air": "10 liter",
            "Detergen cair": "10 ml",
            "Alkohol 70% (opsional)": "100 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk atau blender daun mimba hingga halus",
            "2. Rendam dalam 10 L air + detergen",
            "3. Tambahkan alkohol untuk ekstraksi lebih baik (opsional)",
            "4. Diamkan 24 jam, aduk setiap 6 jam",
            "5. Saring dengan kain halus 2-3 kali",
            "6. Simpan di tempat gelap, tahan 1 minggu"
        ],
        "dosis_aplikasi": "Semprot langsung tanpa pengenceran",
        "volume_semprot": "400-600 L/ha atau 40-60 ml/tanaman",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Pagi (06:00-09:00) atau sore (15:00-18:00)",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "85-90% (sangat tinggi)",
        "kelebihan": [
            "Sistemik - masuk ke jaringan tanaman",
            "Efek jangka panjang (7-10 hari)",
            "Aman untuk musuh alami",
            "Tidak meninggalkan residu berbahaya"
        ],
        "kekurangan": [
            "Bau kurang sedap",
            "Perlu aplikasi rutin",
            "Efektivitas menurun jika terkena hujan"
        ],
        "tips": "Aplikasi sore hari lebih efektif. Tambahkan perekat (sabun) untuk hasil maksimal."
    },
    
    "Ekstrak Bawang Putih": {
        "kategori": "Insektisida + Fungisida",
        "target_hama": ["Kutu daun", "Thrips", "Tungau", "Bakteri", "Jamur patogen"],
        "target_tanaman": ["Cabai", "Tomat", "Kentang", "Bawang", "Sayuran daun"],
        "bahan_aktif": "Allicin (antibakteri & antijamur kuat)",
        "mekanisme": "Kontak - merusak sistem pernapasan serangga",
        "bahan": {
            "Bawang putih": "500 gram",
            "Air": "10 liter",
            "Minyak goreng": "50 ml",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Kupas dan haluskan bawang putih",
            "2. Rendam dalam 2 L air selama 24 jam",
            "3. Saring, tambahkan 8 L air",
            "4. Tambahkan minyak goreng + detergen",
            "5. Aduk rata hingga tercampur sempurna",
            "6. Siap digunakan (tahan 3-5 hari)"
        ],
        "dosis_aplikasi": "Encerkan 1:5 (1 L larutan + 5 L air)",
        "volume_semprot": "300-500 L/ha",
        "interval": "3-5 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "2 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Antibakteri sangat kuat",
            "Mudah didapat",
            "Harga terjangkau",
            "Efektif untuk penyakit bakteri"
        ],
        "kekurangan": [
            "Bau menyengat",
            "Efek jangka pendek (3-5 hari)",
            "Perlu aplikasi sering"
        ],
        "tips": "Kombinasi dengan cabai untuk efek maksimal. Aplikasi pagi lebih baik untuk fungisida."
    },
    
    "Ekstrak Cabai Rawit": {
        "kategori": "Insektisida (Repellent)",
        "target_hama": ["Ulat", "Belalang", "Kutu daun", "Penggerek buah", "Lalat buah"],
        "target_tanaman": ["Cabai", "Tomat", "Terong", "Mentimun", "Sayuran"],
        "bahan_aktif": "Capsaicin (iritan kuat)",
        "mekanisme": "Repellent - mengusir hama dengan rasa pedas",
        "bahan": {
            "Cabai rawit": "500 gram",
            "Air": "5 liter",
            "Detergen": "50 ml",
            "Bawang putih (opsional)": "100 gram"
        },
        "cara_pembuatan": [
            "1. Haluskan cabai rawit (gunakan sarung tangan!)",
            "2. Rebus dengan 5 L air selama 30 menit",
            "3. Dinginkan dan saring",
            "4. Tambahkan detergen sebagai perekat",
            "5. Aduk rata",
            "6. Siap digunakan (tahan 1 minggu)"
        ],
        "dosis_aplikasi": "Encerkan 1:3 (1 L larutan + 3 L air)",
        "volume_semprot": "400 L/ha",
        "interval": "5 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "1 hari sebelum panen",
        "efektivitas": "70-80%",
        "kelebihan": [
            "Efek repellent sangat kuat",
            "Murah dan mudah dibuat",
            "Aman untuk tanaman",
            "Bisa dikombinasi dengan pestisida lain"
        ],
        "kekurangan": [
            "Harus hati-hati saat pembuatan",
            "Bisa iritasi kulit dan mata",
            "Efek hilang jika terkena hujan"
        ],
        "tips": "WAJIB pakai sarung tangan dan masker! Jangan sentuh mata setelah membuat."
    },
    
    "Ekstrak Tembakau": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Kutu", "Thrips", "Wereng", "Penggerek"],
        "target_tanaman": ["Padi", "Jagung", "Sayuran (bukan untuk konsumsi langsung)"],
        "bahan_aktif": "Nikotin (racun saraf)",
        "mekanisme": "Kontak & sistemik - merusak sistem saraf serangga",
        "bahan": {
            "Tembakau kering": "200 gram",
            "Air": "5 liter",
            "Detergen": "25 ml",
            "Kapur sirih": "50 gram"
        },
        "cara_pembuatan": [
            "1. Rendam tembakau dalam air 48 jam",
            "2. Aduk setiap 12 jam",
            "3. Saring dengan kain halus",
            "4. Tambahkan kapur sirih (meningkatkan pH)",
            "5. Tambahkan detergen",
            "6. Aduk rata dan siap digunakan"
        ],
        "dosis_aplikasi": "Encerkan 1:2 (1 L larutan + 2 L air)",
        "volume_semprot": "300-400 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "14 hari sebelum panen (PENTING!)",
        "efektivitas": "85-95% (sangat tinggi)",
        "kelebihan": [
            "Sangat efektif",
            "Kontak dan sistemik",
            "Spektrum luas"
        ],
        "kekurangan": [
            "BERACUN untuk manusia",
            "Masa tunggu panen lama",
            "Berbahaya jika tertelan"
        ],
        "peringatan": "⚠️ BERACUN! Gunakan APD lengkap. JANGAN untuk sayuran menjelang panen!",
        "tips": "Hanya untuk tanaman pangan dengan masa tunggu panjang. Simpan di tempat aman."
    },
    
    "Ekstrak Daun Sirsak": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Kutu daun", "Penggerek buah", "Lalat buah"],
        "target_tanaman": ["Cabai", "Tomat", "Terong", "Buah-buahan"],
        "bahan_aktif": "Annonain (racun perut)",
        "mekanisme": "Racun perut - merusak sistem pencernaan",
        "bahan": {
            "Daun sirsak": "1 kg",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun sirsak hingga halus",
            "2. Rendam dalam 10 L air",
            "3. Diamkan 24 jam",
            "4. Saring 2 kali",
            "5. Tambahkan detergen",
            "6. Siap digunakan"
        ],
        "dosis_aplikasi": "Semprot langsung atau encerkan 1:2",
        "volume_semprot": "400 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Mudah didapat",
            "Aman untuk lingkungan",
            "Efektif untuk ulat"
        ],
        "kekurangan": [
            "Efek jangka pendek",
            "Perlu aplikasi rutin"
        ],
        "tips": "Kombinasi dengan mimba untuk hasil lebih baik."
    },
    
    "Pestisida Nabati Super (Formula Kombinasi)": {
        "kategori": "Insektisida + Fungisida (Spektrum Luas)",
        "target_hama": ["Semua hama umum", "Bakteri", "Jamur"],
        "target_tanaman": ["Semua tanaman"],
        "bahan_aktif": "Kombinasi azadirachtin, allicin, capsaicin",
        "mekanisme": "Multi-mode: sistemik, kontak, repellent",
        "bahan": {
            "Daun mimba": "500 gram",
            "Bawang putih": "250 gram",
            "Cabai rawit": "250 gram",
            "Lengkuas": "100 gram",
            "Jahe": "100 gram",
            "Kunyit": "100 gram",
            "Minyak goreng": "50 ml",
            "Detergen": "50 ml",
            "Air": "10 liter"
        },
        "cara_pembuatan": [
            "1. Haluskan semua bahan padat (kecuali daun mimba)",
            "2. Tumbuk daun mimba terpisah",
            "3. Campur semua bahan dalam 10 L air",
            "4. Diamkan 24 jam, aduk setiap 6 jam",
            "5. Saring 3 kali dengan kain halus",
            "6. Tambahkan minyak + detergen",
            "7. Aduk rata hingga tercampur sempurna"
        ],
        "dosis_aplikasi": "Encerkan 1:3 (1 L larutan + 3 L air)",
        "volume_semprot": "400-600 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "5 hari sebelum panen",
        "efektivitas": "90-95% (sangat tinggi)",
        "kelebihan": [
            "Spektrum sangat luas",
            "Efektivitas tinggi",
            "Tahan lama (7-10 hari)",
            "Multi-fungsi (insektisida + fungisida)"
        ],
        "kekurangan": [
            "Pembuatan lebih rumit",
            "Biaya lebih tinggi",
            "Bau sangat kuat"
        ],
        "tips": "Formula terbaik untuk pengendalian terpadu! Buat dalam jumlah banyak untuk efisiensi."
    },
    
    "Fermentasi Urine Sapi + Daun Pepaya": {
        "kategori": "Insektisida + Pupuk Cair",
        "target_hama": ["Ulat", "Penggerek", "Kutu", "Thrips"],
        "target_tanaman": ["Padi", "Jagung", "Sayuran"],
        "bahan_aktif": "Papain (enzim proteolitik) + Urea alami",
        "mekanisme": "Racun perut + nutrisi tanaman",
        "bahan": {
            "Urine sapi segar": "5 liter",
            "Daun pepaya": "1 kg",
            "Gula merah": "100 gram",
            "EM4 atau MOL": "50 ml"
        },
        "cara_pembuatan": [
            "1. Haluskan daun pepaya",
            "2. Campurkan dengan urine sapi",
            "3. Tambahkan gula merah (dilarutkan)",
            "4. Tambahkan EM4/MOL sebagai starter",
            "5. Masukkan wadah tertutup",
            "6. Fermentasi 7 hari (buka tutup setiap hari)",
            "7. Saring sebelum digunakan"
        ],
        "dosis_aplikasi": "Encerkan 1:10 (1 L larutan + 10 L air)",
        "volume_semprot": "300-500 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi",
        "masa_panen": "7 hari sebelum panen",
        "efektivitas": "70-80%",
        "kelebihan": [
            "Murah (bahan lokal)",
            "Bonus nutrisi untuk tanaman",
            "Efektif untuk ulat",
            "Meningkatkan pertumbuhan"
        ],
        "kekurangan": [
            "Bau sangat menyengat",
            "Proses fermentasi perlu waktu",
            "Harus saring dengan baik"
        ],
        "tips": "Urine sapi juga kaya nitrogen! Aplikasi pagi untuk menghindari bau siang hari."
    },
    
    # ========== TANAMAN DARI M-48 (20 PRIORITAS) ==========
    
    "Akar Tuba (Derris elliptica)": {
        "kategori": "Insektisida + Moluskisida + Nematisida",
        "nama_latin": "Derris elliptica (Wallich) Benth",
        "nama_daerah": "Tuba laut, Areuy ki tonggeret, Gadel, Ketower",
        "target_hama": ["Ulat pemakan daun", "Kutu daun", "Kutu kebul", "Keong mas", "Tungau"],
        "target_tanaman": ["Padi", "Sayuran", "Tanaman hias"],
        "bahan_aktif": "Rotenon, Deguelin, Elliptone, Toxicarol",
        "mekanisme": "Racun perut dan kontak - menyebabkan serangga berhenti makan",
        "bahan": {
            "Akar tuba": "1 kg",
            "Air": "20 liter",
            "Sabun/detergen": "1 sendok teh"
        },
        "cara_pembuatan": [
            "1. Hancurkan akar tuba dengan pisau/alat penumbuk",
            "2. Rendam dalam 20 liter air selama 3 hari",
            "3. Saring dengan kain halus",
            "4. Tambahkan sabun/detergen",
            "5. Aduk rata hingga tercampur sempurna"
        ],
        "dosis_aplikasi": "Semprot langsung ke seluruh bagian tanaman",
        "volume_semprot": "400-500 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore hari",
        "masa_panen": "7 hari sebelum panen",
        "efektivitas": "85-95% (sangat tinggi - spektrum luas)",
        "kelebihan": [
            "Spektrum sangat luas (insektisida + moluskisida + nematisida)",
            "Efektif untuk keong mas",
            "Kematian serangga beberapa jam sampai hari",
            "Bahan aktif rotenon sangat kuat"
        ],
        "kekurangan": [
            "Perlu waktu perendaman 3 hari",
            "Akar tuba tidak mudah didapat",
            "Beracun untuk ikan"
        ],
        "peringatan": "⚠️ BERACUN untuk ikan! Jangan gunakan dekat perairan. Gunakan APD lengkap.",
        "tips": "Sangat efektif untuk keong mas di sawah. Rendam yang cukup untuk ekstraksi rotenon maksimal."
    },
    
    "Bunga Piretrum (Chrysanthemum cinerariaefolium)": {
        "kategori": "Insektisida (Kontak Cepat)",
        "target_hama": ["Lalat", "Nyamuk", "Kutu", "Thrips", "Ulat", "Kecoa"],
        "target_tanaman": ["Semua tanaman", "Penggunaan rumah tangga"],
        "bahan_aktif": "Pyrethrin (insektisida alami paling kuat)",
        "mekanisme": "Racun kontak - menyerang sistem saraf pusat serangga",
        "bahan": {
            "Bunga piretrum kering": "100 gram",
            "Air": "10 liter",
            "Alkohol 70%": "200 ml",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Keringkan bunga piretrum di tempat teduh",
            "2. Tumbuk bunga kering hingga halus",
            "3. Rendam dalam alkohol 70% selama 24 jam",
            "4. Tambahkan air 10 liter",
            "5. Saring dan tambahkan detergen",
            "6. Aduk rata"
        ],
        "dosis_aplikasi": "Semprot langsung atau encerkan 1:2",
        "volume_semprot": "300-400 L/ha",
        "interval": "3-5 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "1 hari sebelum panen",
        "efektivitas": "95-100% (sangat tinggi - knock down cepat)",
        "kelebihan": [
            "Efek knock down sangat cepat (menit)",
            "Aman untuk mamalia",
            "Tidak meninggalkan residu berbahaya",
            "Bisa untuk penggunaan rumah tangga"
        ],
        "kekurangan": [
            "Bunga piretrum mahal dan langka",
            "Tidak stabil di cahaya matahari",
            "Efek jangka pendek"
        ],
        "tips": "Piretrum adalah insektisida nabati terkuat! Aplikasi sore hari untuk menghindari degradasi cahaya."
    },
    
    "Mahoni (Swietenia mahagoni)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Penggerek batang", "Penggerek buah", "Wereng"],
        "target_tanaman": ["Padi", "Jagung", "Sayuran"],
        "bahan_aktif": "Swietenin, Saponin",
        "mekanisme": "Racun perut - mengganggu sistem pencernaan",
        "bahan": {
            "Biji mahoni": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Keringkan biji mahoni",
            "2. Tumbuk/blender hingga halus",
            "3. Rendam dalam 10 L air selama 24 jam",
            "4. Saring 2-3 kali",
            "5. Tambahkan detergen",
            "6. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:3",
        "volume_semprot": "400 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "5 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Biji mudah didapat",
            "Efektif untuk penggerek",
            "Tahan lama (7-10 hari)"
        ],
        "kekurangan": [
            "Perlu penumbukan halus",
            "Bau agak kuat"
        ],
        "tips": "Biji mahoni banyak di taman kota. Tumbuk halus untuk ekstraksi maksimal."
    },
    
    "Mindi (Melia azedarach)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Belalang", "Kutu daun", "Thrips"],
        "target_tanaman": ["Sayuran", "Padi", "Jagung"],
        "bahan_aktif": "Azadirachtin (mirip mimba)",
        "mekanisme": "Sistemik - mengganggu hormon pertumbuhan",
        "bahan": {
            "Daun mindi": "1 kg",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun mindi segar",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Semprot langsung",
        "volume_semprot": "400-500 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Sore hari",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "80-90%",
        "kelebihan": [
            "Mirip mimba tapi lebih mudah didapat",
            "Efek sistemik",
            "Aman untuk musuh alami"
        ],
        "kekurangan": [
            "Bau kurang sedap",
            "Perlu aplikasi rutin"
        ],
        "tips": "Alternatif bagus untuk mimba. Pohon mindi banyak di pinggir jalan."
    },
    
    "Serai Wangi (Cymbopogon nardus)": {
        "kategori": "Insektisida (Repellent)",
        "target_hama": ["Nyamuk", "Lalat", "Kutu", "Thrips"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Citronella oil (minyak atsiri)",
        "mekanisme": "Repellent - mengusir serangga dengan aroma",
        "bahan": {
            "Batang serai": "1 kg",
            "Air": "10 liter",
            "Minyak goreng": "50 ml",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Iris tipis batang serai",
            "2. Rebus dengan 10 L air selama 30 menit",
            "3. Dinginkan dan saring",
            "4. Tambahkan minyak + detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:5",
        "volume_semprot": "300-400 L/ha",
        "interval": "3-5 hari",
        "waktu_aplikasi": "Sore hari",
        "masa_panen": "1 hari sebelum panen",
        "efektivitas": "70-80% (repellent)",
        "kelebihan": [
            "Aroma wangi",
            "Mudah didapat",
            "Aman untuk manusia",
            "Bisa untuk pengusir nyamuk"
        ],
        "kekurangan": [
            "Efek jangka pendek",
            "Perlu aplikasi sering",
            "Lebih sebagai repellent"
        ],
        "tips": "Sangat bagus untuk pengusir nyamuk dan lalat. Tanam di sekitar rumah untuk perlindungan alami."
    },
    
    "Jarak (Ricinus communis)": {
        "kategori": "Insektisida + Moluskisida",
        "target_hama": ["Ulat", "Penggerek", "Keong", "Siput"],
        "target_tanaman": ["Sayuran", "Padi", "Palawija"],
        "bahan_aktif": "Ricin (racun protein)",
        "mekanisme": "Racun perut - sangat toksik",
        "bahan": {
            "Biji jarak": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk biji jarak hingga halus",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring dengan kain halus",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:5",
        "volume_semprot": "300-400 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "14 hari sebelum panen",
        "efektivitas": "85-90%",
        "kelebihan": [
            "Sangat efektif",
            "Mudah didapat",
            "Efektif untuk keong"
        ],
        "kekurangan": [
            "SANGAT BERACUN untuk manusia",
            "Masa tunggu panen lama",
            "Berbahaya jika tertelan"
        ],
        "peringatan": "⚠️ SANGAT BERACUN! Gunakan APD lengkap. Jangan untuk sayuran menjelang panen!",
        "tips": "Ricin sangat toksik! Hanya untuk tanaman dengan masa tunggu panjang."
    },
    
    "Mengkudu (Morinda citrifolia)": {
        "kategori": "Insektisida + Fungisida",
        "target_hama": ["Ulat", "Kutu daun", "Jamur", "Bakteri"],
        "target_tanaman": ["Sayuran", "Buah-buahan"],
        "bahan_aktif": "Anthraquinone",
        "mekanisme": "Racun perut + antijamur",
        "bahan": {
            "Buah mengkudu": "1 kg",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Haluskan buah mengkudu matang",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:3",
        "volume_semprot": "400 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Multi-fungsi (insektisida + fungisida)",
            "Mudah didapat",
            "Aman untuk lingkungan"
        ],
        "kekurangan": [
            "Bau sangat menyengat",
            "Perlu aplikasi rutin"
        ],
        "tips": "Bau mengkudu sangat kuat tapi efektif! Aplikasi sore hari."
    },
    
    "Kelor (Moringa oleifera)": {
        "kategori": "Insektisida + Nutrisi",
        "target_hama": ["Ulat", "Kutu daun", "Thrips"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Pterygospermin",
        "mekanisme": "Racun kontak + bonus nutrisi",
        "bahan": {
            "Daun kelor": "1 kg",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun kelor segar",
            "2. Rendam dalam 10 L air 12 jam",
            "3. Saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Semprot langsung",
        "volume_semprot": "400-500 L/ha",
        "interval": "5 hari",
        "waktu_aplikasi": "Pagi",
        "masa_panen": "2 hari sebelum panen",
        "efektivitas": "70-80%",
        "kelebihan": [
            "Bonus nutrisi untuk tanaman",
            "Mudah didapat",
            "Aman",
            "Meningkatkan pertumbuhan"
        ],
        "kekurangan": [
            "Efektivitas sedang",
            "Perlu aplikasi sering"
        ],
        "tips": "Kelor kaya nutrisi! Selain pestisida, juga pupuk cair."
    },
    
    "Cengkeh (Syzygium aromaticum)": {
        "kategori": "Insektisida + Fungisida",
        "target_hama": ["Lalat", "Nyamuk", "Kutu", "Jamur"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Eugenol (minyak atsiri)",
        "mekanisme": "Racun kontak + repellent",
        "bahan": {
            "Cengkeh kering": "100 gram",
            "Air": "10 liter",
            "Alkohol 70%": "100 ml",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk cengkeh halus",
            "2. Rendam dalam alkohol 24 jam",
            "3. Tambahkan 10 L air",
            "4. Saring dan tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:5",
        "volume_semprot": "300-400 L/ha",
        "interval": "5 hari",
        "waktu_aplikasi": "Sore hari",
        "masa_panen": "2 hari sebelum panen",
        "efektivitas": "80-85%",
        "kelebihan": [
            "Aroma wangi",
            "Efektif untuk lalat dan nyamuk",
            "Antijamur kuat"
        ],
        "kekurangan": [
            "Harga cengkeh mahal",
            "Efek jangka pendek"
        ],
        "tips": "Eugenol sangat efektif! Bisa untuk pengusir nyamuk rumah tangga."
    },
    
    "Jahe (Zingiber officinale)": {
        "kategori": "Fungisida + Bakterisida",
        "target_hama": ["Jamur", "Bakteri", "Nematoda"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Gingerol, Zingeron",
        "mekanisme": "Antijamur + antibakteri",
        "bahan": {
            "Jahe segar": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Parut atau blender jahe",
            "2. Rebus dengan 10 L air 30 menit",
            "3. Dinginkan dan saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:3",
        "volume_semprot": "400 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Pagi",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Antijamur kuat",
            "Mudah didapat",
            "Aman",
            "Aroma segar"
        ],
        "kekurangan": [
            "Perlu perebusan",
            "Efek jangka pendek"
        ],
        "tips": "Kombinasi dengan kunyit untuk fungisida super kuat!"
    },
    
    "Brotowali (Tinospora rumphii)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Kutu daun", "Wereng"],
        "target_tanaman": ["Padi", "Sayuran"],
        "bahan_aktif": "Alkaloid",
        "mekanisme": "Racun perut",
        "bahan": {
            "Batang brotowali": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Potong-potong batang brotowali",
            "2. Rebus dengan 10 L air 30 menit",
            "3. Dinginkan dan saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:2",
        "volume_semprot": "400 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "5 hari sebelum panen",
        "efektivitas": "75-80%",
        "kelebihan": [
            "Efektif untuk wereng",
            "Tahan lama",
            "Mudah didapat"
        ],
        "kekurangan": [
            "Rasa pahit sangat kuat",
            "Perlu perebusan"
        ],
        "tips": "Brotowali sangat pahit - efektif sebagai racun perut!"
    },
    
    "Lidah Buaya (Aloe barbadensis)": {
        "kategori": "Fungisida + Bakterisida",
        "target_hama": ["Jamur", "Bakteri", "Virus"],
        "target_tanaman": ["Sayuran", "Buah-buahan"],
        "bahan_aktif": "Aloin, Saponin",
        "mekanisme": "Antijamur + antibakteri + meningkatkan imunitas",
        "bahan": {
            "Gel lidah buaya": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Ambil gel lidah buaya",
            "2. Blender dengan 2 L air",
            "3. Tambahkan 8 L air",
            "4. Saring dan tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:5",
        "volume_semprot": "300-400 L/ha",
        "interval": "5 hari",
        "waktu_aplikasi": "Pagi",
        "masa_panen": "1 hari sebelum panen",
        "efektivitas": "70-80%",
        "kelebihan": [
            "Meningkatkan imunitas tanaman",
            "Aman",
            "Multi-fungsi",
            "Bisa untuk luka tanaman"
        ],
        "kekurangan": [
            "Perlu banyak lidah buaya",
            "Efek jangka pendek"
        ],
        "tips": "Lidah buaya meningkatkan ketahanan tanaman! Aplikasi preventif sangat baik."
    },
    
    "Sirih (Piper betle)": {
        "kategori": "Fungisida + Bakterisida",
        "target_hama": ["Jamur", "Bakteri", "Virus"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Kavikol, Fenol",
        "mekanisme": "Antibakteri + antijamur kuat",
        "bahan": {
            "Daun sirih": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Rebus daun sirih dengan 10 L air 30 menit",
            "2. Dinginkan dan saring",
            "3. Tambahkan detergen",
            "4. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:3",
        "volume_semprot": "400 L/ha",
        "interval": "5 hari",
        "waktu_aplikasi": "Pagi",
        "masa_panen": "2 hari sebelum panen",
        "efektivitas": "80-85%",
        "kelebihan": [
            "Antibakteri sangat kuat",
            "Mudah didapat",
            "Aroma segar",
            "Aman"
        ],
        "kekurangan": [
            "Perlu perebusan",
            "Efek jangka pendek"
        ],
        "tips": "Sirih sangat efektif untuk penyakit bakteri! Kombinasi dengan bawang putih."
    },
    
    "Sambiloto (Andrographis paniculata)": {
        "kategori": "Insektisida + Fungisida",
        "target_hama": ["Ulat", "Kutu daun", "Jamur"],
        "target_tanaman": ["Sayuran", "Tanaman obat"],
        "bahan_aktif": "Andrographolide",
        "mekanisme": "Racun perut + antijamur",
        "bahan": {
            "Daun sambiloto": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun sambiloto",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:2",
        "volume_semprot": "400 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "5 hari sebelum panen",
        "efektivitas": "75-80%",
        "kelebihan": [
            "Rasa pahit kuat (racun perut)",
            "Antijamur",
            "Mudah dibudidayakan"
        ],
        "kekurangan": [
            "Perlu waktu perendaman",
            "Tidak mudah didapat"
        ],
        "tips": "Sambiloto sangat pahit - efektif sebagai racun perut!"
    },
    
    "Selasih (Ocimum basilicum)": {
        "kategori": "Insektisida (Repellent)",
        "target_hama": ["Lalat", "Nyamuk", "Kutu", "Thrips"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Eugenol, Linalool (minyak atsiri)",
        "mekanisme": "Repellent - mengusir serangga",
        "bahan": {
            "Daun selasih": "500 gram",
            "Air": "10 liter",
            "Minyak goreng": "50 ml",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun selasih segar",
            "2. Rendam dalam 10 L air 12 jam",
            "3. Saring",
            "4. Tambahkan minyak + detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:5",
        "volume_semprot": "300-400 L/ha",
        "interval": "3-5 hari",
        "waktu_aplikasi": "Sore hari",
        "masa_panen": "1 hari sebelum panen",
        "efektivitas": "70-75% (repellent)",
        "kelebihan": [
            "Aroma sangat wangi",
            "Aman",
            "Mudah dibudidayakan",
            "Bisa untuk pengusir nyamuk"
        ],
        "kekurangan": [
            "Efek jangka pendek",
            "Lebih sebagai repellent"
        ],
        "tips": "Tanam selasih di sekitar kebun untuk perlindungan alami!"
    },
    
    "Kenikir (Tagetes erecta)": {
        "kategori": "Insektisida + Nematisida",
        "target_hama": ["Kutu daun", "Thrips", "Nematoda", "Lalat putih"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Thiophene (akar), Limonene (daun)",
        "mekanisme": "Racun kontak + repellent + nematisida",
        "bahan": {
            "Daun dan bunga kenikir": "1 kg",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun dan bunga kenikir",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Semprot langsung",
        "volume_semprot": "400 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Efektif untuk nematoda",
            "Mudah dibudidayakan",
            "Aroma kuat (repellent)",
            "Bisa sebagai tanaman pengiring"
        ],
        "kekurangan": [
            "Bau kurang sedap",
            "Perlu aplikasi rutin"
        ],
        "tips": "Tanam kenikir sebagai tanaman pengiring untuk pengendalian nematoda!"
    },
    
    "Srikaya (Annona squamosa)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Kutu daun", "Penggerek"],
        "target_tanaman": ["Sayuran", "Buah-buahan"],
        "bahan_aktif": "Annonacin (mirip sirsak)",
        "mekanisme": "Racun perut",
        "bahan": {
            "Biji srikaya": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Keringkan dan tumbuk biji srikaya",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring 2 kali",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:2",
        "volume_semprot": "400 L/ha",
        "interval": "7 hari",
        "waktu_aplikasi": "Pagi atau sore",
        "masa_panen": "5 hari sebelum panen",
        "efektivitas": "75-85%",
        "kelebihan": [
            "Efektif untuk ulat",
            "Biji mudah didapat",
            "Tahan lama"
        ],
        "kekurangan": [
            "Perlu penumbukan halus",
            "Waktu perendaman lama"
        ],
        "tips": "Mirip sirsak tapi dari biji. Tumbuk halus untuk ekstraksi maksimal."
    },
    
    "Duku (Lansium domesticum)": {
        "kategori": "Insektisida",
        "target_hama": ["Nyamuk", "Lalat", "Kutu"],
        "target_tanaman": ["Sayuran", "Tanaman hias"],
        "bahan_aktif": "Lansic acid",
        "mekanisme": "Racun kontak + repellent",
        "bahan": {
            "Kulit duku": "500 gram",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Keringkan kulit duku",
            "2. Bakar kulit duku (asap untuk nyamuk) atau",
            "3. Rebus dengan 10 L air 30 menit",
            "4. Saring dan tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Encerkan 1:3",
        "volume_semprot": "300-400 L/ha",
        "interval": "5 hari",
        "waktu_aplikasi": "Sore hari",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "70-80%",
        "kelebihan": [
            "Asap kulit duku efektif untuk nyamuk",
            "Mudah didapat saat musim",
            "Aroma khas"
        ],
        "kekurangan": [
            "Hanya musiman",
            "Perlu pengeringan"
        ],
        "tips": "Bakar kulit duku kering untuk pengusir nyamuk alami!"
    },
    
    "Suren (Toona sureni)": {
        "kategori": "Insektisida",
        "target_hama": ["Ulat", "Penggerek", "Kutu daun"],
        "target_tanaman": ["Sayuran", "Tanaman kehutanan"],
        "bahan_aktif": "Toosendanin (mirip mimba)",
        "mekanisme": "Sistemik - mengganggu hormon",
        "bahan": {
            "Daun suren": "1 kg",
            "Air": "10 liter",
            "Detergen": "20 ml"
        },
        "cara_pembuatan": [
            "1. Tumbuk daun suren segar",
            "2. Rendam dalam 10 L air 24 jam",
            "3. Saring",
            "4. Tambahkan detergen",
            "5. Aduk rata"
        ],
        "dosis_aplikasi": "Semprot langsung",
        "volume_semprot": "400-500 L/ha",
        "interval": "5-7 hari",
        "waktu_aplikasi": "Sore hari",
        "masa_panen": "3 hari sebelum panen",
        "efektivitas": "80-90%",
        "kelebihan": [
            "Mirip mimba (family Meliaceae)",
            "Efek sistemik",
            "Aman untuk musuh alami"
        ],
        "kekurangan": [
            "Tidak mudah didapat",
            "Bau kurang sedap"
        ],
        "tips": "Suren adalah alternatif mimba yang bagus! Pohon besar di hutan."
    }
}

# FUNGISIDA NABATI
FUNGISIDA_DATABASE = {
    "Ekstrak Kunyit": {
        "kategori": "Fungisida",
        "target_penyakit": ["Busuk daun", "Bercak daun", "Layu fusarium", "Antraknosa"],
        "target_tanaman": ["Cabai", "Tomat", "Kentang", "Sayuran"],
        "bahan_aktif": "Curcumin (antijamur)",
        "bahan": {
            "Kunyit segar": "500 gram",
            "Air": "5 liter",
            "Detergen": "25 ml"
        },
        "cara_pembuatan": [
            "1. Parut atau blender kunyit",
            "2. Rebus dengan 5 L air selama 30 menit",
            "3. Dinginkan dan saring",
            "4. Tambahkan detergen",
            "5. Siap digunakan"
        ],
        "dosis_aplikasi": "Encerkan 1:5",
        "interval": "5 hari",
        "efektivitas": "70-80%",
        "tips": "Aplikasi preventif lebih efektif. Kombinasi dengan bawang putih untuk hasil maksimal."
    },
    
    "Ekstrak Lengkuas": {
        "kategori": "Fungisida + Bakterisida",
        "target_penyakit": ["Busuk batang", "Hawar daun bakteri", "Layu bakteri"],
        "target_tanaman": ["Padi", "Cabai", "Tomat"],
        "bahan_aktif": "Galangin (antibakteri)",
        "bahan": {
            "Lengkuas": "500 gram",
            "Air": "5 liter",
            "Detergen": "25 ml"
        },
        "cara_pembuatan": [
            "1. Iris tipis lengkuas",
            "2. Rebus dengan air 30 menit",
            "3. Dinginkan dan saring",
            "4. Tambahkan detergen",
            "5. Siap digunakan"
        ],
        "dosis_aplikasi": "Encerkan 1:3",
        "interval": "5-7 hari",
        "efektivitas": "75-85%",
        "tips": "Sangat efektif untuk penyakit bakteri. Aplikasi saat gejala awal."
    }
}

# ========== HELPER FUNCTIONS ==========
def calculate_dosage(luas_lahan, volume_per_ha, konsentrasi):
    """Kalkulator dosis pestisida"""
    total_volume = (luas_lahan / 10000) * volume_per_ha
    volume_pestisida = total_volume / (konsentrasi + 1)
    volume_air = total_volume - volume_pestisida
    return total_volume, volume_pestisida, volume_air

# ========== MAIN APP ==========
st.title("🌿 Pestisida Nabati - Database Lengkap")
st.markdown("**Referensi: M-48 Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya**")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Cari Berdasarkan Hama",
    "📚 Database Lengkap",
    "🧮 Kalkulator Dosis",
    "📖 Panduan Aplikasi"
])

# TAB 1: SEARCH BY PEST
with tab1:
    st.header("🔍 Cari Pestisida Berdasarkan Hama")
    
    # Collect all unique pests
    all_pests = set()
    for data in PESTISIDA_DATABASE.values():
        all_pests.update(data['target_hama'])
    
    selected_pest = st.selectbox(
        "Pilih Hama yang Ingin Dikendalikan:",
        sorted(list(all_pests))
    )
    
    if selected_pest:
        st.subheader(f"Pestisida untuk: **{selected_pest}**")
        
        # Find matching pesticides
        matches = []
        for nama, data in PESTISIDA_DATABASE.items():
            if selected_pest in data['target_hama']:
                matches.append((nama, data))
        
        if matches:
            for nama, data in matches:
                with st.expander(f"**{nama}** - Efektivitas: {data['efektivitas']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Kategori:** {data['kategori']}")
                        st.markdown(f"**Bahan Aktif:** {data['bahan_aktif']}")
                        st.markdown(f"**Mekanisme:** {data['mekanisme']}")
                        
                        st.markdown("**Bahan:**")
                        for bahan, jumlah in data['bahan'].items():
                            st.markdown(f"- {bahan}: {jumlah}")
                    
                    with col2:
                        st.markdown(f"**Dosis:** {data['dosis_aplikasi']}")
                        st.markdown(f"**Interval:** {data['interval']}")
                        st.markdown(f"**Masa Panen:** {data['masa_panen']}")
                        
                        st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
                    
                    st.markdown("**Cara Pembuatan:**")
                    for step in data['cara_pembuatan']:
                        st.markdown(step)
                    
                    st.info(f"💡 **Tips:** {data['tips']}")
                    
                    if 'peringatan' in data:
                        st.error(data['peringatan'])

# TAB 2: FULL DATABASE
with tab2:
    st.header("📚 Database Pestisida Nabati Lengkap")
    
    # Category filter
    category_filter = st.radio(
        "Filter Kategori:",
        ["Semua", "Insektisida", "Fungisida", "Kombinasi"],
        horizontal=True
    )
    
    # Search
    search_term = st.text_input("🔍 Cari pestisida...", "")
    
    # Display all pesticides
    st.subheader("Insektisida Nabati")
    for nama, data in PESTISIDA_DATABASE.items():
        if search_term.lower() in nama.lower() or search_term == "":
            if category_filter == "Semua" or category_filter in data['kategori']:
                with st.expander(f"**{nama}**"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**Kategori:** {data['kategori']}")
                        st.markdown(f"**Efektivitas:** {data['efektivitas']}")
                        st.markdown(f"**Target Hama:**")
                        for hama in data['target_hama']:
                            st.markdown(f"- {hama}")
                    
                    with col2:
                        st.markdown("**Bahan:**")
                        for bahan, jumlah in data['bahan'].items():
                            st.markdown(f"- {bahan}: {jumlah}")
                    
                    with col3:
                        st.markdown(f"**Dosis:** {data['dosis_aplikasi']}")
                        st.markdown(f"**Interval:** {data['interval']}")
                        st.markdown(f"**Masa Panen:** {data['masa_panen']}")
                    
                    st.markdown("**Cara Pembuatan:**")
                    for i, step in enumerate(data['cara_pembuatan'], 1):
                        st.markdown(step)
                    
                    st.success("**Kelebihan:**\n" + "\n".join([f"✅ {k}" for k in data['kelebihan']]))
                    st.warning("**Kekurangan:**\n" + "\n".join([f"⚠️ {k}" for k in data['kekurangan']]))
                    st.info(f"💡 **Tips:** {data['tips']}")
                    
                    if 'peringatan' in data:
                        st.error(data['peringatan'])
    
    st.subheader("Fungisida Nabati")
    for nama, data in FUNGISIDA_DATABASE.items():
        if search_term.lower() in nama.lower() or search_term == "":
            with st.expander(f"**{nama}**"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Target Penyakit:**")
                    for penyakit in data['target_penyakit']:
                        st.markdown(f"- {penyakit}")
                    
                    st.markdown("**Bahan:**")
                    for bahan, jumlah in data['bahan'].items():
                        st.markdown(f"- {bahan}: {jumlah}")
                
                with col2:
                    st.markdown(f"**Dosis:** {data['dosis_aplikasi']}")
                    st.markdown(f"**Interval:** {data['interval']}")
                    st.markdown(f"**Efektivitas:** {data['efektivitas']}")
                
                st.markdown("**Cara Pembuatan:**")
                for step in data['cara_pembuatan']:
                    st.markdown(step)
                
                st.info(f"💡 **Tips:** {data['tips']}")

# TAB 3: DOSAGE CALCULATOR
with tab3:
    st.header("🧮 Kalkulator Dosis Pestisida")
    
    col1, col2 = st.columns(2)
    
    with col1:
        luas_lahan = st.number_input(
            "Luas Lahan (m²)",
            min_value=1,
            max_value=100000,
            value=1000,
            step=100
        )
        
        volume_per_ha = st.number_input(
            "Volume Semprot per Hektar (L/ha)",
            min_value=100,
            max_value=1000,
            value=400,
            step=50,
            help="Umumnya 300-600 L/ha"
        )
    
    with col2:
        konsentrasi = st.selectbox(
            "Konsentrasi Pengenceran",
            ["Tanpa pengenceran (1:0)", "1:2", "1:3", "1:5", "1:10"],
            index=2
        )
        
        # Parse concentration
        if "Tanpa" in konsentrasi:
            ratio = 0
        else:
            ratio = int(konsentrasi.split(":")[1])
    
    if st.button("💧 Hitung Dosis", type="primary"):
        total, pestisida, air = calculate_dosage(luas_lahan, volume_per_ha, ratio)
        
        st.success("### 📊 Hasil Perhitungan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Volume", f"{total:.1f} L")
        
        with col2:
            st.metric("Larutan Pestisida", f"{pestisida:.1f} L")
        
        with col3:
            st.metric("Air Pengencer", f"{air:.1f} L")
        
        st.info(f"""
        **Cara Aplikasi:**
        1. Siapkan {pestisida:.1f} L larutan pestisida nabati
        2. Tambahkan {air:.1f} L air bersih
        3. Aduk rata
        4. Semprotkan ke seluruh lahan ({luas_lahan} m²)
        5. Volume semprot: {total:.1f} L
        """)
        
        # Estimasi biaya (contoh)
        st.markdown("---")
        st.markdown("### 💰 Estimasi Biaya (Contoh)")
        
        # Contoh harga bahan
        harga_bahan = {
            "Daun mimba": 5000,
            "Bawang putih": 40000,
            "Cabai rawit": 50000,
            "Detergen": 15000
        }
        
        st.markdown("""
        **Estimasi biaya untuk 10 L larutan:**
        - Daun mimba (1 kg): Rp 5,000
        - Detergen (10 ml): Rp 150
        - **Total: Rp 5,150 untuk 10 L**
        - **Biaya per liter: Rp 515**
        """)
        
        biaya_total = (pestisida / 10) * 5150
        st.success(f"**Estimasi biaya untuk {pestisida:.1f} L: Rp {biaya_total:,.0f}**")

# TAB 4: APPLICATION GUIDE
with tab4:
    st.header("📖 Panduan Aplikasi Pestisida Nabati")
    
    st.markdown("""
    ## ⚠️ Keamanan dan Keselamatan
    
    **Alat Pelindung Diri (APD) yang Harus Digunakan:**
    - ✅ Masker atau respirator
    - ✅ Sarung tangan karet
    - ✅ Baju lengan panjang
    - ✅ Celana panjang
    - ✅ Sepatu boot
    - ✅ Kacamata pelindung (untuk pestisida iritan)
    
    **JANGAN:**
    - ❌ Makan, minum, atau merokok saat aplikasi
    - ❌ Menyemprot melawan arah angin
    - ❌ Aplikasi saat hujan atau akan hujan
    - ❌ Menyimpan pestisida di wadah makanan/minuman
    
    ---
    
    ## 🕐 Waktu Aplikasi Terbaik
    
    **Pagi (06:00 - 09:00):**
    - ✅ Stomata daun terbuka (untuk sistemik)
    - ✅ Angin tenang
    - ✅ Embun sudah kering
    - ✅ Cocok untuk fungisida
    
    **Sore (15:00 - 18:00):**
    - ✅ Suhu lebih rendah
    - ✅ Penguapan minimal
    - ✅ Cocok untuk insektisida
    - ✅ Hama mulai aktif
    
    **HINDARI:**
    - ❌ Siang hari (10:00 - 14:00) - penguapan tinggi
    - ❌ Saat hujan atau mendung
    - ❌ Saat angin kencang
    
    ---
    
    ## 💧 Teknik Penyemprotan
    
    **1. Persiapan:**
    - Kalibrasi sprayer
    - Pastikan nozzle tidak tersumbat
    - Siapkan larutan sesuai dosis
    
    **2. Cara Semprot:**
    - Jarak nozzle ke tanaman: 30-50 cm
    - Semprot merata ke seluruh bagian tanaman
    - **Fokus pada bagian bawah daun** (tempat hama bersembunyi)
    - Semprot hingga basah merata (tidak sampai menetes)
    
    **3. Pola Penyemprotan:**
    - Mulai dari tepi lahan
    - Bergerak mundur (jangan melawan arah semprot)
    - Overlap 20-30% antar jalur
    
    ---
    
    ## 📅 Jadwal Aplikasi
    
    **Program Pencegahan (Preventif):**
    - Aplikasi rutin setiap 7-10 hari
    - Mulai sejak tanaman muda
    - Konsentrasi lebih rendah
    
    **Program Pengendalian (Kuratif):**
    - Aplikasi setiap 3-5 hari
    - Saat populasi hama tinggi
    - Konsentrasi lebih tinggi
    
    **Rotasi Pestisida:**
    - Ganti jenis pestisida setiap 2-3 aplikasi
    - Hindari resistensi hama
    - Kombinasikan berbagai bahan aktif
    
    ---
    
    ## 🔄 Masa Tunggu Panen (PHI - Pre-Harvest Interval)
    
    | Pestisida | Masa Tunggu |
    |-----------|-------------|
    | Daun Mimba | 3 hari |
    | Bawang Putih | 2 hari |
    | Cabai Rawit | 1 hari |
    | **Tembakau** | **14 hari** ⚠️ |
    | Formula Kombinasi | 5 hari |
    | Urine Sapi + Pepaya | 7 hari |
    
    ---
    
    ## 📦 Penyimpanan
    
    **Cara Simpan yang Benar:**
    - Wadah tertutup rapat
    - Tempat gelap dan sejuk
    - Jauh dari jangkauan anak-anak
    - Beri label jelas
    - Pisahkan dari bahan makanan
    
    **Masa Simpan:**
    - Ekstrak segar: 3-7 hari
    - Ekstrak fermentasi: 1-2 minggu
    - Simpan di kulkas untuk tahan lebih lama
    
    ---
    
    ## ✅ Tips Meningkatkan Efektivitas
    
    1. **Tambahkan Perekat:**
       - Detergen cair 10-20 ml/10L
       - Sabun colek 1 sendok/10L
       - Minyak goreng 50 ml/10L
    
    2. **Kombinasi Pestisida:**
       - Mimba + Bawang putih (insektisida + fungisida)
       - Cabai + Bawang putih (repellent kuat)
       - Kunyit + Lengkuas (fungisida kuat)
    
    3. **Aplikasi Bersamaan dengan Pupuk Cair:**
       - Tambahkan POC/MOL 100 ml/L
       - Bonus nutrisi untuk tanaman
       - Meningkatkan ketahanan tanaman
    
    4. **Monitoring Rutin:**
       - Cek tanaman setiap 2-3 hari
       - Catat populasi hama
       - Evaluasi efektivitas
    
    ---
    
    ## 🌱 Pengendalian Hama Terpadu (PHT)
    
    Pestisida nabati paling efektif jika dikombinasikan dengan:
    
    1. **Kultur Teknis:**
       - Sanitasi lahan
       - Rotasi tanaman
       - Varietas tahan hama
    
    2. **Pengendalian Fisik:**
       - Perangkap kuning/biru
       - Mulsa plastik
       - Jaring serangga
    
    3. **Pengendalian Biologis:**
       - Musuh alami (predator)
       - Parasitoid
       - Agen hayati
    
    4. **Pestisida Nabati:**
       - Sebagai pelengkap
       - Aplikasi saat diperlukan
       - Rotasi bahan aktif
    """)

# Footer
st.markdown("---")
st.caption("""
🌿 **Pestisida Nabati** - Referensi: M-48 Tumbuhan Bahan Pestisida Nabati dan Cara Pembuatannya

⚠️ **Disclaimer:** Informasi ini bersifat edukatif. Selalu lakukan uji coba skala kecil terlebih dahulu. 
Konsultasikan dengan PPL atau ahli pertanian untuk kasus spesifik.

💡 **Tips:** Pestisida nabati paling efektif untuk pencegahan. Aplikasi rutin sejak dini lebih baik daripada pengendalian saat serangan berat!

📚 **Sumber:** Modul M-48 - Balai Penelitian Tanaman Sayuran & Database Pestisida Nabati Terintegrasi
""")
