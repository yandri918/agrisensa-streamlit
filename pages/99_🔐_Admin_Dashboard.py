# AgriSensa Admin Dashboard
# Streamlit-only admin panel with session-based authentication

import streamlit as st
import pandas as pd
from datetime import datetime, date
import json

# Auth imports 
from utils.auth import require_auth, show_user_info_sidebar, get_current_user, is_authenticated

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Admin Dashboard - AgriSensa",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== AUTH CHECK ==========
user = require_auth()

# Check if admin
if user.get('role') != 'admin':
    st.error("🚫 Akses ditolak! Halaman ini hanya untuk Admin.")
    st.info("Login dengan akun admin untuk mengakses dashboard ini.")
    st.stop()

show_user_info_sidebar()

# ========== STYLING ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .admin-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
    }
    .admin-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .admin-subtitle {
        opacity: 0.8;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE FOR DATA ==========
if 'commodities_db' not in st.session_state:
    st.session_state.commodities_db = [
        {'id': 1, 'name': 'Beras Premium', 'category': 'Pangan', 'unit': 'kg', 'price': 15000, 'active': True},
        {'id': 2, 'name': 'Cabai Rawit', 'category': 'Sayuran', 'unit': 'kg', 'price': 80000, 'active': True},
        {'id': 3, 'name': 'Bawang Merah', 'category': 'Sayuran', 'unit': 'kg', 'price': 45000, 'active': True},
        {'id': 4, 'name': 'Jagung Pipil', 'category': 'Pangan', 'unit': 'kg', 'price': 8000, 'active': True},
        {'id': 5, 'name': 'Kedelai', 'category': 'Pangan', 'unit': 'kg', 'price': 12000, 'active': True},
        {'id': 6, 'name': 'Gula Pasir', 'category': 'Pangan', 'unit': 'kg', 'price': 16000, 'active': True},
        {'id': 7, 'name': 'Bayam', 'category': 'Sayuran', 'unit': 'ikat', 'price': 5000, 'active': True},
        {'id': 8, 'name': 'Kangkung', 'category': 'Sayuran', 'unit': 'ikat', 'price': 4000, 'active': True},
        {'id': 9, 'name': 'Tomat', 'category': 'Sayuran', 'unit': 'kg', 'price': 15000, 'active': True},
        {'id': 10, 'name': 'Jeruk', 'category': 'Buah', 'unit': 'kg', 'price': 25000, 'active': True},
    ]

if 'manual_prices_db' not in st.session_state:
    st.session_state.manual_prices_db = []

if 'audit_log_db' not in st.session_state:
    st.session_state.audit_log_db = []


def log_action(action, table, record_id=None, details=""):
    """Log admin action."""
    st.session_state.audit_log_db.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user': user['username'],
        'action': action,
        'table': table,
        'record_id': record_id,
        'details': details
    })


def get_next_id(db_list):
    """Get next ID for a database."""
    if not db_list:
        return 1
    return max(item['id'] for item in db_list) + 1


# ========== HEADER ==========
st.markdown("""
<div class="admin-header">
    <h1 class="admin-title">🛡️ Admin Dashboard</h1>
    <p class="admin-subtitle">Enterprise Management Console - Streamlit Edition</p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR NAVIGATION ==========
menu = st.sidebar.radio(
    "📱 Menu Admin",
    ["📊 Dashboard", "🌾 Komoditas", "💰 Harga Manual", "📝 Audit Log"],
    label_visibility="collapsed"
)

# ========== DASHBOARD ==========
if menu == "📊 Dashboard":
    st.subheader("📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Komoditas", len(st.session_state.commodities_db))
    with col2:
        active = len([c for c in st.session_state.commodities_db if c['active']])
        st.metric("✅ Komoditas Aktif", active)
    with col3:
        st.metric("💰 Harga Manual", len(st.session_state.manual_prices_db))
    with col4:
        st.metric("📝 Total Log", len(st.session_state.audit_log_db))
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Aktivitas Terbaru")
    if st.session_state.audit_log_db:
        recent = st.session_state.audit_log_db[-10:][::-1]  # Last 10, reversed
        df = pd.DataFrame(recent)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada aktivitas tercatat")

# ========== COMMODITIES ==========
elif menu == "🌾 Komoditas":
    st.subheader("🌾 Manajemen Komoditas")
    
    tab1, tab2, tab3 = st.tabs(["📋 Daftar", "➕ Tambah Baru", "📁 Import CSV"])
    
    with tab1:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            search = st.text_input("🔍 Cari", placeholder="Nama komoditas...")
        with col2:
            category_filter = st.selectbox("Kategori", ["Semua", "Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"])
        
        # Filter data
        commodities = st.session_state.commodities_db
        if search:
            commodities = [c for c in commodities if search.lower() in c['name'].lower()]
        if category_filter != "Semua":
            commodities = [c for c in commodities if c['category'] == category_filter]
        
        if commodities:
            df = pd.DataFrame(commodities)
            df['active'] = df['active'].apply(lambda x: '✅' if x else '❌')
            df['price'] = df['price'].apply(lambda x: f"Rp {x:,}")
            df.columns = ['ID', 'Nama', 'Kategori', 'Unit', 'Harga', 'Aktif']
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Edit section
            st.markdown("---")
            st.subheader("✏️ Edit / Hapus Komoditas")
            
            commodity_options = {c['name']: c['id'] for c in commodities}
            if commodity_options:
                selected_name = st.selectbox("Pilih komoditas", list(commodity_options.keys()))
                selected_id = commodity_options[selected_name]
                selected = next(c for c in st.session_state.commodities_db if c['id'] == selected_id)
                
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Nama", value=selected['name'])
                        new_category = st.selectbox("Kategori", 
                            ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"],
                            index=["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"].index(selected['category']) if selected['category'] in ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"] else 0
                        )
                    with col2:
                        new_unit = st.text_input("Unit", value=selected['unit'])
                        new_price = st.number_input("Harga", value=selected['price'])
                    
                    new_active = st.checkbox("Aktif", value=selected['active'])
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.form_submit_button("💾 Simpan", type="primary", use_container_width=True):
                            for c in st.session_state.commodities_db:
                                if c['id'] == selected_id:
                                    c['name'] = new_name
                                    c['category'] = new_category
                                    c['unit'] = new_unit
                                    c['price'] = new_price
                                    c['active'] = new_active
                                    break
                            log_action('UPDATE', 'commodities', selected_id, f"Updated {new_name}")
                            st.success("✅ Berhasil diupdate!")
                            st.rerun()
                    
                    with col_btn2:
                        if st.form_submit_button("🗑️ Hapus", use_container_width=True):
                            st.session_state.commodities_db = [c for c in st.session_state.commodities_db if c['id'] != selected_id]
                            log_action('DELETE', 'commodities', selected_id, f"Deleted {selected['name']}")
                            st.success("✅ Berhasil dihapus!")
                            st.rerun()
        else:
            st.info("Tidak ada komoditas ditemukan")
    
    with tab2:
        st.subheader("➕ Tambah Komoditas Baru")
        
        with st.form("add_commodity"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nama Komoditas *")
                category = st.selectbox("Kategori *", ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"])
            with col2:
                unit = st.selectbox("Unit", ["kg", "ikat", "butir", "ton"])
                price = st.number_input("Harga Referensi (Rp)", min_value=0)
            
            if st.form_submit_button("💾 Simpan", type="primary", use_container_width=True):
                if name:
                    new_id = get_next_id(st.session_state.commodities_db)
                    st.session_state.commodities_db.append({
                        'id': new_id,
                        'name': name,
                        'category': category,
                        'unit': unit,
                        'price': price,
                        'active': True
                    })
                    log_action('CREATE', 'commodities', new_id, f"Created {name}")
                    st.success(f"✅ Komoditas '{name}' berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Nama komoditas wajib diisi!")
    
    with tab3:
        st.subheader("📁 Import dari CSV")
        st.markdown("""
        **Format CSV:**
        ```
        name,category,unit,price
        Bayam Hijau,Sayuran,ikat,5000
        ```
        """)
        
        uploaded = st.file_uploader("Upload CSV", type=['csv'])
        if uploaded:
            df = pd.read_csv(uploaded)
            st.dataframe(df.head(10), use_container_width=True)
            
            if st.button("📤 Import", type="primary"):
                count = 0
                for _, row in df.iterrows():
                    new_id = get_next_id(st.session_state.commodities_db)
                    st.session_state.commodities_db.append({
                        'id': new_id,
                        'name': row.get('name', ''),
                        'category': row.get('category', 'Lainnya'),
                        'unit': row.get('unit', 'kg'),
                        'price': row.get('price', 0),
                        'active': True
                    })
                    count += 1
                log_action('BULK_IMPORT', 'commodities', None, f"Imported {count} items")
                st.success(f"✅ {count} komoditas berhasil diimport!")
                st.rerun()

# ========== MANUAL PRICES ==========
elif menu == "💰 Harga Manual":
    st.subheader("💰 Harga Manual")
    
    tab1, tab2 = st.tabs(["📋 Daftar", "➕ Tambah Harga"])
    
    with tab1:
        if st.session_state.manual_prices_db:
            df = pd.DataFrame(st.session_state.manual_prices_db)
            df['price'] = df['price'].apply(lambda x: f"Rp {x:,}")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada harga manual. Tambahkan di tab 'Tambah Harga'.")
    
    with tab2:
        st.subheader("➕ Tambah Harga Baru")
        
        commodity_options = {c['name']: c['id'] for c in st.session_state.commodities_db if c['active']}
        
        with st.form("add_price"):
            col1, col2 = st.columns(2)
            with col1:
                selected_commodity = st.selectbox("Komoditas", list(commodity_options.keys()) if commodity_options else ["Tidak ada"])
                price = st.number_input("Harga (Rp)", min_value=0)
                price_date = st.date_input("Tanggal", value=date.today())
            with col2:
                province = st.text_input("Provinsi", placeholder="Jawa Barat")
                city = st.text_input("Kota", placeholder="Bandung")
                price_type = st.selectbox("Tipe", ["retail", "wholesale", "farm_gate"])
            
            if st.form_submit_button("💾 Simpan", type="primary", use_container_width=True):
                if selected_commodity and price > 0:
                    new_id = get_next_id(st.session_state.manual_prices_db)
                    st.session_state.manual_prices_db.append({
                        'id': new_id,
                        'commodity': selected_commodity,
                        'price': price,
                        'date': price_date.isoformat(),
                        'province': province,
                        'city': city,
                        'type': price_type,
                        'reporter': user['username']
                    })
                    log_action('CREATE', 'manual_prices', new_id, f"Price for {selected_commodity}")
                    st.success("✅ Harga berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Pilih komoditas dan isi harga!")

# ========== AUDIT LOG ==========
elif menu == "📝 Audit Log":
    st.subheader("📝 Audit Log")
    
    if st.session_state.audit_log_db:
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            action_filter = st.selectbox("Filter Aksi", ["Semua", "CREATE", "UPDATE", "DELETE", "BULK_IMPORT"])
        with col2:
            table_filter = st.selectbox("Filter Tabel", ["Semua", "commodities", "manual_prices"])
        
        logs = st.session_state.audit_log_db[::-1]  # Reverse to show newest first
        
        if action_filter != "Semua":
            logs = [l for l in logs if l['action'] == action_filter]
        if table_filter != "Semua":
            logs = [l for l in logs if l['table'] == table_filter]
        
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Tidak ada log yang cocok dengan filter")
    else:
        st.info("Belum ada aktivitas tercatat")
