
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
    Generate print-ready label image with MODERN PREMIUM layout
    Args:
        data: batch data dictionary
        size: "small" (5x5cm), "medium" (10x10cm), "large" (15x10cm)
        qr_img: PIL Image of QR code
    Returns:
        PIL Image object
    """
    # Size mapping at 300 DPI for print quality
    # Format: (width, height)
    sizes = {
        # Square/Portrait formats
        "small": (590, 590),          # 5x5 cm
        "medium": (1181, 1181),       # 10x10 cm
        "large": (1772, 1181),        # 15x10 cm
        
        # Landscape formats (RECOMMENDED for products)
        "small_landscape": (1181, 590),      # 10x5 cm - compact
        "medium_landscape": (1772, 1181),    # 15x10 cm - standard
        "large_landscape": (2362, 1181),     # 20x10 cm - premium
    }
    
    width, height = sizes[size]
    is_landscape = "landscape" in size
    
    # Create blank canvas with gradient background
    label = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(label)
    
    # === MODERN GRADIENT BACKGROUND ===
    # Create subtle gradient from light teal to white
    for i in range(height):
        # Gradient from top (light teal) to bottom (white)
        ratio = i / height
        r = int(240 + (255 - 240) * ratio)
        g = int(253 + (255 - 253) * ratio)
        b = int(250 + (255 - 250) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    
    # Try to load fonts with better sizes for hierarchy
    try:
        font_brand = ImageFont.truetype("arialbd.ttf", 45)      # Brand/header
        font_title = ImageFont.truetype("arialbd.ttf", 70)      # Product name (bold)
        font_subtitle = ImageFont.truetype("arial.ttf", 42)     # Varietas
        font_body = ImageFont.truetype("arial.ttf", 38)         # Body text
        font_small = ImageFont.truetype("arial.ttf", 32)        # Small text
        font_tiny = ImageFont.truetype("arial.ttf", 28)         # Tiny text
    except:
        font_brand = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # === MODERN COLOR PALETTE ===
    color_primary = (16, 185, 129)      # Emerald-500
    color_primary_dark = (5, 150, 105)  # Emerald-600
    color_accent = (251, 191, 36)       # Amber-400
    color_text = (31, 41, 55)           # Gray-800
    color_text_light = (107, 114, 128)  # Gray-500
    color_white = (255, 255, 255)
    color_badge_organic = (34, 197, 94)     # Green-500
    color_badge_halal = (59, 130, 246)      # Blue-500
    color_badge_premium = (168, 85, 247)    # Purple-500
    
    margin = 50
    
    # === HEADER CARD (Top Banner) ===
    header_height = 100
    # Draw header with gradient
    for i in range(header_height):
        ratio = i / header_height
        r = int(16 + (5 - 16) * ratio)
        g = int(185 + (150 - 185) * ratio)
        b = int(129 + (105 - 129) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    
    # AgriSensa branding in header
    draw.text((margin, 30), "🌾 AgriSensa Verified", fill=color_white, font=font_brand)
    
    # === MAIN CONTENT CARD ===
    card_top = header_height + 20
    card_margin = 30
    
    # White card with shadow effect (multiple rectangles for shadow)
    shadow_offset = 8
    for i in range(shadow_offset, 0, -1):
        alpha = int(20 * (shadow_offset - i) / shadow_offset)
        shadow_color = (200 - alpha, 200 - alpha, 200 - alpha)
        draw.rounded_rectangle(
            [(card_margin + i, card_top + i), (width - card_margin + i, height - 30 + i)],
            radius=25,
            fill=shadow_color
        )
    
    # Main white card
    draw.rounded_rectangle(
        [(card_margin, card_top), (width - card_margin, height - 30)],
        radius=25,
        fill=color_white,
        outline=color_primary,
        width=3
    )
    
    # === LAYOUT: QR CODE + INFO ===
    content_x = card_margin + 40
    content_y = card_top + 40
    
    if qr_img:
        # QR Code with rounded corners effect
        # Adjust QR size based on label orientation
        if is_landscape:
            qr_size = min(280, height - card_top - 100)  # Fit within height
        else:
            qr_size = 280 if "large" in size else 240
        
        qr_resized = qr_img.resize((qr_size, qr_size))
        
        # QR background card
        qr_bg_padding = 15
        draw.rounded_rectangle(
            [(content_x - qr_bg_padding, content_y - qr_bg_padding),
             (content_x + qr_size + qr_bg_padding, content_y + qr_size + qr_bg_padding)],
            radius=20,
            fill=(248, 250, 252),  # Light gray background
            outline=color_primary,
            width=2
        )
        
        label.paste(qr_resized, (content_x, content_y))
        
        # "Scan Me" text below QR
        scan_text_y = content_y + qr_size + 10
        draw.text((content_x + qr_size//2 - 50, scan_text_y), "📱 Scan Me", 
                 fill=color_primary_dark, font=font_small)
        
        # For landscape: always put text to the right of QR
        # For square/portrait: text below QR
        if is_landscape:
            text_x = content_x + qr_size + 50
            text_y = content_y
        else:
            # Original logic for square labels
            if "large" in size and not is_landscape:
                text_x = content_x + qr_size + 50
                text_y = content_y
            else:
                text_x = content_x
                text_y = scan_text_y + 60
    else:
        text_x = content_x
        text_y = content_y
    
    # === PRODUCT INFO ===
    # Product Name (Bold, Large)
    product_name = data['produk'][:28] if len(data['produk']) > 28 else data['produk']
    draw.text((text_x, text_y), product_name, fill=color_text, font=font_title)
    text_y += 85
    
    # Varietas with accent color
    draw.text((text_x, text_y), f"{data['varietas'][:32]}", fill=color_primary_dark, font=font_subtitle)
    text_y += 55
    
    # Divider line
    draw.rectangle([(text_x, text_y), (text_x + 300, text_y + 2)], fill=color_primary)
    text_y += 20
    
    # Date with icon
    draw.text((text_x, text_y), f"📅 {data['tgl']}", fill=color_text_light, font=font_body)
    text_y += 50
    
    # Farmer info
    draw.text((text_x, text_y), f"👨‍🌾 {data['petani'][:28]}", fill=color_text, font=font_body)
    text_y += 45
    
    # Location
    draw.text((text_x, text_y), f"📍 {data['lokasi'][:30]}", fill=color_text, font=font_body)
    text_y += 55
    
    # Price (if available) - HIGHLIGHTED
    if data.get('harga'):
        # Price card
        price_card_y = text_y
        draw.rounded_rectangle(
            [(text_x, price_card_y), (text_x + 350, price_card_y + 55)],
            radius=12,
            fill=color_accent,
            outline=None
        )
        draw.text((text_x + 15, price_card_y + 12), f"💰 Rp {data['harga']:,}/kg", 
                 fill=color_text, font=font_subtitle)
        text_y += 70
    
    # Contact (if available)
    if data.get('kontak'):
        draw.text((text_x, text_y), f"📞 {data['kontak']}", fill=color_text, font=font_body)
        text_y += 55
    
    # === QUALITY BADGES (Modern Pills) ===
    if data.get('klaim'):
        text_y += 10
        badge_colors = {
            'Organik': color_badge_organic,
            'Halal': color_badge_halal,
            'Premium': color_badge_premium
        }
        
        badge_x = text_x
        for badge in data['klaim']:
            badge_color = badge_colors.get(badge, color_primary)
            badge_width = 160
            
            # Modern pill-shaped badge with shadow
            draw.rounded_rectangle(
                [(badge_x + 2, text_y + 2), (badge_x + badge_width + 2, text_y + 47)],
                radius=25,
                fill=(200, 200, 200)  # Shadow
            )
            draw.rounded_rectangle(
                [(badge_x, text_y), (badge_x + badge_width, text_y + 45)],
                radius=25,
                fill=badge_color,
                outline=None
            )
            draw.text((badge_x + 20, text_y + 10), f"✓ {badge}", fill=color_white, font=font_small)
            badge_x += badge_width + 15
    
    # === FOOTER: Batch ID ===
    footer_y = height - 60
    draw.text((margin + 20, footer_y), f"Batch ID: {data['id']}", 
             fill=color_text_light, font=font_tiny)
    
    # Verification badge
    verify_text = "✓ Verified Product"
    draw.text((width - margin - 250, footer_y), verify_text, 
             fill=color_primary, font=font_tiny)
    
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
                "Ukuran & Orientasi Label",
                ["medium_landscape", "large_landscape", "small_landscape", "medium", "large", "small"],
                index=0,  # Default to medium landscape
                format_func=lambda x: {
                    # Landscape (RECOMMENDED)
                    "small_landscape": "🏞️ Landscape Kecil (10x5 cm) ⭐ Compact",
                    "medium_landscape": "🏞️ Landscape Sedang (15x10 cm) ⭐ RECOMMENDED",
                    "large_landscape": "🏞️ Landscape Besar (20x10 cm) ⭐ Premium",
                    # Square/Portrait
                    "small": "⬜ Square Kecil (5x5 cm)",
                    "medium": "⬜ Square Sedang (10x10 cm)",
                    "large": "⬜ Wide (15x10 cm)"
                }[x]
            )
        
        with col_opt:
            if "landscape" in label_size:
                st.success("✅ **Landscape** - Format horizontal lebih cocok untuk kemasan produk!")
            else:
                st.info("💡 **Tip:** Coba format Landscape untuk hasil lebih profesional!")
        
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
            # Build HTML content
            html_content = f"""
            <div style='border: 8px solid #333; border-radius: 20px; padding: 20px; background-color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.2);'>
                <div style='text-align:center;'>
                    <h3 style='color:#0f766e;'>✅ TERVERIFIKASI</h3>
                    <p style='color:grey;'>AgriSensa Blockchain Network</p>
                    <hr>
                    <h1>🌾</h1>
                    <h2>Produk Asli & Aman</h2>
                </div>
            """
            
            # Add photo if available
            if data.get('foto'):
                foto_base64 = base64.b64encode(data['foto'].getvalue()).decode()
                html_content += f"""
                <div style='text-align:center; margin:10px;'>
                    <img src='data:image/png;base64,{foto_base64}' style='max-width:100%; border-radius:10px;'>
                </div>
                """
            
            # Product info card
            html_content += f"""
                <div style='background:#f0fdfa; padding:15px; border-radius:10px; margin: 15px 0;'>
                    <p><b>📦 Batch ID:</b> <br>{data['id']}</p>
                    <p><b>🗓️ Tanggal Panen:</b> <br>{str(data['tgl'])}</p>
                    <p><b>📍 Lokasi:</b> <br>{data['lokasi']}</p>
            """
            
            # Add price if available
            if data.get('harga'):
                html_content += f"                    <p><b>💰 Harga:</b> <br>Rp {data['harga']:,}/kg</p>\n"
            
            # Add contact if available
            if data.get('kontak'):
                html_content += f"                    <p><b>📞 Kontak Petani:</b> <br>{data['kontak']}</p>\n"
            
            html_content += """
                </div>
                
                <p><b>Cerita Petani:</b></p>
                <p style='font-style:italic; font-size:0.9rem;'>
            """
            
            html_content += f'                    "Produk ini dirawat dengan sepenuh hati oleh {data["petani"]}. Kami menggunakan metode berkelanjutan untuk menjaga alam tetap lestari."\n'
            
            html_content += """
                </p>
                
                <div style='text-align:center; margin-top:20px;'>
            """
            
            # Button text
            button_text = f"Beli Lagi - Rp {data['harga']:,}" if data.get('harga') else "Beli Lagi (Order)"
            html_content += f"                    <button style='background:#0f766e; color:white; border:none; padding:10px 20px; border-radius:50px; width:100%;'>{button_text}</button>\n"
            
            html_content += """
                </div>
                <div style='text-align:center; margin-top:10px;'>
            """
            
            # WhatsApp link
            if data.get('kontak'):
                wa_number = data['kontak'].replace('-', '').replace(' ', '').replace('+', '')
                html_content += f"                    <a href='https://wa.me/{wa_number}' target='_blank'>💬 Hubungi Petani</a>\n"
            else:
                html_content += "                    <a href='#'>💬 Hubungi Petani</a>\n"
            
            html_content += """
                </div>
            </div>
            """
            
            st.markdown(html_content, unsafe_allow_html=True)
            
    else:
        st.warning("⚠️ Belum ada data batch yang dibuat. Silakan input di Tab 1 dulu.")

# Footer
st.markdown("---")
st.caption("AgriSensa Traceability - Membangun Kepercayaan dari Kebun ke Meja Makan.")
