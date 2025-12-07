
# 🌾 AGRI-SENSA CENTRALIZED CROP SERVICE
# Single Source of Truth for: RAB, Growth Tracking, Cultivation Guides, and Harvest Planning.

import sys
import os

class CropService:
    """
    Central service to access standardized crop data.
    """
    
    # MASTER DATABASE
    # Combined from:
    # - Page 28 (RAB Templates)
    # - Growth Engine (Growth Standards)
    # - Page 21 (Cultivation Guides)
    
    CROP_DATABASE = {
        "Cabai Merah": {
            "category": "Sayuran Buah",
            "rab": {
                "params": {"populasi_ha": 18000, "estimasi_panen_kg": 15000, "harga_jual": 25000, "lama_tanam_bulan": 6},
                "items": [
                    {"kategori": "Biaya Tetap", "item": "Sewa Lahan (per musim)", "satuan": "Musim", "volume": 1, "harga": 5000000, "wajib": True},
                    {"kategori": "Biaya Tetap", "item": "Penyusutan Alat (Sprayer, Cangkul)", "satuan": "Paket", "volume": 1, "harga": 1500000, "wajib": True},
                    {"kategori": "Benih (Opsi A)", "item": "Benih Biji (Sachet @10g)", "satuan": "Sachet", "volume": 15, "harga": 135000, "opsi": "semai"},
                    {"kategori": "Benih (Opsi B)", "item": "Bibit Siap Tanam (Polybag)", "satuan": "Tanaman", "volume": 19000, "harga": 600, "opsi": "bibit"},
                    {"kategori": "Pupuk", "item": "Pupuk Kandang/Organik", "satuan": "Karung (50kg)", "volume": 400, "harga": 25000, "wajib": True},
                    {"kategori": "Pupuk", "item": "Kapur Pertanian (Dolomit)", "satuan": "Karung (50kg)", "volume": 20, "harga": 35000, "wajib": True},
                    {"kategori": "Pupuk", "item": "NPK 16-16-16 (Pupuk Dasar)", "satuan": "Kg", "volume": 150, "harga": 18000, "wajib": True},
                    {"kategori": "Pupuk", "item": "NPK Mutiara/Grower (Susulan Kocor)", "satuan": "Kg", "volume": 200, "harga": 22000, "wajib": True},
                    {"kategori": "Pupuk", "item": "KNO3 Merah/Putih (Booster)", "satuan": "Kg", "volume": 50, "harga": 35000, "opsi": "premium"},
                    {"kategori": "Pupuk", "item": "Pupuk Daun & Mikro", "satuan": "Paket", "volume": 1, "harga": 2000000, "wajib": True},
                    {"kategori": "Pestisida", "item": "Insektisida & Fungisida (1 Musim)", "satuan": "Paket", "volume": 1, "harga": 4500000, "wajib": True},
                    {"kategori": "Penunjang", "item": "Mulsa Plastik Hitam Perak", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
                    {"kategori": "Penunjang", "item": "Ajir / Turus Bambu", "satuan": "Batang", "volume": 20000, "harga": 400, "wajib": True},
                    {"kategori": "Penunjang", "item": "Tali Gawar / Salaran", "satuan": "Roll", "volume": 10, "harga": 45000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Olah Tanah & Bedengan", "satuan": "HOK", "volume": 60, "harga": 100000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Pemasangan Mulsa", "satuan": "HOK", "volume": 15, "harga": 90000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Persemaian (Jika Biji)", "satuan": "HOK", "volume": 10, "harga": 90000, "opsi": "semai"},
                    {"kategori": "Tenaga Kerja", "item": "Penanaman", "satuan": "HOK", "volume": 25, "harga": 90000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Pemasangan Ajir & Tali", "satuan": "HOK", "volume": 20, "harga": 90000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Pemeliharaan", "satuan": "HOK", "volume": 80, "harga": 90000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Pemanenan", "satuan": "HOK", "volume": 120, "harga": 80000, "wajib": True},
                ]
            },
            "growth": {
                "phase_switch": 35,
                "targets": {
                    10: {"height": 10, "leaves": 5, "stem": 2},
                    20: {"height": 25, "leaves": 12, "stem": 4},
                    30: {"height": 45, "leaves": 30, "stem": 6},
                    40: {"height": 60, "leaves": 80, "stem": 8},
                    60: {"height": 90, "leaves": 150, "stem": 12},
                    90: {"height": 120, "leaves": 200, "stem": 15}
                }
            },
            "guide": {
                "nama_latin": "Capsicum annuum",
                "umur_panen": "90-120 hari",
                "hasil_panen": "15-25 ton/ha",
                "tips": "Gunakan mulsa plastik untuk hasil maksimal."
                # Full guide data would be here, truncated for brevity in this first pass
                # Ideally we move the HUGE dictionary from Page 21 here.
            }
        },
        "Tomat": {
            "category": "Sayuran Buah",
            "rab": {
                 "params": {"populasi_ha": 20000, "estimasi_panen_kg": 30000, "harga_jual": 5000, "lama_tanam_bulan": 4},
                 "items": [
                    {"kategori": "Biaya Tetap", "item": "Sewa Lahan (per musim)", "satuan": "Musim", "volume": 1, "harga": 5000000, "wajib": True},
                    {"kategori": "Benih (Opsi A)", "item": "Benih Biji (Sachet)", "satuan": "Sachet", "volume": 12, "harga": 150000, "opsi": "semai"},
                    {"kategori": "Pupuk", "item": "Pupuk Kandang", "satuan": "Karung", "volume": 400, "harga": 25000, "wajib": True},
                    {"kategori": "Pupuk", "item": "NPK 16-16-16", "satuan": "Kg", "volume": 350, "harga": 18000, "wajib": True},
                    {"kategori": "Pestisida", "item": "Insektisida & Fungisida", "satuan": "Paket", "volume": 1, "harga": 3500000, "wajib": True},
                    {"kategori": "Penunjang", "item": "Mulsa Plastik", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
                    {"kategori": "Penunjang", "item": "Ajir / Turus", "satuan": "Batang", "volume": 20000, "harga": 350, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "HOK", "volume": 60, "harga": 100000, "wajib": True},
                    {"kategori": "Tenaga Kerja", "item": "Rawat & Panen", "satuan": "HOK", "volume": 170, "harga": 90000, "wajib": True},
                 ]
            },
             "growth": {
                # Generic fallback if no specific standard
                "phase_switch": 30,
                "targets": {
                    10: {"height": 10, "leaves": 4, "stem": 3},
                    30: {"height": 50, "leaves": 20, "stem": 8},
                    60: {"height": 100, "leaves": 50, "stem": 12}
                }
            }
        },
        "Melon (Premium)": {
            "category": "Buah-buahan",
            "rab": {
                 # Mapping from 'Melon (Premium F1)' in Page 28
                 "params": {"populasi_ha": 18000, "estimasi_panen_kg": 25000, "harga_jual": 9000, "lama_tanam_bulan": 3},
                 "items": [
                     {"kategori": "Benih", "item": "Benih F1 (Import)", "satuan": "Bungkus", "volume": 35, "harga": 250000, "wajib": True},
                     {"kategori": "Penunjang", "item": "Mulsa Plastik", "satuan": "Roll", "volume": 10, "harga": 650000, "wajib": True},
                     {"kategori": "Tenaga Kerja", "item": "Pewiwilan (Pruning)", "satuan": "HOK", "volume": 50, "harga": 90000, "wajib": True},
                 ]
            },
            "growth": {
                "phase_switch": 25,
                "targets": {
                    10: {"height": 15, "leaves": 4, "stem": 3},
                    20: {"height": 50, "leaves": 15, "stem": 6},
                    30: {"height": 120, "leaves": 25, "stem": 8},
                    40: {"height": 180, "leaves": 35, "stem": 10},
                    60: {"height": 200, "leaves": 35, "stem": 12}
                }
            }
        },
        "Bawang Merah": {
             "category": "Sayuran Umbi",
             "rab": {
                 "params": {"populasi_ha": 250000, "estimasi_panen_kg": 12000, "harga_jual": 20000, "lama_tanam_bulan": 3},
                 "items": [
                     {"kategori": "Benih", "item": "Bibit Umbi", "satuan": "Kg", "volume": 1000, "harga": 35000},
                     {"kategori": "Pupuk", "item": "Pupuk Dasar & Susulan", "satuan": "Paket", "volume": 1, "harga": 8000000},
                 ]
             },
             "growth": {
                 "phase_switch": 35, # HST enters Bulb Formation
                 "targets": {
                     10: {"height": 12, "leaves": 5, "stem": 4},
                     20: {"height": 25, "leaves": 15, "stem": 7},
                     30: {"height": 35, "leaves": 25, "stem": 10},
                     40: {"height": 40, "leaves": 35, "stem": 12},
                     55: {"height": 42, "leaves": 40, "stem": 15}
                 }
             }
        },
        "Padi Sawah": {
            "category": "Tanaman Pangan",
            "rab": {
                "params": {"populasi_ha": 0, "estimasi_panen_kg": 6500, "harga_jual": 6500, "lama_tanam_bulan": 4},
                "items": [
                   {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Musim", "volume": 1, "harga": 4000000}, 
                   {"kategori": "Benih", "item": "Benih Padi", "satuan": "Kg", "volume": 30, "harga": 15000},
                ]
            },
            "growth": {
                 "phase_switch": 60, # HST enters Generative (Malai)
                 "targets": {
                     15: {"height": 25, "leaves": 5, "stem": 3},
                     30: {"height": 50, "leaves": 15, "stem": 6},
                     45: {"height": 75, "leaves": 25, "stem": 9},
                     60: {"height": 90, "leaves": 35, "stem": 12},
                     90: {"height": 110, "leaves": 40, "stem": 14}
                 }
            }
        },
        "Sayuran Daun (Hidroponik)": {
             "category": "Hidroponik",
             "rab": {
                 "params": {"populasi_ha": 200000, "estimasi_panen_kg": 25000, "harga_jual": 15000, "lama_tanam_bulan": 1.5},
                 "items": [
                     {"kategori": "Biaya Tetap", "item": "Instalasi & Greenhouse", "satuan": "Siklus", "volume": 1, "harga": 15000000},
                     {"kategori": "Nutrisi", "item": "AB Mix", "satuan": "Paket", "volume": 20, "harga": 75000},
                 ]
             },
             "growth": {
                 "phase_switch": 20,
                 "targets": {
                     10: {"height": 5, "leaves": 4, "stem": 2},
                     20: {"height": 15, "leaves": 10, "stem": 4},
                     30: {"height": 25, "leaves": 20, "stem": 6}
                 }
             }
        }
    }

    @staticmethod
    def get_all_crops():
        """Return list of all available crops"""
        return list(CropService.CROP_DATABASE.keys())

    @staticmethod
    def get_rab_template(crop_name):
        """Return RAB data for specific crop"""
        return CropService.CROP_DATABASE.get(crop_name, {}).get('rab', None)

    @staticmethod
    def get_growth_standards(crop_name):
        """Return Growth Standard data for specific crop"""
        return CropService.CROP_DATABASE.get(crop_name, {}).get('growth', None)
    
    @staticmethod
    def get_guide_data(crop_name):
         """Return Cultivation Guide data"""
         return CropService.CROP_DATABASE.get(crop_name, {}).get('guide', None)
