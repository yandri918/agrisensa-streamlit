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

# --- DATA UTILS ---
def init_data():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(JOURNAL_FILE):
        df = pd.DataFrame(columns=['tanggal', 'kategori', 'judul', 'catatan', 'biaya', 'foto_path'])
        df.to_csv(JOURNAL_FILE, index=False)
    if not os.path.exists(GROWTH_FILE):
        df = pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun'])
        df.to_csv(GROWTH_FILE, index=False)

def load_journal():
    try:
        if os.path.exists(JOURNAL_FILE):
            return pd.read_csv(JOURNAL_FILE)
    except:
        pass
    return pd.DataFrame(columns=['tanggal', 'kategori', 'judul', 'catatan', 'biaya', 'foto_path'])

def load_growth():
    try:
        if os.path.exists(GROWTH_FILE):
            return pd.read_csv(GROWTH_FILE)
    except:
        pass
    return pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun'])

def save_activity(tgl, kategori, judul, catatan, biaya):
    df = load_journal()
    new_data = pd.DataFrame({
        'tanggal': [tgl],
        'kategori': [kategori],
        'judul': [judul],
        'catatan': [catatan],
        'biaya': [biaya],
        'foto_path': [""]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(JOURNAL_FILE, index=False)

def save_growth(tgl, komoditas, hst, tinggi, daun):
    df = load_growth()
    new_data = pd.DataFrame({
        'tanggal': [tgl],
        'komoditas': [komoditas],
        'usia_hst': [hst],
        'tinggi_cm': [tinggi],
        'jumlah_daun': [daun]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(GROWTH_FILE, index=False)

init_data()

# UI STYLING
st.markdown("""
<style>
    .journal-card {
        background-color: #ffffff;
        border-left: 5px solid #4CAF50;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: transform 0.1s;
    }
    .journal-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .journal-card.expense { border-left-color: #f44336; }
    .journal-card.harvest { border-left-color: #ff9800; }
    .journal-card.growth { border-left-color: #2196F3; }
    
    .card-date { font-size: 0.8em; color: #888; margin-bottom: 4px; }
    .card-title { font-weight: 700; font-size: 1.05em; color: #333; }
    .card-cost { float: right; font-weight: bold; color: #d32f2f; font-size: 0.9em;}
    .card-metric { 
        display: inline-block; 
        background: #e3f2fd; 
        color: #1565c0; 
        padding: 2px 8px; 
        border-radius: 12px; 
        font-size: 0.8em; 
        font-weight: 500;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.title("📓 Jurnal Harian Modern")
st.caption("Central Control Room: Catat aktivitas & pertumbuhan, pantau biaya, dan review timeline.")

# LAYOUT
col_input, col_feed = st.columns([1.2, 2])

with col_input:
    st.container(border=True)
    
    # TABS INPUT
    tab_act, tab_growth = st.tabs(["📝 Catat Aktivitas", "📏 Catat Pertumbuhan"])
    
    with tab_act:
        with st.form("journal_form"):
            st.subheader("Aktivitas Kebun")
            tgl = st.date_input("Tanggal", datetime.now(), key="tgl_act")
            kategori = st.selectbox("Kategori", ["✅ Umum", "💧 Penyiraman", "💊 Pemupukan", "🛡️ Pengendalian Hama", "🛠️ Perawatan Infrastruktur", "🚜 Panen", "💰 Pembelian/Pengeluaran"])
            judul = st.text_input("Judul Singkat", placeholder="Contoh: Beli Pupuk NPK")
            catatan = st.text_area("Catatan Detail", placeholder="Dosis, cuaca, kendala...", height=80)
            biaya = st.number_input("Biaya (Rp) - Opsional", min_value=0, step=1000)
            
            submit_act = st.form_submit_button("Simpan Aktivitas", use_container_width=True)
            
            if submit_act:
                if judul:
                    save_activity(tgl, kategori, judul, catatan, biaya)
                    st.success("Tersimpan!")
                    st.rerun()
                else:
                    st.error("Judul wajib diisi.")
    
    with tab_growth:
        st.info("Input data ini akan otomatis masuk ke grafik Modul 39.")
        with st.form("growth_form"):
            st.subheader("Data Pertumbuhan")
            tgl_g = st.date_input("Tanggal Ukur", datetime.now(), key="tgl_grow")
            komoditas = st.selectbox("Komoditas", ["Jagung Hibrida", "Padi Inpari", "Cabai Rawit", "Melon"])
            usia_hst = st.number_input("Usia (HST)", min_value=1, value=1)
            tinggi = st.number_input("Tinggi (cm)", min_value=0.0)
            daun = st.number_input("Jumlah Daun", min_value=0)
            
            submit_grow = st.form_submit_button("Simpan Data Pertumbuhan", use_container_width=True)
            
            if submit_grow:
                save_growth(tgl_g, komoditas, usia_hst, tinggi, daun)
                st.success(f"Data {komoditas} tersimpan!")
                st.rerun()

    # Financial Summary Small Widget
    st.divider()
    df_j = load_journal()
    total_expense = df_j['biaya'].sum() if not df_j.empty else 0
    st.metric("Total Pengeluaran", f"Rp {total_expense:,.0f}")

with col_feed:
    st.subheader("📅 Linimasa (Feed)")
    
    # Load & Merge
    df_act = load_journal()
    df_act['type'] = 'activity'
    
    df_grow = load_growth()
    df_grow['type'] = 'growth'
    
    timeline = []
    
    if not df_act.empty:
        for _, r in df_act.iterrows():
            style = "journal-card"
            if r['biaya'] > 0: style = "expense"
            if "Panen" in str(r['kategori']): style = "harvest"
            
            timeline.append({
                'date': pd.to_datetime(r['tanggal']),
                'raw_date': r['tanggal'],
                'title': r['judul'],
                'desc': r['catatan'],
                'meta': r['kategori'],
                'cost': r['biaya'],
                'style': style,
                'type': 'activity'
            })
            
    if not df_grow.empty:
        for _, r in df_grow.iterrows():
            timeline.append({
                'date': pd.to_datetime(r['tanggal']),
                'raw_date': r['tanggal'],
                'title': f"Monitoring {r['komoditas']}",
                'desc': f"<span class='card-metric'>📏 {r['tinggi_cm']} cm</span> <span class='card-metric'>🍃 {r['jumlah_daun']} daun</span>",
                'meta': f"HST {r['usia_hst']}",
                'cost': 0,
                'style': 'growth',
                'type': 'growth'
            })
            
    timeline.sort(key=lambda x: x['date'], reverse=True)
    
    # Filter
    f_mode = st.radio("Tampilkan:", ["Semua", "Hanya Aktivitas", "Hanya Pertumbuhan"], horizontal=True, label_visibility="collapsed")
    
    for item in timeline:
        show = True
        if f_mode == "Hanya Aktivitas" and item['type'] != 'activity': show = False
        if f_mode == "Hanya Pertumbuhan" and item['type'] != 'growth': show = False
        
        if show:
            icon = "📝"
            if item['style'] == 'growth': icon = "📈"
            elif item['style'] == 'harvest': icon = "🌾"
            elif item['style'] == 'expense': icon = "💸"
            
            cost_html = f'<div class="card-cost">- Rp {item["cost"]:,.0f}</div>' if item['cost'] > 0 else ""
            
            st.markdown(f"""
            <div class="{item['style']}">
                <div class="card-date">{item['raw_date']} • {item['meta']}</div>
                {cost_html}
                <div class="card-title">{icon} {item['title']}</div>
                <div style="margin-top: 5px; color: #444;">{item['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    if not timeline:
        st.info("Belum ada data. Mulai mencatat di panel kiri!")
