# Asisten Penelitian Agronomi
# Advanced research assistant with multiple ML models and statistical analysis

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from datetime import datetime
import json

st.set_page_config(page_title="Asisten Penelitian", page_icon="🔬", layout="wide")

# ========== ML MODELS ==========
AVAILABLE_MODELS = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=1.0),
    "Polynomial Regression (deg=2)": "polynomial",
    "Decision Tree": DecisionTreeRegressor(max_depth=5, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
}

# ========== SAMPLE DATASETS ==========
def generate_sample_data(dataset_type):
    """Generate sample agricultural research data"""
    np.random.seed(42)
    n_samples = 100
    
    if dataset_type == "Yield vs NPK":
        # Yield as function of NPK
        N = np.random.uniform(50, 200, n_samples)
        P = np.random.uniform(20, 100, n_samples)
        K = np.random.uniform(30, 150, n_samples)
        
        # Yield with some noise
        yield_val = (
            2000 + 
            15 * N + 
            10 * P + 
            8 * K + 
            0.05 * N * P +
            np.random.normal(0, 300, n_samples)
        )
        
        return pd.DataFrame({
            'Nitrogen (kg/ha)': N,
            'Phosphorus (kg/ha)': P,
            'Potassium (kg/ha)': K,
            'Yield (kg/ha)': yield_val
        })
    
    elif dataset_type == "Growth vs Time":
        # Plant growth over time
        days = np.arange(0, 100, 1)
        
        # Logistic growth curve with noise
        growth = 100 / (1 + np.exp(-0.1 * (days - 50))) + np.random.normal(0, 3, len(days))
        
        return pd.DataFrame({
            'Days After Planting': days,
            'Plant Height (cm)': growth
        })
    
    elif dataset_type == "Yield vs Weather":
        # Yield as function of weather
        rainfall = np.random.uniform(800, 2500, n_samples)
        temp = np.random.uniform(20, 35, n_samples)
        humidity = np.random.uniform(50, 90, n_samples)
        
        # Optimal ranges
        optimal_rain = 1500
        optimal_temp = 27
        optimal_humidity = 70
        
        # Yield decreases with distance from optimal
        yield_val = (
            5000 -
            0.5 * abs(rainfall - optimal_rain) -
            100 * abs(temp - optimal_temp) -
            10 * abs(humidity - optimal_humidity) +
            np.random.normal(0, 200, n_samples)
        )
        
        return pd.DataFrame({
            'Rainfall (mm)': rainfall,
            'Temperature (°C)': temp,
            'Humidity (%)': humidity,
            'Yield (kg/ha)': yield_val
        })

# ========== STATISTICAL ANALYSIS ==========
def perform_statistical_analysis(df, target_col):
    """Perform comprehensive statistical analysis"""
    stats = {}
    
    # Descriptive statistics
    stats['descriptive'] = df.describe()
    
    # Correlation matrix
    stats['correlation'] = df.corr()
    
    # Target variable stats
    if target_col in df.columns:
        stats['target_mean'] = df[target_col].mean()
        stats['target_std'] = df[target_col].std()
        stats['target_min'] = df[target_col].min()
        stats['target_max'] = df[target_col].max()
    
    return stats

def train_and_evaluate_models(X, y, model_names):
    """Train multiple models and compare performance"""
    results = []
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    for model_name in model_names:
        if model_name == "Polynomial Regression (deg=2)":
            # Polynomial features
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            
            # Predictions
            y_pred = model.predict(X_poly)
            
            # Metrics
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            mae = mean_absolute_error(y, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_poly, y, cv=5, scoring='r2')
            
        else:
            model = AVAILABLE_MODELS[model_name]
            
            # Train
            model.fit(X_scaled, y)
            
            # Predictions
            y_pred = model.predict(X_scaled)
            
            # Metrics
            r2 = r2_score(y, y_pred)
            rmse = np.sqrt(mean_squared_error(y, y_pred))
            mae = mean_absolute_error(y, y_pred)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
        
        results.append({
            'Model': model_name,
            'R² Score': r2,
            'RMSE': rmse,
            'MAE': mae,
            'CV Mean R²': cv_scores.mean(),
            'CV Std R²': cv_scores.std()
        })
    
    return pd.DataFrame(results)

# ========== MAIN APP ==========
st.title("🔬 Asisten Penelitian Agronomi")
st.markdown("**Advanced research assistant dengan multiple ML models dan analisis statistik**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 📊 7 model ML berbeda (Linear, Ridge, Lasso, Polynomial, Decision Tree, Random Forest, Gradient Boosting)
    - 📈 Analisis statistik komprehensif
    - 🔍 Model comparison & evaluation
    - 📉 Visualisasi interaktif
    - 💾 Export hasil penelitian
    
    **Workflow:**
    1. Pilih atau upload dataset
    2. Pilih variabel target (Y)
    3. Pilih features (X)
    4. Pilih model ML untuk dibandingkan
    5. Analisis hasil & visualisasi
    6. Export laporan
    
    **Use Cases:**
    - Analisis pengaruh NPK terhadap hasil panen
    - Prediksi pertumbuhan tanaman
    - Optimasi kondisi lingkungan
    - Penelitian agronomi lainnya
    """)

# Data Source Selection
st.subheader("📁 Sumber Data")

data_source = st.radio(
    "Pilih sumber data:",
    ["Sample Dataset", "Upload CSV"],
    horizontal=True
)

if data_source == "Sample Dataset":
    dataset_type = st.selectbox(
        "Pilih sample dataset:",
        ["Yield vs NPK", "Growth vs Time", "Yield vs Weather"]
    )
    
    df = generate_sample_data(dataset_type)
    st.success(f"✅ Loaded sample dataset: {dataset_type}")
    
else:
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} rows from uploaded file")
    else:
        st.info("👆 Upload CSV file untuk mulai analisis")
        st.stop()

# Display data
with st.expander("👀 Preview Data", expanded=False):
    st.dataframe(df.head(10), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

# Variable Selection
st.markdown("---")
st.subheader("🎯 Konfigurasi Analisis")

col1, col2 = st.columns(2)

with col1:
    target_col = st.selectbox(
        "Variabel Target (Y) - yang ingin diprediksi:",
        options=df.columns.tolist(),
        help="Pilih kolom yang ingin diprediksi"
    )

with col2:
    feature_cols = st.multiselect(
        "Variabel Features (X) - yang mempengaruhi:",
        options=[col for col in df.columns if col != target_col],
        default=[col for col in df.columns if col != target_col][:3],
        help="Pilih kolom yang digunakan untuk prediksi"
    )

if not feature_cols:
    st.warning("⚠️ Pilih minimal 1 feature untuk analisis")
    st.stop()

# Model Selection
st.markdown("---")
st.subheader("🤖 Pilih Model ML")

selected_models = st.multiselect(
    "Pilih model untuk dibandingkan:",
    options=list(AVAILABLE_MODELS.keys()),
    default=["Linear Regression", "Random Forest", "Gradient Boosting"],
    help="Pilih minimal 1 model"
)

if not selected_models:
    st.warning("⚠️ Pilih minimal 1 model")
    st.stop()

# Analysis Button
if st.button("🔍 Mulai Analisis", type="primary", use_container_width=True):
    
    with st.spinner("Melakukan analisis..."):
        # Prepare data
        X = df[feature_cols].values
        y = df[target_col].values
        
        # Statistical Analysis
        stats = perform_statistical_analysis(df, target_col)
        
        # Train models
        model_results = train_and_evaluate_models(X, y, selected_models)
    
    # Display Results
    st.markdown("---")
    st.subheader("📊 Hasil Analisis")
    
    # Statistical Summary
    with st.expander("📈 Statistik Deskriptif", expanded=True):
        st.dataframe(stats['descriptive'], use_container_width=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", f"{stats['target_mean']:.2f}")
        with col2:
            st.metric("Std Dev", f"{stats['target_std']:.2f}")
        with col3:
            st.metric("Min", f"{stats['target_min']:.2f}")
        with col4:
            st.metric("Max", f"{stats['target_max']:.2f}")
    
    # Correlation Matrix
    with st.expander("🔗 Matriks Korelasi"):
        fig = px.imshow(
            stats['correlation'],
            labels=dict(color="Correlation"),
            x=stats['correlation'].columns,
            y=stats['correlation'].columns,
            color_continuous_scale='RdBu_r',
            aspect="auto"
        )
        fig.update_layout(title="Correlation Matrix", height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Model Comparison
    st.markdown("---")
    st.subheader("🏆 Perbandingan Model")
    
    # Sort by R² score
    model_results_sorted = model_results.sort_values('R² Score', ascending=False)
    
    # Display table
    st.dataframe(
        model_results_sorted.style.highlight_max(
            subset=['R² Score', 'CV Mean R²'],
            color='lightgreen'
        ).highlight_min(
            subset=['RMSE', 'MAE'],
            color='lightgreen'
        ),
        use_container_width=True,
        hide_index=True
    )
    
    # Best model
    best_model = model_results_sorted.iloc[0]
    st.success(f"""
    🥇 **Model Terbaik: {best_model['Model']}**
    - R² Score: {best_model['R² Score']:.4f}
    - RMSE: {best_model['RMSE']:.2f}
    - MAE: {best_model['MAE']:.2f}
    - Cross-Validation R²: {best_model['CV Mean R²']:.4f} ± {best_model['CV Std R²']:.4f}
    """)
    
    # Visualization
    st.markdown("---")
    st.subheader("📊 Visualisasi")
    
    tab1, tab2, tab3 = st.tabs(["Model Performance", "Feature Importance", "Predictions"])
    
    with tab1:
        # Bar chart of R² scores
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=model_results_sorted['Model'],
            y=model_results_sorted['R² Score'],
            name='R² Score',
            marker_color='#3b82f6',
            text=model_results_sorted['R² Score'].round(4),
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=model_results_sorted['Model'],
            y=model_results_sorted['CV Mean R²'],
            name='CV Mean R²',
            marker_color='#10b981',
            text=model_results_sorted['CV Mean R²'].round(4),
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Model Performance Comparison",
            xaxis_title="Model",
            yaxis_title="R² Score",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # RMSE comparison
        fig2 = go.Figure()
        
        fig2.add_trace(go.Bar(
            x=model_results_sorted['Model'],
            y=model_results_sorted['RMSE'],
            marker_color='#f59e0b',
            text=model_results_sorted['RMSE'].round(2),
            textposition='auto'
        ))
        
        fig2.update_layout(
            title="RMSE Comparison (Lower is Better)",
            xaxis_title="Model",
            yaxis_title="RMSE",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # Feature importance (for tree-based models)
        st.markdown("**Feature Importance Analysis**")
        
        if "Random Forest" in selected_models:
            # Train Random Forest to get feature importance
            from sklearn.ensemble import RandomForestRegressor
            rf = RandomForestRegressor(n_estimators=100, random_state=42)
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            rf.fit(X_scaled, y)
            
            importance_df = pd.DataFrame({
                'Feature': feature_cols,
                'Importance': rf.feature_importances_
            }).sort_values('Importance', ascending=False)
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=importance_df['Importance'],
                y=importance_df['Feature'],
                orientation='h',
                marker_color='#8b5cf6',
                text=importance_df['Importance'].round(4),
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Feature Importance (Random Forest)",
                xaxis_title="Importance",
                yaxis_title="Feature",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Feature importance hanya tersedia untuk tree-based models (Random Forest, Gradient Boosting)")
    
    with tab3:
        # Actual vs Predicted
        st.markdown("**Actual vs Predicted Values**")
        
        # Use best model for predictions
        best_model_name = best_model['Model']
        
        if best_model_name == "Polynomial Regression (deg=2)":
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            y_pred = model.predict(X_poly)
        else:
            model = AVAILABLE_MODELS[best_model_name]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            model.fit(X_scaled, y)
            y_pred = model.predict(X_scaled)
        
        # Scatter plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=y,
            y=y_pred,
            mode='markers',
            name='Predictions',
            marker=dict(size=8, color='#3b82f6', opacity=0.6)
        ))
        
        # Perfect prediction line
        min_val = min(y.min(), y_pred.min())
        max_val = max(y.max(), y_pred.max())
        
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=f"Actual vs Predicted ({best_model_name})",
            xaxis_title=f"Actual {target_col}",
            yaxis_title=f"Predicted {target_col}",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Residuals
        residuals = y - y_pred
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=y_pred,
            y=residuals,
            mode='markers',
            marker=dict(size=8, color='#10b981', opacity=0.6)
        ))
        
        fig2.add_hline(y=0, line_dash="dash", line_color="red")
        
        fig2.update_layout(
            title="Residual Plot",
            xaxis_title=f"Predicted {target_col}",
            yaxis_title="Residuals",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Export Results
    st.markdown("---")
    st.subheader("💾 Export Hasil Penelitian")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export model comparison
        csv_models = model_results.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Model Comparison (CSV)",
            data=csv_models,
            file_name=f"model_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Export predictions
        predictions_df = pd.DataFrame({
            'Actual': y,
            'Predicted': y_pred,
            'Residual': residuals
        })
        
        csv_predictions = predictions_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Predictions (CSV)",
            data=csv_predictions,
            file_name=f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    # Research Summary
    st.markdown("---")
    st.subheader("📝 Ringkasan Penelitian")
    
    summary = f"""
    **Dataset:** {len(df)} samples, {len(df.columns)} variables
    
    **Target Variable:** {target_col}
    - Mean: {stats['target_mean']:.2f}
    - Std Dev: {stats['target_std']:.2f}
    - Range: [{stats['target_min']:.2f}, {stats['target_max']:.2f}]
    
    **Features:** {', '.join(feature_cols)}
    
    **Models Tested:** {len(selected_models)}
    
    **Best Model:** {best_model['Model']}
    - R² Score: {best_model['R² Score']:.4f}
    - RMSE: {best_model['RMSE']:.2f}
    - MAE: {best_model['MAE']:.2f}
    - Cross-Validation R²: {best_model['CV Mean R²']:.4f} ± {best_model['CV Std R²']:.4f}
    
    **Interpretation:**
    - R² Score menunjukkan bahwa model dapat menjelaskan {best_model['R² Score']*100:.1f}% variasi dalam data
    - RMSE rata-rata error prediksi adalah {best_model['RMSE']:.2f} unit
    - Cross-validation menunjukkan model konsisten dengan R² {best_model['CV Mean R²']:.4f}
    """
    
    st.text_area("Copy summary ini untuk laporan penelitian:", summary, height=400)

# Footer
st.markdown("---")
st.caption("""
🔬 **Asisten Penelitian Agronomi** - Advanced ML toolkit untuk penelitian pertanian.
Gunakan hasil analisis ini sebagai dasar penelitian, bukan kesimpulan final.
Validasi hasil dengan data lapangan dan konsultasi dengan ahli statistik.
""")
