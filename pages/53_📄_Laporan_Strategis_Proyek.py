import streamlit as st
import datetime
import pandas as pd
import base64

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

# --- TAB 1: DASHBOARD ---
with tab_dashboard:
    st.header("Project KPI Dashboard")
    
    # Check for Sync Data
    rab_raw = st.session_state.get('global_rab_summary', {})
    sim_raw = st.session_state.get('global_3k_sim', {})
    ledger_raw = st.session_state.get('ledger_db', [])
    
    if rab_raw or sim_raw:
        st.success(f"✅ Data Sinkron Aktif (Last Sync: {rab_raw.get('timestamp', sim_raw.get('timestamp', 'N/A'))})")
    else:
        st.warning("⚠️ Data Belum Sinkron. Silakan isi RAB dan Simulasi di modul terkait untuk data otomatis.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        val_capex = f"Rp {rab_raw['total_biaya']:,.0f}" if rab_raw else "Rp 850 Juta"
        st.metric("Total Biaya (RAB)", val_capex, "Live" if rab_raw else "Blueprint")
    with col2:
        val_roi = f"{rab_raw['roi_percent']:.1f}%" if rab_raw else "24-28 Bln"
        st.metric("Estimasi ROI", val_roi, "RAB Data" if rab_raw else "Market Avg")
    with col3:
        val_kap = f"{sim_raw['kapasitas_mingguan']} kg" if sim_raw else "200 kg"
        st.metric("Kapasitas Suplai", val_kap, "Weekly" if sim_raw else "Target")
    with col4:
        val_safety = "AAA" if len(ledger_raw) > 2 else "B (New)"
        st.metric("Blockchain Score", val_safety, f"{len(ledger_raw)} Blocks")
    
    st.markdown("---")
    # ... rest of dashboard ...
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💡 Visi Strategis")
        desc_kom = rab_raw.get('komoditas', proj_name)
        st.success(f"Proyek **{desc_kom}** bertujuan mendominasi pasar premium melalui efisiensi berbasis data dan standarisasi 3K.")
    with c2:
        st.subheader("🚩 Mitigasi Risiko Utama")
        risk_note = f"Fokus pada retur {sim_raw.get('retur_factor', 5)}% dan gap pembayaran {sim_raw.get('gap_pembayaran', 'N/A')}." if sim_raw else "Otomasi irigasi dan sistem peringatan dini diaktifkan."
        st.warning(risk_note)

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
    st.info("💡 Halaman ini dirancang khusus untuk dicetak ke PDF via Sidebar.")
    
    # PREMIUM CSS FOR THE DOSSIER
    report_css = """
    <style>
        .dossier-root {
            background: white;
            padding: 80px 60px;
            border: 1px solid #e2e8f0;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            color: #1a202c;
            max-width: 850px;
            margin: auto;
            line-height: 1.7;
            position: relative;
        }
        .dossier-watermark {
            position: absolute;
            top: 20px;
            right: 20px;
            border: 2px solid #ef4444;
            color: #ef4444;
            padding: 5px 15px;
            font-weight: bold;
            text-transform: uppercase;
            transform: rotate(5deg);
            opacity: 0.6;
            font-size: 0.8rem;
        }
        .report-header {
            text-align: center;
            border-bottom: 3px solid #059669;
            padding-bottom: 40px;
            margin-bottom: 50px;
        }
        .report-title {
            font-size: 3rem;
            color: #064e3b;
            margin: 10px 0;
            font-weight: 800;
            letter-spacing: -1px;
        }
        .section-title {
            font-size: 1.4rem;
            color: #065f46;
            margin-top: 50px;
            margin-bottom: 20px;
            font-weight: 700;
            display: flex;
            align-items: center;
        }
        .section-title::after {
            content: "";
            flex: 1;
            height: 1px;
            background: #cbd5e1;
            margin-left: 20px;
        }
        /* SWOT GRID */
        .swot-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }
        .swot-card {
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
        }
        .swot-s { background: #f0fdf4; border-left: 5px solid #22c55e; }
        .swot-w { background: #fff1f2; border-left: 5px solid #f43f5e; }
        .swot-o { background: #f0f9ff; border-left: 5px solid #0ea5e9; }
        .swot-t { background: #fefce8; border-left: 5px solid #eab308; }
        .swot-label { font-weight: 800; font-size: 0.9rem; margin-bottom: 5px; display: block; text-transform: uppercase; }

        /* PREMIUM TABLES */
        .premium-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .premium-table th {
            background: #f8fafc;
            color: #475569;
            text-align: left;
            padding: 12px 15px;
            font-size: 0.85rem;
            text-transform: uppercase;
            border-bottom: 2px solid #e2e8f0;
        }
        .premium-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #f1f5f9;
            font-size: 0.95rem;
        }
        .kpi-label { font-weight: 600; color: #334155; background: #f8fafc; width: 40%; }
        
        @media print {
            header, .stSidebar, .stButton, .stTabs, .stInfo, .stMetric, .stAlert, .no-print { display: none !important; }
            .dossier-root { border: none; padding: 0; width: 100%; }
            body { background: white; }
            .stApp { background: white !important; }
        }
    </style>
    """
    
    # BUILD CONTENT
    html_content = f"""
    <div class="dossier-root">
        <div class="dossier-watermark">CONFIDENTIAL & STRATEGIC</div>
        
        <div class="report-header">
            <div style="color:#059669; font-weight:700; font-size:1.1rem; margin-bottom:10px;">PROPOSAL STRATEGIS BISNIS</div>
            <h1 class="report-title">{proj_name}</h1>
            <p style="font-size:1.2rem; margin-top:10px; color:#475569;">Oleh: <b>{company_name}</b></p>
            <p style="color:#94a3b8; font-size:0.9rem;">Dokumen ID: AS-{report_date.strftime('%Y%j')}-PRO</p>
            <p style="color:#94a3b8; font-size:0.9rem;">Diterbitkan pada: {report_date.strftime('%d %B %Y')}</p>
        </div>
        
        <div class="section-title">01. Ringkasan Eksekutif</div>
        <p>
            Proyek <b>{proj_name}</b> merupakan inisiasi strategis yang menggabungkan otomasi cerdas, manajemen 3K, dan transparansi blockchain. 
            Laporan ini berfungsi sebagai dokumen kelayakan utama yang merinci posisi kompetitif, proyeksi ekonomi, dan 
            kerangka waktu implementasi untuk mencapai keunggulan operasional di pasar modern.
        </p>
    """
    
    if include_swot:
        html_content += f"""
        <div class="section-title">02. Matriks Analisis SWOT</div>
        <div class="swot-grid">
            <div class="swot-card swot-s"><span class="swot-label">Strengths</span>{st.session_state['swot_data']['Strengths']}</div>
            <div class="swot-card swot-w"><span class="swot-label">Weaknesses</span>{st.session_state['swot_data']['Weaknesses']}</div>
            <div class="swot-card swot-o"><span class="swot-label">Opportunities</span>{st.session_state['swot_data']['Opportunities']}</div>
            <div class="swot-card swot-t"><span class="swot-label">Threats</span>{st.session_state['swot_data']['Threats']}</div>
        </div>
        """
        
    if include_fin:
        c_capex = f"Rp {rab_raw['total_biaya']:,.0f}" if rab_raw else "Rp 850,000,000"
        c_roi = f"{rab_raw['roi_percent']:.1f}%" if rab_raw else "24 - 28 Bulan"
        c_mkt = f"{sim_raw['gap_pembayaran']}" if sim_raw else "Mati 1 Nota"
        
        html_content += f"""
        <div class="section-title">03. Proyeksi Ekonomi & Investasi</div>
        <table class="premium-table">
            <thead><tr><th>Parameter Investasi</th><th>Estimasi Nilai / Target</th></tr></thead>
            <tbody>
                <tr><td class="kpi-label">Investasi CAPEX</td><td>{c_capex}</td></tr>
                <tr><td class="kpi-label">Target ROI (Musim)</td><td>{c_roi}</td></tr>
                <tr><td class="kpi-label">Model Pembayaran</td><td>{c_mkt}</td></tr>
                <tr><td class="kpi-label">Margin Bersih Est.</td><td>35% - 42%</td></tr>
            </tbody>
        </table>
        """
        
    if include_timeline:
        html_content += """
        <div class="section-title">04. Timeline Rencana Aksi</div>
        <table class="premium-table">
            <thead><tr><th>Fase Proyek</th><th>Ekspektasi Durasi</th></tr></thead>
            <tbody>"""
        for item in st.session_state['timeline_data']:
            html_content += f"<tr><td class='kpi-label'>{item['Fase']}</td><td>{item['Durasi']}</td></tr>"
        html_content += "</tbody></table>"
        
    if include_trace:
        l_count = len(ledger_raw)
        html_content += f"""
        <div class="section-title">05. Keamanan Digital & Traceability</div>
        <p>Integrasi <b>{l_count} transaksi blockchain</b> menjamin transparansi rantai pasok. 
        Sistem sertifikasi digital ini memungkinkan audit instan terhadap kepatuhan SOP.</p>
        <div style="background:#f8fafc; padding:30px; border-radius:12px; margin-top:20px; border: 1px solid #e2e8f0; text-align:center;">
            <div style="color:#059669; font-weight:800; font-size:1.1rem; margin-bottom:5px;">● BLOCKCHAIN VERIFIED ({l_count} BLOCKS)</div>
            <p style="margin:0; font-size:0.85rem; color:#64748b;">Protocol SHA-256 Secured</p>
        </div>
        """
        
    html_content += f"""
        <div class="section-title">06. Pengesahan Strategis</div>
        <table style="width:100%; margin-top:80px; border:none;">
            <tr style="border:none;">
                <td style="text-align:center; border:none; width:50%;">
                    <div style="border-top:1px solid #475569; width:200px; margin:auto; margin-bottom:10px;"></div>
                    <b style="font-size:0.9rem;">Intelligence System AgriSensa</b><br>
                    <span style="font-size:0.8rem; color:gray;">Penyusun Laporan Digital</span>
                </td>
                <td style="text-align:center; border:none; width:50%;">
                    <div style="border-top:1px solid #475569; width:200px; margin:auto; margin-bottom:10px;"></div>
                    <b style="font-size:0.9rem;">{owner_name}</b><br>
                    <span style="font-size:0.8rem; color:gray;">Direktur / Pemilik Proyek</span>
                </td>
            </tr>
        </table>
    </div>
    """
    
    # RENDER
    st.markdown(report_css, unsafe_allow_html=True)
    st.markdown(html_content, unsafe_allow_html=True)
