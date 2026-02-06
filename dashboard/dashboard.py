#MEMANGGIL LIBRARY YANG DIBUTUHKAN
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# SET CONFIG
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("Bike Sharing Dashboard :sparkle:")

# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# OVERVIEW
st.subheader("📌 Overview Penggunaan Bike Sharing")
st.image("https://pin.it/tnynaulNQX")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Penyewaan",
        f"{df['cnt_day'].sum():,}"
    )

with col2:
    st.metric(
        "Rata-rata Penyewaan per Jam",
        int(df['cnt_hour'].mean())
    )

with col3:
    busiest = df.loc[df['cnt_day'].idxmax(), 'dteday']
    date_formatted = f"{busiest:%d/%m/%Y}"
    st.metric(
        "Tanggal Teramai",
        date_formatted
    )

st.markdown("---")

st.subheader("📈 Tren Umum Penyewaan")

col1, col2 = st.columns(2)

with col1:
    daily_trend = df.groupby('dteday')['cnt_day'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.lineplot(data=daily_trend, x='dteday', y='cnt_day', ax=ax)
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Total Penyewaan")
    st.pyplot(fig)

with col2:
    st.subheader("🧠 Insight Overview")
    st.write("""
    Secara umum, layanan bike sharing menunjukkan pola penggunaan yang konsisten
    dengan aktivitas harian masyarakat. Terdapat variasi yang jelas berdasarkan waktu,
    jenis hari, dan kondisi eksternal, yang akan dianalisis lebih lanjut pada bagian berikutnya.
    """)

# SIDEBAR
st.sidebar.image("logo_bike_sharing.png" , width= 180)
st.sidebar.subheader("Bike Sharing Analysis Dashboard")
st.sidebar.write("""
    Dashboard analisis data untuk memahami pola penggunaan sepeda melalui visualisasi berbasis waktu.
    """)

menu = st.sidebar.radio(
    "Pilih Pertanyaan Analisis",
    [
        "1. Pola Waktu & Jenis Hari",
        "2. Pengaruh Kondisi Cuaca",
        "3. Peak Hours",
        "4. Tren 2011 vs 2012",
        "5. Periode Operasional Optimal"
    ]
)

# 1. POLA WAKTU & JENIS HARI
if menu == "1. Pola Waktu & Jenis Hari":
    st.subheader("📅 Pola Penyewaan Berdasarkan Waktu & Jenis Hari")
   
    col1, col2 = st.columns(2)

    # Jam Vs Hari Kerja
    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
       
        sns.pointplot(
            data=df,
            x='hour',
            y='cnt_hour',
            hue='workingday_hour',
            ax=ax1
         )
        
        ax1.set_title(
         'Pola Penyewaan: Jam vs Hari Kerja (1=Workingday, 0=Weekend/Libur)',
         fontsize=11
         )
        ax1.set_xlabel('Jam (0–23)')
        ax1.set_ylabel('Rata-rata Jumlah Sewa')
       
        st.pyplot(fig1)
   
    #Pola berdasarkan bulan    
    with col1:
       fig3, ax3 = plt.subplots(figsize=(6, 4))
      
       sns.boxplot(
           data=df,
           x='month_hour',
           y='cnt_hour',
           ax=ax3
           )

       ax3.set_title(
           'Distribusi Penyewaan Berdasarkan Bulan', 
           fontsize=11
        )
       ax3.set_xlabel('Bulan')
       ax3.set_ylabel('Jumlah Sewa')
       
       st.pyplot(fig3)
   
    # Pola berdasarkan hari dalam seminggu
    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
       
        sns.barplot(
            data=df,
            x='weekday_hour',
            y='cnt_hour',
            ax=ax2
        )
         
        ax2.set_title(
            'Rata-rata Penyewaan Berdasarkan Hari dalam Seminggu',
            fontsize=11
        )
        ax2.set_xlabel('Hari (0=Sunday, 6=Saturday)')
        ax2.set_ylabel('Rata-rata Jumlah Sewa')
        
        st.pyplot(fig2)
           
    #Pola berdasarkan musim
    with col2:
        fig4, ax4 = plt.subplots(figsize=(6, 4))
       
        sns.barplot(
            data=df,
            x='season_hour',
            y='cnt_hour',
            hue='holiday_hour',
            ax=ax4
        )
       
        ax4.set_title(
             'Penyewaan Berdasarkan Musim & Hari Libur',
            fontsize=11
        )
        ax4.set_xlabel('Musim (1:Spring, 2:Summer, 3:Fall, 4:Winter)')
        ax4.set_ylabel('Rata-rata Jumlah Sewa')
       
        st.pyplot(fig4)
   
    st.write("""
       Penyewaan sepeda berbeda jelas antara hari kerja dan libur.
       Hari kerja memiliki dua puncak pada pagi (±08.00) dan sore (±17.00)
       yang mencerminkan aktivitas komuter, sedangkan hari libur lebih landai
       dengan puncak siang (12.00–15.00) bersifat rekreatif. Penyewaan relatif
       stabil sepanjang minggu, sedikit meningkat pada Jumat–Sabtu.
       Secara musiman, peminjaman naik pada pertengahan tahun (Juni–September)
       dan tertinggi di musim gugur, sementara awal tahun lebih rendah.
       """)

# 2. PENGARUH KONDISI CUACA
elif menu == "2. Pengaruh Kondisi Cuaca":
    st.subheader("🌦️ Pengaruh Kondisi Cuaca terhadap Penyewaan")

    fig, ax = plt.subplots(figsize= (12, 6))
    sns.scatterplot(data=df, x='temp_norm_hour', y='cnt_hour', hue='weather_situation_hour', ax=ax)
    ax.set_xlabel("Suhu")
    ax.set_ylabel("Total Penyewaan")
   
    st.pyplot(fig)

    st.write("""
    Suhu memiliki hubungan positif dengan jumlah penyewaan,
    sementara kondisi cuaca yang lebih buruk menurunkan intensitas penggunaan.
    """)

# 3. PEAK HOURS
elif menu == "3. Peak Hours":
    st.subheader("⏰ Jam dengan Beban Tertinggi")

    peak = df.groupby('hour')['cnt_hour'].mean().reset_index()
   
    fig, ax = plt.subplots(figsize= (12, 7))
    sns.lineplot(data=peak, x='hour', y='cnt_hour', marker='o', color='tab:blue')
   
    # Menambahkan detail grafik
    ax.set_title('Rata-rata Peminjaman Sepeda per Jam', fontsize=15)
    ax.set_xlabel('Jam (0-23)', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Peminjaman', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Menyoroti beban tertinggi
    max_hour = peak.loc[peak['cnt_hour'].idxmax(), 'hour']
    max_val = peak['cnt_hour'].max()
    ax.annotate(f'Puncak: Jam {int(max_hour)}',
                 xy=(max_hour, max_val),
                 xytext=(max_hour+1, max_val+20),
                 arrowprops=dict(facecolor='black', shrink=0.05))
   
    st.pyplot(fig)

    # Karakteristik berdasarkan tipe hari
    fig, ax = plt.subplots(figsize= (12, 6))
    sns.lineplot(data=df, x='hour', y='cnt_hour', hue='workingday_hour', marker='o', errorbar=None)
   
    ax.set_title('Perbandingan Beban Jam: Hari Kerja (1) vs Akhir Pekan/Libur (0)', fontsize=15)
    ax.set_xlabel('Jam', fontsize=12)
    ax.set_ylabel('Rata-rata Jumlah Peminjaman', fontsize=12)
    ax.set_xticks(range(0, 24))
    ax.legend(title='Hari Kerja')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
   
    st.pyplot(fig)

    st.write("""
    Penyewaan sepeda mencapai puncak pada pukul 17.00–18.00 dan puncak tambahan sekitar pukul 08.00, 
    menjadikannya jam penggunaan paling krusial. Pada hari kerja, pola membentuk dua lonjakan jelas 
    saat jam berangkat dan pulang kerja yang didominasi komuter, sedangkan pada hari libur atau akhir pekan 
    pola lebih landai dengan peningkatan bertahap mulai pukul 10.00 dan puncak siang–sore (12.00–15.00) 
    untuk aktivitas rekreasi. Beban terendah terjadi pada dini hari pukul 00.00–04.00 ketika mobilitas 
    berada pada titik minimum.
    """)

# 4. TREN 2011 vs 2012
elif menu == "4. Tren 2011 vs 2012":
    st.subheader("📈 Tren Penyewaan 2011 vs 2012")

    yearly = df.groupby('year_day')['cnt_day'].sum().reset_index()

    fig, ax = plt.subplots(figsize= (12, 6))
    sns.barplot(data=yearly, x='year_day', y='cnt_day', hue='year_day', legend=False)

    # Menambahkan judul dan label
    ax.set_title('Perbandingan Total Penyewaan Sepeda (2011 vs 2012)', fontsize=15)
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel('Total Jumlah Penyewaan', fontsize=12)

    # Menambahkan angka total di atas bar
    for index, row in yearly.iterrows():
        plt.text(index, row.cnt_day, f'{row.cnt_day:,}', color='black', ha="center", va="bottom")

    st.pyplot(fig)
   
    # Melihat tren bulanan untuk melihat perubahan lebih detail
    df['numeric_month'] = df['dteday'].dt.month # mengambil nilai bulan dari kolom tanggal

    # Visualisasi tren bulanan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x='numeric_month', y='cnt_day', hue='year_day', marker='o', estimator=sum)

    ax.set_title('Tren Bulanan Penyewaan Sepeda (2011 vs 2012)', fontsize=15)
    ax.set_xlabel('Bulan (1-12)', fontsize=12)
    ax.set_ylabel('Total Penyewaan', fontsize=12)
    ax.set_xticks(range(1, 13))
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(title='Tahun')

    st.pyplot(fig)

    st.write("""
    Terlihat peningkatan signifikan pada tahun 2012,
    yang mencerminkan pertumbuhan layanan dan perubahan perilaku pengguna.
    """)

# 5. PERIODE OPERASIONAL OPTIMAL
elif menu == "5. Periode Operasional Optimal":
    st.subheader("✅ Periode Paling Optimal untuk Memaksimalkan Operasional")
   
    fig, axes = plt.subplots(2, 1, figsize=(15, 12))
    hourly_pattern = df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()

    #Pola Penggunaan Berdasarkan Jam dan Hari Kerja
    sns.lineplot(data=hourly_pattern, x='hour', y='cnt_hour', hue='workingday_hour', marker='o', ax=axes[0])
    axes[0].set_title('Rata-rata Peminjaman Sepeda Berdasarkan Jam (Hari Kerja vs Akhir Pekan)', fontsize=14)
    axes[0].set_xlabel('Jam (0-23)')
    axes[0].set_ylabel('Rata-rata Jumlah Peminjaman')
    axes[0].legend(['Akhir Pekan/Libur', 'Hari Kerja'])
    axes[0].set_xticks(range(0, 24))
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # Pengaruh Kondisi Cuaca dan Suhu
    # Menggunakan scatter plot untuk melihat hubungan suhu (temp_norm), jumlah peminjaman (cnt), dan cuaca
    sns.scatterplot(data=df, x='temp_norm_hour', y='cnt_hour', hue='weather_situation_hour', alpha=0.4, ax=axes[1])
    axes[1].set_title('Pengaruh Suhu dan Kondisi Cuaca terhadap Jumlah Peminjaman', fontsize=14)
    axes[1].set_xlabel('Suhu Normalisasi (Temp)')
    axes[1].set_ylabel('Jumlah Peminjaman')
    axes[1].legend(title='Kondisi Cuaca')

    plt.tight_layout()

    st.pyplot(fig)

    st.write("""
    Rata-rata peminjaman sepeda menunjukkan bahwa hari kerja paling optimal terjadi pada 
    jam sibuk pagi (07.00–09.00) dan sore (16.00–19.00) yang mencerminkan aktivitas komuter, 
    sementara pada akhir pekan pola lebih merata dengan puncak di tengah hari (10.00–16.00). 
    Jumlah peminjaman meningkat seiring suhu yang lebih hangat hingga batas tertentu dan mencapai 
    level tertinggi pada kondisi cuaca cerah atau berawan tipis, namun menurun drastis saat cuaca buruk 
    seperti hujan lebat atau salju. Heatmap hari–jam memperlihatkan konsentrasi peminjaman tertinggi 
    secara jelas, sehingga dapat disimpulkan bahwa periode paling optimal untuk operasional adalah 
    hari kerja saat jam sibuk serta akhir pekan di siang hari, dengan dukungan cuaca cerah dan 
             suhu yang hangat.
    """) 