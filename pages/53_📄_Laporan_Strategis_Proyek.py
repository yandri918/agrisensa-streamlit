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
    include_fin = st.toggle("Analisis Finansial", True)
    include_swot = st.toggle("Analisis SWOT", True)
    include_timeline = st.toggle("Project Timeline", True)
    include_trace = st.toggle("Traceability & Security", True)
    
    st.divider()
    if st.button("🖨️ Generate & Print (Buku Putih)", type="primary", use_container_width=True):
        st.components.v1.html("<script>window.print();</script>", height=0)

# --- HEADER NATIVE ---
st.title("📄 Strategic Project Dossier V2")
st.markdown("Sistem Manajemen Laporan Strategis Terpadu — *AgriSensa Intelligence*")

# --- NATIVE TABS ---
tab_dashboard, tab_editor, tab_preview = st.tabs([
    "📊 Dashboard Strategis", 
    "✍️ Editor Dokumen", 
    "📑 Pratinjau Buku Putih"
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

# --- TAB 1: DASHBOARD ---
with tab_dashboard:
    st.markdown("### 📊 Project Intelligence Dashboard")
    
    # Check for Sync Data
    rab_raw = st.session_state.get('global_rab_summary', {})
    sim_raw = st.session_state.get('global_3k_sim', {})
    ledger_raw = st.session_state.get('ledger_db', [])
    
    # Row 1: Key Metrics
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Total Investment", f"Rp {rab_raw['total_biaya']:,.0f}" if rab_raw else "Rp 850M", "CAPEX")
    with m_col2:
        st.metric("Efficiency ROI", f"{rab_raw['roi_percent']:.1f}%" if rab_raw else "Market Avg", "Profitability")
    with m_col3:
        st.metric("Verified Blocks", f"{len(ledger_raw)} Blocks", "Blockchain")
    with m_col4:
        st.metric("Supply Readiness", f"{sim_raw['kapasitas_mingguan']} kg/wk" if sim_raw else "200 kg/wk", "Consistency")

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
        sync_status = "Online" if rab_raw or sim_raw else "Standalone"
        st.caption(f"Status Sistem: {sync_status} | Last Database Push: {rab_raw.get('timestamp', 'N/A')}")

# --- TAB 2: EDITOR ---
with tab_editor:
    st.header("📝 Dokumentasi Konten & Analisis")
    
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

# --- TAB 3: FINAL PREVIEW (WHITE PAPER) ---
with tab_preview:
    st.markdown("""
        <style>
            .stApp { background: #f1f5f9 !important; }
            .paper-view {
                background: white;
                max-width: 850px;
                margin: 40px auto;
                padding: 70px 90px;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                font-family: 'Inter', sans-serif;
                color: #1e293b;
                line-height: 1.8;
                border-radius: 4px;
            }
            .paper-header { border-bottom: 4px solid #059669; padding-bottom: 30px; margin-bottom: 50px; text-align: center; }
            .paper-title { font-size: 2.8rem; font-weight: 800; color: #064e3b; margin: 0; }
            .paper-section { font-size: 1.2rem; font-weight: 700; color: #065f46; margin-top: 40px; margin-bottom: 15px; border-left: 5px solid #10b981; padding-left: 15px; }
            .swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
            .swot-box { padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 0.9rem; }
            .swot-header { font-weight: bold; text-transform: uppercase; margin-bottom: 5px; display: block; color: #64748b; }
            .data-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            .data-table td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-size: 0.95rem; }
            .label-cell { color: #64748b; font-weight: 600; width: 40%; }
            .sign-grid { display: grid; grid-template-columns: 1fr 1fr; margin-top: 80px; text-align: center; }
            
            @media print {
                .stApp { background: white !important; }
                .paper-view { box-shadow: none; margin: 0; padding: 0; max-width: 100%; }
                header, .stSidebar, .stTabs, .stInfo, .no-print { display: none !important; }
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.info("📑 Mode Pratinjau Dokumen Aktif. Gunakan Sidebar untuk mencetak.")

    # CALCULATE FALLBACKS FOR REPORT
    r_total = f"Rp {rab_raw['total_biaya']:,.0f}" if rab_raw else "Rp 850,000,000"
    r_roi = f"{rab_raw['roi_percent']:.1f}%" if rab_raw else "24 - 28 Bulan"
    r_kap = f"{sim_raw['kapasitas_mingguan']} kg" if sim_raw else "200 kg"

    # BUILD CONTENT
    html_report = f"""
    <div class="paper-view">
        <div class="paper-header">
            <div style="text-transform: uppercase; letter-spacing: 4px; color: #059669; font-weight: bold; font-size: 0.8rem; margin-bottom: 10px;">Strategic Dossier</div>
            <h1 class="paper-title">{proj_name}</h1>
            <p style="margin-top: 10px; font-size: 1.1rem; color: #475569;">Prepared for: <b>Stakeholders & Management</b></p>
            <p style="color: #94a3b8; font-size: 0.85rem;">Official Release: {report_date.strftime('%d %B %Y')} | ID: AS-2025-V3</p>
        </div>

        <div class="paper-section">01. Rencana Strategis</div>
        <p>Proyek <b>{proj_name}</b> diinisiasi oleh <b>{company_name}</b> sebagai jawaban atas permintaan pasar modern terhadap produk pertanian yang konsisten. 
        Melalui integrasi otomasi dan sistem 3K, proyek ini menargetkan kepuasan mitra strategis dan efisiensi biaya yang optimal.</p>

        <div class="paper-section">02. Matriks Analisis SWOT</div>
        <div class="swot-grid">
            <div class="swot-box"><span class="swot-header">Strengths</span>{st.session_state['swot_data']['Strengths']}</div>
            <div class="swot-box"><span class="swot-header">Weaknesses</span>{st.session_state['swot_data']['Weaknesses']}</div>
            <div class="swot-box"><span class="swot-header">Opportunities</span>{st.session_state['swot_data']['Opportunities']}</div>
            <div class="swot-box"><span class="swot-header">Threats</span>{st.session_state['swot_data']['Threats']}</div>
        </div>

        <div class="paper-section">03. Kelayakan Ekonomi</div>
        <table class="data-table">
            <tr><td class="label-cell">Total Investasi Awal</td><td>{r_total}</td></tr>
            <tr><td class="label-cell">Estimasi ROI</td><td>{r_roi}</td></tr>
            <tr><td class="label-cell">Unit Kapasitas</td><td>{r_kap} / Minggu</td></tr>
            <tr><td class="label-cell">Kepatuhan Blockchain</td><td>{len(ledger_raw)} Transaksi Terverifikasi</td></tr>
        </table>

        <div class="paper-section">04. Timeline Implementasi</div>
        <table class="data-table">
    """
    for stage in st.session_state['timeline_data']:
        html_report += f"<tr><td class='label-cell'>{stage['Fase']}</td><td>{stage['Durasi']}</td></tr>"
    
    html_report += f"""
        </table>

        <div class="paper-section">05. Pernyataan & Pengesahan</div>
        <p style="font-size: 0.9rem; font-style: italic; color: #64748b;">Seluruh data di atas dihasilkan dari sistem AgriSensa Intelligence dan dapat dipertanggungjawabkan keakuratannya berdasarkan masukan operasional terkini.</p>
        
        <div class="sign-grid">
            <div>
                <p>Strategic Analyst,</p>
                <div style="height: 60px;"></div>
                <b>AgriSensa AI System</b><br>
                <span style="font-size: 0.8rem; color: #94a3b8;">Automated Report Engine</span>
            </div>
            <div>
                <p>Project Director,</p>
                <div style="height: 60px;"></div>
                <b>{owner_name}</b><br>
                <span style="font-size: 0.8rem; color: #94a3b8;">{company_name}</span>
            </div>
        </div>
    </div>
    """
    st.markdown(html_report, unsafe_allow_html=True)
