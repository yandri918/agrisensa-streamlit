import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Peternakan & Perikanan - AgriSensa",
    page_icon="🐄",
    layout="wide"
)

# Header
st.title("🐄 Manajemen Peternakan & Perikanan")
st.markdown("**Solusi Presisi untuk Ruminansia, Unggas, dan Budidaya Perikanan**")
st.info("💡 Modul ini menyediakan alat bantu hitung teknis (Ransum, FCR, Bioflok) dan asisten kesehatan hewan.")

# Main tabs
tab_ruminant, tab_poultry, tab_fish, tab_feed, tab_vet = st.tabs([
    "🐄 Ruminansia (Sapi/Kambing)",
    "🐓 Unggas (Ayam/Bebek)",
    "🐟 Perikanan (Bioflok/RAS)",
    "🧮 Kalkulator Ransum",
    "🩺 Dokter Hewan AI"
])

# ===== TAB 1: RUMINANSIA =====
with tab_ruminant:
    st.header("🐄 Manajemen Ruminansia")
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.subheader("📊 Kalkulator ADG (PBBH)")
        st.markdown("*Average Daily Gain / Pertambahan Bobot Badan Harian*")
        
        awal = st.number_input("Bobot Awal (kg)", value=250.0, step=0.1)
        akhir = st.number_input("Bobot Akhir (kg)", value=300.0, step=0.1)
        hari = st.number_input("Jangka Waktu (hari)", value=30, step=1)
        
        if st.button("Hitung ADG"):
            if hari > 0:
                adg = (akhir - awal) / hari
                st.metric("ADG (kg/hari)", f"{adg:.2f} kg")
                
                if adg > 1.0:
                    st.success("✅ Pertumbuhan Sangat Baik (Sapi Potong)")
                elif adg > 0.6:
                    st.info("ℹ️ Pertumbuhan Cukup Baik")
                else:
                    st.warning("⚠️ Pertumbuhan Lambat. Evaluasi pakan & kesehatan.")
            else:
                st.error("Hari harus > 0")
                
    with col_r2:
        st.subheader("🍼 Estimasi Kebutuhan Pakan")
        st.markdown("Basis: Bahan Kering (Dry Matter) = 3% Bobot Badan")
        
        bb_sapi = st.number_input("Bobot Sapi Saat Ini (kg)", value=300)
        bk_pct = 3.0 # Persen bahan kering kebutuhan
        
        bk_total = bb_sapi * (bk_pct / 100)
        
        # Asumsi Hijauan punya BK 20%, Konsentrat BK 85%
        # Rasio Hijauan:Konsentrat = 60:40
        ratio_h = 60
        ratio_k = 40
        
        bk_hijauan = bk_total * (ratio_h/100)
        bk_konsentrat = bk_total * (ratio_k/100)
        
        # Konversi ke As Fed (Segar)
        segar_hijauan = bk_hijauan / 0.20
        segar_konsentrat = bk_konsentrat / 0.85
        
        st.write(f"**Total Kebutuhan Bahan Kering:** {bk_total:.2f} kg/hari")
        st.info(f"""
        **Rekomendasi Pemberian (As Fed/Segar):**
        *   🌾 **Hijauan (Rumput):** ± {segar_hijauan:.1f} kg
        *   📦 **Konsentrat:** ± {segar_konsentrat:.1f} kg
        *(Asumsi rasio 60:40)*
        """)

# ===== TAB 2: UNGGAS =====
with tab_poultry:
    st.header("🐓 Manajemen Unggas (Broiler/Layer)")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        st.subheader("📈 Kalkulator FCR (Feed Conversion Ratio)")
        st.markdown("Efisiensi pakan: Semakin kecil FCR, semakin untung.")
        
        pakan_habis = st.number_input("Total Pakan Dihabiskan (kg)", value=3000.0)
        bobot_panen = st.number_input("Total Bobot Panen (kg)", value=2000.0)
        
        if st.button("Hitung FCR"):
            if bobot_panen > 0:
                fcr = pakan_habis / bobot_panen
                st.metric("Nilai FCR", f"{fcr:.3f}")
                
                if fcr < 1.6:
                    st.success("✅ Sangat Efisien (Untung Besar)")
                elif fcr < 1.8:
                    st.info("ℹ️ Standar")
                else:
                    st.error("⚠️ Boros Pakan (Cek tumpahan/kesehatan)")
            else:
                st.error("Bobot panen tidak boleh 0")
                
    with col_p2:
        st.subheader("🏆 Indeks Performa (IP)")
        st.markdown("Ukuran keberhasilan periode pemeliharaan.")
        
        fcr_val = st.number_input("Nilai FCR", value=1.5, step=0.01)
        bb_rata = st.number_input("Bobot Rata-rata (kg)", value=2.0, step=0.1)
        umur = st.number_input("Umur Panen (hari)", value=35, step=1)
        deplesi = st.number_input("Kematian (%)", value=3.0, step=0.1)
        
        hidup = 100 - deplesi
        
        if st.button("Hitung IP"):
            if fcr_val > 0 and umur > 0:
                ip = ((hidup * bb_rata) / (fcr_val * umur)) * 100
                st.metric("Indeks Performa (IP)", f"{ip:.0f}")
                
                if ip > 400:
                    st.success("🌟 Istimewa (>400)")
                elif ip > 350:
                    st.success("✅ Sangat Baik (>350)")
                elif ip > 300:
                    st.info("ℹ️ Cukup (>300)")
                else:
                    st.warning("⚠️ Kurang (<300)")

# ===== TAB 3: PERIKANAN =====
with tab_fish:
    st.header("🐟 Perikanan (Intensif & Bioflok)")
    
    st.subheader("🧪 Kalkulator C/N Ratio (Bioflok)")
    st.markdown("""
    Dalam sistem bioflok, kita perlu menambahkan sumber karbon (molase/gula) untuk menyeimbangkan nitrogen dari sisa pakan/kotoran.
    **Target C/N Ratio ideal: 15:1 s/d 20:1**
    """)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pakan_ikan = st.number_input("Jumlah Pakan per Hari (kg)", value=10.0)
        protein_pakan = st.number_input("Kandungan Protein Pakan (%)", value=30.0)
    
    with col_f2:
        st.info("**Logika Perhitungan:**")
        st.markdown("""
        1. N dalam pakan = Protein / 6.25
        2. N terlarut (amonia) ≈ 50% dari N total pakan
        3. Butuh C organik untuk mengikat N tersebut.
        """)
        
    if st.button("Hitung Kebutuhan Molase"):
        # Rumus Sederhana (Ebeling et al., 2006)
        # N added = Pakan * (Protein/100) * 0.16
        # Amonia (TAN) excreted estimate ~ 50% of N input logic variant
        
        # Simplified practical formula (Avnimelech): 
        # Untuk menetralkan 1 kg N butuh 15-20 kg C.
        # Protein 30% -> 1 kg pakan = 300g protein = 48g N (16% N in protein).
        # Assume 50% excretion -> 24g N emitted.
        # Need C/N 15 -> 24g N * 15 = 360g Carbon needed.
        # Molase content ~50% Carbon.
        # So need 360g / 0.5 = 720g Molase per kg pakan??
        
        # Practical Field Rule of Thumb (BOS): 
        # Tambahkan C organik 50% dari jumlah pakan (jika protein 30%) untuk maintenance.
        
        n_content = pakan_ikan * (protein_pakan/100) * 0.16 # Total N input kg
        tan_excreted = n_content * 0.5 # Estimasi TAN dibuang ke air (50%)
        
        target_cn = 15
        needed_c = tan_excreted * target_cn # Carbon murni dibutuhkan
        
        # Molase roughly 50% Carbon
        molase_needed = needed_c / 0.5 
        
        st.write(f"Total N Masuk: {n_content:.3f} kg")
        st.write(f"Estimasi Amonia (N) Terlarut: {tan_excreted:.3f} kg")
        st.write(f"Kebutuhan Carbon Murni (Target C/N 15): {needed_c:.3f} kg")
        
        st.success(f"🍯 **Tambahkan Molase:** ± {molase_needed:.2f} kg / hari")
        st.caption("Catatan: Ini adalah estimasi teoritis. Selalu cek kualitas air (TAN/Nitrit) aktual.")

    st.markdown("---")
    
    # --- NEW SECTION: BUDIDAYA LELE & PAKAN ---
    st.subheader("😺 Budidaya Lele & Pakan Alternatif")
    
    tab_lele, tab_alt = st.tabs(["🐟 Pakan Lele", "🐛 Pakan Alternatif (Maggot/Cacing)"])
    
    with tab_lele:
        st.markdown("**Kalkulator Pakan Harian Lele**")
        
        col_l1, col_l2 = st.columns(2)
        
        with col_l1:
            jumlah_ikan = st.number_input("Jumlah Ikan (ekor)", value=1000, step=100)
            bobot_rata = st.number_input("Bobot Rata-rata per Ekor (gram)", value=50.0, step=1.0)
            fr_pct = st.number_input("Feeding Rate (%)", value=3.0, step=0.1, help="Biasanya 3-5% dari bobot biomasa")
            
        with col_l2:
            st.info("ℹ️ **Feeding Rate (FR)**")
            st.markdown("""
            *   Bibit (<10g): 5-7%
            *   Pembesaran (10-100g): 3-5%
            *   Konsumsi (>100g): 2-3%
            """)
            
        biomasa_kg = (jumlah_ikan * bobot_rata) / 1000
        pakan_harian = biomasa_kg * (fr_pct / 100)
        
        st.write(f"**Total Biomasa Ikan:** {biomasa_kg:.2f} kg")
        
        st.success(f"📦 **Kebutuhan Pakan Harian:** {pakan_harian:.2f} kg")
        
        col_fr1, col_fr2, col_fr3 = st.columns(3)
        with col_fr1:
            st.metric("Pagi (30%)", f"{pakan_harian*0.3:.2f} kg")
        with col_fr2:
            st.metric("Sore/Malam (40%)", f"{pakan_harian*0.4:.2f} kg")
        with col_fr3:
            st.metric("Malam/Tambahan (30%)", f"{pakan_harian*0.3:.2f} kg")
            
    with tab_alt:
        st.markdown("**Substitusi Pakan dengan Pakan Alternatif (Maggot BSF / Cacing)**")
        st.info("💡 Substitusi pakan pelet dengan pakan alami dapat menghemat biaya hingga 30-50%.")
        
        pakan_total = st.number_input("Total Pakan Komersil Harian (kg)", value=pakan_harian if 'pakan_harian' in locals() else 5.0)
        substitusi_pct = st.slider("Persentase Substitusi (%)", 0, 100, 20)
        
        jenis_alt = st.selectbox("Jenis Pakan Alternatif", ["Maggot BSF (Segar)", "Maggot BSF (Kering)", "Cacing Tanah (Lumbricus)", "Azolla"])
        
        # Data Nutrisi (Estimasi Protein & Konversi)
        # Faktor konversi: berapa kg pakan alternatif setara 1 kg pelet (berdasarkan kadar air & protein)
        # Pelet: ~30% PK, Kering (10% air)
        # Maggot Segar: ~15% PK (karena air tinggi 60-70%). Jadi butuh ~2kg maggot segar utk ganti 1kg pelet protein-wise?
        
        conv_factor = 1.0
        note = ""
        
        if jenis_alt == "Maggot BSF (Segar)":
            conv_factor = 2.5 # Butuh 2.5kg segar utk setara nutrisi 1kg pelet (basah vs kering)
            note = "Maggot segar mengandung air tinggi (~70%). Berikan lebih banyak."
        elif jenis_alt == "Maggot BSF (Kering)":
            conv_factor = 0.9 # Protein tinggi (~40-45%), sedikit lebih irit dari pelet
            note = "Maggot kering sangat padat nutrisi."
        elif jenis_alt == "Cacing Tanah (Lumbricus)":
            conv_factor = 3.0 # Segar, air tinggi
            note = "Cacing segar sangat disukai, tapi kadar air tinggi."
        elif jenis_alt == "Azolla":
            conv_factor = 4.0 # Protein ~25% BK, tapi air sangat tinggi
            note = "Azolla segar memiliki kadar air sangat tinggi (>90%)."
            
        pakan_pelet_sisa = pakan_total * (1 - substitusi_pct/100)
        pakan_diganti = pakan_total * (substitusi_pct/100)
        
        alt_needed = pakan_diganti * conv_factor
        
        st.markdown("#### 📋 Rekomendasi Pemberian")
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Pakan Pelet (Tetap)", f"{pakan_pelet_sisa:.2f} kg", f"-{pakan_diganti:.2f} kg")
        with c2:
            st.metric(f"Tambahan {jenis_alt}", f"{alt_needed:.2f} kg", f"Faktor: {conv_factor}x")
            
        if note:
            st.caption(f"📝 {note}")
            
        st.warning("⚠️ Perhatian: Selalu lakukan adaptasi pakan secara bertahap (misal: 10% -> 20% -> 30%) dalam waktu 1-2 minggu.")

# ===== TAB 4: RANSUM =====
with tab_feed:
    st.header("🧮 Formulasi Ransum (Metode Segi Empat Pearson)")
    st.markdown("Metode sederhana untuk mencampur 2 bahan pakan agar mencapai target Protein Kasar (PK).")
    
    col_fd1, col_fd2 = st.columns(2)
    
    with col_fd1:
        st.subheader("Target & Bahan")
        target_pk = st.number_input("Target Protein (%)", value=16.0)
        
        st.markdown("**Bahan 1 (Sumber Energi - PK Rendah)**")
        nama_b1 = st.text_input("Nama Bahan 1", value="Jagung Giling")
        pk_b1 = st.number_input("Protein Bahan 1 (%)", value=9.0)
        
        st.markdown("**Bahan 2 (Sumber Protein - PK Tinggi)**")
        nama_b2 = st.text_input("Nama Bahan 2", value="Konsentrat/Bungkil Kedelai")
        pk_b2 = st.number_input("Protein Bahan 2 (%)", value=36.0)
        
        total_mix = st.number_input("Total Campuran yang diinginkan (kg)", value=100.0)

    with col_fd2:
        st.subheader("Hasil Formulasi")
        
        if pk_b1 < target_pk < pk_b2:
            # Pearson Square Math
            #    B1(a) ---------> (c) |Target - B2|
            #          Target
            #    B2(b) ---------> (d) |Target - B1|
            
            selisih_b1 = abs(target_pk - pk_b2) # Bagian B1
            selisih_b2 = abs(target_pk - pk_b1) # Bagian B2
            total_bagian = selisih_b1 + selisih_b2
            
            pct_b1 = (selisih_b1 / total_bagian) * 100
            pct_b2 = (selisih_b2 / total_bagian) * 100
            
            kg_b1 = (pct_b1 / 100) * total_mix
            kg_b2 = (pct_b2 / 100) * total_mix
            
            st.write(f"**Proporsi Campuran:**")
            
            df_result = pd.DataFrame({
                "Bahan": [nama_b1, nama_b2, "TOTAL"],
                "Protein Asli (%)": [pk_b1, pk_b2, target_pk],
                "Proporsi (%)": [f"{pct_b1:.1f}%", f"{pct_b2:.1f}%", "100%"],
                "Berat (kg)": [f"{kg_b1:.2f}", f"{kg_b2:.2f}", f"{total_mix:.2f}"]
            })
            st.table(df_result)
            
            st.success("✅ Formulasi Mungkin Dilakukan")
            
            # Chart
            fig = px.pie(names=[nama_b1, nama_b2], values=[kg_b1, kg_b2], title="Komposisi Ransum")
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.error("❌ Target Protein harus berada DI ANTARA Protein Bahan 1 dan Bahan 2.")
            st.info(f"Target ({target_pk}%) tidak bisa dicapai dengan {nama_b1} ({pk_b1}%) dan {nama_b2} ({pk_b2}%) saja.")

# ===== TAB 5: DOKTER HEWAN AI =====
with tab_vet:
    st.header("🩺 Asisten Kesehatan Hewan AI")
    st.markdown("Diskusikan gejala penyakit pada ternak atau ikan Anda.")
    
    # Initialize chat history
    if "vet_messages" not in st.session_state:
        st.session_state.vet_messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.vet_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Contoh: Sapi saya keluar air liur berbusa dan kuku luka..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.vet_messages.append({"role": "user", "content": prompt})

        # Placeholder response Logic
        # In real app, connect to LLM API here.
        # For now, we use a simple static response or "simulated" analysis.
        
        response = f"""
        **Analisis Sementara (Simulasi AI):**
        
        Berdasarkan keluhan "{prompt}", ini membutuhkan diagnosa lebih lanjut.
        
        Namun, jika gejala melibatkan mulut berbusa dan luka kuku pada ruminansia, **Waspadai PMK (Penyakit Mulut dan Kuku)**.
        
        **Saran Awal:**
        1. Pisahkan ternak sakit (Karantina).
        2. Berikan cairan elektrolit/vitamin support.
        3. Segera hubungi Dokter Hewan setempat untuk konfirmasi.
        
        *Catatan: Sistem ini masih dalam pengembangan (Dummy Response).*
        """
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.vet_messages.append({"role": "assistant", "content": response})
