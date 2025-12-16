
import streamlit as st
import pandas as pd
import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Page Config
st.set_page_config(
    page_title="Traceability & QR Passport",
    page_icon="🏷️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .label-preview {
        border: 2px dashed #cbd5e1;
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    h1, h2, h3 { color: #134e4a; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🏷️ AgriPass (Traceability)</h1><p>Paspor Digital Produk Premium & Generator QR Code</p></div>', unsafe_allow_html=True)

# SESSION STATE Init
if 'batch_data' not in st.session_state:
    st.session_state['batch_data'] = {}

# TABS
tab1, tab2 = st.tabs(["📝 Input Data Batch (Produksi)", "📱 Simulasi Scan Konsumen"])

# --- TAB 1: INPUT BATCH ---
with tab1:
    col_in1, col_in2 = st.columns([1, 1.5])
    
    with col_in1:
        st.subheader("1. Identitas Produk")
        jenis_produk = st.selectbox("Jenis Komoditas", ["Beras Premium", "Kopi Robusta", "Sayuran Organik", "Melon Hidroponik", "Madu Murni"])
        varietas = st.text_input("Varietas / Grade", "Cianjur Pandan Wangi (Grade A)")
        tgl_panen = st.date_input("Tanggal Panen", datetime.date.today())
        
        st.subheader("2. Asal Usul (Origin)")
        nama_petani = st.text_input("Nama Petani / Kelompok", "Gapoktan Sejahtera")
        lokasi_kebun = st.text_input("Lokasi Kebun", "Banyumas, Jawa Tengah")
        
        st.subheader("3. Klaim Kualitas")
        is_organik = st.checkbox("✅ Bebas Pestisida / Organik")
        is_halal = st.checkbox("✅ Halal Certified")
        is_premium = st.checkbox("✅ Kualitas Ekspor (Sortir Ketat)")
        
        # Generator ID
        batch_id = f"AGRI-{tgl_panen.strftime('%Y%m%d')}-{hash(jenis_produk)%1000:03d}"
        
        if st.button("💾 Simpan & Generate QR Code"):
            st.session_state['batch_data'] = {
                "id": batch_id,
                "produk": jenis_produk,
                "varietas": varietas,
                "tgl": tgl_panen,
                "petani": nama_petani,
                "lokasi": lokasi_kebun,
                "klaim": [k for k, v in [("Organik", is_organik), ("Halal", is_halal), ("Premium", is_premium)] if v]
            }
            st.success(f"Batch {batch_id} berhasil dibuat!")
            
    with col_in2:
        st.subheader("🖨️ Desain Label Kemasan")
        
        if st.session_state['batch_data']:
            data = st.session_state['batch_data']
            
            # QR Code Generation
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            # Rich Text QR (Offline Compatible)
            qr_content = f"""AgriSensa Verified Product
ID: {data['id']}
Produk: {data['produk']} ({data['varietas']})
Petani: {data['petani']} @ {data['lokasi']}
Panen: {data['tgl']}
Kualitas: {', '.join(data['klaim'])}
"""
            qr.add_data(qr_content)
            qr.make(fit=True)
            img_qr = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to visible image in streamlit
            buf = io.BytesIO()
            img_qr.save(buf)
            byte_im = buf.getvalue()
            
            # Simple "Sticker" Layout using HTML/CSS for preview
            # Professional Label Layout (Japanese Style Compact)
            # Professional Label Layout (Table Based for Stability)
            st.markdown(f"""
            <div style='border: 2px solid #000; background: white; border-radius: 8px; max-width: 480px; margin: auto; padding: 10px;'>
                <table style='width: 100%; border: none;'>
                    <tr style='border: none;'>
                        <td style='width: 140px; padding: 5px; border: none; vertical-align: top;'>
                            <img src="data:image/png;base64,{base64.b64encode(byte_im).decode()}" width="130" style='border: 1px solid #ccc;'>
                        </td>
                        <td style='padding: 5px; border: none; vertical-align: top; text-align: left;'>
                            <h3 style='margin: 0; padding: 0; color: #000; font-size: 20px;'>{data['produk']}</h3>
                            <p style='margin: 0 0 8px 0; color: #555; font-size: 14px;'>{data['varietas']}</p>
                            
                            <p style='margin: 0; font-size: 13px; color: #222; line-height: 1.4;'>
                                <b>Petani:</b> {data['petani']}<br>
                                <b>Lokasi:</b> {data['lokasi']}<br>
                                <b>Panen:</b> {data['tgl']}
                            </p>
                            
                            <div style='margin-top: 8px;'>
                                {' '.join([f"<span style='background:#10b981; color:white; padding:2px 6px; border-radius:4px; font-size:11px; margin-right:4px;'>{k}</span>" for k in data['klaim']])}
                            </div>
                            <p style='margin-top: 5px; font-size: 10px; color: #888;'>ID: {data['id']}</p>
                        </td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            
            st.download_button("⬇️ Download Gambar QR", byte_im, f"QR_{data['id']}.png", "image/png")
            st.caption("Tempel stiker ini di kemasan produk Anda untuk masuk Supermarket.")
            
        else:
            st.info("👈 Isi data di sebelah kiri lalu klik tombol Simpan.")

# --- TAB 2: CONSUMER VIEW ---
with tab2:
    st.markdown("### 📱 Tampilan di HP Konsumen")
    st.info("Ini yang dilihat pembeli saat men-scan QR Code Anda.")
    
    if st.session_state['batch_data']:
        data = st.session_state['batch_data']
        
        # Simulation of Mobile View (Narrow container)
        c_mob1, c_mob2, c_mob3 = st.columns([1.5, 2, 1.5])
        
        with c_mob2:
            st.markdown("""
            <div style='border: 8px solid #333; border-radius: 20px; padding: 20px; background-color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.2);'>
                <div style='text-align:center;'>
                    <h3 style='color:#0f766e;'>✅ TERVERIFIKASI</h3>
                    <p style='color:grey;'>AgriSensa Blockchain Network</p>
                    <hr>
                    <h1>🌾</h1>
                    <h2>Produk Asli & Aman</h2>
                </div>
                
                <div style='background:#f0fdfa; padding:15px; border-radius:10px; margin: 15px 0;'>
                    <p><b>📦 Batch ID:</b> <br>""" + data['id'] + """</p>
                    <p><b>🗓️ Tanggal Panen:</b> <br>""" + str(data['tgl']) + """</p>
                    <p><b>📍 Lokasi:</b> <br>""" + data['lokasi'] + """</p>
                </div>
                
                <p><b>Cerita Petani:</b></p>
                <p style='font-style:italic; font-size:0.9rem;'>
                    "Produk ini dirawat dengan sepenuh hati oleh """ + data['petani'] + """. 
                    Kami menggunakan metode berkelanjutan untuk menjaga alam tetap lestari."
                </p>
                
                <div style='text-align:center; margin-top:20px;'>
                    <button style='background:#0f766e; color:white; border:none; padding:10px 20px; border-radius:50px; width:100%;'>Beli Lagi (Order)</button>
                </div>
                 <div style='text-align:center; margin-top:10px;'>
                    <a href='#'>Lihat Hasil Lab</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Belum ada data batch yang dibuat. Silakan input di Tab 1 dulu.")

# Footer
st.markdown("---")
st.caption("AgriSensa Traceability - Membangun Kepercayaan dari Kebun ke Meja Makan.")
