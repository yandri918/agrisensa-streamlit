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
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total CAPEX", "Rp 850 Juta", "Simulasi")
    with col2:
        st.metric("Estimasi ROI", "24-28 Bln", "-2 Bln")
    with col3:
        st.metric("Market Readiness", "92%", "Excellent")
    with col4:
        st.metric("Safety Score", "AAA", "Blockchain")
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💡 Visi Strategis")
        st.success(f"Proyek **{proj_name}** bertujuan mendominasi pasar premium melalui efisiensi berbasis data dan standarisasi 3K.")
    with c2:
        st.subheader("🚩 Mitigasi Risiko Utama")
        st.warning("Otomasi irigasi dan sistem peringatan dini (Early Warning System) diaktifkan untuk menjaga kuantitas panen.")

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
    
    # CSS remains the same for the print document
    report_css = """
    <style>
        .report-card { background: white; padding: 60px; border: 1px solid #e2e8f0; font-family: 'Georgia', serif; color: #1a202c; max-width: 850px; margin: auto; line-height: 1.6; }
        .report-header { text-align: center; border-bottom: 2px solid #10b981; padding-bottom: 30px; margin-bottom: 40px; }
        .report-title { font-size: 2.8rem; color: #064e3b; margin-bottom: 5px; font-weight: bold; }
        .section-title { font-size: 1.6rem; color: #0f766e; border-bottom: 1.5px solid #cbd5e1; margin-top: 40px; margin-bottom: 15px; padding-bottom: 5px; font-weight: bold; }
        .kpi-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .kpi-table td { padding: 12px; border: 1px solid #e2e8f0; font-size: 0.95rem; }
        .kpi-label { background: #f8fafc; font-weight: bold; width: 40%; }
        .swot-box { padding: 15px; border-left: 4px solid #10b981; background: #f0fdf4; margin-bottom: 10px; }
        
        @media print {
            header, .stSidebar, .stButton, .stTabs, .stInfo, .stMetric, .stAlert, .no-print { display: none !important; }
            .report-card { box-shadow: none; border: none; padding: 0; width: 100%; }
            body { background: white; }
            .stApp { background: white !important; }
        }
    </style>
    """
    
    # Build HTML Content
    html_content = f"""
    <div class="report-card">
        <div class="report-header">
            <div style="color:#10b981; letter-spacing:3px; font-size:0.9rem;">CONFIDENTIAL STRATEGIC DOSSIER</div>
            <h1 class="report-title">{proj_name}</h1>
            <p style="font-size:1.1rem; margin-top:5px;">Oleh: <b>{company_name}</b></p>
            <p style="color:gray;">Tanggal: {report_date.strftime('%d %B %Y')}</p>
        </div>
        
        <div class="section-title">I. Ringkasan Eksekutif</div>
        <p>
            Proyek <b>{proj_name}</b> merupakan inisiasi strategis yang menggabungkan otomasi cerdas, manajemen 3K, dan transparansi blockchain. 
            Laporan ini berfungsi sebagai "Buku Putih" (White Paper) yang merinci kelayakan bisnis dan kesiapan operasional.
        </p>
    """
    
    if include_swot:
        html_content += f"""
        <div class="section-title">II. Analisis SWOT Strategis</div>
        <div class="swot-box"><b>Strengths:</b> {st.session_state['swot_data']['Strengths']}</div>
        <div class="swot-box"><b>Weaknesses:</b> {st.session_state['swot_data']['Weaknesses']}</div>
        <div class="swot-box"><b>Opportunities:</b> {st.session_state['swot_data']['Opportunities']}</div>
        <div class="swot-box"><b>Threats:</b> {st.session_state['swot_data']['Threats']}</div>
        """
        
    if include_fin:
        html_content += f"""
        <div class="section-title">III. Parameter Ekonomi & Investasi</div>
        <table class="kpi-table">
            <tr><td class="kpi-label">Estimasi CAPEX</td><td>Rp 850,000,000</td></tr>
            <tr><td class="kpi-label">Periode BEP</td><td>24 - 28 Bulan</td></tr>
            <tr><td class="kpi-label">Modal Kerja (Reserves)</td><td>Rp 45,000,000</td></tr>
            <tr><td class="kpi-label">Target Margin Bersih</td><td>35% - 42%</td></tr>
        </table>
        """
        
    if include_timeline:
        html_content += """<div class="section-title">IV. Project Timeline & Fasilitas</div><table class="kpi-table">"""
        for item in st.session_state['timeline_data']:
            html_content += f"<tr><td class='kpi-label'>{item['Fase']}</td><td>{item['Durasi']}</td></tr>"
        html_content += "</table>"
        
    if include_trace:
        html_content += """
        <div class="section-title">V. Keamanan Data & Traceability</div>
        <p>Seluruh transaksi serah terima dicatat dalam <b>AgriSensa Blockchain Ledger</b>, menjamin data tidak dapat diubah (immutable) dan dapat diverifikasi oleh konsumen maupun mitra modern market.</p>
        <div style="background:#f1f5f9; padding:20px; border-radius:10px; text-align:center; border: 1px dashed #cbd5e1;">
            <b style="color:#0f172a;">NETWORK STATUS: SECURED</b><br/>
            <span style="font-size:0.8rem; color:gray;">Hash Verification Protocol Active</span>
        </div>
        """
        
    html_content += f"""
        <div class="section-title">VI. Pengesahan</div>
        <table style="width:100%; margin-top:50px; border:none;">
            <tr style="border:none;">
                <td style="text-align:center; border:none;">
                    Dipersiapkan oleh,<br/><br/><br/><br/>
                    <b>Intelligence System AgriSensa</b>
                </td>
                <td style="text-align:center; border:none;">
                    Disetujui oleh,<br/><br/><br/><br/>
                    <b>{owner_name}</b><br/>
                    {company_name}
                </td>
            </tr>
        </table>
    </div>
    """
    
    # Final Rendering
    st.markdown(report_css, unsafe_allow_html=True)
    st.markdown(html_content, unsafe_allow_html=True)
