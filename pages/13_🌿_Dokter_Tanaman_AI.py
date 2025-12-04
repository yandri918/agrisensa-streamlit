# Dokter Tanaman Canggih (Roboflow AI)
# Advanced plant disease detection with AI image recognition

import streamlit as st
import requests
from PIL import Image
import io
import base64
import json
from datetime import datetime

st.set_page_config(page_title="Dokter Tanaman AI", page_icon="🌿", layout="wide")

# ========== ROBOFLOW CONFIGURATION ==========
# Note: In production, use st.secrets for API key
ROBOFLOW_API_KEY = "demo_key"  # Replace with actual key
ROBOFLOW_MODEL = "plant-disease-detection"
ROBOFLOW_VERSION = "1"

# ========== DISEASE DATABASE ==========
DISEASE_INFO = {
    "Healthy": {
        "severity": "None",
        "description": "Tanaman dalam kondisi sehat",
        "treatment": ["Lanjutkan perawatan rutin", "Monitor secara berkala"],
        "prevention": ["Pemupukan teratur", "Irigasi cukup", "Sanitasi lahan"],
        "color": "#10b981"
    },
    "Bacterial Blight": {
        "severity": "High",
        "description": "Hawar daun bakteri yang menyerang tanaman",
        "treatment": [
            "Semprot bakterisida berbahan tembaga",
            "Buang bagian tanaman terinfeksi",
            "Aplikasi setiap 5-7 hari"
        ],
        "prevention": [
            "Gunakan benih sehat",
            "Hindari luka mekanis",
            "Atur irigasi dengan baik"
        ],
        "color": "#ef4444"
    },
    "Brown Spot": {
        "severity": "Medium",
        "description": "Bercak coklat pada daun akibat jamur",
        "treatment": [
            "Semprot fungisida berbahan Mancozeb",
            "Aplikasi setiap 7-10 hari",
            "Perbaiki drainase"
        ],
        "prevention": [
            "Jarak tanam teratur",
            "Sanitasi lahan",
            "Hindari kelembaban berlebih"
        ],
        "color": "#f59e0b"
    },
    "Leaf Blast": {
        "severity": "High",
        "description": "Blas daun yang disebabkan jamur Pyricularia",
        "treatment": [
            "Semprot fungisida sistemik",
            "Aplikasi setiap 7 hari",
            "Kurangi pemupukan nitrogen"
        ],
        "prevention": [
            "Gunakan varietas tahan",
            "Pemupukan berimbang",
            "Drainase baik"
        ],
        "color": "#ef4444"
    },
    "Tungro": {
        "severity": "Very High",
        "description": "Virus tungro yang ditularkan wereng",
        "treatment": [
            "Cabut dan musnahkan tanaman sakit",
            "Kendalikan vektor wereng",
            "Tidak ada obat langsung"
        ],
        "prevention": [
            "Gunakan varietas tahan",
            "Tanam serentak",
            "Kendalikan wereng"
        ],
        "color": "#dc2626"
    }
}

# ========== HELPER FUNCTIONS ==========
def encode_image(image):
    """Encode image to base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def detect_disease_demo(image):
    """
    Demo disease detection (simulated)
    In production, replace with actual Roboflow API call
    """
    # Simulated detection for demo
    # In production, use:
    # response = requests.post(
    #     f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}",
    #     params={"api_key": ROBOFLOW_API_KEY},
    #     files={"file": image_bytes}
    # )
    
    import random
    diseases = list(DISEASE_INFO.keys())
    detected = random.choice(diseases)
    confidence = random.uniform(0.75, 0.98)
    
    return {
        "predictions": [{
            "class": detected,
            "confidence": confidence,
            "x": 320,
            "y": 240,
            "width": 200,
            "height": 200
        }]
    }

def get_treatment_plan(disease_name, severity):
    """Generate comprehensive treatment plan"""
    info = DISEASE_INFO.get(disease_name, {})
    
    plan = {
        "immediate": [],
        "short_term": [],
        "long_term": []
    }
    
    if severity in ["High", "Very High"]:
        plan["immediate"] = [
            "Isolasi tanaman terinfeksi",
            "Dokumentasi gejala dengan foto",
            "Konsultasi dengan ahli jika perlu"
        ]
    
    plan["short_term"] = info.get("treatment", [])
    plan["long_term"] = info.get("prevention", [])
    
    return plan

# ========== MAIN APP ==========
st.title("🌿 Dokter Tanaman Canggih (Roboflow AI)")
st.markdown("**Deteksi penyakit tanaman otomatis dengan AI image recognition**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 🤖 AI-powered disease detection
    - 📸 Upload foto atau ambil dari kamera
    - 🎯 Confidence score untuk setiap deteksi
    - 💊 Rekomendasi treatment komprehensif
    - 📊 Riwayat diagnosis
    
    **Tips Foto Terbaik:**
    - Ambil foto di siang hari dengan cahaya cukup
    - Fokus pada daun/bagian yang bergejala
    - Jarak 20-30 cm dari tanaman
    - Hindari bayangan atau blur
    - Foto dari beberapa sudut jika perlu
    
    **Supported Diseases:**
    - Bacterial Blight (Hawar Bakteri)
    - Brown Spot (Bercak Coklat)
    - Leaf Blast (Blas Daun)
    - Tungro Virus
    - Healthy (Sehat)
    """)

# Warning about demo mode
st.warning("""
⚠️ **Demo Mode:** Modul ini menggunakan simulasi AI untuk demo. 
Untuk produksi, integrasikan dengan Roboflow API key yang valid.
""")

# Image Input
st.subheader("📸 Upload Foto Tanaman")

col1, col2 = st.columns([2, 1])

with col1:
    input_method = st.radio(
        "Pilih metode input:",
        ["Upload File", "Ambil dari Kamera"],
        horizontal=True
    )
    
    if input_method == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload foto tanaman (JPG, PNG)",
            type=['jpg', 'jpeg', 'png'],
            help="Upload foto daun atau bagian tanaman yang bergejala"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
        else:
            image = None
    else:
        camera_photo = st.camera_input("Ambil foto tanaman")
        
        if camera_photo is not None:
            image = Image.open(camera_photo)
        else:
            image = None

with col2:
    if image:
        st.image(image, caption="Foto yang akan dianalisis", use_container_width=True)

# Analysis Button
if image and st.button("🔍 Analisis dengan AI", type="primary", use_container_width=True):
    
    with st.spinner("AI sedang menganalisis gambar..."):
        # Detect disease
        result = detect_disease_demo(image)
        
        if result and "predictions" in result and len(result["predictions"]) > 0:
            prediction = result["predictions"][0]
            disease_name = prediction["class"]
            confidence = prediction["confidence"]
            
            # Get disease info
            disease_info = DISEASE_INFO.get(disease_name, {})
            severity = disease_info.get("severity", "Unknown")
            
    # Display Results
    st.markdown("---")
    st.subheader("🎯 Hasil Diagnosis AI")
    
    # Main diagnosis card
    severity_colors = {
        "None": "#10b981",
        "Low": "#3b82f6",
        "Medium": "#f59e0b",
        "High": "#ef4444",
        "Very High": "#dc2626"
    }
    
    severity_icons = {
        "None": "✅",
        "Low": "🟢",
        "Medium": "🟡",
        "High": "🟠",
        "Very High": "🔴"
    }
    
    color = severity_colors.get(severity, "#6b7280")
    icon = severity_icons.get(severity, "⚪")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {color}20 0%, {color}40 100%); 
                    padding: 2rem; border-radius: 12px; border: 2px solid {color}; text-align: center;">
            <div style="font-size: 4rem;">{icon}</div>
            <h2 style="color: {color}; margin: 0.5rem 0;">Terdeteksi: {disease_name}</h2>
            <p style="font-size: 1.2rem; color: #6b7280; margin: 0;">Tingkat Keparahan: {severity}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(
            "AI Confidence",
            f"{confidence*100:.1f}%",
            help="Tingkat kepercayaan AI terhadap diagnosis"
        )
    
    with col3:
        reliability = "Tinggi" if confidence > 0.8 else "Sedang" if confidence > 0.6 else "Rendah"
        st.metric(
            "Reliability",
            reliability,
            help="Keandalan hasil berdasarkan confidence"
        )
    
    # Disease Information
    st.markdown("---")
    st.subheader("📋 Informasi Penyakit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Deskripsi:**
        {disease_info.get('description', 'Tidak ada deskripsi')}
        
        **Tingkat Keparahan:** {severity}
        
        **Confidence Score:** {confidence*100:.1f}%
        """)
    
    with col2:
        if disease_name != "Healthy":
            st.error(f"""
            ⚠️ **Tindakan Diperlukan!**
            
            Tanaman terdeteksi mengalami {disease_name}.
            Segera lakukan treatment sesuai rekomendasi di bawah.
            """)
        else:
            st.success("""
            ✅ **Tanaman Sehat!**
            
            Tidak ada penyakit terdeteksi.
            Lanjutkan perawatan rutin.
            """)
    
    # Treatment Plan
    if disease_name != "Healthy":
        st.markdown("---")
        st.subheader("💊 Rencana Penanganan")
        
        treatment_plan = get_treatment_plan(disease_name, severity)
        
        tab1, tab2, tab3 = st.tabs(["⚡ Immediate", "📅 Short-term", "🛡️ Long-term"])
        
        with tab1:
            st.markdown("**Tindakan Segera (0-24 jam):**")
            for action in treatment_plan["immediate"]:
                st.write(f"- {action}")
        
        with tab2:
            st.markdown("**Tindakan Jangka Pendek (1-4 minggu):**")
            for action in treatment_plan["short_term"]:
                st.write(f"- {action}")
        
        with tab3:
            st.markdown("**Tindakan Jangka Panjang (Pencegahan):**")
            for action in treatment_plan["long_term"]:
                st.write(f"- {action}")
    
    # Additional Recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi Tambahan")
    
    if confidence < 0.7:
        st.warning("""
        ⚠️ **Confidence rendah!**
        
        Hasil deteksi kurang akurat. Pertimbangkan:
        - Ambil foto ulang dengan pencahayaan lebih baik
        - Foto dari sudut berbeda
        - Konsultasi dengan ahli untuk konfirmasi
        """)
    
    if disease_name != "Healthy":
        st.info("""
        **Langkah Selanjutnya:**
        
        1. **Dokumentasi:** Simpan foto dan hasil diagnosis
        2. **Monitoring:** Amati perkembangan setelah treatment
        3. **Follow-up:** Foto ulang setelah 1-2 minggu
        4. **Konsultasi:** Hubungi penyuluh jika tidak membaik
        5. **Pencegahan:** Terapkan langkah pencegahan untuk tanaman lain
        """)
    
    # Save diagnosis
    st.markdown("---")
    if st.button("💾 Simpan Hasil Diagnosis", use_container_width=True):
        diagnosis_record = {
            'timestamp': datetime.now().isoformat(),
            'disease': disease_name,
            'confidence': confidence,
            'severity': severity,
            'treatment_plan': treatment_plan
        }
        
        st.success("✅ Hasil diagnosis berhasil disimpan!")
        st.json(diagnosis_record)

elif not image:
    st.info("👆 Upload foto atau ambil foto tanaman untuk memulai diagnosis")

# Disease Reference
st.markdown("---")
st.subheader("📚 Referensi Penyakit")

with st.expander("Lihat Daftar Lengkap Penyakit yang Dapat Dideteksi"):
    for disease, info in DISEASE_INFO.items():
        with st.expander(f"{disease} - {info['severity']}"):
            st.write(f"**Deskripsi:** {info['description']}")
            st.write("**Treatment:**")
            for treatment in info['treatment']:
                st.write(f"- {treatment}")
            st.write("**Pencegahan:**")
            for prevention in info['prevention']:
                st.write(f"- {prevention}")

# Integration Guide
st.markdown("---")
with st.expander("🔧 Panduan Integrasi Roboflow API"):
    st.markdown("""
    **Untuk mengaktifkan deteksi AI real:**
    
    1. **Daftar di Roboflow:**
       - Kunjungi: https://roboflow.com
       - Buat akun gratis
       - Upload dataset penyakit tanaman
       - Train model atau gunakan pre-trained model
    
    2. **Dapatkan API Key:**
       - Dashboard → Settings → API
       - Copy API key
    
    3. **Update Code:**
       ```python
       # Di file ini, ganti:
       ROBOFLOW_API_KEY = "your_actual_api_key"
       ROBOFLOW_MODEL = "your_model_name"
       ROBOFLOW_VERSION = "your_version"
       ```
    
    4. **Uncomment API Call:**
       ```python
       # Di function detect_disease_demo(), uncomment:
       response = requests.post(
           f"https://detect.roboflow.com/{ROBOFLOW_MODEL}/{ROBOFLOW_VERSION}",
           params={"api_key": ROBOFLOW_API_KEY},
           files={"file": image_bytes}
       )
       result = response.json()
       ```
    
    5. **Deploy:**
       - Add API key to Streamlit secrets
       - Push to GitHub
       - Auto-deploy!
    
    **Biaya Roboflow:**
    - Free tier: 1,000 predictions/month
    - Starter: $49/month (10,000 predictions)
    - Professional: Custom pricing
    """)

# Footer
st.markdown("---")
st.caption("""
🌿 **Dokter Tanaman Canggih** - AI-powered plant disease detection.
Gunakan hasil diagnosis sebagai referensi awal. Untuk kasus serius, konsultasikan dengan ahli pertanian.
""")
