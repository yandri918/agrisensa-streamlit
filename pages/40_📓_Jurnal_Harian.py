import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import os
import io
from PIL import Image

# Page Config
st.set_page_config(
    page_title="Jurnal Harian Modern - AgriSensa",
    page_icon="📓",
    layout="wide"
)

# Constants
DATA_DIR = "data"
JOURNAL_FILE = os.path.join(DATA_DIR, "activity_journal.csv")
GROWTH_FILE = os.path.join(DATA_DIR, "growth_journal.csv")
COST_FILE = os.path.join(DATA_DIR, "cost_journal.csv")
PHOTOS_DIR = os.path.join(DATA_DIR, "photos")

# Commodity-specific parameters configuration
COMMODITY_PARAMS = {
    "Padi": {
        "basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"],
        "specific": ["jumlah_anakan", "panjang_malai_cm", "persen_pengisian"],
        "stages": ["Vegetatif", "Primordia", "Berbunga", "Pengisian Bulir", "Masak"]
    },
    "Jagung": {
        "basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"],
        "specific": ["jumlah_tongkol", "baris_biji", "panjang_tongkol_cm"],
        "stages": ["Vegetatif", "Tasseling", "Silking", "Pengisian Biji", "Masak Fisiologis"]
    },
    "Cabai": {
        "basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"],
        "specific": ["jumlah_buah", "panjang_buah_cm", "diameter_buah_mm"],
        "stages": ["Vegetatif", "Berbunga", "Berbuah Muda", "Berbuah Matang", "Panen"]
    },
    "Tomat": {
        "basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"],
        "specific": ["jumlah_tandan", "buah_per_tandan", "berat_buah_gram"],
        "stages": ["Vegetatif", "Berbunga", "Fruit Set", "Pembesaran Buah", "Pematangan"]
    },
    "Melon": {
        "basic": ["tinggi_cm", "jumlah_daun", "lebar_kanopi_cm"],
        "specific": ["jumlah_buah", "lingkar_buah_cm", "estimasi_brix"],
        "stages": ["Vegetatif", "Berbunga", "Fruit Set", "Pembesaran", "Pematangan"]
    },
    "Sawi": {
        "basic": ["tinggi_cm", "jumlah_daun", "lebar_daun_cm"],
        "specific": ["panjang_daun_cm", "daun_siap_panen", "berat_estimasi_gram"],
        "stages": ["Vegetatif Awal", "Vegetatif Tengah", "Siap Panen"]
    },
    "Kangkung": {
        "basic": ["tinggi_cm", "jumlah_daun", "diameter_batang_mm"],
        "specific": ["panjang_daun_cm", "lebar_daun_cm", "berat_estimasi_gram"],
        "stages": ["Vegetatif Awal", "Vegetatif Tengah", "Siap Panen"]
    },
    "Bayam": {
        "basic": ["tinggi_cm", "jumlah_daun", "lebar_daun_cm"],
        "specific": ["panjang_daun_cm", "daun_siap_panen", "berat_estimasi_gram"],
        "stages": ["Vegetatif Awal", "Vegetatif Tengah", "Siap Panen"]
    }
}

# Cost categories
COST_CATEGORIES = {
    "🌱 Benih/Bibit": ["Benih Hibrida", "Benih Lokal", "Bibit", "Lainnya"],
    "💊 Pupuk": ["Urea", "NPK", "TSP/SP36", "KCl", "Organik", "Hayati", "Lainnya"],
    "🛡️ Pestisida": ["Insektisida", "Fungisida", "Herbisida", "Nabati", "Lainnya"],
    "👷 Tenaga Kerja": ["Keluarga", "Harian", "Borongan", "Lainnya"],
    "💧 Irigasi/Air": ["Listrik Pompa", "Solar", "Biaya Air", "Lainnya"],
    "🛠️ Alat/Mesin": ["Sewa Traktor", "Sewa Sprayer", "Pembelian Alat", "Lainnya"],
    "🏗️ Infrastruktur": ["Greenhouse", "Mulsa", "Ajir", "Perbaikan", "Lainnya"],
    "🚚 Transportasi": ["Angkut Input", "Angkut Hasil", "BBM", "Lainnya"],
    "📋 Sertifikasi": ["Organik", "GAP", "Lab Test", "Lainnya"],
    "📢 Pemasaran": ["Kemasan", "Label", "Promosi", "Lainnya"]
}

# --- DATA INITIALIZATION ---
def init_data():
    """Initialize data directories and files"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
    
    # Activity journal
    if not os.path.exists(JOURNAL_FILE):
        df = pd.DataFrame(columns=[
            'tanggal', 'kategori', 'judul', 'catatan', 'biaya', 
            'kategori_biaya', 'lokasi', 'prioritas', 'status', 
            'foto_path', 'created_at'
        ])
        df.to_csv(JOURNAL_FILE, index=False)
    
    # Growth journal with enhanced parameters
    if not os.path.exists(GROWTH_FILE):
        df = pd.DataFrame(columns=[
            'tanggal', 'komoditas', 'varietas', 'lokasi', 'usia_hst',
            # Basic parameters
            'tinggi_cm', 'jumlah_daun', 'diameter_batang_mm', 'lebar_kanopi_cm',
            # Advanced parameters
            'spad', 'stage', 'penyakit_score', 'hama_score',
            # Commodity-specific (stored as JSON-like string)
            'param_spesifik',
            'catatan', 'foto_path', 'created_at'
        ])
        df.to_csv(GROWTH_FILE, index=False)
    
    # Cost journal
    if not os.path.exists(COST_FILE):
        df = pd.DataFrame(columns=[
            'tanggal', 'kategori_biaya', 'sub_kategori', 'item',
            'jumlah', 'satuan', 'harga_satuan', 'total',
            'supplier', 'lokasi', 'catatan', 'created_at'
        ])
        df.to_csv(COST_FILE, index=False)

# --- DATA LOADING ---
def load_journal():
    """Load activity journal"""
    try:
        if os.path.exists(JOURNAL_FILE):
            df = pd.read_csv(JOURNAL_FILE)
            # Ensure all columns exist
            required_cols = ['tanggal', 'kategori', 'judul', 'catatan', 'biaya', 
                           'kategori_biaya', 'lokasi', 'prioritas', 'status', 
                           'foto_path', 'created_at']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = ""
            return df
    except Exception as e:
        st.error(f"Error loading journal: {e}")
    return pd.DataFrame(columns=['tanggal', 'kategori', 'judul', 'catatan', 'biaya', 
                                'kategori_biaya', 'lokasi', 'prioritas', 'status', 
                                'foto_path', 'created_at'])

def load_growth():
    """Load growth journal"""
    try:
        if os.path.exists(GROWTH_FILE):
            df = pd.read_csv(GROWTH_FILE)
            # Ensure all columns exist
            required_cols = ['tanggal', 'komoditas', 'varietas', 'lokasi', 'usia_hst',
                           'tinggi_cm', 'jumlah_daun', 'diameter_batang_mm', 'lebar_kanopi_cm',
                           'spad', 'stage', 'penyakit_score', 'hama_score',
                           'param_spesifik', 'catatan', 'foto_path', 'created_at']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = "" if col in ['param_spesifik', 'catatan', 'foto_path', 'created_at', 
                                           'varietas', 'lokasi', 'stage'] else 0
            return df
    except Exception as e:
        st.error(f"Error loading growth data: {e}")
    return pd.DataFrame(columns=['tanggal', 'komoditas', 'varietas', 'lokasi', 'usia_hst',
                                'tinggi_cm', 'jumlah_daun', 'diameter_batang_mm', 'lebar_kanopi_cm',
                                'spad', 'stage', 'penyakit_score', 'hama_score',
                                'param_spesifik', 'catatan', 'foto_path', 'created_at'])

def load_costs():
    """Load cost journal"""
    try:
        if os.path.exists(COST_FILE):
            return pd.read_csv(COST_FILE)
    except Exception as e:
        st.error(f"Error loading costs: {e}")
    return pd.DataFrame(columns=['tanggal', 'kategori_biaya', 'sub_kategori', 'item',
                                'jumlah', 'satuan', 'harga_satuan', 'total',
                                'supplier', 'lokasi', 'catatan', 'created_at'])

# --- DATA SAVING ---
def save_activity(data_dict):
    """Save activity to journal"""
    df = load_journal()
    data_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([data_dict])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(JOURNAL_FILE, index=False)

def save_growth(data_dict):
    """Save growth data"""
    df = load_growth()
    data_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([data_dict])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(GROWTH_FILE, index=False)

def save_cost(data_dict):
    """Save cost data"""
    df = load_costs()
    data_dict['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame([data_dict])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(COST_FILE, index=False)

# Initialize data
init_data()

# --- UI STYLING ---
st.markdown("""
<style>
    /* Card Styles */
    .journal-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-left: 5px solid #4CAF50;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .journal-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    .journal-card.expense { border-left-color: #f44336; }
    .journal-card.harvest { border-left-color: #ff9800; }
    .journal-card.growth { border-left-color: #2196F3; }
    .journal-card.cost { border-left-color: #9c27b0; }
    
    .card-date { 
        font-size: 0.75em; 
        color: #888; 
        margin-bottom: 6px;
        font-weight: 500;
    }
    .card-title { 
        font-weight: 700; 
        font-size: 1.1em; 
        color: #1a1a1a;
        margin-bottom: 8px;
    }
    .card-cost { 
        float: right; 
        font-weight: bold; 
        color: #d32f2f; 
        font-size: 1em;
        background: #ffebee;
        padding: 4px 12px;
        border-radius: 20px;
    }
    .card-metric { 
        display: inline-block; 
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #1565c0; 
        padding: 4px 10px; 
        border-radius: 16px; 
        font-size: 0.85em; 
        font-weight: 600;
        margin-right: 6px;
        margin-top: 4px;
    }
    .priority-high { 
        background: #ffebee; 
        color: #c62828; 
        padding: 2px 8px; 
        border-radius: 12px; 
        font-size: 0.75em;
        font-weight: 600;
    }
    .priority-medium { 
        background: #fff3e0; 
        color: #e65100; 
        padding: 2px 8px; 
        border-radius: 12px; 
        font-size: 0.75em;
        font-weight: 600;
    }
    .priority-low { 
        background: #e8f5e9; 
        color: #2e7d32; 
        padding: 2px 8px; 
        border-radius: 12px; 
        font-size: 0.75em;
        font-weight: 600;
    }
    .status-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75em;
        font-weight: 600;
        margin-left: 8px;
    }
    .status-planned { background: #e3f2fd; color: #1976d2; }
    .status-progress { background: #fff3e0; color: #f57c00; }
    .status-completed { background: #e8f5e9; color: #388e3c; }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        margin: 8px 0;
    }
    .metric-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("📓 Jurnal Harian Modern")
st.caption("🎯 Central Control Room: Catat aktivitas & pertumbuhan, pantau biaya, dan review timeline")

# --- MAIN LAYOUT ---
tab_input, tab_timeline, tab_analytics = st.tabs([
    "📝 Input Data", 
    "📅 Timeline & Review", 
    "📊 Analytics & Reports"
])

# ========================================
# TAB 1: INPUT DATA
# ========================================
with tab_input:
    col_left, col_right = st.columns([1, 1])
    
    # --- ACTIVITY INPUT ---
    with col_left:
        st.subheader("📝 Catat Aktivitas Harian")
        
        with st.form("activity_form", clear_on_submit=True):
            act_date = st.date_input("📅 Tanggal", datetime.now())
            
            col_cat, col_loc = st.columns(2)
            with col_cat:
                act_category = st.selectbox("Kategori", [
                    "✅ Umum", "💧 Penyiraman", "💊 Pemupukan", 
                    "🛡️ Pengendalian Hama", "🛠️ Perawatan", 
                    "🚜 Panen", "💰 Pembelian"
                ])
            with col_loc:
                act_location = st.text_input("Lokasi/Blok", placeholder="Blok A, Lahan 1")
            
            act_title = st.text_input("📌 Judul Aktivitas", placeholder="Contoh: Pemupukan NPK Fase Vegetatif")
            act_notes = st.text_area("📄 Catatan Detail", placeholder="Dosis, kondisi cuaca, kendala yang dihadapi...", height=100)
            
            col_pri, col_stat = st.columns(2)
            with col_pri:
                act_priority = st.selectbox("Prioritas", ["Rendah", "Sedang", "Tinggi", "Kritis"])
            with col_stat:
                act_status = st.selectbox("Status", ["Direncanakan", "Sedang Berjalan", "Selesai"])
            
            col_cost, col_cat_cost = st.columns(2)
            with col_cost:
                act_cost = st.number_input("💰 Biaya (Rp)", min_value=0, step=1000, value=0)
            with col_cat_cost:
                if act_cost > 0:
                    act_cost_cat = st.selectbox("Kategori Biaya", list(COST_CATEGORIES.keys()))
                else:
                    act_cost_cat = ""
            
            submit_activity = st.form_submit_button("💾 Simpan Aktivitas", use_container_width=True, type="primary")
            
            if submit_activity:
                if act_title:
                    save_activity({
                        'tanggal': act_date.strftime("%Y-%m-%d"),
                        'kategori': act_category,
                        'judul': act_title,
                        'catatan': act_notes,
                        'biaya': act_cost,
                        'kategori_biaya': act_cost_cat,
                        'lokasi': act_location,
                        'prioritas': act_priority,
                        'status': act_status,
                        'foto_path': ""
                    })
                    st.success("✅ Aktivitas berhasil disimpan!")
                    st.rerun()
                else:
                    st.error("❌ Judul aktivitas wajib diisi!")
    
    # --- GROWTH TRACKING INPUT ---
    with col_right:
        st.subheader("📏 Catat Pertumbuhan (Advanced)")
        
        with st.form("growth_form", clear_on_submit=True):
            growth_date = st.date_input("📅 Tanggal Pengukuran", datetime.now(), key="gdate")
            
            col_com, col_var = st.columns(2)
            with col_com:
                growth_commodity = st.selectbox("Komoditas", list(COMMODITY_PARAMS.keys()))
            with col_var:
                growth_variety = st.text_input("Varietas", placeholder="Contoh: Inpari 32")
            
            col_hst, col_loc = st.columns(2)
            with col_hst:
                growth_hst = st.number_input("Usia (HST)", min_value=1, value=1)
            with col_loc:
                growth_location = st.text_input("Lokasi", placeholder="Blok/Plot", key="gloc")
            
            st.markdown("**📊 Parameter Dasar**")
            col_p1, col_p2, col_p3 = st.columns(3)
            
            params = COMMODITY_PARAMS[growth_commodity]
            
            with col_p1:
                if "tinggi_cm" in params["basic"]:
                    growth_height = st.number_input("Tinggi (cm)", min_value=0.0, value=0.0, step=0.1)
                else:
                    growth_height = 0.0
            
            with col_p2:
                if "jumlah_daun" in params["basic"]:
                    growth_leaves = st.number_input("Jumlah Daun", min_value=0, value=0)
                else:
                    growth_leaves = 0
            
            with col_p3:
                if "diameter_batang_mm" in params["basic"]:
                    growth_diameter = st.number_input("Diameter Batang (mm)", min_value=0.0, value=0.0, step=0.1)
                elif "lebar_kanopi_cm" in params["basic"]:
                    growth_diameter = st.number_input("Lebar Kanopi (cm)", min_value=0.0, value=0.0, step=0.1)
                elif "lebar_daun_cm" in params["basic"]:
                    growth_diameter = st.number_input("Lebar Daun (cm)", min_value=0.0, value=0.0, step=0.1)
                else:
                    growth_diameter = 0.0
            
            st.markdown(f"**🎯 Parameter Spesifik {growth_commodity}**")
            specific_params = {}
            
            if len(params["specific"]) >= 3:
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    key1 = params["specific"][0]
                    specific_params[key1] = st.number_input(
                        key1.replace("_", " ").title(), 
                        min_value=0.0, value=0.0, step=0.1
                    )
                with col_s2:
                    key2 = params["specific"][1]
                    specific_params[key2] = st.number_input(
                        key2.replace("_", " ").title(), 
                        min_value=0.0, value=0.0, step=0.1
                    )
                with col_s3:
                    key3 = params["specific"][2]
                    specific_params[key3] = st.number_input(
                        key3.replace("_", " ").title(), 
                        min_value=0.0, value=0.0, step=0.1
                    )
            
            st.markdown("**🔬 Parameter Lanjutan**")
            col_a1, col_a2, col_a3, col_a4 = st.columns(4)
            
            with col_a1:
                growth_spad = st.number_input("SPAD (0-99)", min_value=0.0, max_value=99.0, value=0.0, step=0.1)
            with col_a2:
                growth_disease = st.slider("Skor Penyakit", 0, 5, 0, help="0=Sehat, 5=Parah")
            with col_a3:
                growth_pest = st.slider("Skor Hama", 0, 5, 0, help="0=Tidak ada, 5=Parah")
            with col_a4:
                growth_stage = st.selectbox("Fase Pertumbuhan", params["stages"])
            
            growth_notes = st.text_area("📝 Catatan", placeholder="Observasi tambahan...", height=80, key="gnotes")
            
            submit_growth = st.form_submit_button("💾 Simpan Data Pertumbuhan", use_container_width=True, type="primary")
            
            if submit_growth:
                # Convert specific params to string for storage
                import json
                param_str = json.dumps(specific_params)
                
                save_growth({
                    'tanggal': growth_date.strftime("%Y-%m-%d"),
                    'komoditas': growth_commodity,
                    'varietas': growth_variety,
                    'lokasi': growth_location,
                    'usia_hst': growth_hst,
                    'tinggi_cm': growth_height,
                    'jumlah_daun': growth_leaves,
                    'diameter_batang_mm': growth_diameter,
                    'lebar_kanopi_cm': 0.0,  # Can be added later
                    'spad': growth_spad,
                    'stage': growth_stage,
                    'penyakit_score': growth_disease,
                    'hama_score': growth_pest,
                    'param_spesifik': param_str,
                    'catatan': growth_notes,
                    'foto_path': ""
                })
                st.success(f"✅ Data pertumbuhan {growth_commodity} berhasil disimpan!")
                st.rerun()
    
    # --- COST TRACKING INPUT ---
    st.divider()
    st.subheader("💰 Catat Pengeluaran Detail")
    
    with st.form("cost_form", clear_on_submit=True):
        col_c1, col_c2, col_c3 = st.columns(3)
        
        with col_c1:
            cost_date = st.date_input("📅 Tanggal", datetime.now(), key="cdate")
        with col_c2:
            cost_category = st.selectbox("Kategori", list(COST_CATEGORIES.keys()), key="ccat")
        with col_c3:
            cost_subcategory = st.selectbox("Sub-Kategori", COST_CATEGORIES[cost_category])
        
        col_c4, col_c5, col_c6 = st.columns(3)
        
        with col_c4:
            cost_item = st.text_input("Nama Item", placeholder="Contoh: Urea 50kg")
        with col_c5:
            cost_qty = st.number_input("Jumlah", min_value=0.0, value=1.0, step=0.1)
        with col_c6:
            cost_unit = st.text_input("Satuan", placeholder="kg, liter, karung")
        
        col_c7, col_c8 = st.columns(2)
        
        with col_c7:
            cost_price = st.number_input("Harga Satuan (Rp)", min_value=0, step=100, value=0)
        with col_c8:
            cost_total = cost_qty * cost_price
            st.metric("Total Biaya", f"Rp {cost_total:,.0f}")
        
        col_c9, col_c10 = st.columns(2)
        
        with col_c9:
            cost_supplier = st.text_input("Supplier/Toko", placeholder="Nama toko/supplier")
        with col_c10:
            cost_location = st.text_input("Lokasi Penggunaan", placeholder="Blok/Lahan", key="cloc")
        
        cost_notes = st.text_area("Catatan", placeholder="Informasi tambahan...", height=60, key="cnotes")
        
        submit_cost = st.form_submit_button("💾 Simpan Pengeluaran", use_container_width=True, type="primary")
        
        if submit_cost:
            if cost_item and cost_total > 0:
                save_cost({
                    'tanggal': cost_date.strftime("%Y-%m-%d"),
                    'kategori_biaya': cost_category,
                    'sub_kategori': cost_subcategory,
                    'item': cost_item,
                    'jumlah': cost_qty,
                    'satuan': cost_unit,
                    'harga_satuan': cost_price,
                    'total': cost_total,
                    'supplier': cost_supplier,
                    'lokasi': cost_location,
                    'catatan': cost_notes
                })
                st.success(f"✅ Pengeluaran Rp {cost_total:,.0f} berhasil dicatat!")
                st.rerun()
            else:
                st.error("❌ Nama item dan total biaya harus diisi!")

# ========================================
# TAB 2: TIMELINE & REVIEW
# ========================================
with tab_timeline:
    st.subheader("📅 Timeline Aktivitas & Pertumbuhan")
    
    # Load all data
    df_activities = load_journal()
    df_growth = load_growth()
    df_costs = load_costs()
    
    # Filters
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        filter_type = st.multiselect(
            "Tipe Data",
            ["Aktivitas", "Pertumbuhan", "Pengeluaran"],
            default=["Aktivitas", "Pertumbuhan", "Pengeluaran"]
        )
    
    with col_f2:
        # Date range filter
        if not df_activities.empty or not df_growth.empty:
            all_dates = []
            if not df_activities.empty:
                all_dates.extend(pd.to_datetime(df_activities['tanggal']).tolist())
            if not df_growth.empty:
                all_dates.extend(pd.to_datetime(df_growth['tanggal']).tolist())
            
            if all_dates:
                min_date = min(all_dates).date()
                max_date = max(all_dates).date()
                date_range = st.date_input(
                    "Rentang Tanggal",
                    value=(min_date, max_date),
                    key="date_range"
                )
            else:
                date_range = None
        else:
            date_range = None
    
    with col_f3:
        search_keyword = st.text_input("🔍 Cari Kata Kunci", placeholder="Cari judul, catatan...")
    
    with col_f4:
        sort_order = st.selectbox("Urutan", ["Terbaru", "Terlama"])
    
    st.divider()
    
    # Build timeline
    timeline = []
    
    # Add activities
    if "Aktivitas" in filter_type and not df_activities.empty:
        for _, row in df_activities.iterrows():
            timeline.append({
                'date': pd.to_datetime(row['tanggal']),
                'raw_date': row['tanggal'],
                'type': 'activity',
                'title': row['judul'],
                'desc': row['catatan'],
                'meta': row['kategori'],
                'cost': row['biaya'] if pd.notna(row['biaya']) else 0,
                'location': row.get('lokasi', ''),
                'priority': row.get('prioritas', ''),
                'status': row.get('status', ''),
                'style': 'expense' if row['biaya'] > 0 else 'journal-card'
            })
    
    # Add growth data
    if "Pertumbuhan" in filter_type and not df_growth.empty:
        for _, row in df_growth.iterrows():
            import json
            try:
                specific = json.loads(row['param_spesifik']) if pd.notna(row['param_spesifik']) and row['param_spesifik'] else {}
            except:
                specific = {}
            
            # Build metrics HTML with proper handling of numeric values
            metrics_html = ""
            
            if pd.notna(row['tinggi_cm']) and row['tinggi_cm'] > 0:
                metrics_html += f"<span class='card-metric'>📏 {row['tinggi_cm']:.1f} cm</span>"
            
            if pd.notna(row['jumlah_daun']) and row['jumlah_daun'] > 0:
                metrics_html += f"<span class='card-metric'>🍃 {int(row['jumlah_daun'])} daun</span>"
            
            if pd.notna(row['diameter_batang_mm']) and row['diameter_batang_mm'] > 0:
                metrics_html += f"<span class='card-metric'>📐 {row['diameter_batang_mm']:.1f} mm</span>"
            
            if pd.notna(row['spad']) and row['spad'] > 0:
                metrics_html += f"<span class='card-metric'>🔬 SPAD {row['spad']:.1f}</span>"
            
            # Handle empty varietas
            varietas_display = row['varietas'] if pd.notna(row['varietas']) and row['varietas'] else "(Varietas tidak dicatat)"
            
            timeline.append({
                'date': pd.to_datetime(row['tanggal']),
                'raw_date': row['tanggal'],
                'type': 'growth',
                'title': f"Monitoring {row['komoditas']} - {varietas_display}",
                'desc': metrics_html,
                'meta': f"HST {row['usia_hst']} | {row['stage']}",
                'cost': 0,
                'location': row.get('lokasi', ''),
                'priority': '',
                'status': '',
                'style': 'growth'
            })
    
    # Add costs
    if "Pengeluaran" in filter_type and not df_costs.empty:
        for _, row in df_costs.iterrows():
            timeline.append({
                'date': pd.to_datetime(row['tanggal']),
                'raw_date': row['tanggal'],
                'type': 'cost',
                'title': f"💸 {row['item']} ({row['jumlah']} {row['satuan']})",
                'desc': f"{row['kategori_biaya']} - {row['sub_kategori']}",
                'meta': row.get('supplier', ''),
                'cost': row['total'],
                'location': row.get('lokasi', ''),
                'priority': '',
                'status': '',
                'style': 'cost'
            })
    
    # Apply filters
    if date_range and len(date_range) == 2:
        timeline = [t for t in timeline if date_range[0] <= t['date'].date() <= date_range[1]]
    
    if search_keyword:
        timeline = [t for t in timeline if 
                   search_keyword.lower() in t['title'].lower() or 
                   search_keyword.lower() in str(t['desc']).lower()]
    
    # Sort
    timeline.sort(key=lambda x: x['date'], reverse=(sort_order == "Terbaru"))
    
    # Display timeline
    if timeline:
        st.caption(f"📊 Menampilkan {len(timeline)} entri")
        
        for item in timeline:
            # Icon selection
            icon = "📝"
            if item['style'] == 'growth':
                icon = "📈"
            elif item['style'] == 'harvest':
                icon = "🌾"
            elif item['style'] == 'expense':
                icon = "💸"
            elif item['style'] == 'cost':
                icon = "💰"
            
            # Cost display
            cost_html = f'<div class="card-cost">Rp {item["cost"]:,.0f}</div>' if item['cost'] > 0 else ""
            
            # Priority badge
            priority_html = ""
            if item['priority']:
                priority_class = f"priority-{item['priority'].lower()}"
                priority_html = f'<span class="{priority_class}">{item["priority"]}</span>'
            
            # Status badge
            status_html = ""
            if item['status']:
                status_map = {
                    "Direncanakan": "planned",
                    "Sedang Berjalan": "progress",
                    "Selesai": "completed"
                }
                status_class = status_map.get(item['status'], 'planned')
                status_html = f'<span class="status-badge status-{status_class}">{item["status"]}</span>'
            
            # Location - handle nan/empty values
            location_display = item['location'] if item['location'] and str(item['location']).lower() != 'nan' else ""
            location_html = f" 📍 {location_display}" if location_display else ""
            
            # For growth entries, don't add icon since title is already descriptive
            # For other entries, add the icon
            title_display = item['title'] if item['style'] == 'growth' else f"{icon} {item['title']}"
            
            st.markdown(f"""
            <div class="{item['style']}">
                <div class="card-date">{item['raw_date']} • {item['meta']}{location_html}</div>
                {cost_html}
                <div class="card-title">{title_display} {priority_html}{status_html}</div>
                <div style="margin-top: 8px; color: #444;">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 Belum ada data yang sesuai dengan filter. Mulai mencatat di tab **Input Data**!")

# ========================================
# TAB 3: ANALYTICS & REPORTS
# ========================================
with tab_analytics:
    st.subheader("📊 Analytics Dashboard & Reports")
    
    # Load data
    df_costs = load_costs()
    df_activities = load_journal()
    df_growth = load_growth()
    
    # --- COST ANALYTICS ---
    st.markdown("### 💰 Analisis Biaya")
    
    if not df_costs.empty:
        # Summary metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        total_cost = df_costs['total'].sum()
        avg_cost = df_costs['total'].mean()
        num_transactions = len(df_costs)
        
        # Get most expensive category
        category_totals = df_costs.groupby('kategori_biaya')['total'].sum()
        top_category = category_totals.idxmax() if not category_totals.empty else "N/A"
        
        with col_m1:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div class="metric-label">Total Pengeluaran</div>
                <div class="metric-value">Rp {total_cost:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">Rata-rata per Transaksi</div>
                <div class="metric-value">Rp {avg_cost:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">Jumlah Transaksi</div>
                <div class="metric-value">{num_transactions}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label">Kategori Terbesar</div>
                <div class="metric-value" style="font-size: 1.2em;">{top_category.split()[0]}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Pie chart by category
            fig_pie = px.pie(
                df_costs.groupby('kategori_biaya')['total'].sum().reset_index(),
                values='total',
                names='kategori_biaya',
                title='📊 Distribusi Biaya per Kategori',
                hole=0.4
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            # Bar chart by subcategory (top 10)
            subcategory_totals = df_costs.groupby('sub_kategori')['total'].sum().sort_values(ascending=False).head(10)
            fig_bar = px.bar(
                x=subcategory_totals.values,
                y=subcategory_totals.index,
                orientation='h',
                title='📊 Top 10 Sub-Kategori Pengeluaran',
                labels={'x': 'Total (Rp)', 'y': 'Sub-Kategori'}
            )
            fig_bar.update_traces(marker_color='#667eea')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Time series
        df_costs['tanggal'] = pd.to_datetime(df_costs['tanggal'])
        daily_costs = df_costs.groupby('tanggal')['total'].sum().reset_index()
        
        fig_time = px.line(
            daily_costs,
            x='tanggal',
            y='total',
            title='📈 Tren Pengeluaran Harian',
            labels={'tanggal': 'Tanggal', 'total': 'Total Biaya (Rp)'},
            markers=True
        )
        fig_time.update_traces(line_color='#f5576c', line_width=3)
        st.plotly_chart(fig_time, use_container_width=True)
        
        # Detailed table
        with st.expander("📋 Lihat Detail Pengeluaran"):
            st.dataframe(
                df_costs.sort_values('tanggal', ascending=False),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("💡 Belum ada data pengeluaran. Mulai mencatat di tab **Input Data**!")
    
    st.divider()
    
    # --- GROWTH ANALYTICS ---
    st.markdown("### 📈 Analisis Pertumbuhan")
    
    if not df_growth.empty:
        # Select commodity for analysis
        commodities = df_growth['komoditas'].unique()
        selected_commodity = st.selectbox("Pilih Komoditas untuk Analisis", commodities)
        
        df_commodity = df_growth[df_growth['komoditas'] == selected_commodity].copy()
        df_commodity = df_commodity.sort_values('usia_hst')
        
        if not df_commodity.empty:
            # Growth charts
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                # Height growth
                fig_height = px.line(
                    df_commodity,
                    x='usia_hst',
                    y='tinggi_cm',
                    title=f'📏 Pertumbuhan Tinggi {selected_commodity}',
                    labels={'usia_hst': 'Usia (HST)', 'tinggi_cm': 'Tinggi (cm)'},
                    markers=True
                )
                fig_height.update_traces(line_color='#43e97b', line_width=3)
                st.plotly_chart(fig_height, use_container_width=True)
            
            with col_g2:
                # Leaf count
                fig_leaves = px.line(
                    df_commodity,
                    x='usia_hst',
                    y='jumlah_daun',
                    title=f'🍃 Pertumbuhan Jumlah Daun {selected_commodity}',
                    labels={'usia_hst': 'Usia (HST)', 'jumlah_daun': 'Jumlah Daun'},
                    markers=True
                )
                fig_leaves.update_traces(line_color='#4facfe', line_width=3)
                st.plotly_chart(fig_leaves, use_container_width=True)
            
            # Health indicators
            col_h1, col_h2, col_h3 = st.columns(3)
            
            with col_h1:
                if df_commodity['spad'].max() > 0:
                    fig_spad = px.line(
                        df_commodity,
                        x='usia_hst',
                        y='spad',
                        title='🔬 SPAD Index',
                        markers=True
                    )
                    st.plotly_chart(fig_spad, use_container_width=True)
            
            with col_h2:
                fig_disease = px.line(
                    df_commodity,
                    x='usia_hst',
                    y='penyakit_score',
                    title='🦠 Skor Penyakit',
                    markers=True
                )
                fig_disease.update_traces(line_color='#f5576c')
                st.plotly_chart(fig_disease, use_container_width=True)
            
            with col_h3:
                fig_pest = px.line(
                    df_commodity,
                    x='usia_hst',
                    y='hama_score',
                    title='🐛 Skor Hama',
                    markers=True
                )
                fig_pest.update_traces(line_color='#ff9800')
                st.plotly_chart(fig_pest, use_container_width=True)
            
            # Growth stage distribution
            stage_counts = df_commodity['stage'].value_counts()
            fig_stages = px.bar(
                x=stage_counts.index,
                y=stage_counts.values,
                title=f'📊 Distribusi Fase Pertumbuhan {selected_commodity}',
                labels={'x': 'Fase', 'y': 'Jumlah Pengamatan'}
            )
            st.plotly_chart(fig_stages, use_container_width=True)
            
        else:
            st.info(f"Belum ada data untuk {selected_commodity}")
    else:
        st.info("💡 Belum ada data pertumbuhan. Mulai mencatat di tab **Input Data**!")
    
    st.divider()
    
    # --- ACTIVITY ANALYTICS ---
    st.markdown("### 📝 Analisis Aktivitas")
    
    if not df_activities.empty:
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            # Activity by category
            activity_counts = df_activities['kategori'].value_counts()
            fig_act_cat = px.pie(
                values=activity_counts.values,
                names=activity_counts.index,
                title='📊 Distribusi Aktivitas per Kategori',
                hole=0.3
            )
            st.plotly_chart(fig_act_cat, use_container_width=True)
        
        with col_a2:
            # Activity by status
            if 'status' in df_activities.columns:
                status_counts = df_activities['status'].value_counts()
                fig_status = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    title='📊 Status Aktivitas',
                    labels={'x': 'Status', 'y': 'Jumlah'}
                )
                st.plotly_chart(fig_status, use_container_width=True)
        
        # Priority distribution
        if 'prioritas' in df_activities.columns:
            priority_counts = df_activities['prioritas'].value_counts()
            fig_priority = px.bar(
                x=priority_counts.index,
                y=priority_counts.values,
                title='⚡ Distribusi Prioritas Aktivitas',
                labels={'x': 'Prioritas', 'y': 'Jumlah'},
                color=priority_counts.index,
                color_discrete_map={
                    'Kritis': '#c62828',
                    'Tinggi': '#e65100',
                    'Sedang': '#f57c00',
                    'Rendah': '#388e3c'
                }
            )
            st.plotly_chart(fig_priority, use_container_width=True)
    else:
        st.info("💡 Belum ada data aktivitas. Mulai mencatat di tab **Input Data**!")
    
    # --- EXPORT SECTION ---
    st.divider()
    st.markdown("### 📥 Export Data")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        if not df_activities.empty:
            csv_activities = df_activities.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📄 Download Aktivitas (CSV)",
                csv_activities,
                "aktivitas_jurnal.csv",
                "text/csv",
                use_container_width=True
            )
    
    with col_e2:
        if not df_growth.empty:
            csv_growth = df_growth.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Download Pertumbuhan (CSV)",
                csv_growth,
                "pertumbuhan_jurnal.csv",
                "text/csv",
                use_container_width=True
            )
    
    with col_e3:
        if not df_costs.empty:
            csv_costs = df_costs.to_csv(index=False).encode('utf-8')
            st.download_button(
                "💰 Download Pengeluaran (CSV)",
                csv_costs,
                "pengeluaran_jurnal.csv",
                "text/csv",
                use_container_width=True
            )

# --- FOOTER ---
st.divider()
st.caption("💡 **Tips**: Data tersimpan otomatis di folder `data/`. Backup secara berkala untuk keamanan data Anda!")
