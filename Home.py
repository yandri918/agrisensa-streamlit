# AgriSensa Command Center - Professional Dashboard
# Modern UI with Glassmorphism and Advanced Navigation

import streamlit as st
from datetime import datetime

# Auth import
from utils.auth import is_authenticated, login, logout, get_current_user, show_user_info_sidebar

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


# ========== TRANSLATION DICTIONARY ==========
TRANSLATIONS = {
    "ID": {
        "hero_title": "AgriSensa Intelligence",
        "hero_subtitle": "Superapp Pertanian Modern yang mengintegrasikan IoT, Analisis Satelit, dan Kecerdasan Buatan untuk revolusi ketahanan pangan.",
        "badges": ["🚀 v4.0.0 (Dec 2025)", "⚡ AI Powered", "🌍 Enterprise Grade"],
        "section_main": "🛠️ Modul Operasional Utama",
        "section_secondary": "📚 Pusat Pengetahuan & Analisis",
        "cards": {
            "planner": {"title": "Harvest Planner", "desc": "Perencanaan panen berbasis AI, cuaca, dan target profitabilitas presisi.", "btn": "Buka Planner"},
            "vision": {"title": "AgriSensa Vision", "desc": "Diagnosis hama & penyakit tanaman instan menggunakan kamera HP/Drone.", "btn": "Mulai Scan"},
            "gis": {"title": "GIS Intelligence", "desc": "Pemetaan lahan interaktif, kesesuaian tanah, dan analisis topografi.", "btn": "Buka Peta"},
            "climate": {"title": "Smart Climate", "desc": "Prediksi cuaca mikro real-time untuk penjadwalan pertanian yang akurat.", "btn": "Cek Cuaca"}
        },
        "groups": {
            "nutrition": {"title": "💊 Manajemen Nutrisi", "sub": "Kalkulator Pupuk, Analisis NPK, Katalog Harga", "btn": "Akses Modul Pupuk"},
            "protection": {"title": "🛡️ Proteksi Tanaman", "sub": "Pestisida Nabati, Bahan Aktif, Dokter Tanaman", "btn": "Cek Hama & Penyakit"},
            "business": {"title": "📈 Bisnis & Riset", "sub": "Analisis Usaha Tani, Statistik Penelitian", "btn": "Analisis Profit (RAB)"}
        },
        "tip": "💡 **Tip Hari Ini:** Gunakan fitur *AgriSensa Vision* di pagi hari untuk pencahayaan terbaik.",
        "status": "System Status: 🟢 Online"
    },
    "EN": {
        "hero_title": "AgriSensa Intelligence",
        "hero_subtitle": "Modern Agriculture Superapp integrating IoT, Satellite Analysis, and Artificial Intelligence for food security revolution.",
        "badges": ["🚀 v4.0.0 (Dec 2025)", "⚡ AI Powered", "🌍 Enterprise Grade"],
        "section_main": "🛠️ Core Operational Modules",
        "section_secondary": "📚 Knowledge & Analysis Center",
        "cards": {
            "planner": {"title": "Harvest Planner", "desc": "AI-based harvest planning, weather integration, and precision profitability targets.", "btn": "Open Planner"},
            "vision": {"title": "AgriSensa Vision", "desc": "Instant pest & disease diagnosis using Mobile Camera/Drone.", "btn": "Start Scan"},
            "gis": {"title": "GIS Intelligence", "desc": "Interactive land mapping, soil suitability, and topographic analysis.", "btn": "Open Map"},
            "climate": {"title": "Smart Climate", "desc": "Real-time micro-weather prediction for accurate agricultural scheduling.", "btn": "Check Weather"}
        },
        "groups": {
            "nutrition": {"title": "💊 Nutrition Management", "sub": "Fertilizer Calculator, NPK Analysis, Price Catalog", "btn": "Access Fertilizer Module"},
            "protection": {"title": "🛡️ Plant Protection", "sub": "Botanical Pesticides, Active Ingredients, AI Plant Doctor", "btn": "Check Pests & Diseases"},
            "business": {"title": "📈 Business & Research", "sub": "Farm Business Analysis, Research Statistics", "btn": "Profit Analysis (RAB)"}
        },
        "tip": "💡 **Tip of the Day:** Use *AgriSensa Vision* in the morning for best lighting conditions.",
        "status": "System Status: 🟢 Online"
    }
}

def show_login_page():
    """Show beautiful login page."""
    st.markdown("""
    <style>
        .login-hero {
            text-align: center;
            padding: 3rem 2rem;
            background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
            border-radius: 24px;
            margin-bottom: 2rem;
        }
        .login-title {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
    </style>
    <div class="login-hero">
        <div class="login-title">🌾 AgriSensa</div>
        <p style="color: #065f46; margin-top: 0.5rem;">Smart Agriculture Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login untuk Akses Penuh")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="admin / demo / petani")
            password = st.text_input("🔑 Password", type="password", placeholder="••••••••")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_btn = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            with col_btn2:
                st.form_submit_button("📝 Daftar Baru", use_container_width=True, disabled=True)
            
            if login_btn:
                if username and password:
                    success, message = login(username, password)
                    if success:
                        st.success(message)
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("Masukkan username dan password")
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.85rem;">
            <strong>Demo Accounts:</strong><br>
            👨‍💼 admin / admin123<br>
            👤 demo / demo123<br>
            👨‍🌾 petani / petani123
        </div>
        """, unsafe_allow_html=True)
        
        # Features preview
        st.markdown("---")
        st.markdown("#### ✨ Fitur Premium AgriSensa")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("✅ 55+ Modul Pertanian")
            st.markdown("✅ AI Plant Doctor")
            st.markdown("✅ GIS & Pemetaan")
        with col_f2:
            st.markdown("✅ Analisis Cuaca")
            st.markdown("✅ Kalkulator Pupuk")
            st.markdown("✅ Database Lengkap")


def main():
    # === CHECK AUTHENTICATION ===
    if not is_authenticated():
        show_login_page()
        return
    
    # === SHOW USER INFO IN SIDEBAR ===
    show_user_info_sidebar()
    
    # === LANGUAGE SELECTOR ===
    lang_code = st.sidebar.selectbox("🌐 Language / Bahasa", ["Bahasa Indonesia", "English"], index=0)
    lang = "ID" if lang_code == "Bahasa Indonesia" else "EN"
    
    T = TRANSLATIONS[lang]


    # === HERO SECTION ===
    st.markdown(f"""
        <div class="hero-container" style="display: flex; flex-direction: column; align-items: center; text-align: center; justify-content: center;">
            <div style="margin-bottom: 1rem; display: flex; justify-content: center; gap: 10px;">
                <span class="metric-badge">{T['badges'][0]}</span>
                <span class="metric-badge">{T['badges'][1]}</span>
                <span class="metric-badge">{T['badges'][2]}</span>
            </div>
            <h1 class="hero-title" style="text-align: center; margin: 0 auto; width: 100%;">{T['hero_title']}</h1>
            <p class="hero-subtitle" style="text-align: center; margin: 10px auto; width: 80%; display: block;">
                {T['hero_subtitle']}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # === QUICK ACTIONS GRID ===
    st.subheader(T['section_main'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🎯</div>
            <div class="card-title">{T['cards']['planner']['title']}</div>
            <div class="card-desc">{T['cards']['planner']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['planner']['btn'], key="btn_planner", use_container_width=True):
            st.switch_page("pages/16_🎯_Perencana_Panen_AI.py")

    with col2:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🛸</div>
            <div class="card-title">{T['cards']['vision']['title']}</div>
            <div class="card-desc">{T['cards']['vision']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['vision']['btn'], key="btn_vision", use_container_width=True):
            st.switch_page("pages/31_🛸_AgriSensa_Vision.py")

    with col3:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🗺️</div>
            <div class="card-title">{T['cards']['gis']['title']}</div>
            <div class="card-desc">{T['cards']['gis']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['gis']['btn'], key="btn_gis", use_container_width=True):
            st.switch_page("pages/29_🛰️_AgriSensa_GIS.py")
            
    with col4:
        st.markdown(f"""
        <div class="glass-card">
            <div class="card-icon">🌤️</div>
            <div class="card-title">{T['cards']['climate']['title']}</div>
            <div class="card-desc">{T['cards']['climate']['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(T['cards']['climate']['btn'], key="btn_weather", use_container_width=True):
             st.switch_page("pages/27_🌤️_Cuaca_Pertanian.py")

    # === SECONDARY FEATURES ===
    st.markdown("---")
    st.subheader(T['section_secondary'])
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        with st.container(border=True):
            st.markdown(f"### {T['groups']['nutrition']['title']}")
            st.caption(T['groups']['nutrition']['sub'])
            if st.button(T['groups']['nutrition']['btn'], use_container_width=True):
                 st.switch_page("pages/3_🧮_Kalkulator_Pupuk.py")
            st.markdown("- [Katalog Pupuk & Harga](pages/25_🧪_Katalog_Pupuk_Harga.py)")
            st.markdown("- [Rekomendasi Terpadu](pages/14_🎯_Rekomendasi_Terpadu.py)")

    with c2:
        with st.container(border=True):
            st.markdown(f"### {T['groups']['protection']['title']}")
            st.caption(T['groups']['protection']['sub'])
            if st.button(T['groups']['protection']['btn'], use_container_width=True):
                 st.switch_page("pages/19_🐛_Panduan_Hama_Penyakit.py")
            st.markdown("- [Direktori Bahan Aktif](pages/26_🔬_Direktori_Bahan_Aktif.py)")
            st.markdown("- [Resep Pestisida Nabati](pages/18_🌿_Pestisida_Nabati.py)")

    with c3:
        with st.container(border=True):
            st.markdown(f"### {T['groups']['business']['title']}")
            st.caption(T['groups']['business']['sub'])
            if st.button(T['groups']['business']['btn'], use_container_width=True):
                 st.switch_page("pages/28_💰_Analisis_Usaha_Tani.py")
            st.markdown("- [Asisten Penelitian AI](pages/12_🔬_Asisten_Penelitian.py)")
            st.markdown("- [Prediksi Tren Harga](pages/6_📈_Analisis_Tren_Harga.py)")

    # === SYSTEM STATUS ===
    st.markdown("---")
    col_stat1, col_stat2 = st.columns([3, 1])
    
    with col_stat1:
        st.info(T['tip'])
        
    with col_stat2:
        st.markdown(f"""
        <div style="text-align: right; color: #9ca3af; font-size: 0.8rem;">
            {T['status']}<br>
            Server Time: {datetime.now().strftime('%H:%M WIB')}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
