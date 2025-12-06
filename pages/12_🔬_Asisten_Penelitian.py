# Asisten Penelitian Agronomi
# Advanced research assistant with multiple ML models and statistical analysis (ANOVA/RAK/RAL)
# Version: 2.0.0 (Integrated Stats)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ML Imports
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Stats Imports
from scipy import stats

st.set_page_config(page_title="Asisten Penelitian", page_icon="🔬", layout="wide")

# ==========================================
# 📐 STATISTICAL ENGINE (ANOVA & POST-HOC)
# ==========================================
def calculate_anova_ral(df, col_perlakuan, col_hasil):
    """
    Hitung ANOVA Rancangan Acak Lengkap (CRD)
    Sumber Keragaman: Perlakuan, Galat, Total
    """
    # 1. Prepare Data
    groups = df.groupby(col_perlakuan)[col_hasil]
    grand_mean = df[col_hasil].mean()
    n_total = len(df)
    n_treatments = df[col_perlakuan].nunique()
    
    # 2. Sum of Squares (JK)
    # FK (Faktor Koreksi)
    fk = (df[col_hasil].sum()**2) / n_total
    
    # JK Total
    jk_total = (df[col_hasil]**2).sum() - fk
    
    # JK Perlakuan
    jk_perlakuan = (groups.sum()**2 / groups.count()).sum() - fk
    
    # JK Galat
    jk_galat = jk_total - jk_perlakuan
    
    # 3. Degrees of Freedom (DB)
    db_perlakuan = n_treatments - 1
    db_total = n_total - 1
    db_galat = db_total - db_perlakuan
    
    # 4. Mean Square (KT)
    kt_perlakuan = jk_perlakuan / db_perlakuan
    kt_galat = jk_galat / db_galat
    
    # 5. F-Hitung
    f_hitung = kt_perlakuan / kt_galat
    
    # 6. P-Value (1 - CDF)
    p_value = 1 - stats.f.cdf(f_hitung, db_perlakuan, db_galat)
    
    # 7. CV (Koefisien Keragaman)
    cv = (np.sqrt(kt_galat) / grand_mean) * 100
    
    summary = {
        "SK": ["Perlakuan", "Galat", "Total"],
        "DB": [db_perlakuan, db_galat, db_total],
        "JK": [jk_perlakuan, jk_galat, jk_total],
        "KT": [kt_perlakuan, kt_galat, np.nan],
        "F-Hitung": [f_hitung, np.nan, np.nan],
        "P-Value": [p_value, np.nan, np.nan],
        "Signifikan": [p_value < 0.05, np.nan, np.nan]
    }
    
    return pd.DataFrame(summary), kt_galat, db_galat, cv

def calculate_anova_rak(df, col_perlakuan, col_kelompok, col_hasil):
    """
    Hitung ANOVA Rancangan Acak Kelompok (RCBD)
    Sumber Keragaman: Kelompok, Perlakuan, Galat, Total
    """
    # 1. Prereq
    n_total = len(df)
    n_kelompok = df[col_kelompok].nunique()
    n_perlakuan = df[col_perlakuan].nunique()
    grand_mean = df[col_hasil].mean()
    
    # FK
    fk = (df[col_hasil].sum()**2) / n_total
    
    # JK Total
    jk_total = (df[col_hasil]**2).sum() - fk
    
    # JK Kelompok
    jk_kelompok = (df.groupby(col_kelompok)[col_hasil].sum()**2 / n_perlakuan).sum() - fk
    
    # JK Perlakuan
    jk_perlakuan = (df.groupby(col_perlakuan)[col_hasil].sum()**2 / n_kelompok).sum() - fk
    
    # JK Galat
    jk_galat = jk_total - jk_kelompok - jk_perlakuan
    
    # DB
    db_kelompok = n_kelompok - 1
    db_perlakuan = n_perlakuan - 1
    db_total = n_total - 1
    db_galat = db_total - db_kelompok - db_perlakuan
    
    # KT
    kt_kelompok = jk_kelompok / db_kelompok
    kt_perlakuan = jk_perlakuan / db_perlakuan
    kt_galat = jk_galat / db_galat
    
    # F-Hitung
    f_kelompok = kt_kelompok / kt_galat
    f_perlakuan = kt_perlakuan / kt_galat
    
    # P-Value
    p_kelompok = 1 - stats.f.cdf(f_kelompok, db_kelompok, db_galat)
    p_perlakuan = 1 - stats.f.cdf(f_perlakuan, db_perlakuan, db_galat)
    
    # CV
    cv = (np.sqrt(kt_galat) / grand_mean) * 100
    
    summary = {
        "SK": ["Kelompok", "Perlakuan", "Galat", "Total"],
        "DB": [db_kelompok, db_perlakuan, db_galat, db_total],
        "JK": [jk_kelompok, jk_perlakuan, jk_galat, jk_total],
        "KT": [kt_kelompok, kt_perlakuan, kt_galat, np.nan],
        "F-Hitung": [f_kelompok, f_perlakuan, np.nan, np.nan],
        "P-Value": [p_kelompok, p_perlakuan, np.nan, np.nan],
        "Signifikan": [p_kelompok < 0.05, p_perlakuan < 0.05, np.nan, np.nan]
    }
    
    return pd.DataFrame(summary), kt_galat, db_galat, cv

def calculate_bnt(df, col_perlakuan, col_hasil, kt_galat, db_galat, alpha=0.05):
    """
    Uji Beda Nyata Terkecil (LSD/BNT)
    """
    mean_perlakuan = df.groupby(col_perlakuan)[col_hasil].mean().sort_values(ascending=False)
    n_ulangan = len(df) / df[col_perlakuan].nunique() # Asumsi ulangan sama (seimbang)
    
    # T-Table value
    t_val = stats.t.ppf(1 - alpha/2, db_galat)
    
    # BNT Value
    bnt_val = t_val * np.sqrt((2 * kt_galat) / n_ulangan)
    
    # Notasi Huruf logic
    means = mean_perlakuan.values
    labels = mean_perlakuan.index
    notasi = [''] * len(means)
    
    # Simple algorithm for notation (Greedy approach)
    # Note: Full recursive algorithm is complex, using simplified "significant diff check"
    
    # Init with 'a' for highest
    curr_char = 97 # 'a'
    
    # This is a simplified logic placeholder. 
    # Real BNJ grouping requires matrix overlap check.
    # For MVP: Just comparing each to the best.
    
    # Let's do a Pairwise Comparison Matrix instead, simpler and more informative
    matrix = []
    for i in range(len(means)):
        row = []
        for j in range(len(means)):
            diff = abs(means[i] - means[j])
            sig = "*" if diff > bnt_val else "ns"
            row.append(sig)
        matrix.append(row)
            
    df_matrix = pd.DataFrame(matrix, index=labels, columns=labels)
    
    return mean_perlakuan, bnt_val, df_matrix

# ==========================================
# 🤖 ML ENGINE (EXISTING)
# ==========================================
AVAILABLE_MODELS = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=1.0),
    "Polynomial Regression (deg=2)": "polynomial",
    "Decision Tree": DecisionTreeRegressor(max_depth=5, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
}

def train_and_evaluate_models(X, y, model_names):
    results = []
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    for model_name in model_names:
        if model_name == "Polynomial Regression (deg=2)":
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            y_pred = model.predict(X_poly)
            cv_scores = cross_val_score(model, X_poly, y, cv=5, scoring='r2')
        else:
            model = AVAILABLE_MODELS[model_name]
            model.fit(X_scaled, y)
            y_pred = model.predict(X_scaled)
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
        
        results.append({
            'Model': model_name,
            'R² Score': r2_score(y, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y, y_pred)),
            'CV Mean R²': cv_scores.mean()
        })
    return pd.DataFrame(results)

# ==========================================
# 🏗️ UI LAYOUT
# ==========================================
st.title("🔬 Asisten Penelitian Agronomi")
st.markdown("**Platform Analisis Data Pertanian Terpadu: Machine Learning & Statistika**")

# MAIN TABS
tab_ml, tab_stat = st.tabs(["🤖 Mode Machine Learning (Prediksi)", "📊 Mode Statistika (RAL/RAK)"])

# -----------------
# TAB 1: MACHINE LEARNING
# -----------------
with tab_ml:
    st.header("Prediksi & Pemodelan (ML)")
    st.info("Gunakan mode ini untuk memprediksi hasil panen berdasarkan variabel input (NPK, Cuaca, dll).")
    
    ml_data_source = st.radio("Sumber Data ML:", ["Sample (Yield vs NPK)", "Upload CSV"], horizontal=True)
    
    if ml_data_source == "Sample (Yield vs NPK)":
        # Generate dummy
        np.random.seed(42)
        N = np.random.uniform(50, 200, 100)
        P = np.random.uniform(20, 100, 100)
        K = np.random.uniform(30, 150, 100)
        yield_val = 2000 + 15*N + 10*P + 8*K + np.random.normal(0, 300, 100)
        df_ml = pd.DataFrame({'N': N, 'P': P, 'K': K, 'Yield': yield_val})
    else:
        uploaded = st.file_uploader("Upload CSV (ML)", type='csv', key='ml_upload')
        if uploaded:
            df_ml = pd.read_csv(uploaded)
        else:
            df_ml = None
            
    if df_ml is not None:
        st.dataframe(df_ml.head(5), use_container_width=True)
        col1, col2 = st.columns(2)
        target = col1.selectbox("Target (Y)", df_ml.columns)
        feats = col2.multiselect("Features (X)", [c for c in df_ml.columns if c!=target], default=[c for c in df_ml.columns if c!=target])
        
        if st.button("Jalankan Model ML"):
            with st.spinner("Training models..."):
                res = train_and_evaluate_models(df_ml[feats].values, df_ml[target].values, AVAILABLE_MODELS.keys())
                res_sorted = res.sort_values('R² Score', ascending=False)
                
                # Best model info
                best_model = res_sorted.iloc[0]
                best_r2 = best_model['R² Score']
                best_name = best_model['Model']
                
                # Display results
                st.subheader("📊 Hasil Analisis ML")
                
                col_res1, col_res2 = st.columns([2, 1])
                
                with col_res1:
                    st.dataframe(res_sorted, use_container_width=True)
                    
                with col_res2:
                    st.metric("Model Terbaik", best_name)
                    st.metric("Akurasi (R²)", f"{best_r2:.3f}")
                    
                    # Interpretation
                    if best_r2 >= 0.9:
                        st.success("🎯 Excellent! Model sangat akurat")
                    elif best_r2 >= 0.7:
                        st.info("✅ Good! Model cukup reliable")
                    elif best_r2 >= 0.5:
                        st.warning("⚠️ Fair. Perlu improvement")
                    else:
                        st.error("❌ Poor. Data mungkin tidak linear")
                
                # Chart
                fig = px.bar(res_sorted, x='Model', y='R² Score', title="Perbandingan Akurasi Model", 
                            color='R² Score', color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
                
                # 💡 INSIGHTS SECTION
                st.divider()
                st.subheader("💡 Insight & Rekomendasi")
                
                # Feature Importance (for tree-based models)
                if "Random Forest" in res_sorted['Model'].values:
                    from sklearn.ensemble import RandomForestRegressor
                    rf = RandomForestRegressor(n_estimators=100, random_state=42)
                    rf.fit(df_ml[feats].values, df_ml[target].values)
                    
                    importance_df = pd.DataFrame({
                        'Feature': feats,
                        'Importance': rf.feature_importances_
                    }).sort_values('Importance', ascending=False)
                    
                    col_ins1, col_ins2 = st.columns(2)
                    
                    with col_ins1:
                        st.markdown("**🔍 Faktor Paling Berpengaruh:**")
                        fig_imp = px.bar(importance_df, x='Importance', y='Feature', orientation='h',
                                        title="Feature Importance (Random Forest)", color='Importance')
                        st.plotly_chart(fig_imp, use_container_width=True)
                        
                    with col_ins2:
                        st.markdown("**📈 Interpretasi:**")
                        top_feature = importance_df.iloc[0]['Feature']
                        top_importance = importance_df.iloc[0]['Importance']
                        
                        st.write(f"• **{top_feature}** adalah faktor paling dominan ({top_importance*100:.1f}%)")
                        
                        if len(importance_df) > 1:
                            second_feature = importance_df.iloc[1]['Feature']
                            st.write(f"• **{second_feature}** juga berpengaruh signifikan")
                        
                        # Recommendations
                        st.markdown("**🎯 Rekomendasi:**")
                        st.write(f"1. Fokus optimasi pada **{top_feature}**")
                        st.write(f"2. Monitor perubahan **{top_feature}** secara berkala")
                        if best_r2 < 0.8:
                            st.write("3. Pertimbangkan tambah data atau fitur baru")
                
                # Model Selection Advice
                st.divider()
                st.markdown("**🤖 Pemilihan Model:**")
                
                if best_name in ["Random Forest", "Gradient Boosting"]:
                    st.info("✅ Model ensemble (RF/GB) cocok untuk data kompleks dengan interaksi non-linear")
                elif best_name in ["Linear Regression", "Ridge", "Lasso"]:
                    st.info("✅ Model linear cocok untuk hubungan sederhana dan interpretasi mudah")
                elif best_name == "Polynomial Regression (deg=2)":
                    st.info("✅ Polynomial cocok untuk hubungan kuadratik (parabola)")
                
                # Data Quality Check
                st.markdown("**📊 Kualitas Data:**")
                col_qual1, col_qual2, col_qual3 = st.columns(3)
                
                with col_qual1:
                    n_samples = len(df_ml)
                    st.metric("Jumlah Data", n_samples)
                    if n_samples < 50:
                        st.caption("⚠️ Data terlalu sedikit")
                    else:
                        st.caption("✅ Cukup untuk training")
                        
                with col_qual2:
                    n_features = len(feats)
                    st.metric("Jumlah Features", n_features)
                    if n_features > n_samples / 10:
                        st.caption("⚠️ Terlalu banyak fitur")
                    else:
                        st.caption("✅ Rasio baik")
                        
                with col_qual3:
                    cv_std = res_sorted.iloc[0].get('CV Std R²', 0)
                    if cv_std > 0.1:
                        st.metric("Konsistensi", "Low", delta="Perlu validasi")
                    else:
                        st.metric("Konsistensi", "High", delta="Model stabil")

# -----------------
# TAB 2: STATISTIKA
# -----------------
with tab_stat:
    st.header("Rancangan Percobaan (Experimental Design)")
    st.info("Gunakan mode ini untuk analisis ANOVA (Sidik Ragam) pada eksperimen RAL atau RAK.")
    
    stat_source = st.radio("Sumber Data Statistik:", ["Sample RAL (Sederhana)", "Sample RAK (Kompleks Multi-Var)", "Upload CSV"], horizontal=True, key='stat_src')
    
    if stat_source == "Sample RAL (Sederhana)":
        data_stat = {
            'Perlakuan': ['P0', 'P0', 'P0', 'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P3', 'P3', 'P3'],
            'Ulangan': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            'Hasil_Tan': [12.5, 13.0, 12.8, 15.2, 15.5, 15.0, 18.5, 18.2, 18.8, 16.0, 16.2, 16.5]
        }
        df_stat = pd.DataFrame(data_stat)
        default_target = ['Hasil_Tan']
        
    elif stat_source == "Sample RAK (Kompleks Multi-Var)":
        # Generate Complex Dataset: Uji Efektivitas NPK pada Cabai
        # 5 Perlakuan, 4 Kelompok
        treatments = ['K0 (Kontrol)', 'K1 (NPK A)', 'K2 (NPK B)', 'K3 (NPK C)', 'K4 (NPK Premium)']
        blocks = [1, 2, 3, 4]
        
        rows = []
        np.random.seed(42)
        
        for t_idx, treat in enumerate(treatments):
            # Base effect for treatment (increasing logic)
            base_effect = t_idx * 2 
            
            for bird in blocks:
                # Block effect (soil fertility gradient)
                block_effect = bird * 0.5
                noise = np.random.normal(0, 1)
                
                rows.append({
                    'Perlakuan': treat,
                    'Kelompok': bird,
                    # Variable 1: Vegetative (Height) - Sig
                    'Tinggi_Tanaman_cm': 40 + (base_effect * 3) + block_effect + np.random.normal(0, 2),
                    # Variable 2: Generative (Fruit Count) - Sig
                    'Jml_Buah_per_Tan': 15 + (base_effect * 1.5) + np.random.normal(0, 3),
                    # Variable 3: Weight (Yield) - Very Sig
                    'Bobot_Buah_g': 10 + (base_effect * 0.8) + block_effect + np.random.normal(0, 1),
                    # Variable 4: Quality (Brix) - Not Sig (Treatment doesn't affect sweetness much)
                    'Kadar_Gula_Brix': 5 + np.random.normal(0, 0.5), # Flat base
                    # Variable 5: Disease Index - Sig (Negative correlation)
                    'Intensitas_Penyakit_%': max(0, 20 - (base_effect * 2) + np.random.normal(0, 2))
                })
        
        df_stat = pd.DataFrame(rows)
        default_target = ['Tinggi_Tanaman_cm', 'Bobot_Buah_g', 'Kadar_Gula_Brix']
        
    else:
        uploaded_stat = st.file_uploader("Upload CSV (Format: Perlakuan, Kelompok/Ulangan, Hasil)", type='csv', key='stat_upload')
        if uploaded_stat:
            df_stat = pd.read_csv(uploaded_stat)
            default_target = []
        else:
            df_stat = None
            default_target = []
            
    if df_stat is not None:
        st.write("Preview Data:")
        st.dataframe(df_stat.head(), use_container_width=True)
        
        # Config
        st.subheader("⚙️ Konfigurasi Desain")
        col_design1, col_design2 = st.columns(2)
        
        design_type = col_design1.selectbox("Tipe Rancangan", ["RAL (Rancangan Acak Lengkap)", "RAK (Rancangan Acak Kelompok)"])
        
        c_perlakuan = col_design1.selectbox("Kolom Perlakuan", df_stat.columns)
        
        if design_type == "RAK (Rancangan Acak Kelompok)":
            kelompok_options = [c for c in df_stat.columns if c != c_perlakuan]
            c_kelompok = col_design1.selectbox("Kolom Kelompok/Blok", kelompok_options, index=0 if kelompok_options else None)
        else:
            c_kelompok = None
            
        # MULTI-SELECT TARGET
        c_hasil_list = col_design2.multiselect(
            "Pilih Variabel Target (Y) - Bisa Lebih dari 1:",
            [c for c in df_stat.columns if c not in [c_perlakuan, c_kelompok]],
            default=default_target if default_target else None
        )
            
        if st.button("📊 Hitung Batch Analysis (Semua Variabel)", type="primary"):
            if not c_hasil_list:
                st.error("Pilih setidaknya satu variabel target.")
                st.stop()
            
            # Validation for RAK design
            if design_type == "RAK (Rancangan Acak Kelompok)" and c_kelompok is None:
                st.error("⚠️ Untuk desain RAK, Anda harus memilih Kolom Kelompok/Blok!")
                st.stop()
                
            st.divider()
            
            summary_results = []
            
            # 🔄 LOOP OVER TARGETS
            for idx, c_hasil in enumerate(c_hasil_list):
                st.markdown(f"### 📌 Analisis Variabel {idx+1}: {c_hasil}")
                
                with st.expander(f"Detail Hasil: {c_hasil}", expanded=(idx==0)):
                    try:
                        # 1. ANOVA Analysis
                        if design_type == "RAL":
                            df_anova, kt_galat, db_galat, cv = calculate_anova_ral(df_stat, c_perlakuan, c_hasil)
                            p_val = df_anova.loc[0, 'P-Value']
                        else:
                            df_anova, kt_galat, db_galat, cv = calculate_anova_rak(df_stat, c_perlakuan, c_kelompok, c_hasil)
                            p_val = df_anova.loc[1, 'P-Value']
                        
                        is_sig = p_val < 0.05
                        sig_label = "SIGNIFIKAN (Nyata)" if is_sig else "NON-SIGNIFIKAN (Tidak Nyata)"
                        
                        # Add to summary list
                        summary_results.append({
                            "Variabel": c_hasil,
                            "F-Hitung": df_anova.loc[0 if design_type=="RAL" else 1, 'F-Hitung'],
                            "P-Value": p_val,
                            "Kesimpulan": sig_label,
                            "CV (%)": cv
                        })
                        
                        col_a1, col_a2 = st.columns([2, 1])
                        with col_a1:
                            st.write("**Tabel ANOVA:**")
                            st.dataframe(df_anova.style.highlight_between(subset='P-Value', left=0, right=0.05, color='#d4edda'), use_container_width=True)
                        with col_a2:
                            st.metric("Status Hipotesis", sig_label, delta="Tolak H0" if is_sig else "Terima H0", delta_color="normal" if is_sig else "off")
                            st.caption(f"CV: {cv:.2f}%")

                        # 2. Post-Hoc (If Sig) or Just Plot
                        col_viz1, col_viz2 = st.columns(2)
                        
                        # Barplot mean
                        mean_df = df_stat.groupby(c_perlakuan)[c_hasil].agg(['mean', 'std']).reset_index()
                        fig_bar = px.bar(mean_df, x=c_perlakuan, y='mean', error_y='std', title=f"Rata-rata {c_hasil}", color=c_perlakuan)
                        col_viz1.plotly_chart(fig_bar, use_container_width=True)
                        
                        if is_sig:
                            col_viz2.success("✅ Uji Lanjut BNT 5% (Post-Hoc)")
                            means, bnt_val, matrix = calculate_bnt(df_stat, c_perlakuan, c_hasil, kt_galat, db_galat)
                            col_viz2.write(f"**Nilai Beda Nyata (BNT): {bnt_val:.3f}**")
                            col_viz2.dataframe(means.to_frame(name="Rata-rata").style.background_gradient(cmap="Greens"), use_container_width=True)
                        else:
                            col_viz2.info("ℹ️ Tidak ada uji lanjut karena P-Value > 0.05")
                            
                    except Exception as e:
                        import traceback
                        error_detail = str(e) if str(e) else traceback.format_exc()
                        st.error(f"Error pada variabel {c_hasil}: {error_detail}")
                        with st.expander("Debug Info"):
                            st.code(traceback.format_exc())

            # 🏁 FINAL SUMMARY TABLE
            st.divider()
            st.subheader("📝 Ringkasan Eksekutif (Batch Report)")
            df_sums = pd.DataFrame(summary_results)
            
            if not df_sums.empty:
                st.dataframe(
                    df_sums.style.applymap(lambda v: 'color: green; font-weight: bold' if v == 'SIGNIFIKAN (Nyata)' else 'color: gray', subset=['Kesimpulan']),
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Tidak ada hasil analisis yang berhasil dihitung. Periksa visualisasi error di atas.")
