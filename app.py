import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="StockSense Dashboard",
    page_icon="📦",
    layout="wide"
)

# --- LOAD DATA CLEANED ---
@st.cache_data
def load_data():
    df_demand = pd.read_csv('clean_master_demand.csv', parse_dates=['Date'])
    df_rfm = pd.read_csv('clean_rfm_scored.csv')
    return df_demand, df_rfm

try:
    df_demand, df_rfm = load_data()
except FileNotFoundError:
    st.error("❌ File data tidak ditemukan! Pastikan 'clean_master_demand.csv' dan 'clean_rfm_scored.csv' ada di folder yang sama.")
    st.stop()

# --- HEADER UTAMA ---
st.title("📦 StockSense: Demand Forecasting & Customer Segmentation")
st.markdown("**Coding Camp 2026 — DBS Foundation | Tim CC26-PSU032**")
st.write("Dashboard operasional cerdas untuk membantu retail UMKM mengoptimalkan manajemen stok dan strategi retensi pelanggan.")
st.markdown("---")

# --- STRUKTUR TABS (TRACK A & TRACK B) ---
tab_overview, tab_track_a, tab_track_b = st.tabs([
    "📊 Ringkasan Bisnis", 
    "📈 Track A: Demand Forecasting", 
    "👥 Track B: Customer RFM Segmentation"
])

# ==============================================================================
# TAB 1: OVERVIEW
# ==============================================================================
with tab_overview:
    st.header("Metrik Utama Toko")
    
    # Hitung KPI Ringkas
    total_rev = df_demand['Amount'].sum()
    total_qty = df_demand['Quantity'].sum()
    total_cust = df_rfm['Customer ID'].nunique()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pendapatan (IDR)", f"Rp {total_rev:,.0f}")
    col2.metric("Total Produk Terjual", f"{total_qty:,} Unit")
    col3.metric("Total Pelanggan Aktif", f"{total_cust:,} Customer")
    
    st.markdown("### Preview Data Master")
    st.dataframe(df_demand.head(10), use_container_width=True)

# ==============================================================================
# TAB 2: TRACK A - DEMAND FORECASTING
# ==============================================================================
with tab_track_a:
    st.header("Analisis Tren Penjualan & Faktor Eksternal")
    
    # Filter Kategori Produk
    categories = df_demand['Category'].unique().tolist()
    selected_cat = st.selectbox("Pilih Kategori Produk untuk Analisis Tren:", ["Semua Kategori"] + categories)
    
    # Filter Data berdasarkan pilihan
    if selected_cat == "Semua Kategori":
        df_filtered = df_demand
    else:
        df_filtered = df_demand[df_demand['Category'] == selected_cat]

    # Visualisasi 1: Tren Penjualan Harian
    st.subheader(f"Tren Penjualan Harian - {selected_cat}")
    fig_line, ax_line = plt.subplots(figsize=(12, 4))
    df_trend = df_filtered.groupby('Date')['Quantity'].sum().reset_index()
    ax_line.plot(df_trend['Date'], df_trend['Quantity'], color='steelblue', linewidth=2)
    ax_line.set_ylabel("Unit Terjual")
    st.pyplot(fig_line)

    # Visualisasi 2: Dampak Lingkungan (Bivariate Analysis)
    st.subheader("Analisis Dampak Lingkungan terhadap Kuantitas Penjualan")
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.markdown("**Pengaruh Kondisi Cuaca**")
        fig_box1, ax_box1 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df_filtered, x='Weather Condition', y='Quantity', ax=ax_box1, palette='muted')
        st.pyplot(fig_box1)
        
    with col_plot2:
        st.markdown("**Pengaruh Hari Libur / Promo**")
        fig_box2, ax_box2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df_filtered, x='Holiday/Promotion', y='Quantity', ax=ax_box2, palette='Set2')
        ax_box2.set_xticklabels(['Hari Biasa', 'Libur / Promo'])
        st.pyplot(fig_box2)

# ==============================================================================
# TAB 3: TRACK B - CUSTOMER SEGMENTATION
# ==============================================================================
with tab_track_b:
    st.header("Segmentasi Perilaku Pelanggan (RFM Framework)")
    
    # Hitung distribusi segmen
    seg_counts = df_rfm['Segment'].value_counts()
    
    col_rfm1, col_rfm2 = st.columns([1, 2])
    
    with col_rfm1:
        st.subheader("Proporsi Jumlah Pelanggan")
        st.dataframe(seg_counts.to_frame('Jumlah Customer'), use_container_width=True)
        
    with col_rfm2:
        st.subheader("Distribusi Ruang Pelanggan: Recency vs Monetary")
        
        # Grafik Scatter Plot yang sudah kamu buat kemarin
        fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
        segment_colors = {
            'Champions': '#2196F3',
            'Loyal Customers': '#4CAF50',
            'Recent Customers': '#00BCD4',
            'At Risk': '#FF9800',
            'Lost Customers': '#F44336',
            'Big Spenders': '#9C27B0',
            'Potential Loyalists': '#795548',
        }

        for seg, grp in df_rfm.groupby('Segment'):
            ax_scatter.scatter(grp['Recency'], grp['Monetary'],
                        label=seg, alpha=0.7, s=60,
                        color=segment_colors.get(seg, 'gray'))

        ax_scatter.set_xlabel('Recency (Hari sejak transaksi terakhir)')
        ax_scatter.set_ylabel('Monetary (Total Belanja)')
        ax_scatter.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
        ax_scatter.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rp {x/1e6:.1f}M'))
        st.pyplot(fig_scatter)