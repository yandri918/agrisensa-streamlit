import streamlit as st
import datetime
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="AgriSensa Strategic Dossier",
    page_icon="📄",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
if 'swot_data' not in st.session_state:
    st.session_state['swot_data'] = {
        "Strengths": "Teknologi presisi, Akses pasar modern, Traceability Blockchain.",
        "Weaknesses": "Ketergantungan cuaca ekstrim, Biaya awal infrastruktur.",
        "Opportunities": "Pasar ekspor sayuran premium, Pola makan sehat konsumen.",
        "Threats": "Fluktuasi harga pupuk global, Serangan hama bermutasi."
    }

if 'timeline_data' not in st.session_state:
    st.session_state['timeline_data'] = [
        {"Fase": "Persiapan Lahan & Konstruksi", "Durasi": "Bulan 1-2"},
        {"Fase": "Instalasi IoT & Smart Irrigation", "Durasi": "Bulan 3"},
        {"Fase": "Trial Tanam & QC Setup", "Durasi": "Bulan 4"},
        {"Fase": "Operasional Penuh & Harvest", "Durasi": "Bulan 5+"}
    ]

# --- SIDEBAR: GLOBAL CONFIG ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Proyek")
    proj_name = st.text_input("Nama Proyek", "Pusat Agribisnis Melon Premium 3K")
    company_name = st.text_input("Instansi / Perusahaan", "PT. AgriSensa Solusi Madani")
    owner_name = st.text_input("Penanggung Jawab / CEO", "Bpk. Yandri")
    report_date = st.date_input("Tanggal Terbit", datetime.date.today())
    
    st.divider()
    st.subheader("🔌 Sumber Data")
    source_rab = st.radio("Sektor Finansial (RAB)", ["Template Standar", "Sinkron Modul 28"], index=0, help="Pilih sumber data untuk biaya dan ROI.")
    source_3k = st.radio("Sektor Operasional (3K)", ["Template Standar", "Sinkron Modul 33"], index=0, help="Pilih sumber data untuk kapasitas dan model bisnis.")
    source_trace = st.radio("Sektor Keamanan", ["Template Standar", "Sinkron Modul 48"], index=0, help="Pilih sumber data untuk riwayat blockchain.")

    st.divider()
    if st.button("🖨️ Generate & Print (Buku Putih)", type="primary", use_container_width=True):
        st.info("📌 **Cara Mencetak:**\n\n1. Pastikan Anda sudah di Tab 3 (Cetak Buku Putih)\n2. Tekan **Ctrl+P** (Windows) atau **Cmd+P** (Mac)\n3. Pilih 'Save as PDF' atau printer Anda\n4. Klik Print/Save")
        st.components.v1.html("<script>window.print();</script>", height=0)

# --- HEADER NATIVE ---
st.title("📄 Strategic Project Dossier V2")
st.markdown("Sistem Manajemen Laporan Strategis Terpadu — *AgriSensa Intelligence*")

# --- PROCESS GUIDE BANNER ---
st.info("""
**Alur Kerja Strategis:**
1. **Penyusunan Konten** (Isi SWOT & Timeline) ➔ 2. **Analisa Terintegrasi** (Monitor Dashboard) ➔ 3. **Cetak Buku Putih** (Dokumen Final)
""")

# --- NATIVE TABS ---
tab_editor, tab_dashboard, tab_preview = st.tabs([
    "Step 1: Penyusunan Konten",
    "Step 2: Analisa Terintegrasi", 
    "Step 3: Cetak Buku Putih"
])

# --- HELPER FUNCTIONS ---
def get_timeline_dates(d_str):
    try:
        # Simple parser for "Bulan 1-2" or "Bulan 5+"
        # Returns (start_date, end_date) as strings
        base_date = datetime.date(2025, 1, 1)
        d_str = d_str.replace("Bulan ", "").strip()
        
        if "+" in d_str:
            s_val = int(d_str.replace("+", ""))
            start = base_date + datetime.timedelta(days=s_val * 30)
            end = start + datetime.timedelta(days=30)
        elif "-" in d_str:
            parts = d_str.split("-")
            s_val = int(parts[0])
            e_val = int(parts[1])
            start = base_date + datetime.timedelta(days=s_val * 30)
            end = base_date + datetime.timedelta(days=e_val * 30)
        else:
            val = int(d_str)
            start = base_date + datetime.timedelta(days=val * 30)
            end = start + datetime.timedelta(days=30)
            
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    except:
        return "2025-01-01", "2025-02-01"

# --- FETCH DATA (Before Tabs) ---
rab_raw = st.session_state.get('global_rab_summary', {}) if source_rab == "Sinkron Modul 28" else {}
sim_raw = st.session_state.get('global_3k_sim', {}) if source_3k == "Sinkron Modul 33" else {}
ledger_raw = st.session_state.get('ledger_db', []) if source_trace == "Sinkron Modul 48" else []

# --- TAB 2 (Langkah 2): DASHBOARD ---
with tab_dashboard:
    st.markdown("### 📊 Langkah 2: Monitoring & Analisa Terintegrasi")
    st.caption("Lihat visualisasi data strategi Anda yang digabungkan dengan data operasional real-time.")
    
    # Row 1: Key Metrics
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Total Investment", f"Rp {rab_raw['total_biaya']:,.0f}" if rab_raw else "Rp 850M", "RAB Live" if rab_raw else "Template")
    with m_col2:
        st.metric("Efficiency ROI", f"{rab_raw['roi_percent']:.1f}%" if rab_raw else "Market Avg", "RAB Live" if rab_raw else "Standard")
    with m_col3:
        st.metric("Verified Blocks", f"{len(ledger_raw)} Blocks", "Chain Live" if source_trace == "Sinkron Modul 48" else "Template")
    with m_col4:
        st.metric("Supply Readiness", f"{sim_raw['kapasitas_mingguan']} kg/wk" if sim_raw else "200 kg/wk", "3K Live" if sim_raw else "Template")

    st.divider()

    # Row 2: Visualizations
    v_col1, v_col2 = st.columns([3, 2])
    
    with v_col1:
        st.subheader("📅 Project Implementation Roadmap")
        # Prepare Gantt Data
        gantt_list = []
        for stage in st.session_state['timeline_data']:
            start, end = get_timeline_dates(stage['Durasi'])
            gantt_list.append(dict(Task=stage['Fase'], Start=start, Finish=end, Resource='Planning'))
        
        df_gantt = pd.DataFrame(gantt_list)
        if not df_gantt.empty:
            fig_timeline = px.timeline(df_gantt, x_start="Start", x_end="Finish", y="Task", color="Task", 
                                       title="Visual Project Schedule", template="plotly_white")
            fig_timeline.update_yaxes(autorange="reversed")
            fig_timeline.update_layout(showlegend=False, height=300, margin=dict(l=0, r=0, t=30, b=0))
            st.plotly_chart(fig_timeline, use_container_width=True)

    with v_col2:
        st.subheader("🎯 Strategic Balance (SWOT)")
        swot_scores = {
            "Strengths": 90,
            "Opportunities": 85,
            "Weaknesses": 30,
            "Threats": 40
        }
        fig_swot = go.Figure(data=go.Scatterpolar(
            r=[swot_scores[k] for k in swot_scores.keys()] + [swot_scores["Strengths"]],
            theta=list(swot_scores.keys()) + ["Strengths"],
            fill='toself',
            marker=dict(color='#059669')
        ))
        fig_swot.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), 
                               showlegend=False, height=300, margin=dict(l=40, r=40, t=30, b=30))
        st.plotly_chart(fig_swot, use_container_width=True)

    st.divider()
    
    # Row 3: Summaries
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        st.info(f"**Visi Utama:** Menjadi pemimpin pasar untuk komoditas **{rab_raw.get('komoditas', proj_name)}** dengan standar kualitas 3K.")
    with s_col2:
        sync_status = "Connected" if (rab_raw or sim_raw or source_trace == "Sinkron Modul 48") else "Template Mode"
        st.caption(f"Status Data: {sync_status} | Mode: Enterprise V3")

# --- TAB 1 (Langkah 1): EDITOR ---
with tab_editor:
    st.markdown("### ✍️ Langkah 1: Penyusunan Konten Strategis")
    st.caption("Gunakan bagian ini untuk mengisi detail narasi (SWOT) dan jadwal proyek secara manual.")
    
    # SWOT Editor
    st.subheader("1. Matriks SWOT")
    cols = st.columns(2)
    with cols[0]:
        st.session_state['swot_data']['Strengths'] = st.text_area("Kekuatan (Strengths)", st.session_state['swot_data']['Strengths'])
        st.session_state['swot_data']['Opportunities'] = st.text_area("Peluang (Opportunities)", st.session_state['swot_data']['Opportunities'])
    with cols[1]:
        st.session_state['swot_data']['Weaknesses'] = st.text_area("Kelemahan (Weaknesses)", st.session_state['swot_data']['Weaknesses'])
        st.session_state['swot_data']['Threats'] = st.text_area("Ancaman (Threats)", st.session_state['swot_data']['Threats'])
    
    st.divider()
    
    # Timeline Editor
    st.subheader("2. Project Timeline")
    df_timeline = pd.DataFrame(st.session_state['timeline_data'])
    edited_df = st.data_editor(df_timeline, num_rows="dynamic", use_container_width=True)
    st.session_state['timeline_data'] = edited_df.to_dict('records')

# --- TAB 3 (Langkah 3): FINAL PREVIEW ---
with tab_preview:
    st.success("✅ Tab 3 berhasil dimuat!")
    st.write(f"**Nama Proyek:** {proj_name}")
    st.write(f"**Perusahaan:** {company_name}")
    st.write(f"**Tanggal:** {report_date}")
    
    st.divider()
    
    st.subheader("� Data yang Tersedia:")
    st.write(f"- RAB: {'✅ Ada' if rab_raw else '❌ Kosong'}")
    st.write(f"- Greenhouse: {'✅ Ada' if sim_raw else '❌ Kosong'}")
    st.write(f"- Blockchain: {len(ledger_raw)} entries")
    
    st.divider()
    
    st.subheader("📄 Laporan Strategis")
    st.write("Konten laporan akan ditampilkan di sini.")
    
    # Test SWOT
    if st.button("Test Tampilkan SWOT"):
        st.json(st.session_state.get('swot_data', {}))
    
    # Test Timeline
    if st.button("Test Tampilkan Timeline"):
        st.json(st.session_state.get('timeline_data', []))
