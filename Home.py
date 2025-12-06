# AgriSensa Command Center - Professional Dashboard
# Modern UI with Glassmorphism and Advanced Navigation

import streamlit as st
from datetime import datetime

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="AgriSensa Command Center",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/agrisensa',
        'About': "© 2025 AgriSensa Intelligence Systems"
    }
)

# ========== MODERN UI STYLING ==========
st.markdown("""
<style>
    /* GLOBAL THEME */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* BACKGROUND ANIMATION */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgb(16, 185, 129, 0.1) 0%, rgb(0, 0, 0, 0) 40%),
                    radial-gradient(circle at 90% 80%, rgb(5, 150, 105, 0.1) 0%, rgb(0, 0, 0, 0) 40%);
    }

    /* HERO SECTION */
    .hero-container {
        padding: 4rem 2rem;
        text-align: center;
        background: linear-gradient(135deg, rgba(236, 253, 245, 0.8) 0%, rgba(255, 255, 255, 0.4) 100%);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        margin-bottom: 3rem;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-align: center !important;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #4b5563;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        text-align: center !important;
        line-height: 1.6;
    }

    /* GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s ease;
        cursor: default;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.3);
    }
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: #ecfdf5;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #065f46;
        margin-bottom: 0.5rem;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.5;
    }
    
    /* METRICS BADGE */
    .metric-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        background: #ecfdf5;
        border-radius: 50px;
        color: #059669;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # === HERO SECTION ===
    st.markdown("""
        <div class="hero-container">
            <div style="margin-bottom: 1rem;">
                <span class="metric-badge">🚀 v4.0.0 (Dec 2025)</span>
                <span class="metric-badge">⚡ AI Powered</span>
                <span class="metric-badge">🌍 Enterprise Grade</span>
            </div>
            <h1 class="hero-title">AgriSensa Intelligence</h1>
            <p class="hero-subtitle">
                Superapp Pertanian Modern yang mengintegrasikan IoT, Analisis Satelit, 
                dan Kecerdasan Buatan untuk revolusi ketahanan pangan.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # === QUICK ACTIONS GRID ===
    st.subheader("🛠️ Modul Operasional Utama")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🎯</div>
            <div class="card-title">Harvest Planner</div>
            <div class="card-desc">Perencanaan panen berbasis AI, cuaca, dan target profitabilitas presisi.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Planner", key="btn_planner", use_container_width=True):
            st.switch_page("pages/16_🎯_Perencana_Panen_AI.py")

    with col2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🛸</div>
            <div class="card-title">AgriSensa Vision</div>
            <div class="card-desc">Diagnosis hama & penyakit tanaman instan menggunakan kamera HP/Drone.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Mulai Scan", key="btn_vision", use_container_width=True):
            st.switch_page("pages/31_🛸_AgriSensa_Vision.py")

    with col3:
        st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🗺️</div>
            <div class="card-title">GIS Intelligence</div>
            <div class="card-desc">Pemetaan lahan interaktif, kesesuaian tanah, dan analisis topografi.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Peta", key="btn_gis", use_container_width=True):
            st.switch_page("pages/29_🛰️_AgriSensa_GIS.py")
            
    with col4:
        st.markdown("""
        <div class="glass-card">
            <div class="card-icon">🌤️</div>
            <div class="card-title">Smart Climate</div>
            <div class="card-desc">Prediksi cuaca mikro real-time untuk penjadwalan pertanian yang akurat.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Cek Cuaca", key="btn_weather", use_container_width=True):
             st.switch_page("pages/27_🌤️_Cuaca_Pertanian.py")

    # === SECONDARY FEATURES ===
    st.markdown("---")
    st.subheader("📚 Pusat Pengetahuan & Analisis")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.container(border=True):
            st.markdown("### 💊 Manajemen Nutrisi")
            st.caption("Kalkulator Pupuk, Analisis NPK, Katalog Harga")
            if st.button("Akses Modul Pupuk", use_container_width=True):
                 st.switch_page("pages/3_🧮_Kalkulator_Pupuk.py")
            st.markdown("- [Katalog Pupuk & Harga](pages/25_🧪_Katalog_Pupuk_Harga.py)")
            st.markdown("- [Rekomendasi Terpadu](pages/14_🎯_Rekomendasi_Terpadu.py)")

    with c2:
        with st.container(border=True):
            st.markdown("### 🛡️ Proteksi Tanaman")
            st.caption("Pestisida Nabati, Bahan Aktif, Dokter Tanaman")
            if st.button("Cek Hama & Penyakit", use_container_width=True):
                 st.switch_page("pages/19_🐛_Panduan_Hama_Penyakit.py")
            st.markdown("- [Direktori Bahan Aktif](pages/26_🔬_Direktori_Bahan_Aktif.py)")
            st.markdown("- [Resep Pestisida Nabati](pages/18_🌿_Pestisida_Nabati.py)")

    with c3:
        with st.container(border=True):
            st.markdown("### 📈 Bisnis & Riset")
            st.caption("Analisis Usaha Tani, Statistik Penelitian")
            if st.button("Analisis Profit (RAB)", use_container_width=True):
                 st.switch_page("pages/28_💰_Analisis_Usaha_Tani.py")
            st.markdown("- [Asisten Penelitian AI](pages/12_🔬_Asisten_Penelitian.py)")
            st.markdown("- [Prediksi Tren Harga](pages/6_📈_Analisis_Tren_Harga.py)")

    # === SYSTEM STATUS ===
    st.markdown("---")
    col_stat1, col_stat2 = st.columns([3, 1])
    
    with col_stat1:
        st.info("💡 **Tip Hari Ini:** Gunakan fitur *AgriSensa Vision* di pagi hari untuk pencahayaan terbaik saat mendiagnosa penyakit pada daun.")
        
    with col_stat2:
        st.markdown(f"""
        <div style="text-align: right; color: #9ca3af; font-size: 0.8rem;">
            System Status: 🟢 Online<br>
            Server Time: {datetime.now().strftime('%H:%M WIB')}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
