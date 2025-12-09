import streamlit as st
import pandas as pd
import json
import os
import uuid
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
    """Load logs from JSON file and ensure UUIDs exist."""
    try:
        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
            if not isinstance(data, list): return []
            
            # MIGRATION: Auto-assign UUID if missing
            updated = False
            for entry in data:
                if 'id' not in entry:
                    entry['id'] = str(uuid.uuid4())
                    updated = True
            
            if updated:
                with open(LOG_FILE, 'w') as fw:
                    json.dump(data, fw, indent=4)
            
            return data
    except Exception as e:
        st.error(f"Error loading logs: {e}")
        return []

def save_log(entry):
    """Save a new log entry."""
    logs = load_logs()
    # Ensure ID
    if 'id' not in entry:
        entry['id'] = str(uuid.uuid4())
        
    logs.append(entry)
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
    return True

def save_all_logs(logs):
    """Save all logs (bulk update)."""
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)

def delete_log_by_id(log_id):
    """Delete log entry by UUID."""
    logs = load_logs()
    original_len = len(logs)
    logs = [log for log in logs if log['id'] != log_id]
    
    if len(logs) < original_len:
        save_all_logs(logs)
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
                    "id": str(uuid.uuid4()),
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
    # Sort by date desc
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
        st.subheader("📅 Riwayat Kegiatan (Bisa Diedit)")
        st.caption("Klik dua kali pada sel tabel untuk mengedit data.")
        
        # Filtering
        filter_cat = st.multiselect("Filter Kategori", df['category'].unique())
        view_df = df if not filter_cat else df[df['category'].isin(filter_cat)]
        
        # 📝 DATA EDITOR (EDIT FEATURE)
        edited_df = st.data_editor(
            view_df,
            column_config={
                "id": None, # Hide ID
                "month": None, # Hide helper col
                "timestamp": None,
                "date": st.column_config.DateColumn("Tanggal", disabled=True), # Keep date readonly for simplicity in V1
                "category": st.column_config.SelectboxColumn("Kategori", options=[
                    "Tanam", "Pemupukan", "Penyemprotan (Pestisida)", 
                    "Perawatan (Siang Gulma/Pruning)", "Irigasi/Penyiraman", 
                    "Panen", "Pembelian Sarana (Alat/Bahan)", "Lainnya"
                ], required=True),
                "description": "Deskripsi",
                "cost": st.column_config.NumberColumn("Biaya (Rp)", format="Rp %d", min_value=0),
                "notes": "Catatan"
            },
            hide_index=True,
            use_container_width=True,
            num_rows="fixed", # Disable add/del rows via UI, use form/button
            key="journal_editor"
        )
        
        # SAVE LOGIC
        # Detect if edited_df is different from view_df (excluding index/order if needed, but here simple comparison)
        # However, data_editor returns a new object. 
        # Robust way: Check if any content changed.
        # But we need to update the ORIGINAL logs list (which might contain items NOT in view_df)
        
        if not view_df.drop(columns=['month'], errors='ignore').equals(edited_df.drop(columns=['month'], errors='ignore')):
            # Logic to update
            # 1. Convert edited_df back to dicts
            updated_records = edited_df.to_dict('records')
            
            # 2. Update main 'logs' list
            # Create a map of ID -> updated_record
            update_map = {rec['id']: rec for rec in updated_records}
            
            # 3. Apply updates to the master list
            new_master_logs = []
            for original_log in logs:
                uid = original_log.get('id')
                if uid in update_map:
                    # Merge updates (preserve timestamp or other hidden fields if needed)
                    # We just take the updated record content + original hidden fields if any lost?
                    # edited_df has id, date, cat, desc, cost, notes, timestamp (hidden but present in df)
                    # Ensure date format string for JSON
                    rec = update_map[uid]
                    if isinstance(rec['date'], (date, datetime)):
                        rec['date'] = rec['date'].strftime("%Y-%m-%d")
                    new_master_logs.append(rec)
                else:
                    new_master_logs.append(original_log)
            
            # 4. Save and Rerun
            save_all_logs(new_master_logs)
            st.toast("✅ Perubahan disimpan otomatis!", icon="💾")
            # We don't necessarily need to rerun immediately if st.data_editor maintains state, 
            # but syncing is safer.
            # st.rerun() # Optional: might verify later if needed.
        
        # Delete Action
        with st.expander("🗑️ Hapus Data"):
            st.markdown("Pilih ID kegiatan untuk dihapus (Fitur hapus permanen).")
            # Selectbox with description
            # Create label map
            
            delete_options = {row['id']: f"{row['date'].strftime('%d/%m')} - {row['description']} ({row['category']})" 
                              for index, row in view_df.iterrows()}
            
            selected_del_id = st.selectbox("Pilih Data", options=list(delete_options.keys()), 
                                         format_func=lambda x: delete_options[x])
            
            if st.button("Hapus Permanen", type="primary"):
                if delete_log_by_id(selected_del_id):
                    st.success("Data berhasil dihapus!")
                    st.rerun()
                else:
                    st.error("Gagal menghapus data.")

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
