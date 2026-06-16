#Import All Library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime

# Page Configuration
st.set_page_config(page_title="Bike Sharing Analytics Dashboard", layout="wide")
st.title("Bike Sharing Analytics Dashboard")

# Data Loader
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

with st.sidebar:
    st.markdown("# Filter Controls")
    
    # Date Range Filter
    st.markdown("## Date Range")
    min_date = datetime.date(2011, 1, 1)
    max_date = datetime.date(2012, 12, 31)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            label="Start Date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            format="DD/MM/YYYY"
        ) 
    with col2:
        end_date = st.date_input(
            label="End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            format="DD/MM/YYYY"
        )
               
    # Season Filter
    st.markdown("## Season")
    list_season = sorted(df['season_day'].unique())

    selected_season_day = st.segmented_control(
        label="Select Season",
        options=["All"] + list(list_season),
        default="All",
        label_visibility="collapsed"
    )

    # Weather Condition Filter
    st.markdown("## Weather Condition")
    weather_options = [
        "All",
        "Clear",
        "Misty",
        "Light Rain/Snow",
        "Heavy Rain/Snow"
    ]

    selected_weather = st.radio(
        label="Select Weather",
        options=weather_options,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown(" ### Connect with Me")
    col1, col2 = st.columns([3.5, 5.5], gap="small")
    with col1:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/azzahraa248")
    with col2:
        st.link_button("Github", "https://github.com/auliaazza/bike-sharing-analysis")

# Filtered Data
filtered_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]

if selected_season_day != "All":
    filtered_df = filtered_df[filtered_df['season_day'] == selected_season_day]

if selected_weather != "All":
    filtered_df = filtered_df[filtered_df["weather_situation_hour"] == selected_weather]

    
# Main Dashboard Active Range
st.write(f"Active Data Range: **{start_date.strftime('%d %b %Y')}** to **{end_date.strftime('%d %b %Y')}**")

# Dashboard Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", 
    "Usage Patterns",
    "Weather Impact",
    "Peak Demand",
    "Operational Insights"
])

# Overview Tab
with tab1:
    st.subheader("📌 Executive Performance Summary")

    col1, col2, col3, col4, col5 = st.columns(5, border=True)
    with col1:
        st.metric(
            label="Total Rentals",
            value=f"{filtered_df['cnt_day'].sum():,}"
        )      
    with col2:
        st.metric(
            label="Avg. Hourly Rentals",
            value=int(filtered_df['cnt_hour'].mean() if not pd.isna(filtered_df['cnt_hour'].mean()) else 0)
        )
    with col3:
        if not filtered_df.empty:
            busiest_day = filtered_df.groupby('weekday_day')['cnt_day'].sum().idxmax()
            busiest_day_value = filtered_df.groupby('weekday_day')['cnt_day'].sum().max()
        else:
            busiest_day = "No Data"
            busiest_day_value = 0
            
        st.metric(
            label="Busiest Day of Week", 
            value=str(busiest_day), 
            delta=f"{busiest_day_value:,} rides" if busiest_day_value > 0 else None
        )
    with col4:
        if not filtered_df.empty:
            peak_hour = filtered_df.groupby('hour')['cnt_hour'].mean().idxmax()
            peak_hour_value = filtered_df.groupby('hour')['cnt_hour'].sum().max()
        else:
            peak_hour = "No Data"
            peak_hour_value = 0

        hour_display = f"{int(peak_hour):02d}:00" if peak_hour != "No Data" else "No Data"

        st.metric(
            label="Peak Hour",
            value=hour_display,
            delta=f"{peak_hour_value:,} total rides" if peak_hour_value > 0 else None
        )
    with col5:
        total = filtered_df['cnt_day'].sum()
        registered = filtered_df['registered_day'].sum()
        registered_ratio = (registered / total) * 100 if total > 0 else 0
    
        st.metric(
            label="Registered Member Ratio",
            value=f"{registered_ratio:.1f}%"
        )

    col1, col2 = st.columns([2.8, 1.2], border=True)
    with col1:
        daily_trend = filtered_df.groupby('dteday')['cnt_day'].sum().reset_index()
        st.subheader("Daily Rental Timeline")
        st.line_chart(
            data=daily_trend, 
            x='dteday', 
            y='cnt_day',
            x_label='Date',
            y_label='Total Rentals',
            color=["#42A5F5"],
            height=350
        )
        
    with col2:
        st.subheader("User Segmentation")
        user_df = pd.DataFrame({
            "User Type": ["Casual Users", "Registered Members"],
            "Total Volume": [
                filtered_df["casual_day"].sum(),
                filtered_df["registered_day"].sum()
            ]
        })
        
        fig = px.pie(
            user_df,
            names="User Type",
            values="Total Volume",
            hole=0.5
        )
        fig.update_traces(textinfo="percent", textfont_size=14)
        fig.update_layout(
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
            annotations=[dict(text="Users", x=0.5, y=0.5, font_size=16, showarrow=False)],
            height=350            
        )
        st.plotly_chart(fig, use_container_width=True)
        
    col1, col2 = st.columns([1, 2], border=True)
    with col1:
        st.subheader("Weather Condition Share")
        weather_dist = filtered_df['weather_situation_day'].value_counts().reset_index()
        weather_dist.columns = ['Weather Condition', 'Record Count']

        fig = px.pie(
            weather_dist,
            names='Weather Condition',
            values='Record Count'
        )
        fig.update_layout(
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Temperature vs. Rental Volume")
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
            opacity=0.5,
            labels={
                'temp_norm_day': 'Normalized Temperature',
                'cnt_day': 'Daily Rentals',
                'temp_category': 'Temp Level'
            }
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container(border=True):
        st.subheader("Average Hourly Demand by Day Type")
        hourly_trend = filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()
        hourly_pivot = hourly_trend.pivot(index='hour', columns='workingday_hour', values='cnt_hour')

        st.bar_chart(
            data=hourly_pivot,
            x_label="Hour of the Day",
            y_label="Average Rental Count",
            height=350
        )

# Usage Patterns Tab
with tab2:
    st.subheader("📅 Chronological Rental Pattern Analysis")
   
    with st.container(border=True):
        st.subheader("Hourly Distribution: Working Days vs. Weekends")
        hourly_pattern = filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()
        fig = px.line(
            hourly_pattern,
            x='hour',
            y='cnt_hour',
            color='workingday_hour',
            markers=True,
            labels={
                'hour': 'Hour of Day (24h format)',
                'cnt_hour': 'Avg. Rental Count',
                'workingday_hour': 'Day Classification'
            }
        )
        fig.update_layout(height=300)
        fig.update_xaxes(tickmode='linear', tick0=0, dtick=1)
        st.plotly_chart(fig, use_container_width=True)
   
    col1, col2, col3 = st.columns(3, border=True)
    with col1:
        st.subheader("Monthly Historical Trends")
        monthly_trend = filtered_df.groupby('month_day')['cnt_day'].mean().reset_index()
        fig = px.line(
            monthly_trend,
            x='month_day',
            y='cnt_day',
            markers=True,
            labels={'month_day': 'Month', 'cnt_day': 'Avg. Daily Rentals'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.subheader("Demand by Day of the Week")
        weekday_trend = filtered_df.groupby('weekday_hour')['cnt_hour'].mean().reset_index()
        fig = px.bar(
            weekday_trend,
            x='weekday_hour',
            y='cnt_hour',
            color='cnt_hour',
            labels={'weekday_hour': 'Day of Week', 'cnt_hour': 'Avg. Rental Volume'}
        )
        fig.update_layout(height=300, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
           
    with col3:
        st.subheader("Demand by Season & Holiday Status")
        season_trend = filtered_df.groupby(['season_hour', 'holiday_hour'])['cnt_hour'].mean().reset_index()
        fig = px.bar(
            season_trend,
            x='season_hour',
            y='cnt_hour',
            color='holiday_hour',
            barmode='group',
            labels={'season_hour': 'Season', 'cnt_hour': 'Avg. Rentals', 'holiday_hour': 'Holiday'}
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Macro Growth Comparison: 2011 vs. 2012")

    col1, col2 = st.columns(2, border=True)
    with col1:
        st.subheader("Total Annual Rental Volume")
        yearly = filtered_df.groupby('year_day')['cnt_day'].sum().reset_index()
        fig = px.bar(
            yearly,
            x='year_day',
            y='cnt_day',
            text='cnt_day',
            labels={'year_day': 'Year', 'cnt_day': 'Total Aggregate Rentals'}
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig, use_container_width=True)
   
    with col2:
        st.subheader("Monthly Growth Trajectory Year-over-Year")
        monthly_trend = filtered_df.groupby(['numeric_month', 'year_day'])['cnt_day'].sum().reset_index()
        fig = px.line(
            monthly_trend,
            x='numeric_month',
            y='cnt_day',
            color='year_day',
            markers=True,
            labels={'numeric_month': 'Month Matrix', 'cnt_day': 'Total Monthly Rentals', 'year_day': 'Year'}
        )
        fig.update_layout(
            xaxis=dict(tickmode='array', tickvals=list(range(1, 13))),
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

# Weather Impact Tab
with tab3:
    st.subheader("🌦️ Environmental & Weather Impact Matrix")
    
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.subheader("Temperature vs. Hourly Rentals")
        if filtered_df.empty:
            st.warning("No data found for the selected filter combination.")
        else:
            fig = px.scatter(
                filtered_df,
                x="temp_norm_hour",
                y="cnt_hour",
                color="weather_situation_hour",
                labels={
                    "temp_norm_hour": "Normalized Temperature",
                    "cnt_hour": "Total Rentals (Hourly)",
                    "weather_situation_hour": "Weather Condition"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.subheader("Average Ridership by Weather Condition")
        weather_avg = filtered_df.groupby("weather_situation_hour")["cnt_hour"].mean().reset_index()
        fig2 = px.bar(
            weather_avg,
            x="weather_situation_hour",
            y="cnt_hour",
            text="cnt_hour",
            labels={
                "weather_situation_hour": "Weather Condition",
                "cnt_hour": "Average Hourly Rentals"
            }
        )
        fig2.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

# Peak Demand Tab
with tab4:
    st.subheader("⏰ Peak Ridership Hour Identification")
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.subheader("Overall Average Rentals per Hour")
        if filtered_df.empty:
            st.warning("No data found for the selected filter combination.")
        else:
            peak = filtered_df.groupby("hour")["cnt_hour"].mean().reset_index()
            fig = px.line(
                peak,
                x="hour",
                y="cnt_hour",
                markers=True,
                labels={
                    "hour": "Hour of the Day (0–23)",
                    "cnt_hour": "Avg. Rental Count"
                }
            )
            max_row = peak.loc[peak["cnt_hour"].idxmax()]

            fig.add_annotation(
                x=max_row["hour"],
                y=max_row["cnt_hour"],
                text=f"Peak: Hour {int(max_row['hour'])}:00",
                showarrow=True,
                arrowhead=2
            )
            fig.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Hourly Distribution Profile: Workdays vs. Weekends")
        if filtered_df.empty:
            st.warning("No data found for the selected filter combination.")
        else:
            hourly = filtered_df.groupby(["hour", "workingday_hour"])["cnt_hour"].mean().reset_index()
            fig = px.line(
                hourly,
                x="hour",
                y="cnt_hour",
                color="workingday_hour",
                markers=True,
                labels={
                    "hour": "Hour of Day",
                    "cnt_hour": "Avg. Rental Count",
                    "workingday_hour": "Day Classification"
                }
            )
            fig.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig, use_container_width=True)

# Operational Insights Tab
with tab5:
    st.subheader("✅ Data-Driven Fleet Optimization Insights")
    col1, col2 = st.columns(2, border=True)
    with col1:
        st.subheader("Commuter Windows vs. Leisure Patterns")
        if filtered_df.empty:
            st.warning("No data found for the selected filter combination.")
        else:
            hourly_pattern = filtered_df.groupby(['hour', 'workingday_hour'])['cnt_hour'].mean().reset_index()
            fig = px.line(
                hourly_pattern, 
                x='hour', 
                y='cnt_hour', 
                color='workingday_hour',
                markers=True,
                labels={
                    'hour': 'Hour of Day (0-23)', 
                    'cnt_hour': 'Avg. Demand Level', 
                    'workingday_hour': 'Day Type'
                }
            )
            fig.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Correlation Matrix: Temperature, Weather, and Volatility")
        fig = px.scatter(
            filtered_df, 
            x='temp_norm_hour', 
            y='cnt_hour', 
            color='weather_situation_hour',
            opacity=0.5,
            labels={
                'temp_norm_hour': 'Normalized Temperature Matrix', 
                'cnt_hour': 'Ridership Volume', 
                'weather_situation_hour': 'Weather Category'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
