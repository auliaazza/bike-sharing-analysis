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
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

section[data-testid="stSidebar"] {
    background-color: #F8F9FA;
    border-right: 1px solid #EAEAEA;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 700;
    color: #2C3E50;
    text-align: center;
}

.sidebar-subtitle {
    font-size: 14px;
    color: #7F8C8D;
    text-align: center;
    margin-bottom: 20px;
}

.filter-header {
    font-size: 16px;
    font-weight: 600;
    margin-top: 15px;
    margin-bottom: 5px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    # Logo
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2972/2972185.png",
        width=80
    )

    st.markdown(
        '<p class="sidebar-title">Bike Sharing Dashboard</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sidebar-subtitle">Data Analysis Project</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # =====================
    # DATE FILTER
    # =====================
    st.markdown(
        '<p class="filter-header">📅 Date Range</p>',
        unsafe_allow_html=True
    )

    start_date = st.date_input(
        "Start Date",
        value=date(2011, 1, 1)
    )

    end_date = st.date_input(
        "End Date",
        value=date(2012, 12, 31)
    )

    # =====================
    # SEASON FILTER
    # =====================
    st.markdown(
        '<p class="filter-header">🌱 Season</p>',
        unsafe_allow_html=True
    )

    selected_season = st.multiselect(
        "Choose Season",
        options=[
            "Spring",
            "Summer",
            "Fall",
            "Winter"
        ],
        default=[
            "Spring",
            "Summer",
            "Fall",
            "Winter"
        ]
    )

    # =====================
    # WEATHER FILTER
    # =====================
    st.markdown(
        '<p class="filter-header">🌤 Weather</p>',
        unsafe_allow_html=True
    )

    selected_weather = st.multiselect(
        "Choose Weather",
        options=[
            "Clear",
            "Mist",
            "Light Snow/Rain",
            "Heavy Rain"
        ],
        default=[
            "Clear",
            "Mist",
            "Light Snow/Rain",
            "Heavy Rain"
        ]
    )

    st.divider()

    st.info(
        f"""
        Date Range:
        {start_date}
        sampai
        {end_date}
        """
    )

# =========================
# MAIN PAGE
# =========================

st.title("🚲 Bike Sharing Dashboard")

st.write("Dashboard Content Here")
