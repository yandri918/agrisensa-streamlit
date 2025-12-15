
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="AgriSensa Intelligence",
    page_icon="📊",
    layout="wide"
)

# HELPER FUNCTIONS
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Gagal memuat file: {e}")
        return None

# CUSTOM CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .kpi-val { font-size: 2rem; font-weight: bold; color: #4f46e5; }
    .kpi-lbl { color: #6b7280; font-size: 0.9rem; }
    h1, h2, h3 { color: #4338ca; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>📊 AgriSensa Intelligence (ASI)</h1><p>Platform Analisis Data Pertanian Mandiri (Self-Service BI)</p></div>', unsafe_allow_html=True)

# SIDEBAR CONFIG
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload File Laporan (Excel/CSV)", type=["xlsx", "xls", "csv"])

# MAIN LOGIC
if uploaded_file is not None:
    # 1. LOAD DATA
    df = load_data(uploaded_file)
    
    if df is not None:
        # DATA PREVIEW (EXPANDER)
        with st.expander("🔍 Preview Data Mentah", expanded=False):
            st.dataframe(df, use_container_width=True)
            
        # 2. DATA PROFILING (KPIs)
        st.markdown("### 📈 Ringkasan Data")
        c1, c2, c3, c4 = st.columns(4)
        
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        c1.markdown(f'<div class="kpi-card"><div class="kpi-val">{df.shape[0]:,}</div><div class="kpi-lbl">Total Baris</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi-card"><div class="kpi-val">{df.shape[1]}</div><div class="kpi-lbl">Total Kolom</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(num_cols)}</div><div class="kpi-lbl">Kolom Angka</div></div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(cat_cols)}</div><div class="kpi-lbl">Kolom Kategori</div></div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 3. CHART BUILDER INTERFACE
        col_settings, col_chart = st.columns([1, 3])
        
        with col_settings:
            st.markdown("### 🛠️ Chart Builder")
            st.info("Atur visualisasi di sini:")
            
            chart_type = st.selectbox("Jenis Grafik", ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Area Chart", "Histogram"])
            
            x_axis = st.selectbox("Sumbu X (Kategori/Waktu)", options=df.columns)
            y_axis = st.selectbox("Sumbu Y (Nilai)", options=num_cols)
            
            color_dim = st.selectbox("Warna/Group (Opsional)", options=["None"] + cat_cols)
            if color_dim == "None": color_dim = None
            
            st.markdown("---")
            agg_func = st.selectbox("Agregasi Data", ["Sum (Total)", "Average (Rata-rata)", "Count (Jumlah Data)", "Raw (Tanpa Agregasi)"])
            
            st.caption("Tips: Gunakan 'Sum' untuk total panen, 'Average' untuk rata-rata harga.")

        # 4. PLOTTING LOGIC
        with col_chart:
            st.markdown(f"### 🖼️ Visualisasi: {chart_type}")
            
            # Data Processing based on Aggregation
            if agg_func != "Raw (Tanpa Agregasi)":
                try:
                    if color_dim:
                        group_cols = [x_axis, color_dim]
                    else:
                        group_cols = [x_axis]
                        
                    if agg_func == "Sum (Total)":
                        plot_df = df.groupby(group_cols)[y_axis].sum().reset_index()
                    elif agg_func == "Average (Rata-rata)":
                        plot_df = df.groupby(group_cols)[y_axis].mean().reset_index()
                    elif agg_func == "Count (Jumlah Data)":
                        plot_df = df.groupby(group_cols)[y_axis].count().reset_index()
                except Exception as e:
                    st.warning(f"Gagal melakukan agregasi: {e}. Menampilkan data raw.")
                    plot_df = df
            else:
                plot_df = df
            
            # Chart Generation
            try:
                if chart_type == "Bar Chart":
                    fig = px.bar(plot_df, x=x_axis, y=y_axis, color=color_dim, barmode='group', template="plotly_white")
                elif chart_type == "Line Chart":
                    fig = px.line(plot_df, x=x_axis, y=y_axis, color=color_dim, markers=True, template="plotly_white")
                elif chart_type == "Area Chart":
                    fig = px.area(plot_df, x=x_axis, y=y_axis, color=color_dim, template="plotly_white")
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(plot_df, x=x_axis, y=y_axis, color=color_dim, size=y_axis, template="plotly_white")
                elif chart_type == "Pie Chart":
                    fig = px.pie(plot_df, names=x_axis, values=y_axis, color=color_dim, hole=0.4, template="plotly_white")
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x_axis, color=color_dim, template="plotly_white")
                
                # Customize Layout
                fig.update_layout(height=500, title_text=f"{agg_func} of {y_axis} by {x_axis}")
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Gagal membuat grafik. Pastikan kolom yang dipilih sesuai tipe datanya.\nError: {e}")

else:
    # EMPTY STATE
    st.info("👋 **Selamat Datang di AgriSensa Intelligence!**")
    st.markdown("""
    Silakan upload file **Excel (.xlsx)** atau **CSV** di sidebar sebelah kiri untuk memulai analisis.
    
    **Contoh File yang bisa dianalisa:**
    - Laporan Panen (Tanggal, Komoditas, Berat, Harga)
    - Data Cuaca (Tanggal, Suhu, Curah Hujan)
    - Stok Gudang (Item, Jumlah, Expired Date)
    """)
    
    # Generate Dummy Data Button
    if st.button("🔽 Gunakan Contoh Data Dummy"):
        dummy_data = {
            "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun"],
            "Komoditas": ["Padi", "Padi", "Padi", "Padi", "Padi", "Padi", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung"],
            "Hasil_Panen_Ton": [12.5, 10.2, 15.1, 14.0, 11.5, 13.2, 8.5, 9.1, 8.8, 9.5, 10.2, 9.8],
            "Harga_Jual_Rp": [5500, 5600, 5400, 5500, 5700, 5600, 4500, 4600, 4500, 4700, 4800, 4600],
            "Biaya_Produksi_Juta": [15, 14, 16, 15, 14, 15, 8, 9, 8, 9, 10, 9]
        }
        df_dummy = pd.DataFrame(dummy_data)
        csv = df_dummy.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Data Contoh (CSV)",
            data=csv,
            file_name="contoh_data_pertanian.csv",
            mime="text/csv",
        )
        st.success("Silakan download file di atas lalu upload ke sidebar!")

# Footer
st.markdown("---")
st.caption("AgriSensa Intelligence v1.0 - Powered by Plotly & Pandas")
