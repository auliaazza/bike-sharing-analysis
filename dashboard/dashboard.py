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

# SIDEBAR CONTROLS
st.sidebar.image("dashboard/logo_bike_sharing.png", width= 120)
st.sidebar.title("Bike Sharing Analysis")
st.sidebar.markdown("---")

# FILTER INTERACTIVE
st.sidebar.header("Filter Controls")

# FILTER BY DATE
min_date = df["dteday"].min().to_pydatetime()
max_date = df["dteday"].max().to_pydatetime()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range", 
    [min_date, max_date]
    )

# FILTER BY SEASON
list_season = df['season_day'].unique()
selected_season_day = st.sidebar.pills(
    "Select Season",
    options=list_season
)

# FILTER BY WEATHER
weather_options = ["All"] + sorted(df["weather_situation_hour"].unique().tolist())
selected_weather = st.sidebar.selectbox(
    "Select Weather",
    weather_options
)

# FILTERED DATAFRAME
filtered_df = df.copy()

# APPLY DATE FILTER
if isinstance(date_range, tuple) or isinstance(date_range, list):
    if len(date_range) == 2:
        # Jika user sudah selesai memilih Start Date DAN End Date
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        # Jika user baru ngeklik Start Date saja (End Date belum diklik)
        start_date = pd.to_datetime(date_range[0])
        end_date = df['dteday'].max() # Set default ke tanggal paling akhir di dataset kamu
else:
    # Antisipasi jika objek kosong
    start_date = df['dteday'].min()
    end_date = df['dteday'].max()

# Setelah aman, baru jalankan pemotongan dataframe-nya
filtered_df = df[(df['dteday'] >= start_date) & (df['dteday'] <= end_date)]

# APPLY SEASON FILTER
if selected_season:
    filtered_df = filtered_df[filtered_df["season"].isin(selected_seasson)]

# APPLY WEATHER TYPE FILTER
if selected_weather != "All":
    filtered_df = filtered_df[
        filtered_df["weather_situation_hour"] == selected_weather
    ]
