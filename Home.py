# AgriSensa Streamlit - Multipage App
# Main entry point

import streamlit as st

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="AgriSensa - Platform Pertanian Cerdas",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/agrisensa',
        'Report a bug': "https://github.com/agrisensa/issues",
        'About': "# AgriSensa\nPlatform Pertanian Cerdas berbasis AI & Data Science"
    }
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #10b981;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(5, 150, 105, 0.2);
    }
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #059669;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        color: #6b7280;
        line-height: 1.6;
    }
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #059669;
    }
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN PAGE ==========
def main():
    # Header
    st.markdown('<h1 class="main-header">🌾 AgriSensa</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Platform Pertanian Cerdas - Kalkulator, Analisis & Visualisasi Data</p>', unsafe_allow_html=True)
    
    # Welcome message
    st.info("👋 **Selamat datang di AgriSensa Streamlit!** Pilih modul di sidebar untuk memulai.")
    
    # Statistics
    st.markdown("---")
    st.subheader("📊 Statistik Platform")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">27</div>
            <div class="stat-label">Modul Tersedia</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">100%</div>
            <div class="stat-label">Gratis</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Akses</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-value">∞</div>
            <div class="stat-label">Data Storage</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features
    st.markdown("---")
    st.subheader("🎯 Fitur Utama")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌾</div>
            <div class="feature-title">Database Panen</div>
            <div class="feature-desc">
                Catat dan analisis data hasil panen dengan visualisasi interaktif.
                Tracking profitabilitas, ROI, dan tren bulanan.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧮</div>
            <div class="feature-title">Kalkulator Pupuk</div>
            <div class="feature-desc">
                Hitung kebutuhan pupuk NPK berdasarkan luas lahan, jenis tanaman,
                dan kondisi tanah. Rekomendasi dosis yang tepat.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Analisis Tren Harga</div>
            <div class="feature-desc">
                Prediksi harga komoditas dengan machine learning.
                Visualisasi tren dan forecasting 30 hari ke depan.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🗺️</div>
            <div class="feature-title">Peta Data Tanah</div>
            <div class="feature-desc">
                Pemetaan lahan interaktif dengan data NPK, cuaca real-time,
                dan analisis kesesuaian tanaman.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Analisis NPK</div>
            <div class="feature-desc">
                Input dan analisis data NPK tanah. Rekomendasi pupuk otomatis
                berdasarkan kekurangan nutrisi.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔄</div>
            <div class="feature-title">Konversi Pupuk</div>
            <div class="feature-desc">
                Konversi kebutuhan pupuk dari kg ke jumlah karung.
                Support berbagai jenis dan ukuran kemasan pupuk.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌤️</div>
            <div class="feature-title">Cuaca Pertanian</div>
            <div class="feature-desc">
                Informasi cuaca real-time dengan peta interaktif, forecast 5 hari,
                dan rekomendasi aktivitas pertanian berdasarkan kondisi cuaca.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # How to use
    st.markdown("---")
    st.subheader("📖 Cara Menggunakan")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **1️⃣ Pilih Modul**
        
        Gunakan sidebar di kiri untuk memilih modul yang ingin digunakan.
        """)
    with col2:
        st.markdown("""
        **2️⃣ Input Data**
        
        Isi form dengan data yang diperlukan. Semua field memiliki panduan.
        """)
    with col3:
        st.markdown("""
        **3️⃣ Lihat Hasil**
        
        Hasil akan ditampilkan secara real-time dengan visualisasi interaktif.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem 0;">
        <p><strong>AgriSensa Streamlit v1.0</strong></p>
        <p>Platform Pertanian Cerdas berbasis AI & Data Science</p>
        <p>© 2024 AgriSensa. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
