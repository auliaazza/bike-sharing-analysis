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
    opttions=list_season,
    default=list_season
)

# FILTER BY USER TYPE
list_user_type = df["user_type"].unique()
selected_user_type = st.sidebar.selectbox(
    "Select Usser Type",
    options=["All"] + list_user_type
)

# FILTERED DATAFRAME
filtered_df = df.copy()

# APPLY DATE FILTER
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])

filtered_df = filtered_df[
    (filtered_df["dteday"] >= start_date) &
    (filtered_df["dteday"] <= end_date)
]
# APPLY SEASON FILTER
if selected_season:
    filtered_df = filtered_df[filtered_df["season"].isin(selected_seasson)]

# APPLY USER TYPE FILTER
if selected_user_type != "All":
    filtered_df = filtered_df[filtered_df["user_type"] == selected_user_type]
