import streamlit as st
import datetime
import pandas as pd
import base64

# Page Config
st.set_page_config(
    page_title="AgriSensa Strategic Report",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for "White Paper" Look
st.markdown("""
<style>
    .report-card {
        background: white;
        padding: 50px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        font-family: 'Georgia', serif;
        color: #1a202c;
        max-width: 800px;
        margin: auto;
    }
    .report-header {
        text-align: center;
        border-bottom: 2px solid #10b981;
        padding-bottom: 20px;
        margin-bottom: 30px;
    }
    .report-title {
        font-size: 2.5rem;
        color: #064e3b;
        margin-bottom: 5px;
    }
    .section-title {
        font-size: 1.5rem;
        color: #0f766e;
        border-bottom: 1px solid #cbd5e1;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-bottom: 5px;
    }
    .kpi-table {
        width: 100%;
        border-collapse: collapse;
    }
    .kpi-table td {
        padding: 10px;
        border: 1px solid #f1f5f9;
        font-size: 0.9rem;
    }
    .kpi-label {
        background: #f8fafc;
        font-weight: bold;
        width: 40%;
    }
    
    @media print {
        header, .stSidebar, .stButton, .stRadio, .stDownloadButton, .no-print {
            display: none !important;
        }
        .report-card {
            box-shadow: none;
            border: none;
            padding: 0;
            width: 100%;
        }
        body { background: white; }
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.title("📄 Strategic Project Report Generator")
st.markdown("**Ubah Analisis Proyek Anda Menjadi 'Buku Putih' Strategis (White Paper)**")

# --- SIDEBAR: INPUT PARAMETERS ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Laporan")
    proj_name = st.text_input("Nama Proyek", "Pusat Agribisnis Melon Premium 3K")
    company_name = st.text_input("Nama Perusahaan / Kelompok", "PT. AgriSensa Solusi Madani")
    owner_name = st.text_input("Pemilik Proyek / CEO", "Bpk. Yandri")
    report_date = st.date_input("Tanggal Laporan", datetime.date.today())
    
    st.divider()
    include_fin = st.toggle("Sertakan Ringkasan RAB", True)
    include_3k = st.toggle("Sertakan Strategi 3K", True)
    include_trace = st.toggle("Sertakan Traceability", True)
    
    if st.button("🖨️ Print Laporan ke PDF", type="primary", use_container_width=True):
        st.components.v1.html("<script>window.print();</script>", height=0)

# --- MAIN REPORT VIEW ---
st.info("💡 Tip: Gunakan Sidebar untuk mengatur data, lalu gunakan tombol 'Print' untuk menyimpan sebagai PDF.")

# Report Container
with st.container():
    st.markdown(f"""
    <div class="report-card">
        <div class="report-header">
            <h4 style="color:#10b981; margin:0;">📄 LAPORAN STRATEGIS AGRIBISNIS</h4>
            <h1 class="report-title">{proj_name}</h1>
            <p>Diterbitkan Oleh: <b>{company_name}</b></p>
            <p>Tanggal: {report_date.strftime('%d %B %Y')}</p>
        </div>
        
        <div class="section-title">I. Ringkasan Eksekutif</div>
        <p>
            Proyek <b>{proj_name}</b> dirancang untuk menjawab tantangan pasar modern akan kebutuhan pangan yang memiliki kontinuitas, 
            kualitas, dan kuantitas yang terstandarisasi. Laporan ini merangkum strategi budidaya, analisis finansial, 
            serta sistem pelacakan (traceability) yang menjamin keamanan pangan dari kebun hingga ke tangan konsumen.
        </p>
        <p>
            <b>Visi Utama:</b> Menjadi supplier utama sayuran/buah premium dengan efisiensi operasional berbasis data (Data-Driven Farming).
        </p>
    """, unsafe_allow_html=True)
    
    # Section II: Business & Financial
    if include_fin:
        # Pulling simulated data or existing session states
        st.markdown("""
        <div class="section-title">II. Analisis Bisnis & Finansial</div>
        <p>Berdasarkan simulasi investasi dan operasional, berikut adalah parameter ekonomi proyek:</p>
        <table class="kpi-table">
            <tr><td class="kpi-label">Total CAPEX (Investasi Awal)</td><td>Rp 850,000,000</td></tr>
            <tr><td class="kpi-label">Luas Area Produksi</td><td>1,000 m²</td></tr>
            <tr><td class="kpi-label">Target Kapasitas (per Minggu)</td><td>200 kg</td></tr>
            <tr><td class="kpi-label">Estimasi BEP (ROI)</td><td>24 - 28 Bulan</td></tr>
            <tr><td class="kpi-label">Modal Kerja (Consignment Gap)</td><td>Rp 45,000,000</td></tr>
        </table>
        <p style="font-size:0.8rem; font-style:italic; color:gray; margin-top:5px;">
            *Angka di atas adalah proyeksi berdasarkan model konsinyasi "Mati 1 Nota".
        </p>
        """, unsafe_allow_html=True)
        
    # Section III: Strategy 3K
    if include_3k:
        st.markdown("""
        <div class="section-title">III. Strategi Operasional 3K</div>
        <p>Proyek ini mengadopsi standar 3K AgriSensa sebagai pilar keberlanjutan:</p>
        <ul>
            <li><b>Kontinuitas:</b> Implementasi <i>Staggered Planting</i> (tanam bertahap) dalam 4-8 blok untuk menjamin panen mingguan tanpa putus.</li>
            <li><b>Kualitas:</b> Pengendalian nutrisi presisi dan IPM (Integrated Pest Management) untuk mencapai Grade A (Premium).</li>
            <li><b>Kuantitas:</b> Optimalisasi populasi tanaman per m² dan efisiensi Greenhouse mencapai 85% yield target.</li>
        </ul>
        """, unsafe_allow_html=True)

    # Section IV: Traceability
    if include_trace:
        st.markdown("""
        <div class="section-title">IV. Keamanan Pangan & Traceability</div>
        <p>Guna menjamin kepercayaan konsumen dan akses ke pasar modern, proyek mengintegrasikan <b>AgriSensa Blockchain Ledger</b>:</p>
        <ul>
            <li><b>Digital Handover:</b> Setiap perpindahan barang dicatat dengan Immutable Hash.</li>
            <li><b>QR Passport:</b> Setiap kemasan memiliki QR Code unik yang terhubung ke batch history.</li>
            <li><b>Audit Trail:</b> Riwayat pupuk, pestisida, dan tanggal panen dapat diverifikasi secara publik oleh pembeli.</li>
        </ul>
        <div style="text-align:center; padding: 20px; background:#f0fdf4; border-radius:10px; border:1px solid #10b981;">
            <p style="margin:0; font-weight:bold; color:#065f46;">VERIFIED PRODUCT STATUS</p>
            <p style="font-size:0.8rem; margin:0;">Blockchain Network Secured</p>
        </div>
        """, unsafe_allow_html=True)

    # Section V: Conclusion
    st.markdown(f"""
        <div class="section-title">V. Penutup & Pengesahan</div>
        <p>
            Laporan ini disusun sebagai dokumen panduan resmi bagi operasional dan manajemen <b>{company_name}</b>. 
            Strategi yang tertuang di dalamnya bersifat dinamis dan akan terus ditingkatkan seiring perkembangan data lapangan.
        </p>
        
        <table style="width:100%; margin-top:50px;">
            <tr>
                <td style="text-align:center;">
                    Dipersiapkan oleh,<br/><br/><br/><br/>
                    <b>Sistem AgriSensa AI</b><br/>
                    Technical Intelligence
                </td>
                <td style="text-align:center;">
                    Disetujui oleh,<br/><br/><br/><br/>
                    <b>{owner_name}</b><br/>
                    {company_name}
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# CSS for Print specifically
st.markdown("""
<style>
    /* Ensure the print result is clean */
    @media print {
        .report-card { 
            margin: 0; 
            box-shadow: none; 
            border: none; 
            padding: 0;
            display: block !important;
        }
        .stApp { background: white !important; }
    }
</style>
""", unsafe_allow_html=True)
