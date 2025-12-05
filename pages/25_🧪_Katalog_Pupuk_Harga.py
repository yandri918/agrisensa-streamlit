# Katalog Pupuk & Harga
# Module 25 - Comprehensive Fertilizer Catalog
# Version: 1.0.0

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Katalog Pupuk & Harga", page_icon="🧪", layout="wide")

# ========== FERTILIZER DATABASE ==========

FERTILIZER_DATABASE = {
    # UREA
    "Urea Pusri": {
        "category": "Urea",
        "brand": "PT Pupuk Sriwidjaja (Pusri)",
        "formula": "CO(NH₂)₂",
        "n_content": 46,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 2400,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen tunggal untuk fase vegetatif",
        "usage": "Padi, jagung, sayuran",
        "dosage": "200-300 kg/ha",
        "application": "Tabur/kocor, 2-3 kali aplikasi"
    },
    "Urea Petrokimia": {
        "category": "Urea",
        "brand": "PT Petrokimia Gresik",
        "formula": "CO(NH₂)₂",
        "n_content": 46,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 2400,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen untuk pertumbuhan vegetatif",
        "usage": "Padi, jagung, tebu",
        "dosage": "200-300 kg/ha",
        "application": "Tabur/kocor, split application"
    },
    
    # NPK PHONSKA
    "NPK Phonska": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "15-15-15",
        "n_content": 15,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 2650,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk lengkap untuk semua fase",
        "usage": "Padi, jagung, sayuran, buah",
        "dosage": "250-400 kg/ha",
        "application": "Tabur/kocor, 2-3 kali aplikasi"
    },
    "NPK Pelangi 16-16-16": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "16-16-16",
        "n_content": 16,
        "p_content": 16,
        "k_content": 16,
        "price_per_kg": 2750,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk berimbang untuk hasil optimal",
        "usage": "Padi, jagung, kedelai",
        "dosage": "250-350 kg/ha",
        "application": "Tabur saat tanam dan susulan"
    },
    "NPK Mutiara 16-16-16": {
        "category": "NPK",
        "brand": "PT Pupuk Kalimantan Timur",
        "formula": "16-16-16",
        "n_content": 16,
        "p_content": 16,
        "k_content": 16,
        "price_per_kg": 2800,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk premium untuk hasil maksimal",
        "usage": "Padi, jagung, hortikultura",
        "dosage": "250-350 kg/ha",
        "application": "Tabur/kocor"
    },
    "NPK Kebomas 15-15-15": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "15-15-15",
        "n_content": 15,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 2700,
        "package_sizes": ["50 kg"],
        "description": "Pupuk majemuk untuk tanaman pangan",
        "usage": "Padi, jagung, kedelai",
        "dosage": "250-400 kg/ha",
        "application": "Tabur saat tanam"
    },
    
    # NPK KHUSUS
    "NPK Grower 15-9-20": {
        "category": "NPK",
        "brand": "PT Pupuk Kalimantan Timur",
        "formula": "15-9-20",
        "n_content": 15,
        "p_content": 9,
        "k_content": 20,
        "price_per_kg": 3200,
        "package_sizes": ["25 kg", "50 kg"],
        "description": "Pupuk khusus untuk fase generatif dan pembuahan",
        "usage": "Cabai, tomat, melon, semangka",
        "dosage": "300-500 kg/ha",
        "application": "Kocor/tabur, fokus K tinggi"
    },
    "NPK Pelangi 12-12-17+2MgO": {
        "category": "NPK",
        "brand": "PT Petrokimia Gresik",
        "formula": "12-12-17+2MgO",
        "n_content": 12,
        "p_content": 12,
        "k_content": 17,
        "price_per_kg": 2900,
        "package_sizes": ["50 kg"],
        "description": "Pupuk dengan tambahan Magnesium untuk klorofil",
        "usage": "Sawit, karet, kakao",
        "dosage": "300-400 kg/ha",
        "application": "Tabur di piringan"
    },
    "NPK Yara 15-15-15+TE": {
        "category": "NPK",
        "brand": "Yara International",
        "formula": "15-15-15+TE",
        "n_content": 15,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 4500,
        "package_sizes": ["25 kg"],
        "description": "Pupuk premium dengan trace elements lengkap",
        "usage": "Hortikultura, buah premium",
        "dosage": "200-300 kg/ha",
        "application": "Kocor/fertigasi"
    },
    
    # ZA (Zwavelzure Ammoniak)
    "ZA Petrokimia": {
        "category": "ZA",
        "brand": "PT Petrokimia Gresik",
        "formula": "(NH₄)₂SO₄",
        "n_content": 21,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 1800,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen dengan sulfur untuk tanah alkalis",
        "usage": "Padi, tebu, tembakau",
        "dosage": "200-300 kg/ha",
        "application": "Tabur, cocok untuk tanah pH tinggi"
    },
    "ZA Pusri": {
        "category": "ZA",
        "brand": "PT Pupuk Sriwidjaja",
        "formula": "(NH₄)₂SO₄",
        "n_content": 21,
        "p_content": 0,
        "k_content": 0,
        "price_per_kg": 1800,
        "package_sizes": ["50 kg"],
        "description": "Pupuk nitrogen dengan kandungan sulfur 24%",
        "usage": "Padi, jagung, tebu",
        "dosage": "200-300 kg/ha",
        "application": "Tabur/kocor"
    },
    
    # SP-36
    "SP-36 Petrokimia": {
        "category": "SP-36",
        "brand": "PT Petrokimia Gresik",
        "formula": "Ca(H₂PO₄)₂",
        "n_content": 0,
        "p_content": 36,
        "k_content": 0,
        "price_per_kg": 2200,
        "package_sizes": ["50 kg"],
        "description": "Pupuk fosfor untuk perakaran dan pembungaan",
        "usage": "Padi, jagung, kedelai",
        "dosage": "100-150 kg/ha",
        "application": "Tabur saat tanam"
    },
    "SP-36 Pusri": {
        "category": "SP-36",
        "brand": "PT Pupuk Sriwidjaja",
        "formula": "Ca(H₂PO₄)₂",
        "n_content": 0,
        "p_content": 36,
        "k_content": 0,
        "price_per_kg": 2200,
        "package_sizes": ["50 kg"],
        "description": "Super phosphate untuk sistem perakaran kuat",
        "usage": "Padi, jagung, sayuran",
        "dosage": "100-150 kg/ha",
        "application": "Tabur saat tanam"
    },
    
    # KCl (Kalium Klorida)
    "KCl Merah": {
        "category": "KCl",
        "brand": "Import (Kanada/Rusia)",
        "formula": "KCl",
        "n_content": 0,
        "p_content": 0,
        "k_content": 60,
        "price_per_kg": 3500,
        "package_sizes": ["50 kg"],
        "description": "Pupuk kalium untuk kualitas hasil dan ketahanan",
        "usage": "Padi, jagung, buah, sayuran",
        "dosage": "100-200 kg/ha",
        "application": "Tabur/kocor saat generatif"
    },
    "KCl Putih": {
        "category": "KCl",
        "brand": "Import (Kanada)",
        "formula": "KCl",
        "n_content": 0,
        "p_content": 0,
        "k_content": 60,
        "price_per_kg": 3800,
        "package_sizes": ["50 kg"],
        "description": "Pupuk kalium premium untuk hasil berkualitas",
        "usage": "Hortikultura, buah premium",
        "dosage": "100-200 kg/ha",
        "application": "Kocor/fertigasi"
    },
    
    # PUPUK ORGANIK
    "Petroganik": {
        "category": "Organik",
        "brand": "PT Petrokimia Gresik",
        "formula": "Organik",
        "n_content": 2,
        "p_content": 2,
        "k_content": 2,
        "price_per_kg": 800,
        "package_sizes": ["40 kg"],
        "description": "Pupuk organik granul untuk memperbaiki tanah",
        "usage": "Semua tanaman",
        "dosage": "500-1000 kg/ha",
        "application": "Tabur saat pengolahan tanah"
    },
    "Pupuk Kandang Sapi": {
        "category": "Organik",
        "brand": "Lokal",
        "formula": "Organik",
        "n_content": 1.5,
        "p_content": 1,
        "k_content": 1.5,
        "price_per_kg": 500,
        "package_sizes": ["Curah", "Karung 50 kg"],
        "description": "Pupuk organik alami dari kotoran sapi",
        "usage": "Semua tanaman",
        "dosage": "5-10 ton/ha",
        "application": "Tabur saat pengolahan tanah"
    },
    "Pupuk Kompos": {
        "category": "Organik",
        "brand": "Lokal",
        "formula": "Organik",
        "n_content": 1,
        "p_content": 0.5,
        "k_content": 1,
        "price_per_kg": 400,
        "package_sizes": ["Curah", "Karung 50 kg"],
        "description": "Pupuk organik dari dekomposisi bahan organik",
        "usage": "Semua tanaman",
        "dosage": "5-10 ton/ha",
        "application": "Tabur saat pengolahan tanah"
    },
    "NASA POC": {
        "category": "Organik Cair",
        "brand": "PT Natural Nusantara",
        "formula": "Organik Cair",
        "n_content": 3,
        "p_content": 1,
        "k_content": 2,
        "price_per_kg": 35000,  # per liter
        "package_sizes": ["500 ml", "1 liter", "5 liter"],
        "description": "Pupuk organik cair dengan mikroorganisme",
        "usage": "Semua tanaman",
        "dosage": "2-5 liter/ha (diencerkan)",
        "application": "Semprot/kocor"
    },
    
    # PUPUK MAJEMUK KHUSUS
    "Mahkota Merah 12-12-17+TE": {
        "category": "NPK Khusus",
        "brand": "Meroke",
        "formula": "12-12-17+TE",
        "n_content": 12,
        "p_content": 12,
        "k_content": 17,
        "price_per_kg": 3500,
        "package_sizes": ["25 kg", "50 kg"],
        "description": "Pupuk majemuk dengan trace elements untuk sawit",
        "usage": "Sawit, karet, kakao",
        "dosage": "300-500 kg/ha",
        "application": "Tabur di piringan"
    },
    "Mahkota Hijau 15-15-6+TE": {
        "category": "NPK Khusus",
        "brand": "Meroke",
        "formula": "15-15-6+TE",
        "n_content": 15,
        "p_content": 15,
        "k_content": 6,
        "price_per_kg": 3200,
        "package_sizes": ["25 kg", "50 kg"],
        "description": "Pupuk untuk fase vegetatif tanaman perkebunan",
        "usage": "Sawit, karet, kakao",
        "dosage": "300-500 kg/ha",
        "application": "Tabur di piringan"
    },
    
    # PUPUK MIKRO
    "Gandasil D": {
        "category": "Mikro",
        "brand": "PT Petrokimia Gresik",
        "formula": "20-15-15+TE",
        "n_content": 20,
        "p_content": 15,
        "k_content": 15,
        "price_per_kg": 25000,
        "package_sizes": ["1 kg", "5 kg"],
        "description": "Pupuk daun lengkap untuk pertumbuhan vegetatif",
        "usage": "Sayuran, buah, tanaman hias",
        "dosage": "2-3 kg/ha (diencerkan)",
        "application": "Semprot daun"
    },
    "Gandasil B": {
        "category": "Mikro",
        "brand": "PT Petrokimia Gresik",
        "formula": "6-20-30+TE",
        "n_content": 6,
        "p_content": 20,
        "k_content": 30,
        "price_per_kg": 25000,
        "package_sizes": ["1 kg", "5 kg"],
        "description": "Pupuk daun untuk pembungaan dan pembuahan",
        "usage": "Cabai, tomat, melon, buah",
        "dosage": "2-3 kg/ha (diencerkan)",
        "application": "Semprot daun"
    },
    "Growmore 20-20-20": {
        "category": "Mikro",
        "brand": "Growmore",
        "formula": "20-20-20+TE",
        "n_content": 20,
        "p_content": 20,
        "k_content": 20,
        "price_per_kg": 45000,
        "package_sizes": ["1 kg", "5 kg"],
        "description": "Pupuk daun premium untuk semua fase",
        "usage": "Hortikultura, tanaman hias",
        "dosage": "2-3 kg/ha (diencerkan)",
        "application": "Semprot daun/fertigasi"
    }
}

# ========== HELPER FUNCTIONS ==========

def get_categories():
    """Get unique categories"""
    return sorted(list(set([v["category"] for v in FERTILIZER_DATABASE.values()])))

def get_brands():
    """Get unique brands"""
    return sorted(list(set([v["brand"] for v in FERTILIZER_DATABASE.values()])))

def filter_fertilizers(category=None, brand=None, search_term=None, price_range=None):
    """Filter fertilizers based on criteria"""
    filtered = {}
    
    for name, data in FERTILIZER_DATABASE.items():
        # Category filter
        if category and category != "Semua" and data["category"] != category:
            continue
        
        # Brand filter
        if brand and brand != "Semua" and data["brand"] != brand:
            continue
        
        # Search filter
        if search_term:
            search_lower = search_term.lower()
            if not (search_lower in name.lower() or 
                   search_lower in data["description"].lower() or
                   search_lower in data["usage"].lower()):
                continue
        
        # Price filter
        if price_range:
            if not (price_range[0] <= data["price_per_kg"] <= price_range[1]):
                continue
        
        filtered[name] = data
    
    return filtered

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #059669;
        text-align: center;
        margin-bottom: 1rem;
    }
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .product-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-color: #10b981;
    }
    .product-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    .product-brand {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    .product-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #dc2626;
        margin: 1rem 0;
    }
    .formula-badge {
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .category-badge {
        display: inline-block;
        background: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('<h1 class="main-header">🧪 Katalog Pupuk & Harga</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Referensi harga pupuk terkini dari berbagai produsen terpercaya di Indonesia</p>', unsafe_allow_html=True)

# ========== SIDEBAR FILTERS ==========
with st.sidebar:
    st.markdown("### 🔍 Filter & Pencarian")
    
    # Search
    search_term = st.text_input("🔎 Cari Pupuk", placeholder="Nama, deskripsi, atau penggunaan...")
    
    # Category filter
    categories = ["Semua"] + get_categories()
    selected_category = st.selectbox("Kategori", categories)
    
    # Brand filter
    brands = ["Semua"] + get_brands()
    selected_brand = st.selectbox("Produsen", brands)
    
    # Price range
    st.markdown("**Range Harga (Rp/kg):**")
    price_range = st.slider(
        "Pilih range harga",
        min_value=0,
        max_value=50000,
        value=(0, 50000),
        step=500,
        format="Rp %d"
    )
    
    # Sort by
    sort_by = st.selectbox(
        "Urutkan Berdasarkan",
        ["Nama (A-Z)", "Nama (Z-A)", "Harga (Termurah)", "Harga (Termahal)", "Kandungan N", "Kandungan P", "Kandungan K"]
    )
    
    st.markdown("---")
    st.markdown("### 📊 Statistik")
    total_products = len(FERTILIZER_DATABASE)
    st.metric("Total Produk", total_products)

# ========== MAIN CONTENT ==========

# Apply filters
filtered_fertilizers = filter_fertilizers(
    category=selected_category if selected_category != "Semua" else None,
    brand=selected_brand if selected_brand != "Semua" else None,
    search_term=search_term if search_term else None,
    price_range=price_range
)

# Sort
if sort_by == "Nama (A-Z)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items()))
elif sort_by == "Nama (Z-A)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), reverse=True))
elif sort_by == "Harga (Termurah)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["price_per_kg"]))
elif sort_by == "Harga (Termahal)":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["price_per_kg"], reverse=True))
elif sort_by == "Kandungan N":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["n_content"], reverse=True))
elif sort_by == "Kandungan P":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["p_content"], reverse=True))
elif sort_by == "Kandungan K":
    filtered_fertilizers = dict(sorted(filtered_fertilizers.items(), key=lambda x: x[1]["k_content"], reverse=True))

# Display results
st.markdown(f"### Menampilkan {len(filtered_fertilizers)} produk")

if len(filtered_fertilizers) == 0:
    st.warning("Tidak ada produk yang sesuai dengan filter Anda. Coba ubah kriteria pencarian.")
else:
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📦 Katalog Produk", "📊 Perbandingan Harga", "📚 Panduan Pemupukan"])
    
    # TAB 1: PRODUCT CATALOG
    with tab1:
        # Display products in grid
        cols_per_row = 2
        products_list = list(filtered_fertilizers.items())
        
        for i in range(0, len(products_list), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j in range(cols_per_row):
                if i + j < len(products_list):
                    name, data = products_list[i + j]
                    
                    with cols[j]:
                        st.markdown(f"""
                        <div class="product-card">
                            <div class="product-name">{name}</div>
                            <div class="product-brand">📍 {data['brand']}</div>
                            <div>
                                <span class="category-badge">{data['category']}</span>
                                <span class="formula-badge">{data['formula']}</span>
                            </div>
                            <div class="product-price">Rp {data['price_per_kg']:,}/kg</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📋 Detail Produk"):
                            st.markdown(f"**Deskripsi:** {data['description']}")
                            st.markdown(f"**Kandungan:**")
                            st.markdown(f"- N: {data['n_content']}%")
                            st.markdown(f"- P₂O₅: {data['p_content']}%")
                            st.markdown(f"- K₂O: {data['k_content']}%")
                            st.markdown(f"**Penggunaan:** {data['usage']}")
                            st.markdown(f"**Dosis:** {data['dosage']}")
                            st.markdown(f"**Aplikasi:** {data['application']}")
                            st.markdown(f"**Kemasan:** {', '.join(data['package_sizes'])}")
    
    # TAB 2: PRICE COMPARISON
    with tab2:
        st.markdown("### 💰 Perbandingan Harga")
        
        # Create comparison table
        comparison_data = []
        for name, data in filtered_fertilizers.items():
            comparison_data.append({
                "Nama Produk": name,
                "Kategori": data["category"],
                "Produsen": data["brand"],
                "Formula": data["formula"],
                "N (%)": data["n_content"],
                "P (%)": data["p_content"],
                "K (%)": data["k_content"],
                "Harga/kg": f"Rp {data['price_per_kg']:,}"
            })
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True)
        
        # Price chart by category
        st.markdown("### 📊 Grafik Harga per Kategori")
        
        category_prices = {}
        for name, data in filtered_fertilizers.items():
            cat = data["category"]
            if cat not in category_prices:
                category_prices[cat] = []
            category_prices[cat].append(data["price_per_kg"])
        
        chart_data = []
        for cat, prices in category_prices.items():
            chart_data.append({
                "Kategori": cat,
                "Harga Rata-rata": sum(prices) / len(prices),
                "Harga Terendah": min(prices),
                "Harga Tertinggi": max(prices)
            })
        
        df_chart = pd.DataFrame(chart_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Rata-rata',
            x=df_chart['Kategori'],
            y=df_chart['Harga Rata-rata'],
            marker_color='#10b981'
        ))
        fig.add_trace(go.Bar(
            name='Terendah',
            x=df_chart['Kategori'],
            y=df_chart['Harga Terendah'],
            marker_color='#3b82f6'
        ))
        fig.add_trace(go.Bar(
            name='Tertinggi',
            x=df_chart['Kategori'],
            y=df_chart['Harga Tertinggi'],
            marker_color='#ef4444'
        ))
        
        fig.update_layout(
            title="Perbandingan Harga Pupuk per Kategori",
            xaxis_title="Kategori",
            yaxis_title="Harga (Rp/kg)",
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: FERTILIZATION GUIDE
    with tab3:
        st.markdown("### 📚 Panduan Pemupukan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🌾 Pupuk untuk Padi
            
            **Rekomendasi:**
            - **Dasar:** Urea 200 kg + SP-36 100 kg + KCl 100 kg
            - **Alternatif:** NPK Phonska 300 kg + Urea 100 kg
            - **Organik:** Petroganik 500 kg (saat olah tanah)
            
            **Waktu Aplikasi:**
            1. Saat tanam: SP-36 + 1/3 Urea + 1/2 KCl
            2. 21 HST: 1/3 Urea + 1/2 KCl
            3. 42 HST: 1/3 Urea
            
            ---
            
            #### 🌽 Pupuk untuk Jagung
            
            **Rekomendasi:**
            - **Dasar:** Urea 300 kg + SP-36 150 kg + KCl 100 kg
            - **Alternatif:** NPK 16-16-16 350 kg + Urea 150 kg
            
            **Waktu Aplikasi:**
            1. Saat tanam: SP-36 + 1/3 Urea + KCl
            2. 21 HST: 1/3 Urea
            3. 42 HST: 1/3 Urea
            
            ---
            
            #### 🌶️ Pupuk untuk Cabai
            
            **Rekomendasi:**
            - **Dasar:** Urea 200 kg + SP-36 200 kg + KCl 250 kg
            - **Alternatif:** NPK Grower 15-9-20 400 kg
            - **Daun:** Gandasil B 2 kg/ha (semprot)
            
            **Waktu Aplikasi:**
            - Setiap 2 minggu sekali
            - Fokus K tinggi saat berbuah
            """)
        
        with col2:
            st.markdown("""
            #### 🍅 Pupuk untuk Tomat
            
            **Rekomendasi:**
            - **Dasar:** Urea 150 kg + SP-36 200 kg + KCl 200 kg
            - **Alternatif:** NPK 15-15-15 300 kg + KCl 100 kg
            - **Daun:** Gandasil B 2 kg/ha
            
            **Waktu Aplikasi:**
            - Setiap 2 minggu sekali
            - Tingkatkan K saat berbuah
            
            ---
            
            #### 🥬 Pupuk untuk Sayuran Daun
            
            **Rekomendasi:**
            - **Dasar:** Urea 150 kg + NPK 15-15-15 200 kg
            - **Organik:** Kompos 5 ton/ha
            - **Daun:** Gandasil D 2 kg/ha
            
            **Waktu Aplikasi:**
            - Setiap 1-2 minggu
            - Fokus N tinggi untuk daun
            
            ---
            
            #### 💡 Tips Pemupukan
            
            1. **Waktu Aplikasi:**
               - Pagi (06:00-09:00) atau sore (15:00-18:00)
               - Hindari saat hujan atau panas terik
            
            2. **Cara Aplikasi:**
               - Tabur: Jarak 5-10 cm dari batang
               - Kocor: Larutkan dalam air
               - Semprot: Pagi/sore, hindari matahari terik
            
            3. **Penyimpanan:**
               - Tempat kering dan teduh
               - Tutup rapat setelah digunakan
               - Jauhkan dari jangkauan anak-anak
            """)

# ========== FOOTER ==========
st.markdown("---")
st.caption("""
🧪 **Katalog Pupuk & Harga v1.0**

💡 **Catatan**: Harga dapat berubah sewaktu-waktu tergantung lokasi dan distributor. 
Gunakan sebagai referensi dan konfirmasi harga dengan toko pertanian terdekat.

📊 **Sumber**: PT Pupuk Indonesia, Petrokimia Gresik, dan berbagai distributor resmi

⚠️ **Disclaimer**: Selalu ikuti petunjuk penggunaan pada kemasan. Konsultasikan dengan penyuluh pertanian untuk rekomendasi spesifik.
""")
