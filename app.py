import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="StockSense | Business Insight", page_icon="📈", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df_demand = pd.read_csv('clean_master_demand.csv', parse_dates=['Date'])
    df_rfm = pd.read_csv('clean_rfm_scored.csv')
    return df_demand, df_rfm

df_demand, df_rfm = load_data()

# --- SIDEBAR PRESENTASI ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2850/2850343.png", width=100)
    st.title("Project Navigator")
    st.info("""
    **Tim CC26-PSU032**
    *Proyek StockSense*
    
    Dashboard ini digunakan untuk mendemonstrasikan validasi data dan temuan bisnis awal (Business Understanding) sebelum tahap pemodelan AI.
    """)
    st.markdown("---")
    st.write("**Goal Minggu Ini:**")
    st.write("✅ Data Wrangling & Cleaning")
    st.write("✅ Validasi Faktor Eksternal")
    st.write("✅ Segmentasi Pelanggan Riil")

# --- HEADER PRESENTASI ---
st.title("🚀 StockSense: Revolusi Inventaris UMKM")
st.markdown("""
**Masalah Utama:** UMKM kehilangan **potensi pendapatan** karena kehabisan stok (*Understock*) atau **modal macet** karena barang tidak laku (*Overstock*).
Dashboard ini membuktikan bahwa **Data** punya jawaban untuk masalah tersebut.
""")
st.markdown("---")

# --- TAB STRATEGY ---
tab1, tab2, tab3 = st.tabs([
    "🚩 Problem & Market Overview", 
    "⛈️ Why We Need AI? (External Factors)", 
    "🎯 Who is Our Customer? (RFM Strategy)"
])

# ==============================================================================
# TAB 1: OVERVIEW (MENJELASKAN SKALA MASALAH)
# ==============================================================================
with tab1:
    st.header("1. Skala Operasional & Fluktuasi Pasar")
    col1, col2, col3 = st.columns(3)
    
    total_rev = df_demand['Amount'].sum()
    total_qty = df_demand['Quantity'].sum()
    
    with col1:
        st.metric("Volume Transaksi", f"{total_qty:,} Unit")
        st.caption("Total perputaran barang yang harus dikelola stoknya.")
    with col2:
        st.metric("Total Revenue", f"Rp {total_rev:,.0f}")
        st.caption("Besaran aliran dana yang berisiko jika stok macet.")
    with col3:
        st.metric("Kategori Produk", f"{df_demand['Category'].nunique()}")
        st.caption("Kompleksitas produk yang tidak bisa diatur manual.")

    st.subheader("Tren Penjualan: Bukti Fluktuasi Pasar")
    selected_cat = st.selectbox("Simulasi: Pilih kategori untuk melihat ketidakpastian stok:", df_demand['Category'].unique())
    
    df_trend = df_demand[df_demand['Category'] == selected_cat].groupby('Date')['Quantity'].sum().reset_index()
    fig_trend, ax_trend = plt.subplots(figsize=(12, 4))
    ax_trend.plot(df_trend['Date'], df_trend['Quantity'], color='#2196F3', linewidth=2)
    st.pyplot(fig_trend)
    
    st.success(f"**Business Insight:** Penjualan kategori **{selected_cat}** sangat fluktuatif. Tanpa prediksi, pemilik toko akan kesulitan menentukan berapa banyak barang yang harus dipesan minggu depan.")

# ==============================================================================
# TAB 2: EXTERNAL FACTORS (VALIDASI KEBUTUHAN AI)
# ==============================================================================
with tab2:
    st.header("2. Validasi Kebutuhan AI: Faktor Eksternal")
    st.markdown("""
    *Business Understanding:* Mengapa pemilik toko tidak bisa cuma pakai 'insting'? 
    Karena ada faktor luar seperti **Cuaca** dan **Hari Libur** yang memengaruhi mood belanja.
    """)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Dampak Cuaca")
        fig_weather, ax_w = plt.subplots()
        sns.boxplot(data=df_demand[df_demand['Category'] == selected_cat], x='Weather Condition', y='Quantity', ax=ax_w)
        st.pyplot(fig_weather)
        st.warning("**Insight Cuaca:** Kondisi cuaca tertentu terbukti menggeser median penjualan. AI kita akan menggunakan data ramalan cuaca sebagai fitur input.")

    with col_b:
        st.subheader("Dampak Hari Libur & Promo")
        fig_h, ax_h = plt.subplots()
        sns.boxplot(data=df_demand[df_demand['Category'] == selected_cat], x='Holiday/Promotion', y='Quantity', ax=ax_h)
        ax_h.set_xticklabels(['Hari Biasa', 'Libur/Promo'])
        st.pyplot(fig_h)
        st.warning("**Insight Promo:** Lonjakan pada hari libur menunjukkan pola musiman. StockSense akan memberikan 'Smart Alert' sebelum tanggal libur tiba.")

# ==============================================================================
# TAB 3: CUSTOMER SEGMENTATION (STRATEGI RETENSI)
# ==============================================================================
with tab3:
    st.header("3. Segmentasi Pelanggan: Siapa yang Menghasilkan Uang?")
    st.markdown("Analisis RFM membantu kita tahu pelanggan mana yang harus diprioritaskan saat stok terbatas.")
    
    col_rfm_a, col_rfm_b = st.columns([1, 2])
    
    with col_rfm_a:
        st.subheader("Data Segmen Pelanggan")
        st.write(df_rfm['Segment'].value_counts().to_frame("Jumlah Customer"))
        st.info("""
        **Rekomendasi Bisnis:**
        * **Champions:** Jatah stok utama & Program Loyalitas.
        * **At Risk:** Kirim kupon diskon agar mereka kembali belanja.
        """)

    with col_rfm_b:
        st.subheader("Visualisasi Posisi Pelanggan")
        fig_rfm, ax_rfm = plt.subplots(figsize=(10, 6))
        colors = {'Champions': '#2196F3', 'Loyal Customers': '#4CAF50', 'At Risk': '#FF9800', 'Lost Customers': '#F44336', 'Big Spenders': '#9C27B0', 'Recent Customers': '#00BCD4', 'Potential Loyalists': '#795548'}
        
        for seg, grp in df_rfm.groupby('Segment'):
            ax_rfm.scatter(grp['Recency'], grp['Monetary'], label=seg, alpha=0.6, s=100, color=colors.get(seg, 'gray'))
        
        ax_rfm.set_xlabel("Recency (Hari)")
        ax_rfm.set_ylabel("Monetary (IDR)")
        ax_rfm.legend(bbox_to_anchor=(1, 1))
        ax_rfm.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        st.pyplot(fig_rfm)

# --- FOOTER ROADMAP ---
st.markdown("---")
st.subheader("🏁 Roadmap Selanjutnya")
col_next1, col_next2, col_next3 = st.columns(3)
col_next1.write("🛠️ **AI Modeling:** Melatih model demand forecasting menggunakan data yang sudah tervalidasi di atas.")
col_next2.write("🌐 **Web Integration:** Menyerahkan API model ke tim Full-Stack (Hazim & Ray).")
col_next3.write("📱 **End Product:** Website utama akan menampilkan hasil prediksi AI berdasarkan analisis DS ini.")
