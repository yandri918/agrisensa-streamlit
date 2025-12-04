# Kalkulator Konversi Pupuk
# Konversi kebutuhan pupuk dari kg ke jumlah karung

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Konversi Pupuk", page_icon="🔄", layout="wide")

# ========== DATA ==========
# Ukuran kemasan pupuk yang umum (kg)
BAG_SIZES = {
    "Karung 50 kg": 50,
    "Karung 40 kg": 40,
    "Karung 25 kg": 25,
    "Karung 20 kg": 20,
    "Sak 10 kg": 10,
    "Sak 5 kg": 5,
}

# Jenis pupuk dan harga rata-rata per kg
FERTILIZER_TYPES = {
    "Urea (46% N)": {"price_per_kg": 2500, "color": "#3b82f6"},
    "SP-36 (36% P)": {"price_per_kg": 3000, "color": "#10b981"},
    "KCl (60% K)": {"price_per_kg": 3500, "color": "#f59e0b"},
    "NPK 15-15-15": {"price_per_kg": 4000, "color": "#8b5cf6"},
    "NPK 16-16-16": {"price_per_kg": 4200, "color": "#ec4899"},
    "ZA (21% N)": {"price_per_kg": 2000, "color": "#06b6d4"},
    "TSP (46% P)": {"price_per_kg": 3200, "color": "#14b8a6"},
    "Pupuk Organik": {"price_per_kg": 1500, "color": "#84cc16"},
}

# ========== MAIN APP ==========
st.title("🔄 Kalkulator Konversi Pupuk")
st.markdown("**Konversi kebutuhan pupuk dari kg ke jumlah karung dengan perhitungan biaya**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Langkah-langkah:**
    1. Pilih jenis pupuk yang akan dibeli
    2. Masukkan jumlah kebutuhan dalam kg
    3. Pilih ukuran kemasan yang tersedia
    4. (Opsional) Sesuaikan harga per kg jika berbeda
    5. Lihat hasil konversi dan total biaya
    
    **Tips:**
    - Beli dalam kemasan besar untuk efisiensi biaya
    - Perhatikan tanggal kadaluarsa pupuk
    - Simpan pupuk di tempat kering dan tertutup
    - Hitung kebutuhan dengan buffer 5-10% untuk cadangan
    """)

# Input Section
st.subheader("📝 Input Data")

# Method selection
method = st.radio(
    "Pilih Metode Input:",
    ["Input Manual", "Dari Hasil Kalkulator Pupuk"],
    horizontal=True
)

if method == "Input Manual":
    col1, col2 = st.columns(2)
    
    with col1:
        fertilizer_type = st.selectbox(
            "Jenis Pupuk",
            options=list(FERTILIZER_TYPES.keys()),
            help="Pilih jenis pupuk yang akan dibeli"
        )
        
        amount_kg = st.number_input(
            "Jumlah Kebutuhan (kg)",
            min_value=0.0,
            value=100.0,
            step=10.0,
            help="Masukkan jumlah pupuk yang dibutuhkan dalam kg"
        )
    
    with col2:
        bag_size_name = st.selectbox(
            "Ukuran Kemasan",
            options=list(BAG_SIZES.keys()),
            help="Pilih ukuran kemasan yang tersedia di toko"
        )
        
        price_per_kg = st.number_input(
            "Harga per kg (Rp)",
            min_value=0.0,
            value=float(FERTILIZER_TYPES[fertilizer_type]["price_per_kg"]),
            step=100.0,
            help="Sesuaikan dengan harga aktual di toko"
        )
    
    # Calculate button
    if st.button("🔍 Hitung Konversi", type="primary", use_container_width=True):
        bag_size = BAG_SIZES[bag_size_name]
        
        # Calculate
        bags_exact = amount_kg / bag_size
        bags_needed = int(bags_exact) + (1 if bags_exact % 1 > 0 else 0)  # Round up
        total_kg = bags_needed * bag_size
        excess_kg = total_kg - amount_kg
        total_cost = total_kg * price_per_kg
        cost_per_bag = bag_size * price_per_kg
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Hasil Konversi")
        
        # Main metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Kebutuhan",
                f"{amount_kg:.1f} kg",
                help="Jumlah pupuk yang dibutuhkan"
            )
        
        with col2:
            st.metric(
                "Jumlah Karung",
                f"{bags_needed} karung",
                delta=f"{bags_exact:.2f} (exact)",
                help="Jumlah karung yang harus dibeli (dibulatkan ke atas)"
            )
        
        with col3:
            st.metric(
                "Total Pembelian",
                f"{total_kg:.1f} kg",
                delta=f"+{excess_kg:.1f} kg",
                delta_color="normal",
                help="Total kg yang akan dibeli (termasuk kelebihan)"
            )
        
        with col4:
            st.metric(
                "Total Biaya",
                f"Rp {total_cost:,.0f}",
                help="Total biaya pembelian pupuk"
            )
        
        # Detailed breakdown
        st.markdown("---")
        st.subheader("📦 Rincian Pembelian")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Detail Konversi:**
            - Jenis Pupuk: **{fertilizer_type}**
            - Ukuran Kemasan: **{bag_size_name}**
            - Harga per kg: **Rp {price_per_kg:,.0f}**
            - Harga per karung: **Rp {cost_per_bag:,.0f}**
            """)
        
        with col2:
            st.markdown(f"""
            **Perhitungan:**
            - Kebutuhan: **{amount_kg:.1f} kg**
            - Karung dibutuhkan: **{bags_exact:.2f}** → **{bags_needed} karung**
            - Total pembelian: **{bags_needed} × {bag_size} kg = {total_kg:.1f} kg**
            - Kelebihan: **{excess_kg:.1f} kg** ({(excess_kg/amount_kg*100):.1f}%)
            """)
        
        # Shopping list
        st.markdown("---")
        st.subheader("🛒 Daftar Belanja")
        
        shopping_list = pd.DataFrame({
            'Jenis Pupuk': [fertilizer_type],
            'Ukuran': [bag_size_name],
            'Jumlah': [f"{bags_needed} karung"],
            'Total (kg)': [f"{total_kg:.1f} kg"],
            'Harga/karung': [f"Rp {cost_per_bag:,.0f}"],
            'Total Biaya': [f"Rp {total_cost:,.0f}"]
        })
        
        st.dataframe(shopping_list, use_container_width=True, hide_index=True)
        
        # Tips
        if excess_kg > bag_size * 0.5:
            st.warning(f"⚠️ **Perhatian:** Kelebihan pupuk cukup banyak ({excess_kg:.1f} kg). Pertimbangkan untuk menyimpan dengan baik atau gunakan untuk aplikasi berikutnya.")
        
        if excess_kg < bag_size * 0.1:
            st.success(f"✅ **Efisien:** Kelebihan pupuk minimal ({excess_kg:.1f} kg). Pembelian sudah optimal!")

else:  # From Calculator
    st.info("💡 **Fitur ini akan terintegrasi dengan Kalkulator Pupuk**")
    st.markdown("""
    Anda bisa langsung menggunakan hasil dari **Kalkulator Pupuk Holistik** untuk konversi otomatis.
    
    **Cara menggunakan:**
    1. Buka halaman **Kalkulator Pupuk**
    2. Hitung kebutuhan pupuk untuk tanaman Anda
    3. Hasil akan otomatis tersedia di sini untuk konversi
    
    *Fitur ini akan segera tersedia!*
    """)

# Comparison table
st.markdown("---")
st.subheader("💰 Perbandingan Harga Pupuk")

st.markdown("**Harga rata-rata pupuk per kg (dapat disesuaikan dengan harga lokal)**")

price_comparison = pd.DataFrame([
    {
        'Jenis Pupuk': name,
        'Harga/kg': f"Rp {data['price_per_kg']:,.0f}",
        'Harga Karung 50kg': f"Rp {data['price_per_kg'] * 50:,.0f}",
        'Harga Karung 25kg': f"Rp {data['price_per_kg'] * 25:,.0f}",
    }
    for name, data in FERTILIZER_TYPES.items()
])

st.dataframe(price_comparison, use_container_width=True, hide_index=True)

# Quick calculator
st.markdown("---")
st.subheader("⚡ Kalkulator Cepat Multi-Pupuk")

st.markdown("**Hitung total biaya untuk beberapa jenis pupuk sekaligus**")

# Create input for multiple fertilizers
total_cost_all = 0
shopping_cart = []

for i, (fert_name, fert_data) in enumerate(FERTILIZER_TYPES.items()):
    with st.expander(f"{fert_name}", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            qty = st.number_input(
                "Jumlah (kg)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                key=f"qty_{i}"
            )
        
        with col2:
            bag_size_quick = st.selectbox(
                "Ukuran",
                options=list(BAG_SIZES.keys()),
                key=f"size_{i}"
            )
        
        with col3:
            price_quick = st.number_input(
                "Harga/kg",
                min_value=0.0,
                value=float(fert_data["price_per_kg"]),
                step=100.0,
                key=f"price_{i}"
            )
        
        if qty > 0:
            bag_size_val = BAG_SIZES[bag_size_quick]
            bags = int(qty / bag_size_val) + (1 if qty % bag_size_val > 0 else 0)
            total_kg = bags * bag_size_val
            cost = total_kg * price_quick
            total_cost_all += cost
            
            shopping_cart.append({
                'Pupuk': fert_name,
                'Kebutuhan': f"{qty:.1f} kg",
                'Karung': f"{bags} × {bag_size_quick}",
                'Total': f"{total_kg:.1f} kg",
                'Biaya': f"Rp {cost:,.0f}"
            })
            
            st.success(f"✅ {bags} karung × {bag_size_val} kg = {total_kg:.1f} kg → **Rp {cost:,.0f}**")

if shopping_cart:
    st.markdown("---")
    st.subheader("🛒 Ringkasan Belanja")
    
    cart_df = pd.DataFrame(shopping_cart)
    st.dataframe(cart_df, use_container_width=True, hide_index=True)
    
    st.success(f"💰 **Total Biaya Semua Pupuk: Rp {total_cost_all:,.0f}**")

# Footer
st.markdown("---")
st.caption("💡 Harga pupuk dapat berubah sewaktu-waktu. Selalu cek harga terkini di toko pertanian terdekat.")
