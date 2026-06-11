#MEMANGGIL LIBRARY YANG DIBUTUHKAN
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
st.sidebar.subheader("Filter by Date Range")
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

# Menggunakan input rentang tanggal bawaan Streamlit
date_range = st.sidebar.date_input(
    label="Pilih Rentang",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    label_visibility="collapsed"
)

# 2. Filter by Season
st.sidebar.subheader("Filter by Season")
list_season = sorted(df['season_day'].unique())

selected_season_day = st.sidebar.pills(
    label="Pilih Season",
    options=["All"] + list(list_season),
    default="All",
    label_visibility="collapsed"
)

# 3. Filter by Weather
st.sidebar.subheader("Filter by Weather")
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

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(
            "Total Rentals",
            f"{df['cnt_day'].sum():,}"
        )
    with col2:
        st.metric(
            "Average Rentals per Hour",
            int(df['cnt_hour'].mean())
        )
    with col3:
        busiest_day = df.groupby('weekday_day')['cnt_day'].sum().idxmax()
        st.metric(
            "Busiest Day",
            busiest_day
        )
    with col4:
        peak_hour = df.groupby('hour')['cnt_hour'].mean().idxmax() 
        st.metric(
            "Peak Hours",
            f"{peak_hour}:00"
        )
    with col5:
        total = df['cnt_day'].sum()
        registered = df['registered_day'].sum()
        registered_ratio = (registered / total) * 100
    
        st.metric(
            "Member Ratio",
            f"{registered_ratio:.1f}%"
        )

    
    col1, col2 = st.columns(2)
    # DAILY TREND
    with col1:
        df['dteday'] = pd.to_datetime(df['dteday'])
        daily_trend = df.groupby('dteday')['cnt_day'].sum().reset_index()
        
        st.subheader("Daily Rides Trends")
        st.line_chart(
            data=daily_trend, 
            x='dteday', 
            y='cnt_day',
            x_label='Date',
            y_label='Total Rentals'
            )
    # HOURLY USAGE BY DAY TYPE
    with col2:
        hourly_trend = df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()
        hourly_pivot = hourly_trend.pivot(index='hour', columns='workingday_hour', values='cnt_hour')

        st.subheader("Hourly Usage Trends by Day Type")
        st.bar_chart(
                data=hourly_pivot,
                color=["#b0bec5", "#1d2a62"], # Urutan warna: Abu-abu untuk Weekend, Biru Tua untuk Working Day
                x_label="Hour of the Day",
                y_label="Average Rentals"
            )
    
    col1, col2, col3 = st.columns(3)
    #TEMPERATURE IMPACT
    st.subheader("Impact of Temperature on Daily Rentals")
    fig = px.scatter(
                df,
                x="temp_norm_day",    # Sumbu X: Suhu yang sudah dinormalisasi
                y="cnt_day",         # Sumbu Y: Total rental harian
                color="demand_level", # Titik-titik akan berwarna berdasarkan tingkat permintaan
                color_discrete_sequence=['#1d2a62', '#2496B4', '#b0bec5'], # Skema warna biru tua kamu
                labels={
                    "temp_norm_day": "Normalized Temperature",
                    "cnt_day": "Total Daily Rentals",
                    "demand_level": "Demand Level"
                },
                opacity=0.7          # Membuat titik agak transparan agar penumpukan data terlihat
                )
        st.plotly_chart(fig, use_container_width=True)
