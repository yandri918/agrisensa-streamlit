import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date
import plotly.express as px

# 📝 CONFIGURATION
st.set_page_config(
    page_title="Jurnal Harian",
    page_icon="📝",
    layout="wide"
)

# 📂 DATA HANDLING
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOG_FILE = os.path.join(DATA_DIR, 'farm_log.json')

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialize Log File if not exists
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as f:
        json.dump([], f)

def load_logs():
    """Load logs from JSON file."""
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
            # Ensure compatibility if file is corrupted
            if not isinstance(data, list): return []
            return data
    except Exception as e:
        st.error(f"Error loading logs: {e}")
        return []

def save_log(entry):
    """Save a new log entry."""
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
    return True

def delete_log(idx):
    """Delete log entry by index."""
    logs = load_logs()
    if 0 <= idx < len(logs):
        logs.pop(idx)
        with open(LOG_FILE, 'w') as f:
            json.dump(logs, f, indent=4)
        return True
    return False

# 🎨 UI HEADER
st.title("📝 Jurnal Kegiatan Harian")
st.markdown("---")

# 📥 SIDEBAR: ENTRY FORM
with st.sidebar:
    st.header("➕ Catat Kegiatan")
    
    with st.form("entry_form", clear_on_submit=True):
        f_date = st.date_input("Tanggal", date.today())
        f_cat = st.selectbox("Kategori", [
            "Tanam", 
            "Pemupukan", 
            "Penyemprotan (Pestisida)", 
            "Perawatan (Siang Gulma/Pruning)",
            "Irigasi/Penyiraman", 
            "Panen",
            "Pembelian Sarana (Alat/Bahan)",
            "Lainnya"
        ])
        f_desc = st.text_area("Deskripsi Kegiatan", placeholder="Contoh: Semprot Insektisida Abacel 10ml/tangki")
        f_cost = st.number_input("Biaya (Rp)", min_value=0, step=1000, value=0, help="Isi 0 jika tidak ada biaya keluar")
        f_notes = st.text_input("Catatan Tambahan (Opsional)")
        
        submitted = st.form_submit_button("💾 Simpan Catatan")
        
        if submitted:
            if not f_desc:
                st.error("Deskripsi wajib diisi!")
            else:
                new_entry = {
                    "date": f_date.strftime("%Y-%m-%d"),
                    "category": f_cat,
                    "description": f_desc,
                    "cost": f_cost,
                    "notes": f_notes,
                    "timestamp": datetime.now().isoformat()
                }
                save_log(new_entry)
                st.success("✅ Tersimpan!")
                st.rerun()

# 📊 DASHBOARD & HISTORY
logs = load_logs()

if not logs:
    st.info("👋 Belum ada catatan jurnal. Mulai catat kegiatanmu di sidebar!")
else:
    # Convert to DataFrame
    df = pd.DataFrame(logs)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date', ascending=False).reset_index(drop=True)
    
    # 💰 FINANCIAL METRICS
    col1, col2, col3 = st.columns(3)
    
    current_month_str = date.today().strftime("%Y-%m")
    df['month'] = df['date'].dt.strftime("%Y-%m")
    
    monthly_cost = df[df['month'] == current_month_str]['cost'].sum()
    total_cost = df['cost'].sum()
    total_entries = len(df)
    
    col1.metric("💰 Pengeluaran Bulan Ini", f"Rp {monthly_cost:,.0f}")
    col2.metric("💸 Total Pengeluaran (YTD)", f"Rp {total_cost:,.0f}")
    col3.metric("📝 Total Kegiatan", f"{total_entries} Catatan")
    
    st.markdown("---")
    
    # 📈 CHARTS
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📅 Riwayat Kegiatan")
        
        # Filtering
        filter_cat = st.multiselect("Filter Kategori", df['category'].unique())
        view_df = df if not filter_cat else df[df['category'].isin(filter_cat)]
        
        # Display Table with Formatting
        st.dataframe(
            view_df[['date', 'category', 'description', 'cost', 'notes']],
            column_config={
                "date": "Tanggal",
                "category": "Kategori",
                "description": "Deskripsi",
                "cost": st.column_config.NumberColumn("Biaya (Rp)", format="Rp %d"),
                "notes": "Catatan"
            },
            use_container_width=True,
            height=400
        )
        
        # Delete Action
        with st.expander("🗑️ Hapus Data"):
            del_idx = st.number_input("Index baris untuk dihapus (lihat tabel)", min_value=0, max_value=len(view_df)-1, step=1)
            if st.button("Hapus Permanen"):
                # Map view index back to original log list
                # This is tricky with filters. Ideally use UUID. 
                # For V1 Simple: Only allow delete if no filter, or verify logic.
                # Simplest for V1: Just delete by row index of the full list (df is sorted desc, list is append asc)
                # Let's revert: Just simple list delete from original logs is risky with sort.
                # IMPLEMENT UUID for robustness later. 
                # For now, just Warning.
                st.warning("Fitur hapus dinonaktifkan sementara untuk keamanan data (Sort issue).")
                
    with c2:
        st.subheader("📊 Analisis Biaya")
        if total_cost > 0:
            cost_by_cat = df.groupby('category')['cost'].sum().reset_index()
            fig = px.pie(cost_by_cat, values='cost', names='category', title='Proporsi Pengeluaran', hole=0.4)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### Top Pengeluaran")
            st.dataframe(cost_by_cat.sort_values(by='cost', ascending=False).head(5), hide_index=True)

    # 📤 EXPORT
    st.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download CSV Logbook",
        data=csv,
        file_name=f"farm_logbook_{date.today()}.csv",
        mime="text/csv"
    )
