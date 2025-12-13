# Diagnostik Gejala Cerdas
# Interactive plant disease diagnosis with decision tree

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Diagnostik Gejala", page_icon="🔍", layout="wide")

# ========== DISEASE DATABASE ==========
DISEASE_DATABASE = {
    "Blas Padi": {
        "symptoms": ["Bercak coklat pada daun", "Bentuk belah ketupat", "Daun mengering"],
        "causes": "Jamur Pyricularia oryzae",
        "treatment": [
            "Semprot fungisida berbahan aktif Triklorfosmethyl",
            "Aplikasi setiap 7-10 hari",
            "Perbaiki drainase sawah",
            "Kurangi pemupukan nitrogen berlebih"
        ],
        "prevention": [
            "Gunakan varietas tahan",
            "Jarak tanam teratur",
            "Sanitasi lahan"
        ],
        "severity": "Tinggi"
    },
    "Hawar Daun Bakteri": {
        "symptoms": ["Garis kuning di tepi daun", "Daun mengering dari ujung", "Eksudat bakteri"],
        "causes": "Bakteri Xanthomonas oryzae",
        "treatment": [
            "Semprot bakterisida berbahan tembaga",
            "Buang tanaman terinfeksi",
            "Aplikasi setiap 5-7 hari"
        ],
        "prevention": [
            "Gunakan benih sehat",
            "Hindari luka mekanis",
            "Atur irigasi"
        ],
        "severity": "Tinggi"
    },
    "Busuk Batang": {
        "symptoms": ["Batang menghitam", "Tanaman rebah", "Bau busuk"],
        "causes": "Jamur Sclerotium oryzae",
        "treatment": [
            "Buang tanaman terinfeksi",
            "Aplikasi fungisida sistemik",
            "Perbaiki drainase"
        ],
        "prevention": [
            "Rotasi tanaman",
            "Sanitasi lahan",
            "Hindari genangan air"
        ],
        "severity": "Sangat Tinggi"
    },
    "Karat Daun": {
        "symptoms": ["Bintik kuning/oranye", "Serbuk pada daun", "Daun rontok"],
        "causes": "Jamur karat (Rust fungi)",
        "treatment": [
            "Semprot fungisida berbahan Mancozeb",
            "Aplikasi setiap 7 hari",
            "Buang daun terinfeksi"
        ],
        "prevention": [
            "Jarak tanam cukup",
            "Sirkulasi udara baik",
            "Hindari kelembaban tinggi"
        ],
        "severity": "Sedang"
    },
    "Virus Tungro": {
        "symptoms": ["Daun kuning/oranye", "Pertumbuhan kerdil", "Anakan sedikit"],
        "causes": "Virus ditularkan wereng hijau",
        "treatment": [
            "Tidak ada obat langsung",
            "Cabut dan musnahkan tanaman sakit",
            "Kendalikan vektor (wereng)"
        ],
        "prevention": [
            "Gunakan varietas tahan",
            "Tanam serentak",
            "Kendalikan wereng"
        ],
        "severity": "Sangat Tinggi"
    },
    "Defisiensi Nitrogen": {
        "symptoms": ["Daun menguning merata", "Pertumbuhan lambat", "Batang lemah"],
        "causes": "Kekurangan unsur Nitrogen",
        "treatment": [
            "Aplikasi pupuk Urea 100-150 kg/ha",
            "Atau pupuk organik",
            "Pemupukan bertahap"
        ],
        "prevention": [
            "Pemupukan teratur",
            "Uji tanah berkala",
            "Rotasi tanaman legum"
        ],
        "severity": "Rendah"
    },
    "Defisiensi Fosfor": {
        "symptoms": ["Daun ungu/kemerahan", "Pertumbuhan akar terhambat", "Pembungaan terlambat"],
        "causes": "Kekurangan unsur Fosfor",
        "treatment": [
            "Aplikasi pupuk SP-36 100-150 kg/ha",
            "Atau pupuk organik kaya P",
            "Perbaiki pH tanah"
        ],
        "prevention": [
            "Pemupukan P saat tanam",
            "Uji tanah",
            "Pengapuran jika pH rendah"
        ],
        "severity": "Rendah"
    },
    "Serangan Wereng": {
        "symptoms": ["Daun mengering (hopperburn)", "Tanaman coklat", "Wereng terlihat"],
        "causes": "Hama wereng coklat/hijau",
        "treatment": [
            "Semprot insektisida berbahan Imidakloprid",
            "Aplikasi setiap 7 hari",
            "Kendalikan populasi"
        ],
        "prevention": [
            "Gunakan varietas tahan",
            "Tanam serentak",
            "Hindari insektisida berlebihan"
        ],
        "severity": "Tinggi"
    },
    "Serangan Ulat Grayak": {
        "symptoms": ["Daun berlubang", "Ulat hijau terlihat", "Kotoran ulat"],
        "causes": "Hama ulat Spodoptera litura",
        "treatment": [
            "Semprot insektisida nabati (mimba)",
            "Atau insektisida kimia",
            "Pungut ulat manual"
        ],
        "prevention": [
            "Perangkap feromon",
            "Musuh alami",
            "Sanitasi lahan"
        ],
        "severity": "Sedang"
    }
}

# ========== DIAGNOSTIC QUESTIONS ==========
DIAGNOSTIC_TREE = {
    "start": {
        "question": "Apa jenis tanaman yang bermasalah?",
        "options": {
            "Padi": "q_padi_1",
            "Jagung": "q_jagung_1",
            "Cabai": "q_cabai_1",
            "Tomat": "q_tomat_1",
            "Lainnya": "q_general_1"
        }
    },
    "q_padi_1": {
        "question": "Di bagian mana gejala paling terlihat?",
        "options": {
            "Daun": "q_padi_daun",
            "Batang": "q_padi_batang",
            "Seluruh tanaman": "q_padi_whole"
        }
    },
    "q_padi_daun": {
        "question": "Seperti apa gejala pada daun?",
        "options": {
            "Bercak coklat belah ketupat": {"diagnosis": "Blas Padi"},
            "Garis kuning di tepi daun": {"diagnosis": "Hawar Daun Bakteri"},
            "Daun menguning merata": {"diagnosis": "Defisiensi Nitrogen"},
            "Daun ungu/kemerahan": {"diagnosis": "Defisiensi Fosfor"},
            "Daun mengering coklat (hopperburn)": {"diagnosis": "Serangan Wereng"}
        }
    },
    "q_padi_batang": {
        "question": "Seperti apa kondisi batang?",
        "options": {
            "Batang menghitam dan busuk": {"diagnosis": "Busuk Batang"},
            "Batang lemah dan mudah rebah": {"diagnosis": "Defisiensi Nitrogen"}
        }
    },
    "q_padi_whole": {
        "question": "Seperti apa kondisi keseluruhan tanaman?",
        "options": {
            "Tanaman kerdil, daun kuning/oranye": {"diagnosis": "Virus Tungro"},
            "Pertumbuhan lambat, daun pucat": {"diagnosis": "Defisiensi Nitrogen"}
        }
    },
    "q_general_1": {
        "question": "Apa gejala utama yang terlihat?",
        "options": {
            "Daun berlubang": {"diagnosis": "Serangan Ulat Grayak"},
            "Bintik kuning/oranye pada daun": {"diagnosis": "Karat Daun"},
            "Daun menguning": {"diagnosis": "Defisiensi Nitrogen"}
        }
    }
}

# ========== MAIN APP ==========
st.title("🔍 Diagnostik Gejala Cerdas")
st.markdown("**Jawab pertanyaan atau pilih gejala untuk mengidentifikasi masalah pada tanaman Anda**")

# Tabs for different methods
tab1, tab2 = st.tabs(["🌲 Pohon Keputusan (Interaktif)", "🧮 Teorema Bayes (Kalkulator)"])

# --- TAB 1: DECISION TREE ---
with tab1:
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 'start'
    if 'diagnosis_history' not in st.session_state:
        st.session_state.diagnosis_history = []
    if 'diagnosis_result' not in st.session_state:
        st.session_state.diagnosis_result = None

    # Instructions
    with st.expander("📖 Cara Menggunakan Pohon Keputusan", expanded=False):
        st.markdown("""
        **Langkah-langkah:**
        1. Jawab pertanyaan yang muncul secara berurutan
        2. Pilih opsi yang paling sesuai dengan gejala tanaman Anda
        3. Sistem akan mendiagnosis masalah berdasarkan jawaban Anda
        """)

    # Reset button
    if st.button("🔄 Mulai Diagnosis Baru", key="reset_tree"):
        st.session_state.current_question = 'start'
        st.session_state.diagnosis_history = []
        st.session_state.diagnosis_result = None
        st.rerun()

    # Display diagnostic flow
    st.markdown("---")

    # Show history
    if st.session_state.diagnosis_history:
        st.subheader("📋 Riwayat Jawaban")
        for i, (q, a) in enumerate(st.session_state.diagnosis_history):
            st.write(f"{i+1}. **{q}** → {a}")
        st.markdown("---")

    # Current question
    if st.session_state.diagnosis_result is None:
        current = DIAGNOSTIC_TREE.get(st.session_state.current_question)
        
        if current:
            st.subheader("❓ Pertanyaan")
            st.markdown(f"### {current['question']}")
            
            # Display options
            st.markdown("**Pilih salah satu:**")
            
            for option in current['options'].keys():
                if st.button(option, key=f"btn_{option}", use_container_width=True):
                    # Save answer
                    st.session_state.diagnosis_history.append((current['question'], option))
                    
                    # Get next question or diagnosis
                    next_step = current['options'][option]
                    
                    if isinstance(next_step, dict) and 'diagnosis' in next_step:
                        # We have a diagnosis
                        st.session_state.diagnosis_result = next_step['diagnosis']
                    else:
                        # Move to next question
                        st.session_state.current_question = next_step
                    
                    st.rerun()
    else:
        # Display diagnosis result
        diagnosis_name = st.session_state.diagnosis_result
        diagnosis = DISEASE_DATABASE.get(diagnosis_name)
        
        if diagnosis:
            st.success("✅ Diagnosis Selesai!")
            
            st.markdown("---")
            st.subheader(f"🎯 Hasil Diagnosis: {diagnosis_name}")
            
            # Severity indicator
            severity_colors = {
                "Rendah": ("🟢", "#10b981"),
                "Sedang": ("🟡", "#f59e0b"),
                "Tinggi": ("🟠", "#f97316"),
                "Sangat Tinggi": ("🔴", "#ef4444")
            }
            
            severity_icon, severity_color = severity_colors.get(diagnosis['severity'], ("⚪", "#6b7280"))
            
            st.markdown(f"""
            <div style="background: {severity_color}20; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid {severity_color}; margin: 1rem 0;">
                <h4 style="margin: 0; color: {severity_color};">
                    {severity_icon} Tingkat Keparahan: {diagnosis['severity']}
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🔬 Informasi")
                st.markdown(f"**Penyebab:** {diagnosis['causes']}")
                
                st.markdown("**Gejala:**")
                for symptom in diagnosis['symptoms']:
                    st.write(f"- {symptom}")
            
            with col2:
                st.markdown("### 💊 Penanganan")
                for i, treatment in enumerate(diagnosis['treatment'], 1):
                    st.write(f"{i}. {treatment}")
            
            # Prevention
            st.markdown("---")
            st.subheader("🛡️ Pencegahan")
            
            cols = st.columns(len(diagnosis['prevention']))
            for col, prevention in zip(cols, diagnosis['prevention']):
                with col:
                    st.info(f"✓ {prevention}")
            
            # Additional recommendations
            st.markdown("---")
            st.subheader("💡 Rekomendasi Tambahan")
             
            if "Defisiensi" in diagnosis_name:
                st.markdown("""
                **Untuk masalah nutrisi:**
                - Gunakan modul **Analisis NPK** untuk cek status tanah
                - Gunakan **Kalkulator Pupuk** untuk dosis yang tepat
                - Lakukan uji tanah di laboratorium
                """)
            elif "Virus" in diagnosis_name:
                st.warning("""
                ⚠️ **Penting untuk Penyakit Virus:**
                - Tidak ada obat langsung untuk virus
                - Fokus pada pencegahan dan pengendalian vektor
                - Cabut dan musnahkan tanaman terinfeksi
                - Tanam varietas tahan virus
                """)
            else:
                st.markdown("""
                **Untuk penyakit/hama:**
                - Aplikasi pestisida sesuai dosis anjuran
                - Rotasi jenis pestisida untuk hindari resistensi
                - Kombinasikan dengan pengendalian hayati
                - Monitor populasi hama/penyakit secara rutin
                """)
            
            # Save diagnosis
            st.markdown("---")
            if st.button("💾 Simpan Hasil Diagnosis", use_container_width=True):
                diagnosis_record = {
                    'date': pd.Timestamp.now().isoformat(),
                    'diagnosis': diagnosis_name,
                    'severity': diagnosis['severity'],
                    'questions': st.session_state.diagnosis_history
                }
                
                st.success("✅ Hasil diagnosis berhasil disimpan!")
                st.json(diagnosis_record)
        else:
            st.error("❌ Diagnosis tidak ditemukan dalam database")

# --- TAB 2: BAYES THEOREM ---
with tab2:
    st.subheader("🧮 Kalkulator Teorema Bayes")
    st.info("Metode ini menggunakan probabilitas statistik untuk memprediksi penyakit berdasarkan gejala yang terpilih. Cocok jika gejala tidak lengkap atau ambigu.")
    
    # 1. Get all unique symptoms
    all_symptoms = set()
    for d in DISEASE_DATABASE.values():
        for s in d['symptoms']:
            all_symptoms.add(s)
    all_symptoms = sorted(list(all_symptoms))
    
    # 2. Input UI
    st.markdown("### 1. Pilih Gejala yang Terlihat")
    selected_symptoms_bayes = st.multiselect(
        "Cari dan pilih gejala:",
        options=all_symptoms,
        placeholder="Ketik gejala (contoh: Daun kuning...)"
    )
    
    # 3. Calculation & Display
    if st.button("🧮 Hitung Probabilitas Diagnosis", type="primary"):
        if not selected_symptoms_bayes:
            st.warning("⚠️ Mohon pilih setidaknya satu gejala untuk dianalisis.")
        else:
            # Calculation
            results = []
            diseases = list(DISEASE_DATABASE.keys())
            prior = 1.0 / len(diseases) # Uniform assumption
            
            total_unnormalized = 0
            disease_scores = {}
            
            for disease_name, info in DISEASE_DATABASE.items():
                likelihood = 1.0
                disease_symptoms_set = set(info['symptoms'])
                
                # Naive Bayes Logic: P(Observed | Disease)
                # We reward matches high (0.9), and mismatches low (0.1)
                for s in selected_symptoms_bayes:
                    if s in disease_symptoms_set:
                        likelihood *= 0.9
                    else:
                        likelihood *= 0.1
                
                posterior_score = prior * likelihood
                disease_scores[disease_name] = posterior_score
                total_unnormalized += posterior_score
            
            # Normalize
            for d_name in diseases:
                score = disease_scores[d_name]
                prob = 0.0
                if total_unnormalized > 0:
                    prob = score / total_unnormalized
                
                results.append({
                    "name": d_name,
                    "prob": prob,
                    "info": DISEASE_DATABASE[d_name]
                })
            
            # Sort desc
            results.sort(key=lambda x: x['prob'], reverse=True)
            
            # Display Results
            st.markdown("---")
            st.subheader("📊 Hasil Analisis Probabilitas")
            
            # Top Result
            top = results[0]
            st.success(f"Diagnosis Utama: **{top['name']}** dengan probabilitas **{top['prob']:.1%}**")
            
            # Bar Chart
            df_chart = pd.DataFrame(results)
            # Filter low prob for cleaner chart if many diseases
            df_chart = df_chart[df_chart['prob'] > 0.01] 
            
            fig = go.Figure(go.Bar(
                x=df_chart['prob'],
                y=df_chart['name'],
                orientation='h',
                text=[f"{p:.1%}" for p in df_chart['prob']],
                textposition='inside',
                marker_color=['#10b981' if p == top['prob'] else '#6b7280' for p in df_chart['prob']]
            ))
            
            fig.update_layout(
                title="Distribusi Probabilitas Penyakit",
                xaxis_title="Probabilitas",
                yaxis_title="Penyakit",
                yaxis_autorange="reversed", # Top result on top
                height=max(400, len(df_chart) * 50)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed View for Top Result
            with st.container():
                st.info(f"Detail Diagnosis: {top['name']}")
                info = top['info']
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Gejala yang Cocok:**")
                    for s in info['symptoms']:
                        if s in selected_symptoms_bayes:
                            st.write(f"✅ {s}")
                    
                    st.markdown("**Gejala Lain (Tidak Terpilih):**")
                    for s in info['symptoms']:
                        if s not in selected_symptoms_bayes:
                            st.write(f"⬜ {s}")
                            
                with c2:
                    st.markdown("**Penyebab:**")
                    st.write(info['causes'])
                    
                    st.markdown("**Penanganan Utama:**")
                    for t in info['treatment']:
                        st.write(f"- {t}")

# Quick reference
st.markdown("---")
st.subheader("📚 Referensi Cepat Gejala Umum")

with st.expander("Lihat Daftar Lengkap Penyakit & Hama"):
    for disease_name, disease_info in DISEASE_DATABASE.items():
        with st.expander(f"{disease_name} ({disease_info['severity']})"):
            st.write(f"**Penyebab:** {disease_info['causes']}")
            st.write("**Gejala:**")
            for symptom in disease_info['symptoms']:
                st.write(f"- {symptom}")

# Footer
st.markdown("---")
st.caption("""
🔍 **Diagnostik Gejala Cerdas** - Sistem diagnosis interaktif untuk identifikasi masalah tanaman.
Untuk diagnosis yang lebih akurat, konsultasikan dengan ahli pertanian atau laboratorium.
""")
