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

# CSS for the Report
report_css = """
<style>
    .report-card {
        background: white;
        padding: 60px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
        font-family: 'Georgia', serif;
        color: #1a202c;
        max-width: 850px;
        margin: 20px auto;
        line-height: 1.6;
    }
    .report-header {
        text-align: center;
        border-bottom: 2px solid #10b981;
        padding-bottom: 30px;
        margin-bottom: 40px;
    }
    .report-title {
        font-size: 2.8rem;
        color: #064e3b;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .report-subtitle {
        font-size: 1.2rem;
        color: #10b981;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    .section-title {
        font-size: 1.6rem;
        color: #0f766e;
        border-bottom: 1.5px solid #cbd5e1;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 8px;
        font-weight: bold;
    }
    .kpi-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    .kpi-table td {
        padding: 12px;
        border: 1px solid #e2e8f0;
        font-size: 1rem;
    }
    .kpi-label {
        background: #f8fafc;
        font-weight: bold;
        width: 45%;
        color: #334155;
    }
    .report-footer-table {
        width: 100%;
        margin-top: 60px;
        border: none;
    }
    .report-footer-table td {
        text-align: center;
        border: none;
        width: 50%;
    }
    
    @media print {
        header, .stSidebar, .stButton, .stRadio, .stDownloadButton, .no-print, .stInfo {
            display: none !important;
        }
        .report-card {
            box-shadow: none;
            border: none;
            padding: 0;
            width: 100%;
            margin: 0;
        }
        body { background: white !important; }
        .stApp { background: white !important; }
    }
</style>
"""

# START BUILDING THE HTML
full_html = f"""
{report_css}
<div class="report-card">
    <div class="report-header">
        <div class="report-subtitle">LAPORAN STRATEGIS AGRIBISNIS</div>
        <h1 class="report-title">{proj_name}</h1>
        <p style="font-size: 1.1rem; margin-top: 10px;">
            Diterbitkan Oleh: <br><b style="color: #064e3b; font-size: 1.3rem;">{company_name}</b>
        </p>
        <p style="color: #64748b;">Tanggal Terbit: {report_date.strftime('%d %B %Y')}</p>
    </div>
    
    <div class="section-title">I. Ringkasan Eksekutif</div>
    <p>
        Proyek <b>{proj_name}</b> dirancang untuk menjawab tantangan pasar modern akan kebutuhan pangan yang memiliki kontinuitas, 
        kualitas, dan kuantitas yang terstandarisasi. Laporan ini merangkum strategi budidaya, analisis finansial, 
        serta sistem pelacakan (traceability) yang menjamin keamanan pangan dari kebun hingga ke tangan konsumen.
    </p>
    <p>
        <b>Visi Utama:</b> Menjadi supplier utama sayuran/buah premium dengan efisiensi operasional berbasis data (Data-Driven Farming) 
        yang unggul dalam persaingan pasar global maupun lokal.
    </p>
"""

if include_fin:
    full_html += f"""
    <div class="section-title">II. Analisis Bisnis & Finansial</div>
    <p>Berdasarkan simulasi investasi dan operasional yang telah dilakukan melalui ekosistem AgriSensa, berikut adalah parameter ekonomi proyek:</p>
    <table class="kpi-table">
        <tr><td class="kpi-label">Total CAPEX (Investasi Awal)</td><td>Rp 850,000,000</td></tr>
        <tr><td class="kpi-label">Luas Area Produksi</td><td>1,000 m²</td></tr>
        <tr><td class="kpi-label">Target Kapasitas (per Minggu)</td><td>200 kg</td></tr>
        <tr><td class="kpi-label">Estimasi BEP (ROI)</td><td>24 - 28 Bulan</td></tr>
        <tr><td class="kpi-label">Kebutuhan Modal Kerja (Consignment)</td><td>Rp 45,000,000</td></tr>
    </table>
    <p style="font-size:0.9rem; font-style:italic; color:#64748b; margin-top:10px;">
        *Catatan: Proyeksi menggunakan model pembayaran "Mati 1 Nota" dengan tempo 2 minggu.
    </p>
    """

if include_3k:
    full_html += """
    <div class="section-title">III. Strategi Operasional 3K</div>
    <p>Pilar utama keberhasilan operasional proyek ini bersandar pada standar 3K AgriSensa:</p>
    <ul>
        <li><b>Kontinuitas (Continuity):</b> Menjamin ketersediaan barang di rak supermarket melalui jadwal tanam <i>Staggered Planting</i> yang presisi.</li>
        <li><b>Kualitas (Quality):</b> Pemantauan nutrisi real-time dan standar GAP (Good Agricultural Practices) untuk hasil Grade A.</li>
        <li><b>Kuantitas (Quantity):</b> Pencapaian target tonase melalui efisiensi populasi dan manajemen hama terpadu.</li>
    </ul>
    <p>Implementasi ini memastikan bahwa <b>PT. AgriSensa Solusi Madani</b> mampu memenuhi kontrak pasokan secara profesional.</p>
    """

if include_trace:
    full_html += """
    <div class="section-title">IV. Keamanan Pangan & Traceability</div>
    <p>Proyek ini mengedepankan transparansi total terhadap konsumen melalui teknologi Blockchain:</p>
    <ul>
        <li><b>Immutable Records:</b> Setiap batch produksi memiliki sidik jari digital (Hash) yang tidak dapat dimanipulasi.</li>
        <li><b>Traceability Passport:</b> Konsumen dapat melacak asal-usul tanah, pupuk, dan tanggal panen melalui QR Code pada kemasan.</li>
        <li><b>Kepuasan Konsumen:</b> Menjamin bahwa produk yang dikonsumsi adalah produk asli, segar, dan sehat.</li>
    </ul>
    <div style="text-align:center; padding: 25px; background:#f0fdf4; border-radius:12px; border:1px solid #10b981; margin-top: 20px;">
        <p style="margin:0; font-weight:bold; color:#065f46; font-size: 1.1rem;">✅ VERIFIED BY AGRISENSA BLOCKCHAIN</p>
        <p style="font-size:0.85rem; margin:5px 0 0 0; color: #059669;">Data Keamanan Pangan Terjamin & Terenkripsi</p>
    </div>
    """

full_html += f"""
    <div class="section-title">V. Penutup & Pengesahan</div>
    <p>
        Laporan ini disusun sebagai dokumen panduan strategis resmi. Seluruh data dan proyeksi di dalamnya merupakan hasil integrasi 
        cerdas dari platform AgriSensa yang menggabungkan keahlian agronomi dan teknologi digital.
    </p>
    
    <table class="report-footer-table">
        <tr>
            <td>
                <p>Dipersiapkan secara digital oleh,</p>
                <br><br><br>
                <b style="font-size: 1.1rem;">Sistem AgriSensa AI</b><br>
                <span style="color: #64748b;">Technical Intelligence Provider</span>
            </td>
            <td>
                <p>Disetujui dan Disahkan oleh,</p>
                <br><br><br>
                <b style="font-size: 1.1rem;">{owner_name}</b><br>
                <span style="color: #64748b;">Managing Director / Owner</span>
            </td>
        </tr>
    </table>
</div>
"""

# Render Everything in One Go
st.markdown(full_html, unsafe_allow_html=True)
