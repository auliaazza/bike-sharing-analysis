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
weather_options = ["All"] + sorted(df["weather_situation_hour"].unique().tolist())
selected_weather = st.sidebar.pills(
    label="Select Weather",
    options=weather_options,
    default="All",
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

# MAIN DATA
st.write(f"Active Data Range: **{start_date}** to **{end_date}**")

# Membuat 5 tab sesuai request kamu
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "Usage Patterns",
    "Weather Conditions Analysis",
    "Peak Demand Hours",
    "Operational Insight"
])
