import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add updated path logic if needed, but for same-repo deployment:
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_farm_service import get_ai_model, optimize_solution

# ==========================================
# 📊 DATABASE STANDARD OPERATIONAL (RAB)
# ==========================================
# Harga asumsi nasional (bisa diedit user)
# HOK = Hari Orang Kerja (standar 8 jam kerja)

CROP_TEMPLATES = {
    "Cabai Merah": {
        "params": {"populasi_ha": 18000, "estimasi_panen_kg": 15000, "harga_jual": 25000, "lama_tanam_bulan": 6},
        "items": [
            # 1. BIAYA TETAP
            {"kategori": "Biaya Tetap", "item": "Sewa Lahan (per musim)", "satuan": "Musim", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Biaya Tetap", "item": "Penyusutan Alat (Sprayer, Cangkul)", "satuan": "Paket", "volume": 1, "harga": 1500000, "wajib": True},
            
            # 2. SARANA PRODUKSI (SAPRODI) - BENIH
            # User nanti pilih salah satu (Semai vs Bibit)
            {"kategori": "Benih (Opsi A)", "item": "Benih Biji (Sachet @10g)", "satuan": "Sachet", "volume": 15, "harga": 135000, "opsi": "semai", "catatan": "Butuh semai 1 bulan"},
            {"kategori": "Benih (Opsi B)", "item": "Bibit Siap Tanam (Polybag)", "satuan": "Tanaman", "volume": 19000, "harga": 600, "opsi": "bibit", "catatan": "Termasuk sulam 5%"},
            
            # 2. SAPRODI - PUPUK & OBAT
            {"kategori": "Pupuk", "item": "Pupuk Kandang/Organik", "satuan": "Karung (50kg)", "volume": 400, "harga": 25000, "wajib": True},
            {"kategori": "Pupuk", "item": "Kapur Pertanian (Dolomit)", "satuan": "Karung (50kg)", "volume": 20, "harga": 35000, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK 16-16-16 (Pupuk Dasar)", "satuan": "Kg", "volume": 150, "harga": 18000, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK Mutiara/Grower (Susulan Kocor)", "satuan": "Kg", "volume": 200, "harga": 22000, "wajib": True, "catatan": "Kocor interval 7-10 hari (Perpaduan Terbaik)"},
            {"kategori": "Pupuk", "item": "KNO3 Merah/Putih (Booster)", "satuan": "Kg", "volume": 50, "harga": 35000, "opsi": "premium", "catatan": "Tambahan untuk buah lebat (Opsional)"},
             {"kategori": "Pupuk", "item": "Pupuk Daun & Mikro", "satuan": "Paket", "volume": 1, "harga": 2000000, "wajib": True},
            {"kategori": "Pestisida", "item": "Insektisida & Fungisida (1 Musim)", "satuan": "Paket", "volume": 1, "harga": 4500000, "wajib": True},
            
            # 2. SAPRODI - PENUNJANG
            {"kategori": "Penunjang", "item": "Mulsa Plastik Hitam Perak", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
            {"kategori": "Penunjang", "item": "Ajir / Turus Bambu", "satuan": "Batang", "volume": 20000, "harga": 400, "wajib": True},
            {"kategori": "Penunjang", "item": "Tali Gawar / Salaran", "satuan": "Roll", "volume": 10, "harga": 45000, "wajib": True},

            # 3. TENAGA KERJA (HOK)
            # Standar HOK: Pria Rp 100rb, Wanita Rp 80rb (rata-rata 90rb)
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah & Bedengan", "satuan": "HOK", "volume": 60, "harga": 100000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemasangan Mulsa", "satuan": "HOK", "volume": 15, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Persemaian (Jika Biji)", "satuan": "HOK", "volume": 10, "harga": 90000, "opsi": "semai"},
            {"kategori": "Tenaga Kerja", "item": "Penanaman", "satuan": "HOK", "volume": 25, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemasangan Ajir & Tali", "satuan": "HOK", "volume": 20, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemeliharaan (Kocor, Semprot, Siang)", "satuan": "HOK", "volume": 80, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemanenan (Petik)", "satuan": "HOK", "volume": 120, "harga": 80000, "wajib": True},
        ]
    },
    "Padi Sawah": {
        "params": {"populasi_ha": 0, "estimasi_panen_kg": 6500, "harga_jual": 6500, "lama_tanam_bulan": 4},
        "items": [
             # 1. BIAYA TETAP
            {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Musim", "volume": 1, "harga": 4000000, "wajib": True},
            
             # 2. SAPRODI
            {"kategori": "Benih", "item": "Benih Padi Label Ungu", "satuan": "Kg", "volume": 30, "harga": 15000, "wajib": True},
            {"kategori": "Pupuk", "item": "Urea (Subsidi/Non)", "satuan": "Kg", "volume": 250, "harga": 6000, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK Phonska", "satuan": "Kg", "volume": 300, "harga": 8000, "wajib": True},
            {"kategori": "Pestisida", "item": "Herbisida Pra-Tumbuh", "satuan": "Liter", "volume": 2, "harga": 120000, "wajib": True},
            {"kategori": "Pestisida", "item": "Insektisida & Fungisida", "satuan": "Paket", "volume": 1, "harga": 1200000, "wajib": True},

             # 3. TENAGA KERJA (HOK)
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah (Traktor)", "satuan": "Borongan/Ha", "volume": 1, "harga": 2500000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Tanam (Tandur)", "satuan": "HOK", "volume": 25, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemupukan & Penyiangan", "satuan": "HOK", "volume": 15, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Penyemprotan", "satuan": "HOK", "volume": 8, "harga": 100000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Panen (Bawon/Combine)", "satuan": "Borongan", "volume": 1, "harga": 3000000, "wajib": True},
        ]
    },
    "Jagung Hibrida": {
        "params": {"populasi_ha": 66000, "estimasi_panen_kg": 9000, "harga_jual": 5000, "lama_tanam_bulan": 4},
        "items": [
            {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Musim", "volume": 1, "harga": 3000000, "wajib": True},
            {"kategori": "Benih", "item": "Benih Hibrida (Exp: NK/Bisi)", "satuan": "Kg", "volume": 20, "harga": 110000, "wajib": True},
            {"kategori": "Pupuk", "item": "Urea", "satuan": "Kg", "volume": 350, "harga": 6000, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK", "satuan": "Kg", "volume": 300, "harga": 15000, "wajib": True},
             {"kategori": "Pestisida", "item": "Herbisida Selektif Jagung", "satuan": "Liter", "volume": 3, "harga": 180000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "Borongan/Ha", "volume": 1, "harga": 2000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Tanam", "satuan": "HOK", "volume": 15, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemupukan I & II", "satuan": "HOK", "volume": 12, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Panen & Pipil", "satuan": "Borongan", "volume": 1, "harga": 3500000, "wajib": True},
        ]
    },
     "Tomat": {
        "params": {"populasi_ha": 20000, "estimasi_panen_kg": 30000, "harga_jual": 5000, "lama_tanam_bulan": 4},
        "items": [
            {"kategori": "Biaya Tetap", "item": "Sewa Lahan (per musim)", "satuan": "Musim", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Biaya Tetap", "item": "Penyusutan Alat", "satuan": "Paket", "volume": 1, "harga": 1000000, "wajib": True},
            
            # Benih
            {"kategori": "Benih (Opsi A)", "item": "Benih Biji (Sachet)", "satuan": "Sachet", "volume": 12, "harga": 150000, "opsi": "semai", "catatan": "Perlu disemai dulu"},
            {"kategori": "Benih (Opsi B)", "item": "Bibit Siap Tanam", "satuan": "Tanaman", "volume": 21000, "harga": 400, "opsi": "bibit", "catatan": "Lebih praktis, mahal"},

            # Pupuk
            {"kategori": "Pupuk", "item": "Pupuk Kandang/Organik", "satuan": "Karung", "volume": 400, "harga": 25000, "wajib": True},
            {"kategori": "Pupuk", "item": "Kapur Pertanian (Dolomit)", "satuan": "Karung", "volume": 15, "harga": 35000, "wajib": True, "catatan": "Penting untuk pH stabil"},
            {"kategori": "Pupuk", "item": "NPK 16-16-16 (Pupuk Dasar)", "satuan": "Kg", "volume": 150, "harga": 18000, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK Grower (Susulan Kocor)", "satuan": "Kg", "volume": 200, "harga": 22000, "wajib": True},
            {"kategori": "Pupuk", "item": "KNO3/Kalsium (Booster)", "satuan": "Kg", "volume": 40, "harga": 35000, "opsi": "premium", "catatan": "Agar buah lebat & keras"},
            
            # Obat
             {"kategori": "Pestisida", "item": "Insektisida & Fungisida (1 Musim)", "satuan": "Paket", "volume": 1, "harga": 3500000, "wajib": True, "catatan": "Termasuk Perekat"},

             # Penunjang
             {"kategori": "Penunjang", "item": "Mulsa Plastik", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
            {"kategori": "Penunjang", "item": "Ajir / Turus", "satuan": "Batang", "volume": 20000, "harga": 350, "wajib": True},
             {"kategori": "Penunjang", "item": "Tali Salaran", "satuan": "Roll", "volume": 8, "harga": 45000, "wajib": True},

            # Tenaga Kerja
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah & Bedengan", "satuan": "HOK", "volume": 60, "harga": 100000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pasang Mulsa & Ajir", "satuan": "HOK", "volume": 30, "harga": 90000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Rawat (Kocor/Semprot)", "satuan": "HOK", "volume": 60, "harga": 90000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Panen (Petik Berkala)", "satuan": "HOK", "volume": 80, "harga": 80000, "wajib": True},
        ]
    },
    
    # --- PROPOSED ADDITIONS (STEP 1: HORTI HIGH VALUE) ---
    "Bawang Merah": {
        "params": {"populasi_ha": 250000, "estimasi_panen_kg": 12000, "harga_jual": 20000, "lama_tanam_bulan": 3},
        "items": [
             {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Musim", "volume": 1, "harga": 7000000, "wajib": True},
             {"kategori": "Benih", "item": "Bibit Umbi (Bima Brebes/Tajuk)", "satuan": "Kg", "volume": 1000, "harga": 35000, "wajib": True, "catatan": "Harga fluktuatif"},
             {"kategori": "Pupuk", "item": "Pupuk Dasar (SP-36/Phonska)", "satuan": "Kg", "volume": 300, "harga": 6000, "wajib": True},
             {"kategori": "Pupuk", "item": "NPK 16-16-16", "satuan": "Kg", "volume": 200, "harga": 18000, "wajib": True},
             {"kategori": "Pestisida", "item": "Fungisida & Insektisida (Intensif)", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True, "catatan": "Penyemprotan harian jika hujan"},
             {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "Borongan", "volume": 1, "harga": 3000000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Tanam (Borongan)", "satuan": "HOK", "volume": 40, "harga": 90000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Panen & Curing (Jemur)", "satuan": "Borongan", "volume": 1, "harga": 4500000, "wajib": True},
        ]
    },
    "Kentang (Dieng/Granola)": {
         "params": {"populasi_ha": 25000, "estimasi_panen_kg": 20000, "harga_jual": 12000, "lama_tanam_bulan": 4},
         "items": [
             {"kategori": "Biaya Tetap", "item": "Sewa Lahan Bukit", "satuan": "Musim", "volume": 1, "harga": 8000000, "wajib": True},
             {"kategori": "Benih", "item": "Bibit Knol (G1/G2)", "satuan": "Kg", "volume": 1200, "harga": 25000, "wajib": True},
             {"kategori": "Pupuk", "item": "Pupuk Kandang (Ayam/Sapi)", "satuan": "Ton", "volume": 15, "harga": 800000, "wajib": True},
             {"kategori": "Pestisida", "item": "Fungisida (Phytophthora)", "satuan": "Paket", "volume": 1, "harga": 10000000, "wajib": True, "catatan": "Sangat tinggi di musim hujan"},
             {"kategori": "Tenaga Kerja", "item": "Garpu/Bedengan Tinggi", "satuan": "HOK", "volume": 80, "harga": 100000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Panen & Angkut", "satuan": "Borongan", "volume": 1, "harga": 5000000, "wajib": True},
         ]
    },
    
    # --- STEP 2: BUAH (MELON/SEMANGKA) ---
    "Melon (Premium F1)": {
        "params": {"populasi_ha": 18000, "estimasi_panen_kg": 25000, "harga_jual": 9000, "lama_tanam_bulan": 3},
        "items": [
            {"kategori": "Benih", "item": "Benih F1 (Import)", "satuan": "Bungkus", "volume": 35, "harga": 250000, "wajib": True, "catatan": "Benih mahal"},
            {"kategori": "Penunjang", "item": "Mulsa Plastik", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
            {"kategori": "Penunjang", "item": "Ajir Bambu Tinggi", "satuan": "Batang", "volume": 18000, "harga": 500, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK & KNO3 (Kocor)", "satuan": "Paket", "volume": 1, "harga": 6000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pewiwilan (Pruning)", "satuan": "HOK", "volume": 50, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Polinasi Manual", "satuan": "HOK", "volume": 20, "harga": 90000, "wajib": True},
        ]
    },
    "Semangka (Non-Biji)": {
         "params": {"populasi_ha": 4000, "estimasi_panen_kg": 25000, "harga_jual": 4500, "lama_tanam_bulan": 3},
         "items": [
            {"kategori": "Benih", "item": "Benih Non-Biji + Serbuk Sari", "satuan": "Paket", "volume": 1, "harga": 3000000, "wajib": True},
            {"kategori": "Penunjang", "item": "Mulsa", "satuan": "Roll", "volume": 5, "harga": 650000, "wajib": True},
            {"kategori": "Pupuk", "item": "Pupuk Kandang & NPK", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "Borongan", "volume": 1, "harga": 2500000, "wajib": True},
         ]
    },

    # --- STEP 3: SAYURAN ---
    "Kubis / Kol": {
        "params": {"populasi_ha": 30000, "estimasi_panen_kg": 50000, "harga_jual": 2000, "lama_tanam_bulan": 3},
        "items": [
            {"kategori": "Benih", "item": "Benih Hibrida", "satuan": "Sachet", "volume": 15, "harga": 80000, "wajib": True},
            {"kategori": "Pupuk", "item": "Pupuk Kandang & Urea", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Pestisida", "item": "Insektisida (Ulat Krop)", "satuan": "Paket", "volume": 1, "harga": 3000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Perawatan Intensif", "satuan": "HOK", "volume": 40, "harga": 90000, "wajib": True},
        ]
    },
    "Wortel": {
         "params": {"populasi_ha": 250000, "estimasi_panen_kg": 25000, "harga_jual": 3000, "lama_tanam_bulan": 3.5},
         "items": [
             {"kategori": "Benih", "item": "Benih Unggul", "satuan": "Kaleng", "volume": 8, "harga": 300000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Olah Tanah (Gembur)", "satuan": "HOK", "volume": 50, "harga": 100000, "wajib": True, "catatan": "Tanah harus sangat gembur"},
             {"kategori": "Tenaga Kerja", "item": "Panen (Cabut & Cuci)", "satuan": "HOK", "volume": 80, "harga": 80000, "wajib": True},
         ]
    },

    # --- STEP 4: INVESTASI TAHUNAN ---
    "Buah Naga (Investasi Tahun 1)": {
        "params": {"populasi_ha": 2000, "estimasi_panen_kg": 0, "harga_jual": 12000, "lama_tanam_bulan": 12}, 
        # Note: Yield Year 1 is usually 0 or low. We set 0 for konservatif, or allow small harvest.
        "items": [
            {"kategori": "Investasi Awal", "item": "Tiang Panjat (Beton/Kayu)", "satuan": "Batang", "volume": 500, "harga": 150000, "wajib": True, "catatan": "Jarak 2.5 x 2.5m (populasi 4 tan/tiang)"},
            {"kategori": "Investasi Awal", "item": "Ban Bekas / Penyangga", "satuan": "Buah", "volume": 500, "harga": 10000, "wajib": True},
            {"kategori": "Benih", "item": "Stek Batang (Bibit)", "satuan": "Batang", "volume": 2000, "harga": 5000, "wajib": True},
            {"kategori": "Pupuk", "item": "Pupuk Kandang (Awal)", "satuan": "Truk", "volume": 5, "harga": 1500000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Lubang Tanam & Pasang Tiang", "satuan": "Borongan", "volume": 1, "harga": 6000000, "wajib": True},
        ]
    },
    # --- STEP 5: GREENHOUSE MODERN (COMPARISON) ---
    "Cabai Merah (Greenhouse Hydroponic)": {
        "params": {"populasi_ha": 30000, "estimasi_panen_kg": 25000, "harga_jual": 30000, "lama_tanam_bulan": 6},
        "items": [
            # Investasi & Fixed Cost
            {"kategori": "Biaya Tetap", "item": "Amortisasi Green house (Sewa/Penyusutan)", "satuan": "Musim", "volume": 1, "harga": 75000000, "wajib": True, "catatan": "Asumsi GH 1 Ha @1.5M, umur 10 thn"},
            {"kategori": "Biaya Tetap", "item": "Listrik & Air (Pompa)", "satuan": "Bulan", "volume": 6, "harga": 500000, "wajib": True},
            
            # Nutrisi AB Mix (Mahal tapi Efisien)
            {"kategori": "Nutrisi (AB Mix)", "item": "Paket AB Mix Cabai (Pekat)", "satuan": "Paket (5L)", "volume": 100, "harga": 85000, "wajib": True, "catatan": "Kebutuhan Fertigasi Harian"},
            
            # Media Tanam
            {"kategori": "Media Tanam", "item": "Cocopeat & Polybag", "satuan": "Paket", "volume": 1, "harga": 15000000, "wajib": True, "catatan": "Dipakai 2-3 musim"},
            
            # Benih
            {"kategori": "Benih", "item": "Benih F1 Import", "satuan": "Sachet", "volume": 20, "harga": 180000, "wajib": True},

            # Pestisida (Sangat Rendah)
            {"kategori": "Pestisida", "item": "Bio-Pesticide (Preventif)", "satuan": "Paket", "volume": 1, "harga": 1500000, "wajib": True, "catatan": "Hanya 30% dibanding Open Field"},
            
            # Tenaga Kerja (Efisien)
            {"kategori": "Tenaga Kerja", "item": "Operator Fertigasi & Pruning", "satuan": "HOK", "volume": 120, "harga": 100000, "wajib": True, "catatan": "Manajemen Intensif"},
             {"kategori": "Tenaga Kerja", "item": "Panen (Sortir Grade A)", "satuan": "HOK", "volume": 150, "harga": 90000, "wajib": True},
        ]
    },
    "Melon (Greenhouse Premium)": {
        "params": {"populasi_ha": 22000, "estimasi_panen_kg": 35000, "harga_jual": 25000, "lama_tanam_bulan": 3},
        "items": [
            # Investasi
             {"kategori": "Biaya Tetap", "item": "Amortisasi Green house", "satuan": "Musim", "volume": 1, "harga": 75000000, "wajib": True},
             {"kategori": "Biaya Tetap", "item": "Talianjir & Klip Gantung", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},

            # Benih Mahal
            {"kategori": "Benih", "item": "Benih Melon Premium (Intanon/Fujisawa)", "satuan": "Biji", "volume": 22000, "harga": 2500, "wajib": True, "catatan": "Harga per biji!"},
            
            # Nutrisi
             {"kategori": "Nutrisi (AB Mix)", "item": "Nutrisi Buah Premium", "satuan": "Paket", "volume": 150, "harga": 90000, "wajib": True},
             {"kategori": "Pestisida", "item": "Fungisida Powdery Mildew", "satuan": "Paket", "volume": 1, "harga": 1000000, "wajib": True},

             # Tenaga Kerja
             {"kategori": "Tenaga Kerja", "item": "Polinasi & Gantung Buah", "satuan": "HOK", "volume": 80, "harga": 100000, "wajib": True, "catatan": "Kritis & Rumit"},
             {"kategori": "Tenaga Kerja", "item": "Panen & Packaging", "satuan": "HOK", "volume": 60, "harga": 90000, "wajib": True},
        ]
    },
    # --- STEP 6: SAYURAN HIDROPONIK (NEW) ---
    "Sayuran Daun (Hidroponik)": {
        "params": {"populasi_ha": 200000, "estimasi_panen_kg": 25000, "harga_jual": 15000, "lama_tanam_bulan": 1.5},
        # Asumsi 1 ha bisa muat ~20.000 lubang tanam efektif (dengan jalan) atau lebih? 
        # Modul NFT standar per meja 2x10m = 800 lubang. 
        # 1 Ha = 50 meja x 800 = 40.000 lubang tanam (konservatif dengan greenhouse area).
        # Tapi "populasi_ha" dihitung ulang dinamis.
        "items": [
            # Investasi / Biaya Tetap
            {"kategori": "Biaya Tetap", "item": "Amortisasi Greenhouse & Instalasi", "satuan": "Siklus", "volume": 1, "harga": 15000000, "wajib": True, "catatan": "Asumsi umur 5 tahun per siklus tanam"},
            {"kategori": "Biaya Tetap", "item": "Listrik (Pompa & Aerator)", "satuan": "Bulan", "volume": 2, "harga": 300000, "wajib": True},
            
            # Sarana Produksi
            {"kategori": "Media Tanam", "item": "Rockwool (Slab)", "satuan": "Slab", "volume": 100, "harga": 65000, "wajib": True, "catatan": "1 Slab = 200-300 cubes"},
            {"kategori": "Benih", "item": "Benih Sayur (Pakcoy/Selada Import)", "satuan": "Kaleng", "volume": 5, "harga": 120000, "wajib": True},
            {"kategori": "Nutrisi (AB Mix)", "item": "AB Mix Sayuran Daun", "satuan": "Paket (5L)", "volume": 20, "harga": 75000, "wajib": True},
            
            # Operasional
            {"kategori": "Pestisida", "item": "Pestisida Nabati / Trap", "satuan": "Paket", "volume": 1, "harga": 500000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Semai & Pindah Tanam", "satuan": "HOK", "volume": 20, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Monitoring Nutrisi (Harian)", "satuan": "HOK", "volume": 30, "harga": 100000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Panen & Packing", "satuan": "HOK", "volume": 25, "harga": 80000, "wajib": True},
            {"kategori": "Pasca Panen", "item": "Plastik Kemasan / Selotip", "satuan": "Paket", "volume": 1, "harga": 1000000, "wajib": True},
        ]
    }
}

# ==========================================
# 🧠 LOGIC & UI
# ==========================================

st.title("💰 RAB Usaha Tani Presisi")
st.markdown("Buat Rencana Anggaran Biaya (RAB) dengan kalkulasi amandemen lahan, populasi, dan mulsa yang akurat.")

# 1. SMART CALCULATOR & CONFIGURATION
with st.sidebar:
    st.header("⚙️ Kalkulator Agronomi")
    
    # A. Land & Crop
    selected_crop = st.selectbox("Komoditas", list(CROP_TEMPLATES.keys()))
    luas_lahan_ha = st.number_input("Luas Lahan (Ha)", 0.1, 50.0, 1.0, step=0.1)
    luas_lahan_m2 = luas_lahan_ha * 10000
    st.caption(f"Luas: {luas_lahan_m2:,.0f} m²")
    
    st.divider()
    
    # B. Planting System (The Upgrade)
    st.subheader("📐 Jarak Tanam & Bedengan")
    
    # Defaults based on crop
    # Defaults based on crop
    is_hydroponic = "Hidroponik" in selected_crop
    
    if "Bawang" in selected_crop:
        def_jarak = 15; def_bedengan = 120
    elif "Melon" in selected_crop:
        def_jarak = 40; def_bedengan = 100
    elif "Cabai" in selected_crop:
        def_jarak = 50; def_bedengan = 100
    elif "Sayuran Daun" in selected_crop: # Hydroponic default
        def_jarak = 20; def_bedengan = 200 # Meja lebar 2m
    else:
        def_jarak = 25; def_bedengan = 100
        
    def_parit = 50
    
    if is_hydroponic:
        st.subheader("🏗️ Instalasi Hidroponik")
        # Override Concept: Bedengan -> Meja/Gully, Parit -> Jalan Antar Meja
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            jarak_tanam = st.number_input("Jarak Lubang Tanam (cm)", 10, 50, def_jarak, step=5)
            lebar_bedengan = st.number_input("Lebar Meja/Rak (cm)", 50, 400, def_bedengan, step=10)
        with col_p2:
            lebar_parit = st.number_input("Jalan Antar Meja (cm)", 30, 150, def_parit, step=10)
            baris_per_bedeng = st.number_input("Baris per Meja", 1, 20, int(def_bedengan/20), step=1, help="Lebar meja dibagi jarak tanam")
    else:
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            jarak_tanam = st.number_input("Jarak Tanam (cm)", 10, 100, def_jarak, step=5)
            lebar_bedengan = st.number_input("Lebar Bedengan (cm)", 50, 200, def_bedengan, step=10)
        with col_p2:
            lebar_parit = st.number_input("Lebar Parit (cm)", 30, 100, 50, step=10)
            baris_per_bedeng = st.selectbox("Model Tanam", [1, 2], index=1, format_func=lambda x: f"{x} Baris (Zigzag)" if x==2 else "1 Baris (Single)")
    
    # C. Mulch Specs
    st.divider()
    # C. Mulch Specs (Dynamic Check)
    template_items = CROP_TEMPLATES[selected_crop]['items']
    needs_mulsa = any("Mulsa" in i['item'] for i in template_items)
    
    st.divider()
    if needs_mulsa:
        st.subheader("⚫ Spesifikasi Mulsa")
        panjang_roll = st.number_input("Panjang per Roll (m)", 100, 1000, 250, step=50, help="Biasanya 250m atau 500m")
    else:
        panjang_roll = None

    # --- CALCULATION ENGINE ---
    # 1. Efficiency Metric
    total_lebar_segmen = (lebar_bedengan + lebar_parit) / 100 # meter
    # More accurate: Effective Bed Area = Area * (Bed / (Bed + Ditch))
    efisiensi_lahan = lebar_bedengan / (lebar_bedengan + lebar_parit)
    luas_bedengan_netto = luas_lahan_m2 * efisiensi_lahan
    
    # 2. Mulch Needs
    # Total Length of Beds = Net Bed Area / Bed Width (in meters)
    total_panjang_bedengan = luas_bedengan_netto / (lebar_bedengan / 100)
    
    if panjang_roll and not is_hydroponic:
        kebutuhan_mulsa_roll = total_panjang_bedengan / panjang_roll
        # Round up safely e.g. 10% safety margin for cutting
        kebutuhan_mulsa_roll = np.ceil(kebutuhan_mulsa_roll * 1.05) 
    else:
        kebutuhan_mulsa_roll = 0
        
    # 3. Population Needs (Seeds)
    # Pop = (Total Bed Length / Plant Spacing) * Rows per Bed
    populasi_tanaman = (total_panjang_bedengan / (jarak_tanam / 100)) * baris_per_bedeng
    # Safety margin 10% for 'sulam' (replanting dead seeds)
    populasi_tanaman = int(populasi_tanaman * 1.10)
    
    # Display Calc Results in Sidebar
    # Display Calc Results in Sidebar
    info_mulsa = f"- Kebutuhan Mulsa: **{kebutuhan_mulsa_roll:.0f}** Roll" if not is_hydroponic else ""
    st.info(f"""
    **🔍 Hasil Kalkulasi:**
    - Populasi: **{populasi_tanaman:,.0f}** Tanaman
    - Tot. Panjang Bedengan/Rak: **{total_panjang_bedengan:,.0f}** m
    {info_mulsa}
    """)
    
    # D. Metode Bibit (Restored)
    pilih_metode_bibit = "semai"
    if "Cabai" in selected_crop or "Tomat" in selected_crop:
        st.divider()
        st.subheader("🌱 Metode Bibit")
        metode_bibit_ui = st.radio("Sumber Bibit:", ["Semai Sendiri", "Beli Bibit Jadi"], index=0)
        pilih_metode_bibit = "semai" if "Semai" in metode_bibit_ui else "bibit"
        
        st.caption("💎 **Opsi Pupuk**")
        pakai_booster = st.checkbox("Pakai Booster (KNO3/Kalsium)?", value=True, help="Centang untuk hasil panen premium (Perpaduan Terbaik)")

    st.divider()

    # F. Pesticide Calculator (New Request)
    st.subheader("🚿 Kalkulator Penyemprotan")
    cap_tangki = st.number_input("Kapasitas Tangki (Liter)", 10, 20, 16, help="Standar Knapsack Sprayer 16L")
    luas_per_tangki = st.number_input("Luas Semprot per Tangki (m²)", 100, 5000, 500, step=50, help="Satu tangki habis untuk berapa meter persegi?")
    
    def_freq = 24 if "Cabai" in selected_crop else 10 # Cabai intensif
    freq_semprot = st.number_input("Frekuensi Semprot (kali/musim)", 1, 100, def_freq, step=1)
    biaya_per_tangki = st.number_input("Biaya Racikan per Tangki (Rp)", 0, 100000, 15000, step=1000, help="Total harga obat dalam 1 tangki (Insek+Fungi+Perekat)")

    # Calc Pesticide Needs
    jumlah_tangki_per_aplikasi = np.ceil(luas_lahan_m2 / luas_per_tangki)
    total_tangki_musim = jumlah_tangki_per_aplikasi * freq_semprot
    estimasi_biaya_pestisida = total_tangki_musim * biaya_per_tangki
    
    st.info(f"""
    **🔍 Data Penyemprotan:**
    - Kebutuhan: **{jumlah_tangki_per_aplikasi:.0f}** Tangki / aplikasi
    - Total: **{total_tangki_musim:.0f}** Tangki / musim
    - Est. Biaya: **Rp {estimasi_biaya_pestisida:,.0f}**
    """)
    if estimasi_biaya_pestisida > 100000000:
        st.error("⚠️ Biaya Pestisida > 100 Juta! Cek input 'Luas per Tangki' atau 'Harga per Tangki'.")

    # G. AI Integration (ENTERPRISE FEATURE)
    st.divider()
    st.markdown("### 🔮 Integrasi AI Smart Farming")
    
    # Check for Integration Context (from Map or NPK Module)
    ctx = st.session_state.get('rab_context', {})
    
    # Auto-enable AI if context exists
    default_ai_check = True if ctx else False
    use_ai_opt = st.checkbox("Optimasi Hasil dengan AI", value=default_ai_check)
    
    if ctx and use_ai_opt:
        with st.container():
            st.info(f"📋 **Inisiasi Data dari: {ctx.get('source')}**")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("pH Tanah", f"{ctx.get('ph')}", delta="Aktual")
            k2.metric("Tekstur", ctx.get('texture', '-'))
            k3.metric("N-P-K (ppm)", f"{int(ctx.get('n_ppm',0))}-{int(ctx.get('p_ppm',0))}-{int(ctx.get('k_ppm',0))}")
            
            if st.button("🔄 Reset Data Integrasi"):
                del st.session_state['rab_context']
                st.rerun()
        st.divider()

    ai_suggestion = None
        
    if use_ai_opt:
        st.markdown("##### 🧪 Input Data Tanah (Real-Time)")
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            # Auto-fill from Context if available
            def_ph = ctx.get('ph', 6.0)
            real_ph = st.number_input("pH Tanah Aktual", 3.0, 8.0, float(def_ph), step=0.1, help="Dari hasil tes tanah / Modul Peta Data Tanah")
            
            # Map Texture Strings
            def_tex_idx = 0
            if ctx.get('texture'):
                tex_str = ctx.get('texture').lower()
                if "pasir" in tex_str: def_tex_idx = 1
                elif "liat" in tex_str: def_tex_idx = 2
                
            real_texture = st.selectbox("Tekstur Tanah", ["Lempung (Ideal)", "Pasir (Boros Air)", "Liat (Padat)"], index=def_tex_idx)
            
        # Map Texture to Float (0-1 Index for AI)
        tex_map = {"Lempung (Ideal)": 0.7, "Pasir (Boros Air)": 0.2, "Liat (Padat)": 0.5}
        
        with st.spinner("AI sedang menghitung SOP optimal berdasarkan kondisi tanah..."):
            model = get_ai_model()
            # Advanced assumption mappings
            ai_params = {
                'rain': 2000, 
                'temp': 27,
                'texture': tex_map[real_texture],
                'pest_strategy': "IPM (Terpadu)"
            }
            # Optimize for Yield
            ai_suggestion = optimize_solution(model, 10000, "Yield", ai_params, price_per_kg=6000)
            
            st.success(f"✅ AI menyesuaikan resep dengan tanah {real_texture} & pH {real_ph}!")
            
            # Simple Dolomite Logic override based on pH Gap
            kebutuhan_kapur = 0
            if real_ph < 6.0:
                kebutuhan_kapur = (6.5 - real_ph) * 2000 # Rule of thumb: 1 ton per 0.5 pH delta? Simplified: 2 ton/ha per 1.0 delta
                kebutuhan_kapur = max(kebutuhan_kapur, 500) # Min 500kg if acidic
                
            st.markdown(f"""
            **Saran AI (Disesuaikan Kondisi Lapangan):**
            - Urea (N): {ai_suggestion['n_kg']:.0f} kg/ha
            - SP-36 (P): {ai_suggestion['p_kg']:.0f} kg/ha
            - KCl (K): {ai_suggestion['k_kg']:.0f} kg/ha
            - Kapur (Dolomit): {kebutuhan_kapur:.0f} kg/ha (utk netralisir pH {real_ph})
            """)

    # H. Market Assumptions
    st.subheader("💵 Asumsi Pasar")
    crop_data = CROP_TEMPLATES[selected_crop]['params']
    
    if ai_suggestion:
        def_target_panen = float(ai_suggestion['predicted_yield'])
        st.caption("✨ Target hasil otomatis diisi oleh AI")
    else:
        def_target_panen = float(crop_data['estimasi_panen_kg'])
        
    target_harga = st.number_input("Harga Jual (Rp/kg)", 0, 200000, crop_data['harga_jual'], step=500)
    target_panen = st.number_input("Target Hasil (kg/ha)", 0, 100000, int(def_target_panen), step=500)

# 2. GENERATE DATA FRAME (DYNAMICALLY)
template_items = CROP_TEMPLATES[selected_crop]['items']
rab_data = []

for item in template_items:
    # Filter based on options
    if 'opsi' in item:
        if item['opsi'] in ['semai', 'bibit'] and item['opsi'] != pilih_metode_bibit:
            continue
        if item['opsi'] == 'premium' and not pakai_booster:
            continue
            
    # --- DYNAMIC VOLUME ASSIGNMENT ---
    vol = 0
    price_override = None
    item_name_override = None
    
    # AI OVERRIDES (If Active)
    ai_override_active = False
    
    if ai_suggestion:
        # Map AI outputs to RAB Items
        if "Urea" in item['item'] and "Pupuk" in item['kategori']:
            vol = ai_suggestion['n_kg'] * luas_lahan_ha
            item_name_override = f"{item['item']} (Saran AI: {ai_suggestion['n_kg']:.0f} kg/ha)"
            ai_override_active = True
        elif "SP-36" in item['item'] or ("kocor" in item['item'].lower() and "kompleks" not in item['item'].lower()):
             pass
        elif "Kapur" in item['item'] or "Dolomit" in item['item']:
            vol = kebutuhan_kapur # From pH logic
            item_name_override = f"{item['item']} (pH {real_ph} -> Butuh {kebutuhan_kapur:.0f} kg)"
            ai_override_active = True
    
    if not ai_override_active:
        # Case 1: Benih/Bibit (Use Calculated Population)
        if "Bibit Siap Tanam" in item['item']:
            vol = populasi_tanaman
        elif "Benih Biji" in item['item']:
            vol = np.ceil(populasi_tanaman / 1750)
        elif "Benih" in item['item'] and "Kg" in item['satuan']: 
             vol = item['volume'] * luas_lahan_ha
             
        # Case 2: Mulsa (Use Calculated Rolls)
        elif "Mulsa" in item['item']:
            vol = kebutuhan_mulsa_roll
            
        # Case 3: Ajir (Matches Population)
        elif "Ajir" in item['item']:
            vol = populasi_tanaman 
            
        # Case 4: Pesticide (New Logic)
        elif "Insektisida & Fungisida" in item['item']:
            vol = total_tangki_musim
            item['satuan'] = "Tangki" # Override unit
            price_override = biaya_per_tangki
            item_name_override = f"Pestisida ({freq_semprot}x Aplikasi, @{biaya_per_tangki/1000:.0f}k/tangki)"
            
        # Case 5: Default Scaling by Area
            # Case 5: Default Scaling by Area
        else:
            if "Rockwool" in item['item']:
                # 1 Slab = 200 cubes approx
                vol = np.ceil(populasi_tanaman / 250) 
            elif "Benih" in item['item'] and "Kaleng" in item['satuan'] and "Sayur" in item['item']:
                 # 1 Kaleng 20ml = ~2000-3000 seeds? Let's assume high density
                 # Assume 1 kaleng covers 5000 plants
                 vol = np.ceil(populasi_tanaman / 5000)
            elif "AB Mix" in item['item']:
                 # 1 Paket 5L pekat = 1000L larutan siap pakai (EC 2.0).
                 # 1 Tanaman sayur butuh ~1-2 Liter nutrisi selama hidup (30 hari x 50ml/hari)
                 # Total Liter = Populasi * 1.5 Liter
                 total_larutan = populasi_tanaman * 1.5
                 vol = np.ceil(total_larutan / 1000)
                 item_name_override = f"{item['item']} (Butuh ~{total_larutan:,.0f} L Larutan)"
            elif item['item'] == "Pupuk Kandang/Organik":
                vol = item['volume'] * luas_lahan_ha
            else:
                vol = item['volume'] * luas_lahan_ha

    # Merge with User Edits (Persist manual changes)
    unique_key = item_name_override if item_name_override else item['item']
    
    # Final Append
    rab_data.append({
        "Kategori": item['kategori'],
        "Uraian": unique_key,
        "Satuan": item['satuan'],
        "Volume": float(vol),
        "Harga Satuan (Rp)": int(price_override if price_override is not None else item['harga']),
        "Total (Rp)": int(vol * (price_override if price_override is not None else item['harga'])),
        "Catatan": item.get('catatan', '-')
    })

# --- FIX: PERSIST EDITS AND RECALC TOTALS ---
if "rab_editor" in st.session_state:
    # Verify if it's the same crop context to avoid garbage mapping
    pass

df_rab = pd.DataFrame(rab_data)

cols_config = {
    "Kategori": st.column_config.TextColumn("Kategori", disabled=True),
    "Uraian": st.column_config.TextColumn("Uraian Pekerjaan/Barang", width="large"),
    "Satuan": st.column_config.TextColumn("Satuan", width="small"),
    "Volume": st.column_config.NumberColumn("Volume", format="%.1f"),
    "Harga Satuan (Rp)": st.column_config.NumberColumn("Harga Satuan", format="Rp %d"),
    "Total (Rp)": st.column_config.NumberColumn("Total Biaya", format="Rp %d", disabled=True),
}

# 3. MAIN TABLE EDITOR
st.subheader(f"📝 Tabel RAB: {selected_crop} ({luas_lahan_ha} Ha)")
st.info("💡 Klik pada sel tabel untuk mengubah Volume atau Harga. Tekan Enter untuk update Total.")

# Session State for Dataframe to support "Reactive" updates
if 'df_rab_current' not in st.session_state or st.session_state.get('last_crop') != selected_crop:
    st.session_state['df_rab_current'] = df_rab
    st.session_state['last_crop'] = selected_crop
    # If we just switched crops, we disregard old edits
else:
    # If we are in same crop, we want to respect the LATEST edits from the user
    # But we also want to respect the "defaults" if param changed? 
    # Complexity: balancing "Auto-calc" vs "User Edit".
    # User said: "Perkalian tidak berubah". 
    # Best fix: Always use the *output* of the previous run as the *input* of the next, 
    # BUT re-run the multiplication logic on it.
    
    # Check if there's an edited DF from the widget
    pass

# We use a callback pattern effectively by just processing the previous `edited_df` if it exists in the variable scope from the last run? 
# No, streamlit reruns the whole script. 
# We just need to capture the `data_editor` return value, recalculate Total, and use THAT as the input for the NEXT render?
# No, that creates a lag.

# CORRECT PATTERN:
# 1. Create base `df_rab` from template (fresh).
# 2. Render data_editor with `df_rab`.
# 3. Capture `edited_df`.
# 4. Display `edited_df` metrics. 
# PROBLEM: The Table Widget itself shows (1), not (3).
# SOLUTION: We must use `st.data_editor` on a state-backed dataframe.

# Composite Context Key to detect upstream changes
current_input_context = f"{selected_crop}_{luas_lahan_ha}_{target_panen}_{target_harga}_{use_ai_opt}_{ai_override_active}"

if "rab_state_df" not in st.session_state:
    st.session_state.rab_state_df = df_rab
    st.session_state.last_input_context = current_input_context
elif st.session_state.get("last_input_context") != current_input_context:
    # Inputs changed! Reset the dataframe to reflect new params (Area scaling, etc)
    st.session_state.rab_state_df = df_rab
    st.session_state.last_input_context = current_input_context
    # Optional: We could try to migrate manual edits here, but it's risky if structure changes.
    # For now, safer to reset to "Correct Logical Defaults" when inputs change.

# Display Editor
edited_df = st.data_editor(
    st.session_state.rab_state_df, # Use persistence
    column_config=cols_config,
    use_container_width=True,
    num_rows="dynamic",
    key="rab_editor"
)

# RECALC LOGIC
# Whenever 'edited_df' changes (user edit), we update the state AND the total column
if not edited_df.equals(st.session_state.rab_state_df):
    # User made an edit!
    # Update totals
    edited_df["Total (Rp)"] = edited_df["Volume"] * edited_df["Harga Satuan (Rp)"]
    # Save back to state so it renders correctly NEXT time? 
    # Actually, saving it to state allows the NEXT RERUN to show the correct values.
    # But we need to trigger that rerun or the user won't see it until they act again.
    st.session_state.rab_state_df = edited_df
    st.rerun() # Force rerun to update the table UI with new totals immediately

total_biaya = edited_df["Total (Rp)"].sum()

estimasi_omzet = target_panen * luas_lahan_ha * target_harga
profit = estimasi_omzet - total_biaya
roi = (profit / total_biaya) * 100 if total_biaya > 0 else 0

# 4. ANALYSIS & INSIGHTS
st.markdown("---")
st.subheader("📊 Analisis Kelayakan Usaha")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Biaya (Modal)", f"Rp {total_biaya:,.0f}")
c2.metric("Estimasi Omzet", f"Rp {estimasi_omzet:,.0f}", f"Yield: {target_panen*luas_lahan_ha:,.0f} kg")
c3.metric("Keuntungan Bersih", f"Rp {profit:,.0f}", delta=f"ROI: {roi:.1f}%")

# BEP Calculation
# BEP Calculation
bep_harga = total_biaya / (target_panen * luas_lahan_ha) if target_panen > 0 else 0
bep_unit = total_biaya / target_harga if target_harga > 0 else 0

if target_panen > 0:
    c4.metric("BEP Harga (Titik Impas)", f"Rp {bep_harga:,.0f} /kg", help="Anda tidak rugi jika harga jual di atas ini")
else:
    c4.metric("BEP Harga", "Fase Investasi", help="Belum ada panen di tahun pertama (Masa Konstruksi/Vegetatif)")

# Visualisasi Cost Structure
st.markdown("### 🍰 Struktur Biaya")
col_chart, col_advice = st.columns([1, 1])

with col_chart:
    try:
        cost_breakdown = edited_df.groupby("Kategori")["Total (Rp)"].sum().reset_index()
        # Pie Chart
        import plotly.express as px
        fig = px.pie(cost_breakdown, values="Total (Rp)", names="Kategori", hole=0.4, 
                     title="Proporsi Pengeluaran")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.warning("Data belum cukup untuk visualisasi.")

with col_advice:
    st.markdown("### 💡 Saran & Rekomendasi")
    
    # 1. Cek Biaya Tenaga Kerja (Labor Cost)
    # Fix: Handle NA to avoid bool index error
    labor_cost = edited_df[edited_df['Kategori'].str.contains("Tenaga", case=False, na=False)]["Total (Rp)"].sum()
    labor_pct = (labor_cost / total_biaya * 100) if total_biaya > 0 else 0
    
    # 2. Top Cost Drivers
    st.markdown("**🏆 3 Pengeluaran Terbesar:**")
    top_costs = edited_df.sort_values("Total (Rp)", ascending=False).head(3)
    for index, row in top_costs.iterrows():
        st.write(f"- **{row['Uraian']}**: Rp {row['Total (Rp)']:,.0f} ({row['Total (Rp)']/total_biaya*100:.1f}%)")

    # 3. Analisis Labor Check
    if labor_pct > 40:
        st.warning(f"⚠️ **Biaya Tenaga Kerja Tinggi ({labor_pct:.1f}%)**: HOK Anda cukup besar. Pertimbangkan mekanisasi (traktor/kultivator) atau penggunaan herbisida untuk mengurangi penyiangan manual.")
    else:
        st.success(f"✅ **Efisiensi Tenaga Kerja Baik ({labor_pct:.1f}%)**: Masih dalam batas wajar (<40%).")

    # 4. Cek Margin/BEP
    margin_aman = 0.7 * crop_data['harga_jual'] # Asumsi aman jika BEP < 70% harga pasar
    
    if target_panen == 0:
        st.info("ℹ️ **Fase Investasi**: Biaya tinggi di awal adalah wajar untuk tanaman tahunan (Buah Naga/Jeruk). Fokus pada kualitas konstruksi tiang/lahan.")
    elif bep_harga > margin_aman:
        st.error(f"⚠️ **Risiko Tinggi!** BEP Harga Anda (Rp {bep_harga:,.0f}) terlalu dekat dengan harga pasar. Coba kurangi biaya input atau targetkan hasil panen lebih tinggi.")
    else:
        st.success(f"✅ **Potensi Aman**: BEP Harga (Rp {bep_harga:,.0f}) masih jauh di bawah harga pasar. Usaha ini layak dijalankan.")

    # 5. Mulsa Check (Safe)
    has_mulsa = not edited_df[edited_df['Uraian'].str.contains("Mulsa", case=False, na=False)].empty
    if "Cabai" in selected_crop and not has_mulsa:
        st.warning("ℹ️ **Saran Teknis**: Budidaya Cabai tanpa Mulsa berisiko tinggi serangan penyakit dan gulma. Disarankan tetap menggunakan mulsa meski biaya awal tinggi.")

# UNIT ECONOMICS (New Feature)
st.markdown("---")
st.subheader("🌱 Analisis Per Tanaman (Unit Economics)")

if populasi_tanaman > 0:
    biaya_per_tanaman = total_biaya / populasi_tanaman
    pendapatan_per_tanaman = estimasi_omzet / populasi_tanaman
    margin_per_tanaman = pendapatan_per_tanaman - biaya_per_tanaman
    
    ue1, ue2, ue3 = st.columns(3)
    
    ue1.metric("Biaya per Batang", f"Rp {biaya_per_tanaman:,.0f}", help="Modal yang Anda keluarkan untuk merawat 1 tanaman sampai panen")
    ue2.metric("Pendapatan per Batang", f"Rp {pendapatan_per_tanaman:,.0f}", help="Hasil penjualan rata-rata dari 1 tanaman")
    ue3.metric("Profit per Batang", f"Rp {margin_per_tanaman:,.0f}", 
              delta="Untung" if margin_per_tanaman > 0 else "Rugi",
              delta_color="normal")
              
    st.info(f"💡 **Insight:** Dengan modal **Rp {biaya_per_tanaman:,.0f}** per tanaman, Anda mendapatkan untung bersih **Rp {margin_per_tanaman:,.0f}**. Pastikan tanaman tidak mati lebih dari {roi/2:.0f}% agar tetap untung.")
else:
    st.info("Populasi tanaman tidak terdefinisi (bukan tanaman individu). Analisis per batang dilewati.")

# Download Button
st.markdown("---")
csv = edited_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download RAB (Excel/CSV)",
    data=csv,
    file_name=f"RAB_{selected_crop}_{luas_lahan_ha}Ha.csv",
    mime="text/csv",
    type="primary"
)
