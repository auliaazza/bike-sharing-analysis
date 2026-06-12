#MEMANGGIL LIBRARY YANG DIBUTUHKAN
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# SET CONFIG
st.set_page_config(page_title="Bike Sharing Analysis Dashboard", layout="wide")
st.title("Bike Sharing Analysis Dashboard")


# LOAD DATA
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# SIDEBAR
st.sidebar.image("dashboard/logo_bike_sharing.png" , width= 220)

#Filter Interaktif
st.sidebar.header("Filter Controls")

# 1. Filter Custome Date Range
st.sidebar.subheader("Select Date Range")
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

# Menggunakan input rentang tanggal bawaan Streamlit
date_range = st.sidebar.date_input(
    label="Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    label_visibility="collapsed"
)

# 2. Filter by Season
st.sidebar.subheader("Choose a Season")
list_season = sorted(df['season_day'].unique())

selected_season_day = st.sidebar.pills(
    label="Pilih Season",
    options=["All"] + list(list_season),
    default="All",
    label_visibility="collapsed"
)

# 3. Filter by Weather
st.sidebar.subheader("Choose a Weather")
weather_options = [
    "All",
    "Clear",
    "Mist",
    "Light Snow",
    "Light Rain",
    "Heavy Rain"
]

selected_weather = st.sidebar.radio(
    label="Select Weather",
    options=weather_options,
    index=0,
    label_visibility="collapsed"
)

# FILTER DATA (DATA PIPELINE)

# Filter Berdasarkan Tanggal Dengan Tuple (Anti-Error)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range[0], date_range[1]
else:
    start_date, end_date = min_date, max_date

filtered_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

# Filter Berdasarkan Season
if selected_season_day != "All":
    filtered_df = filtered_df[filtered_df['season_day'] == selected_season_day]

# Filter Berdasarkan Weather
if selected_weather != "All":
    filtered_df = filtered_df[filtered_df["weather_situation_hour"] == selected_weather]
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# MAIN DATA
st.write(f"Active Data Range: **{start_date}** to **{end_date}**")

# TAB
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", 
    "Usage Patterns",
    "Weather Conditions Analysis",
    "Peak Demand Hours",
    "Operational Insight"
])

# TAB 1 (OVERVIEW)
with tab1:
    st.subheader("📌 Bike Sharing Usage Overview")

    col1, col2, col3, col4, col5 = st.columns(5, border=True)
    with col1:
        st.metric(
            "Total Rentals",
            f"{filtered_df['cnt_day'].sum():,}"
        )      
    with col2:
        st.metric(
            "Average Rentals per Hour",
            int(filtered_df['cnt_hour'].mean() if not pd.isna(filtered_df['cnt_hour'].mean()) else 0)
        )
    with col3:
        if not filtered_df.empty:
            busiest_day = filtered_df.groupby('weekday_day')['cnt_day'].sum().idxmax()
            busiest_day_value = filtered_df.groupby('weekday_day')['cnt_day'].sum().max()
        else:
            busiest_day = "No Data"
            busiest_day_value = 0
            
        st.metric(
            label="Busiest Day", 
            value=str(busiest_day), 
            delta=f"{busiest_day_value:,} total rides" if busiest_day_value > 0 else None
        )
    with col4:
        if not filtered_df.empty:
            peak_hour = filtered_df.groupby('hour')['cnt_hour'].mean().idxmax()
            peak_hour_value = filtered_df.groupby('hour')['cnt_hour'].sum().max()
        else:
            peak_hour = "No Data"
            peak_hour_value = 0

        if peak_hour != "No Data":
            hour_display = f"{int(peak_hour):02d}:00"
        else:
            hour_display = "No Data"

        st.metric(
            label="Peak Hour",
            value=hour_display,
            delta=f"{peak_hour_value:,} total rides" if peak_hour_value > 0 else None
        )
    with col5:
        total = filtered_df['cnt_day'].sum()
        registered = filtered_df['registered_day'].sum()
        registered_ratio = (registered / total) * 100
    
        st.metric(
            "Member Ratio",
            f"{registered_ratio:.1f}%"
        )

    
    col1, col2 = st.columns([3, 1], border=True)
    # DAILY TREND
    with col1:
        filtered_df['dteday'] = pd.to_datetime(filtered_df['dteday'])
        daily_trend = filtered_df.groupby('dteday')['cnt_day'].sum().reset_index()
        
        st.subheader("Daily Rides Trends")
        st.line_chart(
            data=daily_trend, 
            x='dteday', 
            y='cnt_day',
            x_label='Date',
            y_label='Total Rentals',
            color=["#42A5F5"]
            )
        
    # HOURLY USAGE BY DAY TYPE
    with col2:
        st.subheader("User Type Comparison")
        
        total_casual = filtered_df['casual_day'].sum()
        total_registered = filtered_df['registered_day'].sum()
        
        if total_casual == 0 and total_registered == 0:
            st.warning("Tidak ada data untuk kombinasi filter ini.")
        else:
            labels = ['Casual Users', 'Registered Users']
            sizes = [total_casual, total_registered]
            colors = ['#90CAF9', '#2196F3']

        fig, ax = plt.subplots(figsize=(6, 6))
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors, 
            autopct='%1.1f%%', 
            startangle=90,     
            textprops=dict(color="black", fontsize=18)
        )
        
        for autotext in autotexts:
            autotext.set_color('white') 
            autotext.set_weight('bold')
            
        ax.axis('equal')  
        plt.tight_layout()
        
        st.pyplot(fig)
        
    
    col1, col2, col3 = st.columns(3)
    #TEMPERATURE IMPACT
    with col1:
        st.subheader("Impact of Temperature on Daily Rentals")
        fig = px.scatter(
            filtered_df,
            x='temp_norm_day',
            y='cnt_day',
            color='season_hour',
            opacity=0.5
        )
        fig.update_layout(
            xaxis_tittle='Normalized Temperature',
            yaxis_title='Total Daily Rentals'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    #WEATHER IMPACT
    with col2:
        weather_trend = df.groupby('weather_situation_day')['cnt_day'].mean().reset_index()
        st.subheader("Rides by Weather Situation")
        st.bar_chart(
            data=weather_trend,
            x='weather_situation_day',
            y='cnt_day',
            x_label='Weather Situation',
            y_label='Average Daily Rentals'
        )
    #USER TYPE
    with col3:
        hourly_trend = filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()
        hourly_pivot = hourly_trend.pivot(index='hour', columns='workingday_hour', values='cnt_hour')

        st.subheader("Hourly Usage Trends by Day Type")
        st.bar_chart(
                data=hourly_pivot,
                x_label="Hour of the Day",
                y_label="Average Rentals"
            )

# USAGE PATTERN ANALYSIS
with tab2:
    st.subheader("📅 Rental Patterns by Time and Day Type")
   
    col1, col2 = st.columns(2)

    # Date Vs Workingday
    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
       
        sns.pointplot(
            data=filtered_df,
            x='hour',
            y='cnt_hour',
            hue='workingday_hour',
            ax=ax1
         )
        
        ax1.set_title(
         'Rental Patterns: Hour vs Working Day (1=Workingday, 0=Weekend/Libur)',
         fontsize=11
         )
        ax1.set_xlabel('Time (0–23)')
        ax1.set_ylabel('Average Rental Count')
       
        st.pyplot(fig1)
   
    #Monthly Rental Trends   
    with col1:
       fig3, ax3 = plt.subplots(figsize=(6, 4))
      
       sns.boxplot(
           data=filtered_df,
           x='month_hour',
           y='cnt_hour',
           ax=ax3
           )

       ax3.set_title(
           'Monthly Rental Trends',
           fontsize=11
        )
       ax3.set_xlabel('Month')
       ax3.set_ylabel('Rental Count')
       
       st.pyplot(fig3)
            
    # Rental Patterns by Day of the Week
    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
       
        sns.barplot(
            data=filtered_df,
            x='weekday_hour',
            y='cnt_hour',
            ax=ax2
        )
         
        ax2.set_title(
            'Rental Patterns by Day of the Week',
            fontsize=11
        )
        ax2.set_xlabel('Day (0=Sunday, 6=Saturday)')
        ax2.set_ylabel('Average Rental Count')
        
        st.pyplot(fig2)
           
    #Rental Patterns by Season
    with col2:
        fig4, ax4 = plt.subplots(figsize=(6, 4))
       
        sns.barplot(
            data=filtered_df,
            x='season_hour',
            y='cnt_hour',
            hue='holiday_hour',
            ax=ax4
        )
       
        ax4.set_title(
             'Rental Patterns by Season & Holiday',
            fontsize=11
        )
        ax4.set_xlabel('Season (1:Spring, 2:Summer, 3:Fall, 4:Winter)')
        ax4.set_ylabel('Average Rental Count')
        
        st.pyplot(fig4)

    # TREN 2011 vs 2012
    st.subheader("📈 Rental Trends: 2011 vs 2012")

    yearly = filtered_df.groupby('year_day')['cnt_day'].sum().reset_index()

    fig, ax = plt.subplots(figsize= (12, 6))
    sns.barplot(data=yearly, x='year_day', y='cnt_day', hue='year_day', legend=False)

    # Menambahkan judul dan label
    ax.set_title('Total Bike Rental Comparison (2011 vs 2012)', fontsize=15)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Total Rental Count', fontsize=12)

    # Menambahkan angka total di atas bar
    for index, row in yearly.iterrows():
        plt.text(index, row.cnt_day, f'{row.cnt_day:,}', color='black', ha="center", va="bottom")

    if filtered_df.empty:
        st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    else:
        st.pyplot(fig)
   
    # Melihat tren bulanan untuk melihat perubahan lebih detail
    df['numeric_month'] = filtered_df['dteday'].dt.month # mengambil nilai bulan dari kolom tanggal

    # Visualisasi tren bulanan
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_df, x='numeric_month', y='cnt_day', hue='year_day', marker='o', estimator=sum)

    ax.set_title('Monthly Rental Trends (2011 vs 2012)', fontsize=15)
    ax.set_xlabel('Month (1-12)', fontsize=12)
    ax.set_ylabel('Total Rentals', fontsize=12)
    ax.set_xticks(range(1, 13))
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(title='Year')
    
    st.pyplot(fig)
   


# Weather Conditions Analysis
with tab3:
    st.subheader("🌦️ Impact of Weather Conditions on Rentals")

    fig, ax = plt.subplots(figsize= (12, 6))
    sns.scatterplot(data=filtered_df, x='temp_norm_hour', y='cnt_hour', hue='weather_situation_hour', ax=ax)
    ax.set_xlabel("Temperature")
    ax.set_ylabel("Total Rentals")
   
    if filtered_df.empty:
        st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    else:
        st.pyplot(fig)

# Peak Demand Hours
with tab4:
    st.subheader("⏰ Peak Usage Hours")
    col1, col2 = st.columns (2)
    with col1:
        peak = filtered_df.groupby('hour')['cnt_hour'].mean().reset_index()
   
        fig, ax = plt.subplots(figsize= (12, 7))
        sns.lineplot(data=peak, x='hour', y='cnt_hour', marker='o', color='tab:blue')
       
        # Menambahkan detail grafik
        ax.set_title('Average Bike Rental per Hour', fontsize=15)
        ax.set_xlabel('Hour (0-23)', fontsize=12)
        ax.set_ylabel('Average Rental Count', fontsize=12)
        ax.set_xticks(range(0, 24))
        ax.grid(axis='y', linestyle='--', alpha=0.7)
    
        # Menyoroti beban tertinggi
        max_hour = peak.loc[peak['cnt_hour'].idxmax(), 'hour']
        max_val = peak['cnt_hour'].max()
        ax.annotate(f'Puncak: Jam {int(max_hour)}',
                     xy=(max_hour, max_val),
                     xytext=(max_hour+1, max_val+20),
                     arrowprops=dict(facecolor='black', shrink=0.05))
       
        if filtered_df.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        else:
            st.pyplot(fig)

    with col2:
        # Karakteristik berdasarkan tipe hari
        fig, ax = plt.subplots(figsize= (12, 6))
        sns.lineplot(data=filtered_df, x='hour', y='cnt_hour', hue='workingday_hour', marker='o', errorbar=None)
       
        ax.set_title('Hourly Demand: Working Days vs Weekends/Holidays', fontsize=15)
        ax.set_xlabel('Jam', fontsize=12)
        ax.set_ylabel('Average Rentals', fontsize=12)
        ax.set_xticks(range(0, 24))
        ax.legend(title='Workingday')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
       
        if filtered_df.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        else:
            st.pyplot(fig)

# Operational Insight
with tab5:
    st.subheader("✅ Optimal Period for Maximizing Operations")
   
    fig, axes = plt.subplots(2, 1, figsize=(15, 12))
    hourly_pattern = filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()

    #Pola Penggunaan Berdasarkan Jam dan Hari Kerja
    sns.lineplot(data=hourly_pattern, x='hour', y='cnt_hour', hue='workingday_hour', marker='o', ax=axes[0])
    axes[0].set_title('Average Bike Rental by Hour (Working Days vs Weekends)', fontsize=14)
    axes[0].set_xlabel('Hour (0-23)')
    axes[0].set_ylabel('Average Rental Count')
    axes[0].legend(['Weekends/Holidays', 'Working Days'])
    axes[0].set_xticks(range(0, 24))
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # Pengaruh Kondisi Cuaca dan Suhu
    # Menggunakan scatter plot untuk melihat hubungan suhu (temp_norm), jumlah peminjaman (cnt), dan cuaca
    sns.scatterplot(data=filtered_df, x='temp_norm_hour', y='cnt_hour', hue='weather_situation_hour', alpha=0.4, ax=axes[1])
    axes[1].set_title('Impact of Temperature and Weather Conditions on Rental Demand', fontsize=14)
    axes[1].set_xlabel('Normalized Temperature (Temp)')
    axes[1].set_ylabel('Rental Count')
    axes[1].legend(title='Weather Conditions')

    plt.tight_layout()

    if filtered_df.empty:
        st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    else:
        st.pyplot(fig)
