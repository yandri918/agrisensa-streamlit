# 🌤️ Modul Cuaca Pertanian (Open-Meteo Version)

Modul cuaca pertanian yang **gratis** dan **powerful** menggunakan data **Open-Meteo**, tanpa memerlukan API key.

## ✨ Fitur Baru (v2.0)

### 1. ⛰️ Altimeter & Elevasi
- Otomatis mendeteksi ketinggian lahan (mdpl)
- Menggunakan database topografi global
- **Manfaat:** Menentukan kesesuaian tanaman (contoh: Kopi Arabika > 1000 mdpl)

### 2. 🌱 Data Tanah (Soil Data)
- **Suhu Tanah (°C):** Penting untuk perkecambahan benih
- **Kelembaban Tanah (m³/m³):** Indikator kebutuhan irigasi
- Data diambil dari kedalaman 0-1 cm (topsoil)

### 3. 🌧️ Curah Hujan Presisi
- Curah hujan real-time (mm)
- Forecast akumulasi hujan harian
- Grafik tren hujan 7 hari

### 4. 🌤️ Cuaca Standar
- Suhu, Kelembaban Udara, Kecepatan Angin, Tekanan Udara
- Forecast 7 hari lengkap

### 5. 🌾 Rekomendasi Agronomi Cerdas
Rekomendasi disesuaikan dengan:
- **Ketinggian Lahan:** (Dataran Rendah vs Tinggi)
- **Kondisi Hujan:** (Saran penyemprotan & pemupukan)
- **Suhu & Angin:** (Stress tanaman & drift hazard)

## 🔧 Setup (Zero Config)

Tidak perlu setup API key!

1. Install dependencies:
   ```bash
   pip install streamlit pandas plotly folium streamlit-folium requests
   ```
2. Jalankan aplikasi:
   ```bash
   streamlit run pages/27_🌤️_Cuaca_Pertanian.py
   ```

## 📊 Data Source

Powered by **[Open-Meteo API](https://open-meteo.com/)**:
- ✅ Gratis (Non-commercial use)
- ✅ Tidak perlu API Key
- ✅ Data historis & forecast presisi
- ✅ Endpoint khusus Soil & Elevation

## 🎯 Panduan Penggunaan

1. **Pilih Lokasi:** Klik peta atau input manual.
2. **Lihat Elevasi:** Cek ketinggian untuk kesesuaian tanaman.
3. **Cek Data Tanah:** Lihat kelembaban tanah sebelum menyiram.
4. **Cek Hujan:** Lihat grafik hujan sebelum memupuk.
5. **Ikuti Rekomendasi:** Baca saran agronomi di dashboard.

---
**AgriSensa** - Smart Farming Solutions 🌾
