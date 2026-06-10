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

# ==============================================================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (WARNA PALET & STYLE KAPSUL)
# ==============================================================================
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

st.markdown("""
    <style>
    /* Mengubah warna tombol kapsul (st.pills) yang sedang aktif menjadi Biru #87AECE */
    div[data-testid="stBaseButton-pillsActiveElements"] {
        background-color: #87AECE !important;
        color: white !important;
        border-color: #87AECE !important;
    }
    
    /* Mengubah warna tombol kapsul yang tidak aktif menjadi Abu-abu #EDEDED */
    div[data-testid="stBaseButton-pillsNeutralElements"] {
        background-color: #EDEDED !important;
        color: #5A6A85 !important;
        border-color: #EDEDED !important;
    }

    /* Mengubah warna border input tanggal saat aktif */
    div[data-testid="stDateInput"] input:focus {
        border-color: #87AECE !important;
        box-shadow: 0 0 0 0.2rem rgba(135, 174, 206, 0.25) !important;
    }

    /* Mengubah warna teks judul kategori filter di sidebar (Biru Gelap #1D2A62) */
    .filter-label {
        font-weight: 600;
        color: #1D2A62;
        font-size: 14px;
        margin-top: 18px;
        margin-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================
# 3. AREA SIDEBAR FILTER (TAMPILAN UI KAPSUL BALUT)
# ==============================================================================
st.sidebar.title("Filter")

# --- KATEGORI 1: Filter by Date Range (Preset Cepat) ---
st.sidebar.markdown('<p class="filter-label">Filter by Date Range</p>', unsafe_allow_html=True)
date_preset = st.sidebar.pills(
    label="Preset Tanggal", 
    options=["Last 30 Days", "Last 6 Months"],
    label_visibility="collapsed"
)

# --- KATEGORI 2: Custome Date Range ---
st.sidebar.markdown('<p class="filter-label">Custome Date Range</p>', unsafe_allow_html=True)

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

# --- KATEGORI 3: Filter by Season ---
st.sidebar.markdown('<p class="filter-label">Filter by Season</p>', unsafe_allow_html=True)
list_season = sorted(df['season_day'].unique())
selected_season_day = st.sidebar.pills(
    label="Pilih Season",
    options=["All"] + list(list_season),
    default="All",
    label_visibility="collapsed"
)

# --- KATEGORI 4: Filter by Weather ---
st.sidebar.markdown('<p class="filter-label">Filter by Weather</p>', unsafe_allow_html=True)
weather_options = ["All"] + sorted(df["weather_situation_hour"].unique().tolist())
selected_weather = st.sidebar.pills(
    label="Select Weather",
    options=weather_options,
    default="All",
    label_visibility="collapsed"
)


# ==============================================================================
# 4. LOGIKA PROSES FILTER DATA (DATA PIPELINE)
# ==============================================================================

# A. Ambil nilai tanggal dari widget date_input dengan PENGAMAN TUPLE (Anti-Error)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range[0], date_range[1]
else:
    start_date, end_date = min_date, max_date

# B. Logika tombol Preset Cepat (Jika diklik, menimpa rentang tanggal di atas)
if date_preset == "Last 30 Days":
    start_date = max_date - datetime.timedelta(days=30)
    end_date = max_date
elif date_preset == "Last 6 Months":
    start_date = max_date - datetime.timedelta(days=180)
    end_date = max_date

# C. Eksekusi Pemotongan Data (Filtering DataFrame)
# Filter Berdasarkan Tanggal
filtered_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

# Filter Berdasarkan Season
if selected_season_day != "All":
    filtered_df = filtered_df[filtered_df['season_day'] == selected_season_day]

# Filter Berdasarkan Weather
if selected_weather != "All":
    filtered_df = filtered_df[filtered_df["weather_situation_hour"] == selected_weather]
