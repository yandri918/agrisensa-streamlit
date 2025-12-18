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
    "�️ Langkah 1: Penyusunan Konten",
    "📊 Langkah 2: Analisa Terintegrasi", 
    "� Langkah 3: Cetak Buku Putih"
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
    try:
        st.markdown("### 📑 Dokumentasi Resmi (Buku Putih)")
        st.caption("Pratinjau akhir sebelum dicetak ke PDF. Gunakan sidebar jika ingin mengubah sumber data atau mencetak.")
        
        # ADD PRINT CSS
        st.markdown("""
        <style>
            @media print {
                /* Hide Streamlit UI elements */
                header, .stSidebar, .stTabs, [data-testid="stHeader"], 
                [data-testid="stToolbar"], .stDeployButton, .stDecoration,
                .stMarkdown > div:first-child { display: none !important; }
                
                /* Make content full width */
                .main .block-container { max-width: 100% !important; padding: 0 !important; }
                
                /* Ensure tables print properly */
                table { page-break-inside: avoid; }
                
                /* Remove backgrounds */
                body, .stApp { background: white !important; }
            }
        </style>
        """, unsafe_allow_html=True)
        
        # CALCULATE FALLBACKS FOR REPORT (Safe access)
        r_total = f"Rp {rab_raw.get('total_biaya', 0):,.0f}" if rab_raw else "Rp 850,000,000"
        r_roi = f"{rab_raw.get('roi_percent', 0):.1f}%" if rab_raw else "24 - 28 Bulan"
        r_kap = f"{sim_raw.get('kapasitas_mingguan', 0)} kg" if sim_raw else "200 kg"
        r_blocks = f"{len(ledger_raw)} Transaksi" if source_trace == "Sinkron Modul 48" else "Sistem Terintegrasi"
        
        # DEBUG INFO (Optional - can be removed later)
        with st.expander("🔍 Debug: Status Data Sumber"):
            st.write(f"**RAB Data:** {'✅ Tersedia' if rab_raw else '❌ Kosong'}")
            st.write(f"**Greenhouse Data:** {'✅ Tersedia' if sim_raw else '❌ Kosong'}")
            st.write(f"**Blockchain Data:** {len(ledger_raw)} entries")
            st.write(f"**Source RAB:** {source_rab}")
            st.write(f"**Source 3K:** {source_3k}")
            st.write(f"**Source Trace:** {source_trace}")
        
        # === NATIVE STREAMLIT REPORT ===
        st.markdown("---")
        
        # HEADER
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #059669 0%, #064e3b 100%); color: white; border-radius: 10px; margin-bottom: 30px;'>
            <div style='font-size: 0.9rem; letter-spacing: 3px; margin-bottom: 10px;'>STRATEGIC DOSSIER</div>
            <h1 style='margin: 0; font-size: 2.5rem;'>{proj_name}</h1>
            <p style='margin-top: 10px; opacity: 0.9;'>Prepared for: Stakeholders & Management</p>
            <p style='font-size: 0.85rem; opacity: 0.8;'>Official Release: {report_date.strftime('%d %B %Y')} | ID: AS-2025-V3</p>
        </div>
        """, unsafe_allow_html=True)
        
        # SECTION 1: RENCANA STRATEGIS
        st.subheader("01. Rencana Strategis")
        st.write(f"""
        Proyek **{proj_name}** diinisiasi oleh **{company_name}** sebagai jawaban atas permintaan pasar modern 
        terhadap produk pertanian yang konsisten. Melalui integrasi otomasi dan sistem 3K, proyek ini menargetkan 
        kepuasan mitra strategis dan efisiensi biaya yang optimal.
        """)
        
        st.markdown("---")
        
        # SECTION 2: SWOT
        st.subheader("02. Matriks Analisis SWOT")
        swot_col1, swot_col2 = st.columns(2)
        with swot_col1:
            st.success(f"**💪 Strengths**\n\n{st.session_state['swot_data']['Strengths']}")
            st.info(f"**🌟 Opportunities**\n\n{st.session_state['swot_data']['Opportunities']}")
        with swot_col2:
            st.warning(f"**⚠️ Weaknesses**\n\n{st.session_state['swot_data']['Weaknesses']}")
            st.error(f"**🚨 Threats**\n\n{st.session_state['swot_data']['Threats']}")
        
        st.markdown("---")
        
        # SECTION 3: KELAYAKAN EKONOMI
        st.subheader("03. Kelayakan Ekonomi")
        df_ekonomi = pd.DataFrame({
            "Parameter Investasi": ["Total Investasi Awal", "Estimasi ROI", "Unit Kapasitas", "Kepatuhan Blockchain"],
            "Nilai / Target": [r_total, r_roi, f"{r_kap} / Minggu", r_blocks]
        })
        st.table(df_ekonomi)
        
        st.markdown("---")
        
        # SECTION 4: TIMELINE
        st.subheader("04. Timeline Implementasi")
        df_timeline_display = pd.DataFrame(st.session_state['timeline_data'])
        df_timeline_display.columns = ["Fase Proyek", "Ekspektasi Durasi"]
        st.table(df_timeline_display)
        
        st.markdown("---")
        
        # SECTION 5: PENGESAHAN
        st.subheader("05. Pernyataan & Pengesahan")
        st.caption("_Seluruh data di atas dihasilkan dari sistem AgriSensa Intelligence dan dapat dipertanggungjawabkan keakuratannya berdasarkan masukan operasional terkini._")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        sig_col1, sig_col2 = st.columns(2)
        with sig_col1:
            st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <p>Strategic Analyst,</p>
                <div style='height: 60px;'></div>
                <b>AgriSensa AI System</b><br>
                <span style='font-size: 0.85rem; color: gray;'>Automated Report Engine</span>
            </div>
            """, unsafe_allow_html=True)
        with sig_col2:
            st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <p>Project Director,</p>
                <div style='height: 60px;'></div>
                <b>{owner_name}</b><br>
                <span style='font-size: 0.85rem; color: gray;'>{company_name}</span>
            </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ **Error saat me-render laporan:**\n\n```\n{str(e)}\n```")
        st.info("💡 **Kemungkinan penyebab:**\n- Data dari modul lain belum tersedia\n- Session state belum ter-initialize\n- Variabel tidak terdefinisi")
        
        # Show traceback for debugging
        import traceback
        with st.expander("🔧 Detail Error (untuk debugging)"):
            st.code(traceback.format_exc())
