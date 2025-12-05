# 🌤️ Modul Cuaca Pertanian

Modul cuaca pertanian yang komprehensif dengan informasi real-time dan rekomendasi aktivitas pertanian.

## ✨ Fitur Utama

### 1. 📍 Pemilihan Lokasi
- **Peta Interaktif**: Klik pada peta untuk memilih lokasi
- **Input Manual**: Masukkan koordinat latitude/longitude secara manual
- **Default Location**: Indonesia center sebagai default

### 2. 🌡️ Cuaca Saat Ini
- Suhu (°C) dan feels like temperature
- Kelembaban udara (%)
- Kecepatan angin (m/s)
- Tekanan udara (hPa)
- Deskripsi cuaca dengan icon
- Waktu sunrise dan sunset

### 3. ⚠️ Peringatan Cuaca Ekstrem
- Alert untuk suhu ekstrem (> 38°C atau < 10°C)
- Peringatan angin kencang (> 10 m/s)
- Alert kelembaban tinggi (> 90%)

### 4. 🌾 Rekomendasi Aktivitas Pertanian
Rekomendasi otomatis berdasarkan kondisi cuaca:
- **Suhu**: Perlindungan tanaman, frekuensi penyiraman
- **Kelembaban**: Risiko penyakit jamur, kebutuhan irigasi
- **Hujan**: Timing penyemprotan dan pemupukan
- **Angin**: Keamanan penyemprotan

### 5. 📋 Kesesuaian Aktivitas
Status kesesuaian untuk:
- ✅ Penyemprotan Pestisida
- ✅ Pemupukan
- ✅ Penyiraman
- ✅ Panen
- ✅ Pengolahan Tanah
- ✅ Penanaman

### 6. 📅 Prakiraan Cuaca 5 Hari
- Suhu maksimum dan minimum
- Kondisi cuaca dengan icon
- Kelembaban
- Grafik tren suhu

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install streamlit pandas plotly folium streamlit-folium requests
```

### 2. Dapatkan API Key OpenWeatherMap

1. Daftar di [OpenWeatherMap](https://openweathermap.org/)
2. Buat akun gratis
3. Pergi ke [API Keys](https://home.openweathermap.org/api_keys)
4. Copy API key Anda

### 3. Konfigurasi API Key

Buat file `.streamlit/secrets.toml`:
```toml
OPENWEATHER_API_KEY = "your_api_key_here"
```

**PENTING**: Jangan commit file `secrets.toml` ke Git!

### 4. Jalankan Aplikasi
```bash
streamlit run pages/27_🌤️_Cuaca_Pertanian.py
```

## 📊 Data Source

- **API**: OpenWeatherMap API
- **Free Tier**: 
  - 1,000 calls/day
  - Current weather data
  - 5 day / 3 hour forecast
  - Cukup untuk penggunaan normal

## 🎯 Cara Penggunaan

1. **Pilih Lokasi**:
   - Klik pada peta untuk memilih lokasi, ATAU
   - Input koordinat manual (latitude, longitude)

2. **Dapatkan Data Cuaca**:
   - Klik tombol "🌤️ Dapatkan Data Cuaca"
   - Tunggu beberapa detik

3. **Lihat Informasi**:
   - Cuaca saat ini
   - Peringatan (jika ada)
   - Rekomendasi aktivitas
   - Kesesuaian aktivitas
   - Forecast 5 hari

## 📚 Panduan Interpretasi

### Suhu
- **< 15°C**: Risiko frost, lindungi tanaman sensitif
- **15-30°C**: Optimal untuk sebagian besar tanaman
- **> 35°C**: Stress panas, tingkatkan irigasi

### Kelembaban
- **< 40%**: Rendah, tingkatkan penyiraman
- **40-70%**: Optimal
- **> 80%**: Tinggi, risiko penyakit jamur

### Angin
- **< 3 m/s**: Tenang, baik untuk semua aktivitas
- **3-5 m/s**: Sedang, hati-hati saat penyemprotan
- **> 5 m/s**: Kencang, tunda penyemprotan

### Hujan
- Tunda penyemprotan pestisida 24 jam sebelum dan sesudah hujan
- Periksa drainase saat hujan lebat
- Manfaatkan periode tidak hujan untuk pemupukan

## 🌍 Contoh Lokasi

| Kota | Latitude | Longitude |
|------|----------|-----------|
| Jakarta | -6.2088 | 106.8456 |
| Surabaya | -7.2575 | 112.7521 |
| Bandung | -6.9175 | 107.6191 |
| Medan | 3.5952 | 98.6722 |
| Yogyakarta | -7.7956 | 110.3695 |
| Bali (Denpasar) | -8.6705 | 115.2126 |

## 💡 Tips

1. **Cek Cuaca Pagi Hari**: Untuk merencanakan aktivitas hari itu
2. **Perhatikan Forecast**: Rencanakan aktivitas 3-5 hari ke depan
3. **Ikuti Rekomendasi**: Sistem memberikan saran berdasarkan best practices
4. **Alert Cuaca**: Perhatikan peringatan cuaca ekstrem
5. **Kombinasi dengan Modul Lain**: Gunakan bersama Peta Data Tanah untuk analisis lengkap

## 🔄 Update & Maintenance

- Data cuaca diupdate setiap kali tombol diklik
- Forecast diupdate setiap 3 jam oleh OpenWeatherMap
- Refresh halaman untuk data terbaru

## ⚙️ Troubleshooting

### Error: "Gagal mengambil data cuaca"
- Periksa koneksi internet
- Pastikan API key valid
- Cek quota API (max 1000 calls/day untuk free tier)

### Data tidak muncul
- Pastikan sudah klik tombol "Dapatkan Data Cuaca"
- Periksa lokasi yang dipilih valid

### API Key tidak terdeteksi
- Pastikan file `.streamlit/secrets.toml` ada
- Pastikan format: `OPENWEATHER_API_KEY = "your_key"`
- Restart aplikasi Streamlit

## 📝 Changelog

### Version 1.0.0 (2024-12-05)
- ✅ Initial release
- ✅ Peta interaktif untuk pilih lokasi
- ✅ Cuaca real-time
- ✅ Forecast 5 hari
- ✅ Rekomendasi aktivitas pertanian
- ✅ Alert cuaca ekstrem
- ✅ Grafik tren suhu

## 🚀 Future Enhancements

- [ ] Historical weather data (30 hari)
- [ ] Rainfall prediction dengan ML
- [ ] Soil moisture estimation
- [ ] Evapotranspiration calculation
- [ ] Crop-specific recommendations
- [ ] Weather-based irrigation scheduling
- [ ] Integration dengan IoT sensors

## 📞 Support

Untuk pertanyaan atau masalah, silakan buka issue di GitHub repository.

---

**AgriSensa** - Platform Pertanian Cerdas 🌾
