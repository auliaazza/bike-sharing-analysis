#MEMANGGIL LIBRARY YANG DIBUTUHKAN
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px # type: ignore

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
        
    #USER TYPE
    with col2:
        st.subheader("User Type Comparison")
        user_df = pd.DataFrame({
            "User Type": ["Casual Users", "Registered Users"],
            "Count": [
                filtered_df["casual_day"].sum(),
                filtered_df["registered_day"].sum()
                ]
            })
        
        fig = px.pie(
            user_df,
            names="User Type",
            values="Count",
            hole=0.5  # donut chart
            )

        fig.update_traces(
            textinfo="percent",
            textfont_size=14
        )

        fig.update_layout(
            legend=dict(
                orientation="h",      # horizontal
                y=-0.15,              # posisi di bawah chart
                x=0.5,
                xanchor="center"
            ),
            annotations=[
                dict(
                text="Users",
                x=0.5,
                y=0.5,
                font_size=16,
                showarrow=False
                )
            ]      
        )

        st.plotly_chart(fig, use_container_width=True)
        

    col1, col2 = st.columns([1, 2], border=True)
    
    #WEATHER IMPACT
    with col1:
        st.subheader("Weather Situation Distribution")
        weather_dist = (
            filtered_df['weather_situation_day']
            .value_counts()
            .reset_index()
        )
        
        weather_dist.columns = ['weather_situation_day', 'count']

        fig = px.pie(
            weather_dist,
            names='weather_situation_day',
            values='count'
        )
        fig.update_layout(
            legend=dict(
                orientation="h",      # horizontal
                y=-0.15,              # posisi di bawah chart
                x=0.5,
                xanchor="center"
                )
        )

        st.plotly_chart(fig, use_container_width=True)
    
    #TEMPERATURE IMPACT
    with col2:
        st.subheader("Temperature vs. Rental Trends")
        filtered_df['temp_category'] = pd.cut(
            filtered_df['temp_norm_day'],
            bins=[0, 0.33, 0.66, 1],
            labels=['Low', 'Medium', 'High']
        )
            
        fig = px.scatter(
            filtered_df,
            x='temp_norm_day',
            y='cnt_day',
            color='temp_category',
            opacity=0.5
        )
        fig.update_layout(
            xaxis_title='Normalized Temperature',
            yaxis_title='Total Daily Rentals'
        )
            
        st.plotly_chart(fig, use_container_width=True)
    
    # HOURLY USAGE BY DAY TYPE
    with st.container(border=True):
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
   
    col1, col2, col3, col4 = st.columns(4, border=True)

    # Date Vs Workingday
    with col1:
        hourly_pattern = (
            filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour']
            .mean()
            .reset_index()
        )
        fig = px.line(
            hourly_pattern,
            x='hour',
            y='cnt_hour',
            color='workingday_hour',
            markers=True
        )
        fig.update_layout(
            title='Rental Patterns: Hour vs Working Day',
            xaxis_title='Hour',
            yaxis_title='Average Rental Count'
        )
        st.plotly_chart(fig, use_container_width=True)
   
    #Monthly Rental Trends   
    with col2:
       monthly_trend =(
           filtered_df.groupby('month_day')['cnt_day']
           .mean()
           .reset_index()
       )
       fig = px.line(
            monthly_trend,
            x='month_day',
            y='cnt_day',
            markers=True,
            title='Monthly Rental Trends'
        )
       fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Average Rental Count'
        )
       st.plotly_chart(fig, use_container_width=True)
            
    # Rental Patterns by Day of the Week
    with col3:
        weekday_trend = (
            filtered_df.groupby('weekday_hour')['cnt_hour']
            .mean()
            .reset_index()
        )
        fig = px.bar(
            weekday_trend,
            x='weekday_hour',
            y='cnt_hour',
            title='Rental Patterns by Day of the Week'
        )
        fig.update_layout(
            xaxis_title='Day',
            yaxis_title='Average Rental Count'
        )
        st.plotly_chart(fig, use_container_width=True)
           
    #Rental Patterns by Season
    with col4:
        season_trend = (
            filtered_df.groupby(['season_hour', 'holiday_hour'])['cnt_hour']
            .mean()
            .reset_index()
        )
        fig = px.bar(
            season_trend,
            x='season_hour',
            y='cnt_hour',
            color='holiday_hour',
            barmode='group',
            title='Rental Patterns by Season & Holiday'
        )
        fig.update_layout(
            xaxis_title='Season',
            yaxis_title='Average Rental Count',
            legend_title='Holiday'
        )
        st.plotly_chart(fig, use_container_width=True)

    # TREN 2011 vs 2012
    st.subheader("📈 Rental Trends: 2011 vs 2012")

    col1, col2 = st.columns(2, border=True)
    with col1:
        yearly =(
            filtered_df.groupby('year_day')['cnt_day']
            .sum()
            .reset_index()
        )
        fig = px.bar(
            yearly,
            x='year_day',
            y='cnt_day',
            text='cnt_day',
            title='Total Bike Rental Comparison (2011 vs 2012)'
        )
        fig.update_traces(
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Rental Count',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
   
    #Tren bulanan
    with col2:
        monthly_trend = (
            filtered_df.groupby(['numeric_month', 'year_day'])['cnt_day']
            .sum()
            .reset_index()
        )
        fig = px.line(
            monthly_trend,
            x='numeric_month',
            y='cnt_day',
            color='year_day',
            markers=True,
            title='Monthly Rental Trends (2011 vs 2012)'
        )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Rentals',
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13))
            ),
            legend_title='Year'
        )
        st.plotly_chart(fig, use_container_width=True)
   

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
