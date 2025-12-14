import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Page Config
st.set_page_config(
    page_title="Jurnal Harian Pertanian - AgriSensa",
    page_icon="📓",
    layout="wide"
)

# Constants
JOURNAL_FILE = "data/activity_journal.csv"
GROWTH_FILE = "data/growth_journal.csv"

# Ensure Data Utils
def init_journal():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(JOURNAL_FILE):
        df = pd.DataFrame(columns=['tanggal', 'kategori', 'judul', 'catatan', 'biaya', 'foto_path'])
        df.to_csv(JOURNAL_FILE, index=False)

def load_journal():
    init_journal()
    try:
        return pd.read_csv(JOURNAL_FILE)
    except:
        return pd.DataFrame(columns=['tanggal', 'kategori', 'judul', 'catatan', 'biaya', 'foto_path'])

def save_entry(tgl, kategori, judul, catatan, biaya):
    df = load_journal()
    new_data = pd.DataFrame({
        'tanggal': [tgl],
        'kategori': [kategori],
        'judul': [judul],
        'catatan': [catatan],
        'biaya': [biaya],
        'foto_path': [""] # Future proofing
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(JOURNAL_FILE, index=False)

def load_growth_data():
    if os.path.exists(GROWTH_FILE):
        try:
            return pd.read_csv(GROWTH_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# UI STYLING
st.markdown("""
<style>
    .journal-card {
        background-color: #f8f9fa;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .journal-card.expense {
        border-left-color: #f44336;
    }
    .journal-card.harvest {
        border-left-color: #ff9800;
    }
    .journal-card.growth {
        border-left-color: #2196F3;
    }
    .card-date {
        font-size: 0.85em;
        color: #666;
        margin-bottom: 5px;
    }
    .card-title {
        font-weight: bold;
        font-size: 1.1em;
        color: #333;
    }
    .card-cost {
        float: right;
        font-weight: bold;
        color: #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("📓 Jurnal Harian Modern")
st.markdown("Catat aktivitas, pantau biaya, dan kumpulkan memori pertanian Anda dalam satu linimasa terpadu.")

# LAYOUT
col_input, col_feed = st.columns([1, 2])

with col_input:
    st.container(border=True)
    st.subheader("✍️ Tulis Jurnal Baru")
    
    with st.form("journal_form"):
        tgl = st.date_input("Tanggal", datetime.now())
        kategori = st.selectbox("Kategori", ["✅ Umum", "💧 Penyiraman", "💊 Pemupukan", "🛡️ Pengendalian Hama", "🛠️ Perawatan Infrastruktur", "🚜 Panen", "💰 Pembelian/Pengeluaran"])
        judul = st.text_input("Judul Singkat", placeholder="Contoh: Beli Pupuk NPK")
        catatan = st.text_area("Catatan Detail", placeholder="Dosis, cuaca, kendala...", height=100)
        biaya = st.number_input("Biaya (Rp) - Opsional", min_value=0, step=1000)
        
        submit = st.form_submit_button("Simpan Aktivitas", use_container_width=True)
        
        if submit:
            if judul:
                save_entry(tgl, kategori, judul, catatan, biaya)
                st.success("Tersimpan!")
                st.rerun()
            else:
                st.error("Judul wajib diisi.")

    # Financial Summary
    st.divider()
    st.subheader("💰 Ringkasan Biaya")
    df_j = load_journal()
    if not df_j.empty:
        total_expense = df_j['biaya'].sum()
        this_month_expense = df_j[pd.to_datetime(df_j['tanggal']).dt.month == datetime.now().month]['biaya'].sum()
        
        st.metric("Total Pengeluaran (Semua)", f"Rp {total_expense:,.0f}")
        st.metric("Pengeluaran Bulan Ini", f"Rp {this_month_expense:,.0f}")
        
        # Expense by Category Pie
        if total_expense > 0:
            exp_by_cat = df_j.groupby('kategori')['biaya'].sum().reset_index()
            fig_pie = px.pie(exp_by_cat, values='biaya', names='kategori', title='Komposisi Biaya', hole=0.4)
            fig_pie.update_layout(showlegend=False, margin=dict(t=30, b=0, l=0, r=0), height=200)
            st.plotly_chart(fig_pie, use_container_width=True)

with col_feed:
    st.subheader("📅 Linimasa Aktivitas (Timeline)")
    
    # MERGE DATA SOURCES
    # 1. Activity Data
    df_act = load_journal()
    df_act['source'] = 'activity'
    
    # 2. Growth Data (from Modul 39)
    df_grow = load_growth_data()
    timeline_items = []
    
    # Convert Activity DF to List
    if not df_act.empty:
        for _, row in df_act.iterrows():
            style_class = "expense" if row['biaya'] > 0 else "journal-card"
            if "Panen" in row['kategori']: style_class = "harvest"
            
            timeline_items.append({
                'date': pd.to_datetime(row['tanggal']),
                'title': row['judul'],
                'desc': row['catatan'],
                'meta': f"{row['kategori']}",
                'cost': row['biaya'],
                'type': 'activity',
                'style': style_class,
                'raw_date': row['tanggal']
            })
            
    # Convert Growth DF to List
    if not df_grow.empty:
        for _, row in df_grow.iterrows():
            timeline_items.append({
                'date': pd.to_datetime(row['tanggal']),
                'title': f"Monitoring: {row['komoditas']}",
                'desc': f"Tinggi: {row['tinggi_cm']} cm | Daun: {row['jumlah_daun']} helai | HST: {row['usia_hst']}",
                'meta': "📏 Data Pertumbuhan",
                'cost': 0,
                'type': 'growth',
                'style': "growth",
                'raw_date': row['tanggal']
            })
            
    # Sort by Date Descending
    timeline_items.sort(key=lambda x: x['date'], reverse=True)
    
    # RENDER FEED
    # Filter Controls
    f_col1, f_col2 = st.columns(2)
    filter_type = f_col1.multiselect("Filter Tipe", ["activity", "growth"], default=["activity", "growth"])
    
    cnt = 0
    for item in timeline_items:
        if item['type'] in filter_type:
            cnt += 1
            
            cost_html = f'<span class="card-cost">- Rp {item["cost"]:,.0f}</span>' if item['cost'] > 0 else ""
            icon = "📝"
            if item['style'] == 'growth': icon = "📏"
            elif item['style'] == 'harvest': icon = "🌾"
            elif item['style'] == 'expense': icon = "💸"
            
            st.markdown(f"""
            <div class="journal-card {item['style']}">
                <div class="card-date">{item['raw_date']} • {item['meta']}</div>
                <div class="card-title">{icon} {item['title']} {cost_html}</div>
                <div style="margin-top: 5px; color: #555;">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    if cnt == 0:
        st.info("Belum ada catatan aktivitas. Mulailah mencatat di panel sebelah kiri!")

# Analytics Logic? Maybe next time.
