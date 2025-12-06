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
    def_jarak = 50 if "Cabai" in selected_crop else 40 if "Tomat" in selected_crop else 25
    def_bedengan = 100 if "Cabai" in selected_crop else 100
    def_parit = 50
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        jarak_tanam = st.number_input("Jarak Tanam (cm)", 10, 100, def_jarak, step=5)
        lebar_bedengan = st.number_input("Lebar Bedengan (cm)", 50, 200, def_bedengan, step=10)
    with col_p2:
        lebar_parit = st.number_input("Lebar Parit (cm)", 30, 100, def_parit, step=10)
        baris_per_bedeng = st.selectbox("Model Tanam", [1, 2], index=1, format_func=lambda x: f"{x} Baris (Zigzag)" if x==2 else "1 Baris (Single)")
    
    # C. Mulch Specs
    st.divider()
    if "Padi" not in selected_crop and "Jagung" not in selected_crop:
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
    
    if panjang_roll:
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
    st.info(f"""
    **🔍 Hasil Kalkulasi:**
    - Populasi: **{populasi_tanaman:,.0f}** Tanaman
    - Tot. Panjang Bedengan: **{total_panjang_bedengan:,.0f}** m
    - Kebutuhan Mulsa: **{kebutuhan_mulsa_roll:.0f}** Roll
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
    # Merge with User Edits (Persist manual changes)
    # logic: If user edited this specific row in previous run, keep their value
    # We use 'Uraian' as a simple key (assuming unique enough within crop context)
    
    unique_key = item_name_override if item_name_override else item['item']
    
    if "rab_editor" in st.session_state and "edited_rows" in st.session_state["rab_editor"]:
        # Streamlit data_editor state structure: {edited_rows: {row_index: {col_name: new_value}}}
        # This is tricky because indices might shift if items change. 
        # Better approach: Use the DATAFRAME returned by data_editor in previous run if possible?
        # Actually, simpler: Let data_editor manage state, but we force recalculate the "Total" column 
        # by passing a dataframe where Total is already updated based on *previous* output if it matches.
        pass

    # Simplified Approach for Stability:
    # 1. Std Generate (as above)
    # 2. If 'edited_df_state' exists in session, use its Volume/Price for matching rows
    # But complexity is high.
    
    # NEW FIX: Trust the loop logic for defaults, but allow override if we have a "saved state" 
    # OR -> Just use the standard behaviour but ensure we use the 'edited_df' result for calculations below.
    # The user complaint is visual: "Total" column in table doesn't change.
    # We can fix this by enabling the "Total" column to be calculated implicitly? No.
    
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

if "rab_state_df" not in st.session_state:
    st.session_state.rab_state_df = df_rab
elif st.session_state.get("last_crop_check") != selected_crop:
    # Reset if crop changed
    st.session_state.rab_state_df = df_rab
    st.session_state.last_crop_check = selected_crop

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
bep_harga = total_biaya / (target_panen * luas_lahan_ha) if target_panen > 0 else 0
bep_unit = total_biaya / target_harga if target_harga > 0 else 0

c4.metric("BEP Harga (Titik Impas)", f"Rp {bep_harga:,.0f} /kg", help="Anda tidak rugi jika harga jual di atas ini")

# Visualisasi Cost Structure
st.markdown("### 🍰 Struktur Biaya")
col_chart, col_advice = st.columns([1, 1])

with col_chart:
    cost_breakdown = edited_df.groupby("Kategori")["Total (Rp)"].sum().reset_index()
    # Pie Chart
    import plotly.express as px
    fig = px.pie(cost_breakdown, values="Total (Rp)", names="Kategori", hole=0.4, 
                 title="Proporsi Pengeluaran")
    st.plotly_chart(fig, use_container_width=True)

with col_advice:
    st.markdown("### 💡 Saran & Rekomendasi")
    
    # 1. Cek Biaya Tenaga Kerja (Labor Cost)
    labor_cost = edited_df[edited_df['Kategori'].str.contains("Tenaga", case=False)]["Total (Rp)"].sum()
    labor_pct = (labor_cost / total_biaya * 100) if total_biaya > 0 else 0
    
    # 2. Top Cost Drivers (New Debugging Aid)
    st.markdown("**🏆 3 Pengeluaran Terbesar:**")
    top_costs = edited_df.sort_values("Total (Rp)", ascending=False).head(3)
    for index, row in top_costs.iterrows():
        st.write(f"- **{row['Uraian']}**: Rp {row['Total (Rp)']:,.0f} ({row['Total (Rp)']/total_biaya*100:.1f}%)")
    
    if labor_pct > 40:
        st.warning(f"⚠️ **Biaya Tenaga Kerja Tinggi ({labor_pct:.1f}%)**: HOK Anda cukup besar. Pertimbangkan mekanisasi (traktor/kultivator) atau penggunaan herbisida untuk mengurangi penyiangan manual.")
    else:
        st.success(f"✅ **Efisiensi Tenaga Kerja Baik ({labor_pct:.1f}%)**: Masih dalam batas wajar (<40%).")

    # 3. Cek BEP
    margin_aman = 0.7 * crop_data['harga_jual'] # Asumsi aman jika BEP < 70% harga pasar
    if bep_harga > margin_aman:
        st.error(f"⚠️ **Risiko Tinggi!** BEP Harga Anda (Rp {bep_harga:,.0f}) terlalu dekat dengan harga pasar. Coba kurangi biaya input atau targetkan hasil panen lebih tinggi.")
    else:
        st.success(f"✅ **Potensi Aman**: BEP Harga (Rp {bep_harga:,.0f}) masih jauh di bawah harga pasar. Usaha ini layak dijalankan.")

    # 3. Mulsa Check
    has_mulsa = not edited_df[edited_df['Uraian'].str.contains("Mulsa", case=False)].empty
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
