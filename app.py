import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="StockSense | Final Presentation", page_icon="📈", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df_demand = pd.read_csv('clean_master_demand.csv', parse_dates=['Date'])
    df_rfm = pd.read_csv('clean_rfm_scored.csv')
    return df_demand, df_rfm

df_demand, df_rfm = load_data()

# --- SIDEBAR PRESENTASI FINAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2850/2850343.png", width=100)
    st.title("StockSense Analytics")
    st.subheader("Tim CC26-PSU032")
    st.markdown("""
    **Data Science Deliverables:**
    * ✅ End-to-End Data Wrangling
    * ✅ Feature Engineering (Weather & Holiday)
    * ✅ Customer RFM Segmentation
    """)
    st.markdown("---")
    st.success("🎯 Status Track: **100% Completed**")

# --- HEADER PRESENTASI FINAL ---
st.title("🚀 StockSense: Hasil Analisis Data & Strategi Bisnis Retail UMKM")
st.markdown("""
**Presentasi Final Capstone Project — Coding Camp 2026 Powered by DBS Foundation**
Dashboard ini menyajikan kesimpulan analitik (Business Insights) yang mendasari pengembangan kecerdasan buatan dan integrasi sistem pada web utama *StockSense*.
""")
st.markdown("---")

# --- TAB STRATEGY (BERSIFAT KESIMPULAN AKHIR) ---
tab1, tab2, tab3 = st.tabs([
    "📊 Kesimpulan Tren & Kompleksitas Pasar", 
    "⛈️ Validasi Fitur Eksternal (AI Input)", 
    "🎯 Hasil Akhir Segmentasi Pelanggan (RFM)"
])

# ==============================================================================
# TAB 1: MARKET OVERVIEW
# ==============================================================================
with tab1:
    st.header("1. Analisis Volume & Fluktuasi Pasar")
    st.markdown("*Kesimpulan Business Understanding:* Retail UMKM memiliki tingkat kompleksitas produk yang tinggi, membuat manajemen stok manual sangat berisiko terhadap kerugian finansial.")
    
    col1, col2, col3 = st.columns(3)
    total_rev = df_demand['Amount'].sum()
    total_qty = df_demand['Quantity'].sum()
    
    with col1:
        st.metric("Total Volume Transaksi", f"{total_qty:,} Unit")
    with col2:
        st.metric("Total Finansial Terkelola", f"Rp {total_rev:,.0f}")
    with col3:
        st.metric("Total Kategori Produk", f"{df_demand['Category'].nunique()} Kategori")

    st.subheader("Visualisasi Tren Fluktuasi Penjualan")
    selected_cat = st.selectbox("Pilih Kategori Produk untuk Menampilkan Tren:", df_demand['Category'].unique())
    
    df_trend = df_demand[df_demand['Category'] == selected_cat].groupby('Date')['Quantity'].sum().reset_index()
    fig_trend, ax_trend = plt.subplots(figsize=(12, 3.5))
    ax_trend.plot(df_trend['Date'], df_trend['Quantity'], color='#2196F3', linewidth=2)
    ax_trend.set_ylabel("Unit Terjual")
    st.pyplot(fig_trend)
    
    st.info(f"💡 **Temuan Kunci:** Data historis menunjukkan penjualan kategori **{selected_cat}** memiliki pola naik-turun yang tajam. Hal ini memvalidasi bahwa penentuan stok berbasis intuisi tidak efektif, sehingga diperlukan model prediktif berbasis AI.")

# ==============================================================================
# TAB 2: EXTERNAL FACTORS
# ==============================================================================
with tab2:
    st.header("2. Pembuktian Pengaruh Faktor Eksternal")
    st.markdown("""
    *Kesimpulan Analisis Data:* Pengujian statistik dan visualisasi data membuktikan secara nyata bahwa **Kondisi Cuaca** dan **Hari Libur/Promo** memiliki korelasi kuat terhadap volume penjualan produk.
    """)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Analisis Distribusi Kuantitas Berdasarkan Cuaca")
        fig_weather, ax_w = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df_demand[df_demand['Category'] == selected_cat], x='Weather Condition', y='Quantity', ax=ax_w, palette='Blues')
        st.pyplot(fig_weather)
        st.write("👉 **Insight:** Pergeseran nilai median penjualan pada cuaca tertentu membuktikan bahwa faktor atmosferik wajib dimasukkan sebagai *fitur input* penting dalam melatih model kecerdasan buatan (AI Forecasting).")

    with col_b:
        st.subheader("Analisis Dampak Hari Libur & Kampanye Promo")
        fig_h, ax_h = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df_demand[df_demand['Category'] == selected_cat], x='Holiday/Promotion', y='Quantity', ax=ax_h, palette='Oranges')
        ax_h.set_xticklabels(['Hari Biasa', 'Libur/Promo'])
        st.pyplot(fig_h)
        st.write("👉 **Insight:** Terjadi lonjakan volume penjualan yang signifikan pada hari libur nasional. Data ini berhasil diolah sebagai komponen musiman untuk memicu fitur *Smart Alert* ketersediaan stok.")

# ==============================================================================
# TAB 3: CUSTOMER SEGMENTATION
# ==============================================================================
with tab3:
    st.header("3. Hasil Segmentasi Perilaku Pelanggan (RFM)")
    st.markdown("Dengan memetakan profil pelanggan, retail UMKM dapat mengambil keputusan strategis terkait prioritas alokasi stok ketika ketersediaan barang di gudang sedang terbatas.")
    
    col_rfm_a, col_rfm_b = st.columns([1, 2])
    
    with col_rfm_a:
        st.subheader("Distribusi Segmen Pelanggan")
        st.dataframe(df_rfm['Segment'].value_counts().to_frame("Jumlah Customer"), use_container_width=True)
        st.success("""
        🎯 **Rekomendasi Strategi Bisnis Terapan:**
        1. **Champions (Loyalitas Tertinggi):** Berikan prioritas jatah stok utama dan program *reward* eksklusif.
        2. **At Risk (Hampir Kehilangan):** Aktifkan promosi terarah (*targeted marketing*) melalui aplikasi web untuk mengembalikan kebiasaan belanja mereka.
        """)

    with col_rfm_b:
        st.subheader("Pemetaan Ruang Pelanggan: Recency vs Monetary")
        fig_rfm, ax_rfm = plt.subplots(figsize=(10, 6))
        colors = {'Champions': '#2196F3', 'Loyal Customers': '#4CAF50', 'At Risk': '#FF9800', 'Lost Customers': '#F44336', 'Big Spenders': '#9C27B0', 'Recent Customers': '#00BCD4', 'Potential Loyalists': '#795548'}
        
        for seg, grp in df_rfm.groupby('Segment'):
            ax_rfm.scatter(grp['Recency'], grp['Monetary'], label=seg, alpha=0.6, s=100, color=colors.get(seg, 'gray'))
        
        ax_rfm.set_xlabel("Recency (Hari sejak transaksi terakhir)")
        ax_rfm.set_ylabel("Monetary (Total Nilai Belanja - IDR)")
        ax_rfm.legend(bbox_to_anchor=(1, 1), title="Segmen Pelanggan")
        ax_rfm.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        st.pyplot(fig_rfm)

# --- FOOTER INTEGRASI SISTEM (MENJELASKAN HUBUNGAN KE WEB UTAMA) ---
st.markdown("---")
st.subheader("🔗 Arsitektur Integrasi & End Product")
st.markdown("""
Bagaimana hasil kerja **Data Science Track** ini terhubung ke produk akhir website *StockSense*?
1. **Pondasi Fitur:** Variabel cuaca, hari libur, dan tren kategori yang divalidasi di sini telah sukses diekstraksi menjadi data latih untuk model **AI Demand Forecasting (LSTM/GRU)** yang dikembangkan oleh tim AI Engineer.
2. **Implementasi ke Web Utama (Full-Stack):** Logika visualisasi tren, filter kategori, serta hasil segmentasi pelanggan (RFM) ini diserahkan kepada tim Full-Stack (Hazim & Ray) sebagai *blueprint* visual untuk membangun antarmuka web akhir yang diakses langsung oleh pemilik UMKM.
""")
