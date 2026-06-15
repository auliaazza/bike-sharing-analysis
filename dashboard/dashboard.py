#MEMANGGIL LIBRARY YANG DIBUTUHKAN
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime

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
min_date = datetime.date(2011, 1, 1)
max_date = datetime.date(2012, 12, 31)

col1,col2= st.sidebar.columns (2, border=True)
with col1:
    start_date = st.date_input(
        label="Start date",
        value=min_date,          # Nilai awal langsung di-set ke awal data (1 Jan 2011)
        min_value=min_date,      # Batas minimum kalender
        max_value=max_date,      # Batas maksimum kalender
        format="DD/MM/YYYY"
    )

with col2:
    end_date = st.date_input(
        label="End date",
        value=max_date,          # Nilai awal langsung di-set ke akhir data (31 Des 2012)
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY"
    )

# 2. Filter by Season
st.sidebar.subheader("Choose a Season")
list_season = sorted(df['season_day'].unique())

selected_season_day = st.sidebar.segmented_control(
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
    "Misty",
    "Light Rain/Snow",
    "Heavy Rain/Snow"
]

selected_weather = st.sidebar.radio(
    label="Select Weather",
    options=weather_options,
    index=0,
    label_visibility="collapsed"
)

# FILTER DATA (DATA PIPELINE)

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

    
    col1, col2 = st.columns([2.8, 1.2], border=True)
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
            color=["#42A5F5"],
            height=350
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
            ],
            height=350            
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
                ),
            height=350
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
            yaxis_title='Total Daily Rentals',
            height=350
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
            y_label="Average Rentals",
            height=350
        )
        

# USAGE PATTERN ANALYSIS
with tab2:
    st.subheader("📅 Rental Patterns by Time and Day Type")
   
    # Date Vs Workingday
    with st.container(border=True):
        st.subheader("Rental Patterns: Hour vs Working Day")
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
            xaxis_title='Hour',
            yaxis_title='Average Rental Count'
        )
        fig.update_xaxes(
            tickmode='linear',
            tick0=0,
            dtick=1
        )
        st.plotly_chart(fig, use_container_width=True)
   
    col1, col2, col3 = st.columns(3, border=True)
    #Monthly Rental Trends   
    with col1:
       st.subheader("Monthly Rental Trends")
       monthly_trend =(
           filtered_df.groupby('month_day')['cnt_day']
           .mean()
           .reset_index()
       )
       fig = px.line(
            monthly_trend,
            x='month_day',
            y='cnt_day',
            markers=True
        )
       fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Average Rental Count'
        )
       st.plotly_chart(fig, use_container_width=True)
            
    # Rental Patterns by Day of the Week
    with col2:
        st.subheader("Rental Patterns by Day of the Week")
        weekday_trend = (
            filtered_df.groupby('weekday_hour')['cnt_hour']
            .mean()
            .reset_index()
        )
        fig = px.bar(
            weekday_trend,
            x='weekday_hour',
            y='cnt_hour',
            color='cnt_hour'
        )
        fig.update_layout(
            xaxis_title='Day',
            yaxis_title='Average Rental Count'
        )
        st.plotly_chart(fig, use_container_width=True)
           
    #Rental Patterns by Season
    with col3:
        st.subheader("Rental Patterns by Season & Holiday")
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
            barmode='group'
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
        st.subheader("Total Bike Rental Comparison (2011 vs 2012)")
        yearly =(
            filtered_df.groupby('year_day')['cnt_day']
            .sum()
            .reset_index()
        )
        fig = px.bar(
            yearly,
            x='year_day',
            y='cnt_day',
            text='cnt_day'
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
        st.subheader("Monthly Rental Trends (2011 vs 2012)")
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
            markers=True
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
    
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.subheader("Temperature vs Rentals")
        if filtered_df.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        else:
            fig = px.scatter(
                filtered_df,
                x="temp_norm_hour",
                y="cnt_hour",
                color="weather_situation_hour",
                labels={
                    "temp_norm_hour": "Temperature",
                    "cnt_hour": "Total Rentals",
                    "weather_situation_hour": "Weather"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
    #Average Rentals by Weather Condition
    with col2:
        st.subheader("Average Rentals by Weather Condition")
        weather_avg =(
            filtered_df.groupby("weather_situation_hour")["cnt_hour"]
            .mean()
            .reset_index()
        )
        fig2 = px.bar(
            weather_avg,
            x="weather_situation_hour",
            y="cnt_hour",
            text="cnt_hour",
            labels={
                "weather_situation_hour": "Weather Condition",
                "cnt_hour": "Average Rentals"
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

# Peak Demand Hours
with tab4:
    st.subheader("⏰ Peak Usage Hours")
    col1, col2 =st.columns(2, border=True)
    with col1:
        st.subheader("Average Bike Rental per Hour")
        if filtered_df.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")

        else:
            peak = (
                filtered_df.groupby("hour")["cnt_hour"]
                .mean()
                .reset_index()
            )
            fig = px.line(
                peak,
                x="hour",
                y="cnt_hour",
                markers=True,
                labels={
                    "hour": "Hour (0–23)",
                    "cnt_hour": "Average Rental Count"
                }
            )
            max_row = peak.loc[peak["cnt_hour"].idxmax()]

            fig.add_annotation(
                x=max_row["hour"],
                y=max_row["cnt_hour"],
                text=f"Puncak: Jam {int(max_row['hour'])}",
                showarrow=True,
                arrowhead=2
            )
            fig.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig, use_container_width=True)

    #Working Day vs Weekend
    with col2:
        st.subheader("Hourly Demand: Working Days vs Weekends/Holidays")
        if filtered_df.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        else:
            hourly = (
                filtered_df
                .groupby(["hour", "workingday_hour"])["cnt_hour"]
                .mean()
                .reset_index()
            )
            fig = px.line(
                hourly,
                x="hour",
                y="cnt_hour",
                color="workingday_hour",
                markers=True,
                labels={
                    "hour": "Hour",
                    "cnt_hour": "Average Rentals",
                    "workingday_hour": "Working Day"
                }
            )
            fig.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig, use_container_width=True)

# Operational Insight
with tab5:
    st.subheader("✅ Optimal Period for Maximizing Operations")
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.subheader("Average Bike Rental by Hour (Working Days vs Weekends)")
        if filtered_df.empty:
            st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
        else:
            hourly_pattern =(
                filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour']
                .mean()
                .reset_index()
            )
            fig = px.line(
                hourly_pattern, 
                x='hour', 
                y='cnt_hour', 
                color='workingday_hour',
                markers=True,
                labels={'hour': 'Hour (0-23)', 'cnt_hour': 'Average Rental Count', 'workingday_hour': 'Day Type'}
            )
            fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
            st.plotly_chart(fig, use_container_width=True)

    #Pengaruh Kondisi Cuaca dan Suhu
    with col2:
        st.subheader("Impact of Weather and Temperature on Rental Demand")
        fig = px.scatter(
            filtered_df, 
            x='temp_norm_hour', 
            y='cnt_hour', 
            color='weather_situation_hour',
            opacity=0.5,
            labels={'temp_norm_hour': 'Normalized Temperature (Temp)', 'cnt_hour': 'Rental Count', 'weather_situation_hour': 'Weather'}
        )
        st.plotly_chart(fig, use_container_width=True)
