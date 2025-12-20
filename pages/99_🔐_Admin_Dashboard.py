# AgriSensa Admin Dashboard
# Enterprise-grade admin panel with JWT authentication and full CRUD capabilities

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import json

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Admin Dashboard - AgriSensa",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== STYLING ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Admin Header */
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
    
    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .stat-label {
        opacity: 0.9;
        font-size: 0.9rem;
    }
    
    /* Table Styling */
    .dataframe {
        font-size: 0.85rem;
    }
    
    /* Login Form */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ========== CONFIG ==========
API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:5000")
ADMIN_API_URL = f"{API_BASE_URL}/api/admin"

# ========== SESSION STATE ==========
if 'admin_token' not in st.session_state:
    st.session_state.admin_token = None
if 'admin_user' not in st.session_state:
    st.session_state.admin_user = None

# ========== API HELPERS ==========
def api_request(method, endpoint, data=None, params=None):
    """Make authenticated API request."""
    headers = {
        'Content-Type': 'application/json'
    }
    if st.session_state.admin_token:
        headers['Authorization'] = f"Bearer {st.session_state.admin_token}"
    
    url = f"{ADMIN_API_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=30)
        
        return response.json()
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Cannot connect to API server. Make sure Flask is running.'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def login(username, password):
    """Login to admin API."""
    result = api_request('POST', '/login', {'username': username, 'password': password})
    if result.get('success'):
        st.session_state.admin_token = result['access_token']
        st.session_state.admin_user = result['user']
        return True, None
    return False, result.get('error', 'Login failed')


def logout():
    """Logout from admin."""
    st.session_state.admin_token = None
    st.session_state.admin_user = None


# ========== LOGIN PAGE ==========
def show_login_page():
    """Display login form."""
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <h1>🔐 AgriSensa Admin</h1>
        <p style="color: #6b7280;">Enterprise Management Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### Login")
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
            
            if submitted:
                if username and password:
                    success, error = login(username, password)
                    if success:
                        st.success("Login berhasil!")
                        st.rerun()
                    else:
                        st.error(f"Login gagal: {error}")
                else:
                    st.warning("Masukkan username dan password")
        
        st.markdown("---")
        st.caption("Default: admin / admin123")
        st.caption("⚠️ Pastikan Flask API running di localhost:5000")


# ========== DASHBOARD PAGE ==========
def show_dashboard():
    """Display main dashboard with stats."""
    st.markdown("""
    <div class="admin-header">
        <h1 class="admin-title">🛡️ Admin Dashboard</h1>
        <p class="admin-subtitle">Enterprise Management Console</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch stats
    result = api_request('GET', '/stats')
    
    if result.get('success'):
        stats = result['stats']
        
        # Stats Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Total Komoditas", stats.get('total_commodities', 0))
        with col2:
            st.metric("✅ Komoditas Aktif", stats.get('active_commodities', 0))
        with col3:
            st.metric("💰 Harga Manual", stats.get('total_manual_prices', 0))
        with col4:
            st.metric("👥 Total Users", stats.get('total_users', 0))
        
        # Activity Summary
        st.markdown("---")
        st.subheader("📊 Aktivitas 7 Hari Terakhir")
        
        activity = stats.get('recent_activity', {})
        if activity:
            df_activity = pd.DataFrame([
                {'Aksi': k, 'Jumlah': v} for k, v in activity.items()
            ])
            st.bar_chart(df_activity.set_index('Aksi'))
        else:
            st.info("Belum ada aktivitas tercatat")
    else:
        st.error(f"Gagal memuat statistik: {result.get('error')}")


# ========== COMMODITIES PAGE ==========
def show_commodities():
    """Manage commodities."""
    st.header("🌾 Manajemen Komoditas")
    
    tab1, tab2, tab3 = st.tabs(["📋 Daftar", "➕ Tambah Baru", "📁 Import CSV"])
    
    with tab1:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("🔍 Cari", placeholder="Nama komoditas...")
        with col2:
            category = st.selectbox("Kategori", ["Semua", "Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan"])
        with col3:
            active_only = st.checkbox("Aktif saja", value=True)
        
        # Fetch commodities
        params = {
            'per_page': 50,
            'active_only': str(active_only).lower()
        }
        if search:
            params['search'] = search
        if category != "Semua":
            params['category'] = category
        
        result = api_request('GET', '/commodities', params=params)
        
        if result.get('success'):
            commodities = result['commodities']
            if commodities:
                # Convert to DataFrame
                df = pd.DataFrame(commodities)
                
                # Select columns to display
                display_cols = ['id', 'name', 'category', 'unit', 'price_reference', 'is_active']
                df_display = df[display_cols].copy()
                df_display['is_active'] = df_display['is_active'].apply(lambda x: '✅' if x else '❌')
                df_display.columns = ['ID', 'Nama', 'Kategori', 'Unit', 'Harga Ref', 'Aktif']
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                # Edit/Delete Section
                st.markdown("---")
                st.subheader("✏️ Edit Komoditas")
                
                commodity_options = {c['name']: c['id'] for c in commodities}
                selected_name = st.selectbox("Pilih komoditas", list(commodity_options.keys()))
                
                if selected_name:
                    selected_id = commodity_options[selected_name]
                    selected = next(c for c in commodities if c['id'] == selected_id)
                    
                    with st.form("edit_commodity"):
                        col1, col2 = st.columns(2)
                        with col1:
                            new_name = st.text_input("Nama", value=selected['name'])
                            new_category = st.selectbox("Kategori", 
                                ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan", "Lainnya"],
                                index=["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan", "Lainnya"].index(selected.get('category', 'Lainnya')) if selected.get('category') in ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan", "Lainnya"] else 5
                            )
                            new_unit = st.text_input("Unit", value=selected.get('unit', 'kg'))
                        with col2:
                            new_price = st.number_input("Harga Referensi", value=float(selected.get('price_reference') or 0))
                            new_active = st.checkbox("Aktif", value=selected.get('is_active', True))
                        
                        new_description = st.text_area("Deskripsi", value=selected.get('description', '') or '')
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.form_submit_button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                                update_data = {
                                    'name': new_name,
                                    'category': new_category,
                                    'unit': new_unit,
                                    'price_reference': new_price,
                                    'is_active': new_active,
                                    'description': new_description
                                }
                                result = api_request('PUT', f'/commodities/{selected_id}', update_data)
                                if result.get('success'):
                                    st.success("Komoditas berhasil diupdate!")
                                    st.rerun()
                                else:
                                    st.error(f"Gagal update: {result.get('error')}")
                        
                        with col_btn2:
                            if st.form_submit_button("🗑️ Hapus (Nonaktifkan)", use_container_width=True):
                                result = api_request('DELETE', f'/commodities/{selected_id}')
                                if result.get('success'):
                                    st.success("Komoditas berhasil dinonaktifkan!")
                                    st.rerun()
                                else:
                                    st.error(f"Gagal hapus: {result.get('error')}")
            else:
                st.info("Belum ada komoditas. Tambah baru di tab 'Tambah Baru'.")
        else:
            st.error(f"Gagal memuat data: {result.get('error')}")
    
    with tab2:
        st.subheader("➕ Tambah Komoditas Baru")
        
        with st.form("add_commodity"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nama Komoditas *", placeholder="contoh: Bayam Hijau")
                name_local = st.text_input("Nama Lokal", placeholder="contoh: Bayem")
                category = st.selectbox("Kategori *", ["Sayuran", "Buah", "Pangan", "Rempah", "Perkebunan", "Lainnya"])
                unit = st.selectbox("Satuan", ["kg", "ikat", "butir", "buah", "ton"])
            
            with col2:
                price_reference = st.number_input("Harga Referensi (Rp)", min_value=0)
                water_need = st.selectbox("Kebutuhan Air", ["rendah", "sedang", "tinggi"])
                days_min = st.number_input("Hari Panen (Min)", min_value=0, value=30)
                days_max = st.number_input("Hari Panen (Max)", min_value=0, value=60)
            
            description = st.text_area("Deskripsi", placeholder="Deskripsi singkat komoditas...")
            cultivation_guide = st.text_area("Panduan Budidaya", placeholder="Panduan menanam...")
            
            if st.form_submit_button("💾 Simpan Komoditas", type="primary", use_container_width=True):
                if name and category:
                    data = {
                        'name': name,
                        'name_local': name_local,
                        'category': category,
                        'unit': unit,
                        'price_reference': price_reference,
                        'water_need': water_need,
                        'days_to_harvest_min': days_min,
                        'days_to_harvest_max': days_max,
                        'description': description,
                        'cultivation_guide': cultivation_guide,
                        'price_source': 'manual'
                    }
                    result = api_request('POST', '/commodities', data)
                    if result.get('success'):
                        st.success(f"Komoditas '{name}' berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error(f"Gagal: {result.get('error')}")
                else:
                    st.warning("Nama dan Kategori wajib diisi!")
    
    with tab3:
        st.subheader("📁 Import dari CSV")
        
        st.markdown("""
        **Format CSV yang diharapkan:**
        ```
        name,category,unit,price_reference
        Bayam Hijau,Sayuran,ikat,5000
        Cabai Rawit,Sayuran,kg,80000
        ```
        """)
        
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df.head(10), use_container_width=True)
                
                if st.button("📤 Import Data", type="primary"):
                    # Convert to list of dicts
                    data = df.to_dict('records')
                    result = api_request('POST', '/commodities/bulk', data)
                    if result.get('success'):
                        res = result['result']
                        st.success(f"Import selesai! Created: {res['created']}, Updated: {res['updated']}")
                        if res['errors']:
                            st.warning(f"Errors: {res['errors']}")
                    else:
                        st.error(f"Gagal import: {result.get('error')}")
            except Exception as e:
                st.error(f"Error membaca CSV: {e}")


# ========== MANUAL PRICES PAGE ==========
def show_manual_prices():
    """Manage manual prices."""
    st.header("💰 Harga Manual")
    
    tab1, tab2 = st.tabs(["📋 Daftar Harga", "➕ Tambah Harga"])
    
    with tab1:
        result = api_request('GET', '/prices', params={'per_page': 100})
        
        if result.get('success'):
            prices = result['prices']
            if prices:
                df = pd.DataFrame(prices)
                df['price'] = df['price'].apply(lambda x: f"Rp {x:,.0f}" if x else "-")
                df_display = df[['id', 'commodity_name', 'price', 'unit', 'price_date', 'source', 'is_verified']]
                df_display['is_verified'] = df_display['is_verified'].apply(lambda x: '✅' if x else '⏳')
                df_display.columns = ['ID', 'Komoditas', 'Harga', 'Unit', 'Tanggal', 'Sumber', 'Verified']
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.info("Belum ada data harga manual.")
        else:
            st.error(f"Gagal memuat: {result.get('error')}")
    
    with tab2:
        st.subheader("➕ Tambah Harga Baru")
        
        # Fetch commodities for dropdown
        comm_result = api_request('GET', '/commodities', params={'per_page': 200})
        
        if comm_result.get('success'):
            commodities = comm_result['commodities']
            commodity_options = {c['name']: c['id'] for c in commodities}
            
            with st.form("add_price"):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_commodity = st.selectbox("Komoditas *", list(commodity_options.keys()) if commodity_options else ["No commodities"])
                    price = st.number_input("Harga (Rp) *", min_value=0)
                    price_date = st.date_input("Tanggal", value=date.today())
                
                with col2:
                    province_name = st.text_input("Provinsi", placeholder="contoh: Jawa Barat")
                    city_name = st.text_input("Kota/Kabupaten", placeholder="contoh: Bandung")
                    price_type = st.selectbox("Tipe Harga", ["retail", "wholesale", "farm_gate"])
                
                notes = st.text_area("Catatan", placeholder="Informasi tambahan...")
                
                if st.form_submit_button("💾 Simpan Harga", type="primary", use_container_width=True):
                    if selected_commodity and price > 0:
                        data = {
                            'commodity_id': commodity_options[selected_commodity],
                            'price': price,
                            'price_date': price_date.isoformat(),
                            'province_name': province_name,
                            'city_name': city_name,
                            'price_type': price_type,
                            'notes': notes,
                            'source': 'admin_input'
                        }
                        result = api_request('POST', '/prices', data)
                        if result.get('success'):
                            st.success("Harga berhasil ditambahkan!")
                            st.rerun()
                        else:
                            st.error(f"Gagal: {result.get('error')}")
                    else:
                        st.warning("Komoditas dan Harga wajib diisi!")
        else:
            st.error("Gagal memuat daftar komoditas")


# ========== AUDIT LOG PAGE ==========
def show_audit_log():
    """Display audit log."""
    st.header("📝 Audit Log")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        action_filter = st.selectbox("Aksi", ["Semua", "CREATE", "UPDATE", "DELETE", "LOGIN", "BULK_IMPORT"])
    with col2:
        table_filter = st.selectbox("Tabel", ["Semua", "commodities", "manual_prices", "users"])
    
    params = {'per_page': 100}
    if action_filter != "Semua":
        params['action'] = action_filter
    if table_filter != "Semua":
        params['table'] = table_filter
    
    result = api_request('GET', '/audit-log', params=params)
    
    if result.get('success'):
        logs = result['logs']
        if logs:
            df = pd.DataFrame(logs)
            df_display = df[['created_at', 'username', 'action', 'table_name', 'record_id', 'status']]
            df_display.columns = ['Waktu', 'User', 'Aksi', 'Tabel', 'Record ID', 'Status']
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada log aktivitas.")
    else:
        st.error(f"Gagal memuat: {result.get('error')}")


# ========== MAIN APP ==========
def main():
    # Check if logged in
    if not st.session_state.admin_token:
        show_login_page()
        return
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 1rem; background: #f0fdf4; border-radius: 12px; margin-bottom: 1rem;">
            <strong>👤 {st.session_state.admin_user.get('username', 'Admin')}</strong><br>
            <small style="color: #6b7280;">{st.session_state.admin_user.get('role', 'admin')}</small>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio(
            "📱 Menu",
            ["📊 Dashboard", "🌾 Komoditas", "💰 Harga Manual", "📝 Audit Log"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
    
    # Main Content
    if menu == "📊 Dashboard":
        show_dashboard()
    elif menu == "🌾 Komoditas":
        show_commodities()
    elif menu == "💰 Harga Manual":
        show_manual_prices()
    elif menu == "📝 Audit Log":
        show_audit_log()


if __name__ == "__main__":
    main()
