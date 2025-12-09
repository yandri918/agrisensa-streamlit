import streamlit as st
import pandas as pd

# 🧪 CONFIGURATION
st.set_page_config(
    page_title="Kalkulator Hidroponik",
    page_icon="🧪",
    layout="wide"
)

# 📚 CROP DATABASE (Standard PPM & pH Ranges)
# Sources: General Hydroponics standards (variable by region/climate)
HYDROPONIC_CROPS = {
    "Selada (Lettuce)": {"ppm_min": 560, "ppm_max": 840, "ph_min": 5.5, "ph_max": 6.5, "ec": "0.8-1.2"},
    "Pakcoy / Sawi": {"ppm_min": 1050, "ppm_max": 1400, "ph_min": 6.0, "ph_max": 7.0, "ec": "1.5-2.0"},
    "Bayam (Spinach)": {"ppm_min": 1260, "ppm_max": 1600, "ph_min": 5.5, "ph_max": 6.6, "ec": "1.8-2.3"},
    "Kangkung": {"ppm_min": 1050, "ppm_max": 1400, "ph_min": 5.5, "ph_max": 6.5, "ec": "1.5-2.0"},
    "Kale": {"ppm_min": 1050, "ppm_max": 1750, "ph_min": 5.5, "ph_max": 6.5, "ec": "1.5-2.5"},
    "Tomat": {"ppm_min": 1400, "ppm_max": 3500, "ph_min": 5.5, "ph_max": 6.5, "ec": "2.0-5.0"},
    "Cabai": {"ppm_min": 1260, "ppm_max": 1540, "ph_min": 6.0, "ph_max": 6.5, "ec": "1.8-2.2"},
    "Melon": {"ppm_min": 1400, "ppm_max": 1750, "ph_min": 5.5, "ph_max": 6.0, "ec": "2.0-2.5"},
    "Timun": {"ppm_min": 1190, "ppm_max": 1750, "ph_min": 5.5, "ph_max": 6.0, "ec": "1.7-2.5"},
    "Semangka": {"ppm_min": 1260, "ppm_max": 1680, "ph_min": 5.5, "ph_max": 6.0, "ec": "1.8-2.4"},
    "Stroberi": {"ppm_min": 1260, "ppm_max": 1540, "ph_min": 5.5, "ph_max": 6.5, "ec": "1.8-2.2"},
    "Terong": {"ppm_min": 1750, "ppm_max": 2450, "ph_min": 5.5, "ph_max": 6.5, "ec": "2.5-3.5"},
    "Mint / Herbal": {"ppm_min": 1400, "ppm_max": 1680, "ph_min": 5.5, "ph_max": 6.0, "ec": "2.0-2.4"},
}

# 🎨 HEADER
st.title("🧪 Kalkulator Hidroponik (PPM Planner)")
st.markdown("""
Aplikasi ini membantu menghitung kebutuhan **Larutan Stok (Pekatan) A & B** yang harus dituang ke tandon 
untuk mencapai target PPM tanaman Anda.
""")
st.info("💡 **Rumus Standar**: 5ml Stok A + 5ml Stok B per 1 Liter Air ≈ 1000 PPM (Bisa dikalibrasi).")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1️⃣ Parameter Tanam")
    
    # Crop Selector
    selected_crop = st.selectbox("Pilih Tanaman:", list(HYDROPONIC_CROPS.keys()))
    crop_data = HYDROPONIC_CROPS[selected_crop]
    
    # Show Reference
    st.caption(f"ℹ️ Referensi {selected_crop}:")
    c_ref1, c_ref2, c_ref3 = st.columns(3)
    c_ref1.metric("Range PPM", f"{crop_data['ppm_min']} - {crop_data['ppm_max']}")
    c_ref2.metric("Range pH", f"{crop_data['ph_min']} - {crop_data['ph_max']}")
    c_ref3.metric("EC (mS/cm)", crop_data['ec'])
    
    st.markdown("---")
    st.header("2️⃣ Kondisi Aktual")
    
    # Input Tandon
    volume_tandon = st.number_input("Volume Air Tandon (Liter)", min_value=1, value=100, step=10, 
                                   help="Total air yang ada di dalam tandon saat ini.")
    
    # PPM Inputs
    target_ppm = st.number_input("Target PPM", min_value=100, max_value=5000, 
                                 value=int((crop_data['ppm_min'] + crop_data['ppm_max'])/2),
                                 help="PPM yang ingin dicapai.")
    
    current_ppm = st.number_input("PPM Saat Ini (Awal)", min_value=0, max_value=5000, value=0,
                                 help="Jika air baku atau top-up, masukkan PPM yang terukur TDS meter sekarang.")

    # Calibration
    with st.expander("⚙️ Kalibrasi Pekatan (Lanjutan)"):
        st.caption("Secara umum: 5ml A + 5ml B dalam 1L air = 1000 PPM.")
        mix_ratio = st.number_input("Rasio Pekatan (ml/L untuk 1000 PPM)", value=5.0, step=0.1)

with col2:
    st.header("3️⃣ Hasil Perhitungan")
    
    # LOGIC
    ppm_needed = target_ppm - current_ppm
    
    if ppm_needed <= 0:
        st.success("✅ **PPM sudah tercapai atau melebihi target!** Tidak perlu menambah pupuk.")
        if ppm_needed < 0:
            st.warning(f"⚠️ PPM terlalu tinggi (Kelebihan {abs(ppm_needed)} PPM). Tambahkan air baku untuk menurunkan PPM.")
    
    else:
        # Calculate Required ML
        # Formula: (PPM_Rise / 1000) * Ratio_per_L * Volume_L
        factor = ppm_needed / 1000.0
        ml_stock_needed = factor * mix_ratio * volume_tandon
        
        st.markdown(f"""
        Untuk menaikkan dari **{current_ppm} PPM** ke **{target_ppm} PPM** 
        (Selisih: +{ppm_needed} PPM) pada **{volume_tandon} Liter** air:
        """)
        
        st.success(f"""
        ### Tuangkan:
        # 🟢 {int(ml_stock_needed):,} ml Stok A
        # 🔴 {int(ml_stock_needed):,} ml Stok B
        """)
        
        st.markdown(f"*(Total {int(ml_stock_needed*2):,} ml pekatan akan masuk ke tandon)*")
        
        st.info("⚠️ **Tips**: Masukkan Stok A dulu, aduk rata, baru masukkan Stok B. Jangan dicampur saat pekat!")
        
        # Simulation Table
        st.markdown("#### 📊 Tabel Dosing Cepat (Untuk Tandon Anda)")
        
        sim_data = []
        for p in [500, 800, 1000, 1200, 1500, 2000]:
            needed = (p / 1000.0) * mix_ratio * volume_tandon
            sim_data.append({
                "Target PPM": p,
                "Stok A (ml)": int(needed),
                "Stok B (ml)": int(needed)
            })
        st.table(pd.DataFrame(sim_data))

# 📝 NOTES / LOG
st.markdown("---")
st.caption("AgriSensa Hydroponic Module - Data referensi bersifat umum. Selalu gunakan TDS Meter dan pH Meter untuk hasil akurat.")
