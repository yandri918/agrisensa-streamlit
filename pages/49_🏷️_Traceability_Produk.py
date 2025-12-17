
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

# Custom CSS with Print Styles
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
    
    /* Print Styles */
    @media print {
        .stApp > header, .main-header, .stTabs, button, .stDownloadButton {
            display: none !important;
        }
        .printable-label {
            page-break-after: always;
            margin: 0;
            padding: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🏷️ AgriPass (Traceability)</h1><p>Paspor Digital Produk Premium & Generator QR Code</p></div>', unsafe_allow_html=True)

# SESSION STATE Init
if 'batch_data' not in st.session_state:
    st.session_state['batch_data'] = {}

# ===== HELPER FUNCTIONS =====

def generate_printable_label(data, size="medium", qr_img=None):
    """
    Generate print-ready label image with professional layout
    Args:
        data: batch data dictionary
        size: "small" (5x5cm), "medium" (10x10cm), "large" (15x10cm)
        qr_img: PIL Image of QR code
    Returns:
        PIL Image object
    """
    # Size mapping at 300 DPI for print quality
    sizes = {
        "small": (590, 590),      # 5x5 cm
        "medium": (1181, 1181),   # 10x10 cm
        "large": (1772, 1181)     # 15x10 cm
    }
    
    width, height = sizes[size]
    
    # Create blank canvas
    label = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(label)
    
    # Try to load fonts, fallback to default if not available
    try:
        font_title = ImageFont.truetype("arial.ttf", 60)
        font_subtitle = ImageFont.truetype("arial.ttf", 40)
        font_body = ImageFont.truetype("arial.ttf", 35)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Colors
    color_primary = (15, 118, 110)  # Teal
    color_text = (0, 0, 0)
    color_gray = (100, 100, 100)
    
    # Layout positions
    margin = 40
    y_pos = margin
    
    # Draw border
    draw.rectangle([(10, 10), (width-10, height-10)], outline=color_primary, width=5)
    
    # QR Code (top left or center depending on size)
    if qr_img:
        qr_size = 300 if size == "large" else 250
        qr_resized = qr_img.resize((qr_size, qr_size))
        qr_x = margin + 20
        qr_y = y_pos + 20
        label.paste(qr_resized, (qr_x, qr_y))
        
        # Text starts next to QR for large, below for others
        if size == "large":
            text_x = qr_x + qr_size + 40
            text_y = y_pos + 20
        else:
            text_x = margin + 20
            text_y = qr_y + qr_size + 30
    else:
        text_x = margin + 20
        text_y = y_pos
    
    # Product Name (Title)
    draw.text((text_x, text_y), data['produk'][:30], fill=color_primary, font=font_title)
    text_y += 70
    
    # Varietas & Date
    draw.text((text_x, text_y), f"{data['varietas'][:35]}", fill=color_text, font=font_subtitle)
    text_y += 50
    draw.text((text_x, text_y), f"Panen: {data['tgl']}", fill=color_gray, font=font_body)
    text_y += 60
    
    # Farmer & Location
    draw.text((text_x, text_y), f"Petani: {data['petani'][:30]}", fill=color_text, font=font_body)
    text_y += 45
    draw.text((text_x, text_y), f"Lokasi: {data['lokasi'][:35]}", fill=color_text, font=font_body)
    text_y += 60
    
    # Price (if available)
    if data.get('harga'):
        draw.text((text_x, text_y), f"💰 Harga: Rp {data['harga']:,}/kg", fill=color_primary, font=font_subtitle)
        text_y += 55
    
    # Contact (if available)
    if data.get('kontak'):
        draw.text((text_x, text_y), f"📞 Kontak: {data['kontak']}", fill=color_text, font=font_body)
        text_y += 55
    
    # Quality Badges
    if data.get('klaim'):
        badge_y = text_y
        for badge in data['klaim']:
            draw.rounded_rectangle(
                [(text_x, badge_y), (text_x + 200, badge_y + 40)],
                radius=10,
                fill=(34, 197, 94),  # Green
                outline=None
            )
            draw.text((text_x + 15, badge_y + 8), f"✓ {badge}", fill='white', font=font_small)
            badge_y += 50
        text_y = badge_y + 20
    
    # Batch ID at bottom
    id_y = height - margin - 40
    draw.text((margin + 20, id_y), f"ID: {data['id']}", fill=color_gray, font=font_small)
    
    return label

def pil_to_pdf_bytes(pil_image):
    """Convert PIL Image to PDF bytes"""
    pdf_buffer = io.BytesIO()
    pil_image.save(pdf_buffer, format='PDF', resolution=300.0)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# TABS
tab1, tab2, tab3 = st.tabs(["📝 Input Data Batch (Produksi)", "🖨️ Cetak Label", "📱 Simulasi Scan Konsumen"])

# --- TAB 1: INPUT BATCH ---
with tab1:
    col_in1, col_in2 = st.columns([1, 1])
    
    with col_in1:
        st.subheader("1. Identitas Produk")
        
        # Extended Commodity Options
        opsi_komoditas = [
            "Beras (Pandan Wangi/Rojolele)", "Beras Merah/Hitam", 
            "Kopi Arabika", "Kopi Robusta", "Kakao (Cokelat)",
            "Cabai Rawit", "Cabai Merah", "Bawang Merah", "Bawang Putih",
            "Sayuran Daun (Bayam/Kangkung)", "Selada Hidroponik", "Tomat Cherry",
            "Melon Premium", "Semangka", "Mangga", "Durian", "Alpukat",
            "Telur Ayam Kampung", "Madu Murni", "Ikan Nila", "Ikan Lele",
            "Lainnya (Ketik Manual)..."
        ]
        
        pilihan_awal = st.selectbox("Pilih Komoditas", opsi_komoditas)
        
        if pilihan_awal == "Lainnya (Ketik Manual)...":
            jenis_produk = st.text_input("✍️ Masukkan Nama Komoditas", placeholder="Contoh: Vanili Eksport")
            if not jenis_produk:
                jenis_produk = "Produk Tanpa Nama"
        else:
            jenis_produk = pilihan_awal
        varietas = st.text_input("Varietas / Grade", "Cianjur Pandan Wangi (Grade A)")
        tgl_panen = st.date_input("Tanggal Panen", datetime.date.today())
        
        st.subheader("2. Asal Usul (Origin)")
        nama_petani = st.text_input("Nama Petani / Kelompok", "Gapoktan Sejahtera")
        lokasi_kebun = st.text_input("Lokasi Kebun", "Banyumas, Jawa Tengah")
        
        # Photo Upload
        foto_produk = st.file_uploader("Foto Petani / Kebun (Opsional)", type=['jpg', 'jpeg', 'png'])
        
    with col_in2:
        st.subheader("3. Informasi Komersial")
        
        # Price Input
        harga_produk = st.number_input(
            "💰 Harga per Kg/Unit (Rp)", 
            min_value=0, 
            value=50000, 
            step=1000,
            help="Harga jual produk yang akan ditampilkan di label"
        )
        
        # Contact Input
        kontak_petani = st.text_input(
            "📞 Nomor Kontak (WhatsApp/Telp)",
            placeholder="Contoh: 0812-3456-7890",
            help="Nomor yang bisa dihubungi pembeli"
        )
        
        st.subheader("4. Klaim Kualitas")
        is_organik = st.checkbox("✅ Bebas Pestisida / Organik")
        is_halal = st.checkbox("✅ Halal Certified")
        is_premium = st.checkbox("✅ Kualitas Ekspor (Sortir Ketat)")
        
        # Generator ID
        batch_id = f"AGRI-{tgl_panen.strftime('%Y%m%d')}-{hash(jenis_produk)%1000:03d}"
        
        st.markdown("---")
        if st.button("💾 Simpan & Generate QR Code", type="primary", use_container_width=True):
            st.session_state['batch_data'] = {
                "id": batch_id,
                "produk": jenis_produk,
                "varietas": varietas,
                "tgl": tgl_panen,
                "petani": nama_petani,
                "lokasi": lokasi_kebun,
                "foto": foto_produk,
                "harga": harga_produk if harga_produk > 0 else None,
                "kontak": kontak_petani if kontak_petani else None,
                "klaim": [k for k, v in [("Organik", is_organik), ("Halal", is_halal), ("Premium", is_premium)] if v]
            }
            st.success(f"✅ Batch {batch_id} berhasil dibuat!")
            st.info("📌 Silakan ke tab **'🖨️ Cetak Label'** untuk mencetak label produk Anda!")

# --- TAB 2: PRINT LABEL ---
with tab2:
    st.subheader("🖨️ Generator Label Siap Cetak")
    
    if st.session_state['batch_data']:
        data = st.session_state['batch_data']
        
        # Label Size Selection
        col_size, col_opt = st.columns([1, 2])
        
        with col_size:
            label_size = st.selectbox(
                "Ukuran Label",
                ["small", "medium", "large"],
                index=1,
                format_func=lambda x: {
                    "small": "📦 Kecil (5x5 cm) - Sachet/Kemasan Kecil",
                    "medium": "📋 Sedang (10x10 cm) - Standar Stiker",
                    "large": "📄 Besar (15x10 cm) - Box/Kemasan Besar"
                }[x]
            )
        
        with col_opt:
            st.info("💡 **Tips:** Pilih ukuran sesuai kemasan produk Anda. Label akan digenerate dengan resolusi 300 DPI untuk kualitas cetak terbaik.")
        
        # Generate QR Code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr_content = f"""AgriSensa Verified Product
ID: {data['id']}
Produk: {data['produk']} ({data['varietas']})
Petani: {data['petani']} @ {data['lokasi']}
Panen: {data['tgl']}
Harga: Rp {data.get('harga', 0):,}
Kontak: {data.get('kontak', '-')}
Kualitas: {', '.join(data['klaim'])}
"""
        qr.add_data(qr_content)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        # Generate Printable Label
        label_image = generate_printable_label(data, label_size, img_qr)
        
        # Convert to bytes for display and download
        label_buffer = io.BytesIO()
        label_image.save(label_buffer, format='PNG', dpi=(300, 300))
        label_bytes = label_buffer.getvalue()
        
        # Preview
        st.markdown("---")
        st.caption("🔍 Preview Label:")
        
        col_prev1, col_prev2, col_prev3 = st.columns([1, 2, 1])
        with col_prev2:
            st.image(label_bytes, use_container_width=True)
        
        # Action Buttons
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            st.download_button(
                "⬇️ Download PNG",
                label_bytes,
                f"Label_{data['id']}_{label_size}.png",
                "image/png",
                use_container_width=True
            )
        
        with col_btn2:
            # Generate PDF
            pdf_bytes = pil_to_pdf_bytes(label_image)
            st.download_button(
                "📄 Download PDF",
                pdf_bytes,
                f"Label_{data['id']}_{label_size}.pdf",
                "application/pdf",
                use_container_width=True
            )
        
        with col_btn3:
            # Print button with JavaScript
            if st.button("🖨️ Print Langsung", use_container_width=True):
                # Encode image to base64 for embedding
                img_base64 = base64.b64encode(label_bytes).decode()
                
                # JavaScript to open print dialog
                print_js = f"""
                <script>
                    function printLabel() {{
                        var printWindow = window.open('', '', 'height=800,width=800');
                        printWindow.document.write('<html><head><title>Print Label</title>');
                        printWindow.document.write('<style>@media print {{ @page {{ margin: 0; }} body {{ margin: 0; }} }}</style>');
                        printWindow.document.write('</head><body>');
                        printWindow.document.write('<img src="data:image/png;base64,{img_base64}" style="width:100%; height:auto;">');
                        printWindow.document.write('</body></html>');
                        printWindow.document.close();
                        printWindow.focus();
                        setTimeout(function() {{ printWindow.print(); }}, 250);
                    }}
                    printLabel();
                </script>
                """
                st.components.v1.html(print_js, height=0)
                st.success("✅ Dialog print akan muncul. Pastikan printer Anda sudah siap!")
        
        st.markdown("---")
        st.success("✅ **Label siap cetak!** Gunakan kertas stiker atau print di kertas biasa lalu tempel dengan lem.")
        
    else:
        st.warning("⚠️ Belum ada data batch. Silakan input data di **Tab 1** terlebih dahulu.")

# --- TAB 3: CONSUMER VIEW ---
with tab3:
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
                """ + (f"<div style='text-align:center; margin:10px;'><img src='data:image/png;base64,{base64.b64encode(data['foto'].getvalue()).decode()}' style='max-width:100%; border-radius:10px;'></div>" if data.get('foto') else "") + """
                
                <div style='background:#f0fdfa; padding:15px; border-radius:10px; margin: 15px 0;'>
                    <p><b>📦 Batch ID:</b> <br>""" + data['id'] + """</p>
                    <p><b>🗓️ Tanggal Panen:</b> <br>""" + str(data['tgl']) + """</p>
                    <p><b>📍 Lokasi:</b> <br>""" + data['lokasi'] + """</p>
                    """ + (f"<p><b>💰 Harga:</b> <br>Rp {data['harga']:,}/kg</p>" if data.get('harga') else "") + """
                    """ + (f"<p><b>📞 Kontak Petani:</b> <br>{data['kontak']}</p>" if data.get('kontak') else "") + """
                </div>
                
                <p><b>Cerita Petani:</b></p>
                <p style='font-style:italic; font-size:0.9rem;'>
                    "Produk ini dirawat dengan sepenuh hati oleh """ + data['petani'] + """. 
                    Kami menggunakan metode berkelanjutan untuk menjaga alam tetap lestari."
                </p>
                
                <div style='text-align:center; margin-top:20px;'>
                    <button style='background:#0f766e; color:white; border:none; padding:10px 20px; border-radius:50px; width:100%;'>""" + (f"Beli Lagi - Rp {data['harga']:,}" if data.get('harga') else "Beli Lagi (Order)") + """</button>
                </div>
                 <div style='text-align:center; margin-top:10px;'>
                    <a href='""" + (f"https://wa.me/{data['kontak'].replace('-', '').replace(' ', '')}" if data.get('kontak') else "#") + """'>💬 Hubungi Petani</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Belum ada data batch yang dibuat. Silakan input di Tab 1 dulu.")

# Footer
st.markdown("---")
st.caption("AgriSensa Traceability - Membangun Kepercayaan dari Kebun ke Meja Makan.")
