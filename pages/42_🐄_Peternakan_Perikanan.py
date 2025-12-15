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
    st.header("🐟 Perikanan (Komoditas & Pakan)")
    st.markdown("Panduan teknis budidaya, pakan alternatif berbasis jurnal, dan manajemen kualitas air.")
    
    # --- SUB TABS PERIKANAN ---
    stab_lele, stab_nila, stab_gurame, stab_unagi, stab_bioflok, stab_pakan = st.tabs([
        "🐟 Lele (Catfish)",
        "🐠 Nila (Tilapia)",
        "🐡 Gurame (Gourami)",
        "🐍 Sidat (Unagi)",
        "🧪 Bioflok & Air",
        "🦗 Database Pakan Alami"
    ])

    # === 1. LELE ===
    with stab_lele:
        st.subheader("😺 Budidaya Lele Intensif")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.info("**Kunci Sukses:** Manajemen pakan dan grading (penyortiran) rutin.")
            jumlah_ikan = st.number_input("Jumlah Tebar (ekor)", value=1000, step=100)
            bobot_rata = st.number_input("Bobot Rata-rata per Ekor (gram)", value=50.0, step=1.0)
            fr_pct = st.number_input("Feeding Rate (%)", value=3.0, step=0.1, help="3-5% dari bobot biomasa")
            
        with col_l2:
            st.markdown("""
            **Rekomendasi Feeding Rate (FR):**
            *   Bibit (<10g): **5-7%** (Cepat tumbuh)
            *   Pembesaran (10-100g): **3-5%**
            *   Konsumsi (>100g): **2-3%** (Maintenance)
            """)
            
        biomasa_kg = (jumlah_ikan * bobot_rata) / 1000
        pakan_harian = biomasa_kg * (fr_pct / 100)
        
        st.success(f"📦 **Kebutuhan Pakan Harian:** {pakan_harian:.2f} kg (Biomasa: {biomasa_kg:.1f} kg)")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Pagi (08:00)", f"{pakan_harian*0.3:.2f} kg")
        c2.metric("Sore (16:00)", f"{pakan_harian*0.4:.2f} kg")
        c3.metric("Malam (21:00)", f"{pakan_harian*0.3:.2f} kg")
        
    # === 2. NILA ===
    with stab_nila:
        st.subheader("🐠 Budidaya Nila (Tilapia)")
        st.info("Nila adalah raja Bioflok. Tahan banting, omnivora, dan tumbuh cepat.")
        
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            st.markdown("#### 🌟 Sistem Monosex Jantan")
            st.markdown("""
            **Kenapa Monosex?**
            *   Nila jantan tumbuh **40% lebih cepat** dari betina.
            *   Mencegah perkimpoian liar di kolam yang membuat populasi over (ikan kerdil).
            *   **Teknik:** Gunakan hormon *17α-methyltestosterone* pada larva usia dini (Panduan khusus).
            """)
        with col_n2:
            st.markdown("#### 🌊 Parameter Kritis")
            st.markdown("""
            *   **Oksigen (DO):** Wajib > 3 mg/L (Gunakan Aerator/Kincir).
            *   **pH Air:** 6.5 - 8.5.
            *   **Suhu:** 25 - 30°C (Nila mogok makan di bawah 20°C).
            """)
            
    # === 3. GURAME ===
    with stab_gurame:
        st.subheader("🐡 Budidaya Gurame (Si Santai)")
        st.warning("⚠️ **Karakter:** Tumbuh lambat, rentan jamur, tapi harga jual tinggi & stabil.")
        
        tab_g1, tab_g2 = st.tabs(["🍃 Pakan & Nutrisi", "🏥 Kesehatan"])
        
        with tab_g1:
            st.markdown("#### Strategi Pakan Hemat (Herbivora)")
            st.markdown("""
            Gurame dewasa punya usus panjang yang mampu mencerna serat kasar. **Manfaatkan pakan alami!**
            1.  **Daun Sente (Lompong):** Pakan favorit, tinggi serat.
            2.  **Daun Pepaya:** Mengandung papain (bantu pencernaan) & antimikroba alami.
            3.  **Daun Mengkudu:** Meningkatkan kekebalan tubuh.
            """)
            
        with tab_g2:
            st.success("✅ **Probiotik Wajib:** Gunakan probiotik (Lactobacillus) pada pakan untuk mencegah kembung.")
            st.error("❌ **Musuh Utama:** Jamur Saprolegnia (Bercak Putih). Jaga suhu stabil, berikan garam krosok 500g/m³ saat hujan.")

    # === 4. UNAGI (SIDAT) ===
    with stab_unagi:
        st.subheader("🐍 Budidaya Sidat (Unagi) - Emas Berlendir")
        st.info("Komoditas ekspor premium (Jepang). Membutuhkan air jernih dan protein tinggi.")
        
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown("#### 🍣 Pakan Pasta (Dough Feed)")
            st.markdown("""
            Sidat tidak suka pelet keras. Pakan harus berbentuk **Pasta**.
            *   **Resep:** Pelet powder (Tepung) + Air + Minyak Ikan + Vitamin Mix.
            *   **Protein Target:**
                *   Glass Eel: **50 - 55%**
                *   Elver: **45 - 50%**
                *   Market Size: **40 - 45%**
            """)
        with col_u2:
            st.markdown("#### 🏠 Habitat Gelap")
            st.markdown("""
            *   **Sifat:** Nokturnal & Fotofobik (Takut Cahaya).
            *   **Setting Kolam:** Wajib diberi naungan/shelter (paralon/gelap).
            *   **Salinitas:** Glass eel butuh adaptasi dari air payau ke tawar (Aklimatisasi perlahan).
            """)

    # === 5. BIOFLOK & AIR (Calculator preserved) ===
    with stab_bioflok:
        st.subheader("🧪 Kalkulator C/N Ratio (Bioflok)")
        st.markdown("**Target C/N Ratio ideal: 15:1 s/d 20:1**")

    # --- SHARED DATA: DATABASE PAKAN ALAMI ---
    # Defined here to be accessible by both "Database Tab" and "Calculator Tab"
    pakan_alami_db = [
        {"Nama": "Tepung Ikan (Lokal)", "Protein": 50.0, "Lemak": 8.0, "Fungsi": "Sumber Protein Utama", "Ket": "Mahal, hati-hati pemalsuan"},
        {"Nama": "Maggot BSF (Kering)", "Protein": 42.0, "Lemak": 20.0, "Fungsi": "Substitusi Tepung Ikan", "Ket": "High Fat, Antimikroba"},
        {"Nama": "Maggot BSF (Segar)", "Protein": 15.0, "Lemak": 6.0, "Fungsi": "Pakan Tambahan", "Ket": "Kadar air ~70% (Konversi 4:1)"},
        {"Nama": "Cacing Sutera (Tubifex)", "Protein": 57.0, "Lemak": 13.0, "Fungsi": "Pakan Larva (Benih)", "Ket": "Terbaik untuk burayak"},
        {"Nama": "Cacing Tanah (Lumbricus)", "Protein": 65.0, "Lemak": 9.0, "Fungsi": "Atraktan & Protein", "Ket": "Basis BK (Kering)"},
        {"Nama": "Azolla microphylla", "Protein": 25.0, "Lemak": 3.0, "Fungsi": "Sumber Protein Nabati", "Ket": "Hemat, mudah kultur"},
        {"Nama": "Lemna sp. (Duckweed)", "Protein": 30.0, "Lemak": 4.0, "Fungsi": "Pakan Nila/Gurame", "Ket": "Menyerap amonia air"},
        {"Nama": "Tepung Keong Mas", "Protein": 52.0, "Lemak": 6.0, "Fungsi": "Sumber Protein Hewani", "Ket": "Hama sawit jadi pakan"},
        {"Nama": "Bungkil Kedelai (SBM)", "Protein": 44.0, "Lemak": 1.5, "Fungsi": "Protein Nabati Utama", "Ket": "Asam amino lengkap"},
        {"Nama": "Dedak Padi (Halus)", "Protein": 12.0, "Lemak": 10.0, "Fungsi": "Sumber Energi (Karbo)", "Ket": "Perekat pelet"},
        {"Nama": "Tepung Jagung", "Protein": 9.0, "Lemak": 4.0, "Fungsi": "Sumber Energi", "Ket": "Karbohidrat tinggi"},
        {"Nama": "Tepung Tapioka", "Protein": 2.0, "Lemak": 0.5, "Fungsi": "Binder (Perekat)", "Ket": "Gunakan 5-10%"}
    ]
    # Helper for dropdown
    pakan_dict = {item["Nama"]: item["Protein"] for item in pakan_alami_db}

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pakan_ikan_bf = st.number_input("Jumlah Pakan per Hari (kg)", value=10.0, key="bf_pakan")
        protein_pakan_bf = st.number_input("Kandungan Protein Pakan (%)", value=30.0, key="bf_prot")

    with col_f2:
        if st.button("Hitung Kebutuhan Molase"):
            n_content = pakan_ikan_bf * (protein_pakan_bf/100) * 0.16 
            tan_excreted = n_content * 0.5 
            target_cn = 15
            needed_c = tan_excreted * target_cn
            molase_needed = needed_c / 0.5 
            
            st.success(f"🍯 **Tambahkan Molase:** ± {molase_needed:.2f} kg / hari")
            st.caption(f"Basis: TAN terbuang {tan_excreted:.3f} kg. Dibutuhkan Carbon {needed_c:.3f} kg.")

    # === 6. DATABASE PAKAN ALAMI ===
    with stab_pakan:
        st.subheader("🦗 Database Nutrisi Pakan Alternatif (Jurnal Ilmiah)")
        st.info("Referensi nutrisi untuk formulasi pakan mandiri.")
        
        # Display DataFrame from Shared Data
        df_pakan = pd.DataFrame(pakan_alami_db)
        # Format displayed float columns for readability if needed, or just show as is
        st.dataframe(df_pakan)
        
        st.markdown("### 💡 Tips Formulasi:")
        st.markdown("""
        *   **Keseimbangan:** Jangan andalkan 1 jenis saja. Campur protein hewani (Ikan/Maggot) dan nabati (Kedelai/Azolla).
        *   **Lemak:** Hati-hati penggunaan Maggot Penuh > 30% karena lemak tinggi bisa bikin ikan berlemak (gajih).
        *   **Binder:** Gunakan Tepung Tapioka/Terigu (5-10%) agar pelet tidak mudah hancur di air.
        """)

# ===== TAB 4: RANSUM =====
# ===== TAB 4: RANSUM =====
with tab_feed:
    st.header("🧮 Kalkulator Formulasi Ransum Mandiri")
    st.markdown("Buat pakan ikan/ternak sendiri dengan formulasi multi-bahan untuk mencapai target protein.")
    
    # Init Session State untuk Pakan
    if "feed_ingredients" not in st.session_state:
        st.session_state.feed_ingredients = [
            {"nama": "Tepung Ikan", "pk": 50.0, "porsi": 30.0},
            {"nama": "Dedak Padi", "pk": 11.0, "porsi": 30.0},
            {"nama": "Bungkil Kedelai", "pk": 44.0, "porsi": 40.0}
        ]
        
    col_fc1, col_fc2 = st.columns([1, 1.5])
    
    with col_fc1:
        st.subheader("🛠️ Atur Komposisi")
        target_pk = st.number_input("Target Protein Kasar (%)", value=30.0, step=1.0)
        total_pakan = st.number_input("Rencana Total Pakan (kg)", value=100.0, step=10.0)
        
        st.divider()
        st.write("**Daftar Bahan:**")
        
        # Editor Bahan
        updated_ingredients = []
        total_porsi = 0.0
        
        # Use pakan_dict for dropdown options
        db_options = ["-- Pilih dari Database --"] + list(pakan_dict.keys())
        
        for i, item in enumerate(st.session_state.feed_ingredients):
            c_nama, c_pk, c_pct = st.columns([2, 1, 1])
            with c_nama:
                # Logic: Show text input if "Custom" or if existing value is not in DB (or manual edit)
                # But to keep it simple, we use a selectbox helper. 
                # Improving UI: Selectbox to pick ingredient, it auto-updates name & pk.
                
                # We need a key mechanism. 
                sel_key = f"sel_{i}"
                
                # Check if current item name matches DB, if so set index
                current_name = item['nama']
                try:
                    idx = db_options.index(current_name)
                except ValueError:
                    idx = 0 # Default to "-- Pilih --"
                
                selected_opt = st.selectbox(f"Bahan {i+1}", db_options, index=idx, key=sel_key, label_visibility="collapsed")
                
                # If selection changes from default/previous, update the item values
                final_name = current_name
                final_pk = item['pk']
                
                if selected_opt != "-- Pilih dari Database --":
                    final_name = selected_opt
                    final_pk = pakan_dict.get(selected_opt, 0.0)
                
                # Also allow manual override via text input? 
                # For simplicity in this iteration, allow the Selectbox to be the primary 'Chooser'.
                # But what if custom? -> "Custom" Not implemented yet in DB list. 
                # Let's add text input BELOW it for manual name override if needed? No, too cluttered.
                # Approach: Just use selectbox for now to solve user's "Source" question.
            
            with c_pk:
                # If we just selected from DB, the number input should default to that.
                # But st.number_input is stateful. We rely on the re-run cycle or 'value' param if key changed?
                # Simpler: Just display the PK input. If user selected something new, we might need to force update state.
                # In Streamlit, updating state mid-loop is tricky.
                # Better Pattern: Input is driven by state. State is updated by callback or logic before rendering.
                
                # Quick Fix: If the dropdown selection (selected_opt) is different from stored item['nama'], update it immediately?
                # Yes, logic above: final_pk = pakan_dict.get...
                
                pk = st.number_input(f"PK", value=float(final_pk), key=f"p_{i}", label_visibility="collapsed")
            with c_pct:
                porsi = st.number_input(f"%", value=item['porsi'], key=f"r_{i}", label_visibility="collapsed")
            
            updated_ingredients.append({"nama": final_name, "pk": pk, "porsi": porsi})
            total_porsi += porsi
            
        st.session_state.feed_ingredients = updated_ingredients
        
        # Tools Add/Remove
        b_add, b_reset = st.columns(2)
        if b_add.button("➕ Tambah Bahan"):
            st.session_state.feed_ingredients.append({"nama": "Bahan Baru", "pk": 0.0, "porsi": 0.0})
            st.rerun()
            
        if b_reset.button("🔄 Reset Default"):
            st.session_state.feed_ingredients = [
                {"nama": "Tepung Ikan", "pk": 50.0, "porsi": 30.0},
                {"nama": "Dedak Padi", "pk": 11.0, "porsi": 30.0},
                {"nama": "Bungkil Kedelai", "pk": 44.0, "porsi": 40.0}
            ]
            st.rerun()
            
    with col_fc2:
        st.subheader("📊 Analisis Nutrisi")
        
        # Real-time Calculation
        calc_pk = 0.0
        details = []
        
        for item in st.session_state.feed_ingredients:
            # Contribution PK = (Porsi / Total Porsi) * PK Bahan
            if total_porsi > 0:
                real_pct = (item['porsi'] / total_porsi) * 100
                contrib_pk = (real_pct / 100) * item['pk']
                real_kg = (real_pct / 100) * total_pakan
                
                calc_pk += contrib_pk
                details.append({
                    "Bahan": item['nama'],
                    "PK Bahan (%)": item['pk'],
                    "Proporsi (%)": f"{real_pct:.1f}%",
                    "Berat (kg)": f"{real_kg:.2f}",
                    "Sumbangan PK (%)": f"{contrib_pk:.2f}"
                })
        
        # Display Gauge
        delta_pk = calc_pk - target_pk
        st.metric("Total Protein Kasar (Calculated)", f"{calc_pk:.2f} %", f"{delta_pk:.2f} % dari Target")
        
        # Logic Check
        if abs(total_porsi - 100.0) > 0.1:
            st.error(f"⚠️ Total Proporsi belum 100% (Saat ini: {total_porsi:.1f}%). Harap sesuaikan porsi bahan.")
        else:
            if calc_pk >= target_pk - 1.0 and calc_pk <= target_pk + 1.0:
                st.success("✅ **Formulasi Ideal!** Sesuai dengan target protein.")
            elif calc_pk < target_pk:
                st.warning("⚠️ **Protein Kurang.** Tambahkan porsi bahan protein tinggi (Tepung Ikan/Kedelai).")
            else:
                st.info("ℹ️ **Protein Tinggi.** Bisa dikurangi untuk hemat biaya.")
                
            st.table(pd.DataFrame(details))
            
            # Recommendation Chart
            fig_feed = px.pie(
                names=[d['Bahan'] for d in details],
                values=[float(d['Berat (kg)']) for d in details],
                title=f"Komposisi untuk {total_pakan} kg Pakan"
            )
            st.plotly_chart(fig_feed, use_container_width=True)
            
            st.info("""
            **Tips Formulasi:**
            *   Gunakan **Metode Trial & Error** dengan mengubah angka 'Porsi%' di sebelah kiri sampai Total Proporsi 100% dan Target Protein tercapai.
            *   PK = Protein Kasar (Crude Protein).
            """)

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
