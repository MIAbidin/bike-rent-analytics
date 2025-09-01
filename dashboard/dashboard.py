import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Configure page
st.set_page_config(
    page_title="🚴‍♂️ Bike Sharing Analytics Dashboard",
    page_icon="🚴‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-box {
        background-color: #f0f8ff;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data from CSV files
@st.cache_data
def load_data():
    """Load bike sharing data from CSV files"""
    try:
        # Load daily data
        day_df = pd.read_csv('../dataset/day.csv')
        hour_df = pd.read_csv('../dataset/hour.csv')
        
        # Data cleaning and preprocessing (same as your analysis)
        # Rename columns for readability
        day_df = day_df.rename(columns={
            'dteday': 'date',
            'season': 'season',
            'yr': 'year',
            'mnth': 'month',
            'holiday': 'is_holiday',
            'weekday': 'weekday',
            'workingday': 'is_workingday',
            'weathersit': 'weather_situation',
            'temp': 'temperature',
            'atemp': 'feels_temperature',
            'hum': 'humidity',
            'windspeed': 'wind_speed',
            'casual': 'casual_users',
            'registered': 'registered_users',
            'cnt': 'total_count'
        })

        hour_df = hour_df.rename(columns={
            'dteday': 'date',
            'season': 'season',
            'yr': 'year',
            'mnth': 'month',
            'hr': 'hour',
            'holiday': 'is_holiday',
            'weekday': 'weekday',
            'workingday': 'is_workingday',
            'weathersit': 'weather_situation',
            'temp': 'temperature',
            'atemp': 'feels_temperature',
            'hum': 'humidity',
            'windspeed': 'wind_speed',
            'casual': 'casual_users',
            'registered': 'registered_users',
            'cnt': 'total_count'
        })

        # Convert date to datetime
        day_df['date'] = pd.to_datetime(day_df['date'])
        hour_df['date'] = pd.to_datetime(hour_df['date'])

        # Apply mappings
        season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
        yr_mapping = {0: '2011', 1: '2012'}
        mnth_mapping = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                        7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
                           4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
        weathersit_mapping = {
            1: 'Clear/Partly Cloudy',
            2: 'Mist/Cloudy',
            3: 'Light Snow/Light Rain',
            4: 'Severe Weather'
        }
        holiday_mapping = {0: 'No Holiday', 1: 'Holiday'}
        workingday_mapping = {0: 'No', 1: 'Yes'}

        # Apply mappings to day_df
        day_df['season'] = day_df['season'].map(season_mapping)
        day_df['year'] = day_df['year'].map(yr_mapping)
        day_df['month'] = day_df['month'].map(mnth_mapping)
        day_df['weekday'] = day_df['weekday'].map(weekday_mapping)
        day_df['weather_situation'] = day_df['weather_situation'].map(weathersit_mapping)
        day_df['is_holiday'] = day_df['is_holiday'].map(holiday_mapping)
        day_df['is_workingday'] = day_df['is_workingday'].map(workingday_mapping)

        # Apply mappings to hour_df  
        hour_df['season'] = hour_df['season'].map(season_mapping)
        hour_df['year'] = hour_df['year'].map(yr_mapping)
        hour_df['month'] = hour_df['month'].map(mnth_mapping)
        hour_df['weekday'] = hour_df['weekday'].map(weekday_mapping)
        hour_df['weather_situation'] = hour_df['weather_situation'].map(weathersit_mapping)
        hour_df['is_holiday'] = hour_df['is_holiday'].map(holiday_mapping)
        hour_df['is_workingday'] = hour_df['is_workingday'].map(workingday_mapping)

        hourly_avg = hour_df.groupby(['hour', 'is_workingday'])['total_count'].mean().reset_index()
        workday_avg = hourly_avg[hourly_avg['is_workingday'] == 'Yes'][['hour', 'total_count']].rename(columns={'total_count': 'workday_avg'})
        weekend_avg = hourly_avg[hourly_avg['is_workingday'] == 'No'][['hour', 'total_count']].rename(columns={'total_count': 'weekend_avg'})
        hour_df = workday_avg.merge(weekend_avg, on='hour')


        # Add demand clusters
        def categorize_demand(count):
            if count >= 6000:
                return 'High Demand'
            elif count >= 3000:
                return 'Medium Demand'
            else:
                return 'Low Demand'
        
        day_df['demand_cluster'] = day_df['total_count'].apply(categorize_demand)
        day_df['casual_ratio'] = (day_df['casual_users'] / day_df['total_count'] * 100).round(1)
        day_df['registered_ratio'] = (day_df['registered_users'] / day_df['total_count'] * 100).round(1)
        
        return day_df, hour_df
        
    except FileNotFoundError:
        st.error("⚠️ Dataset files not found! Please ensure 'dataset/day.csv' and 'dataset/hour.csv' exist in your directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

# Load data
day_df, hour_df = load_data()

# Header
st.markdown('<h1 class="main-header">🚴‍♂️ Bike Sharing Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 📊 Dashboard Controls")
st.sidebar.markdown("---")

# Date range selector
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(day_df['date'].min(), day_df['date'].max()),
    min_value=day_df['date'].min(),
    max_value=day_df['date'].max()
)

# Season filter
selected_seasons = st.sidebar.multiselect(
    "Select Seasons",
    options=day_df['season'].unique(),
    default=day_df['season'].unique()
)

# Weather filter
selected_weather = st.sidebar.multiselect(
    "Select Weather Conditions", 
    options=day_df['weather_situation'].unique(),
    default=day_df['weather_situation'].unique()
)

# Filter data
filtered_df = day_df[
    (day_df['date'].dt.date >= date_range[0]) & 
    (day_df['date'].dt.date <= date_range[1]) &
    (day_df['season'].isin(selected_seasons)) &
    (day_df['weather_situation'].isin(selected_weather))
]

if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust the date range or filters.")


# Key Metrics Row
st.markdown("### 📈 Key Performance Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if not filtered_df.empty:
        avg_daily = int(filtered_df['total_count'].mean())
        delta_value = avg_daily - 4504
    else:
        avg_daily = 0
        delta_value = 0
    st.metric("Avg Daily Rentals", f"{avg_daily:,}", delta=f"{delta_value}")

with col2:
    total_days = len(filtered_df)
    st.metric("Total Days", total_days)

with col3:
    peak_day = filtered_df['total_count'].max()
    st.metric("Peak Day Rentals", f"{peak_day:,}")

with col4:
    utilization = (avg_daily / peak_day * 100)
    st.metric("Utilization Rate", f"{utilization:.1f}%")

st.markdown("---")

# Main Analysis Section
tab1, tab2, tab3, tab4 = st.tabs(["🌸 Seasonal Patterns", "🌤️ Weather Impact", "👥 User Behavior", "⏰ Peak Hours"])

seasonal_avg = filtered_df.groupby('season')['total_count'].mean().reset_index()

if not seasonal_avg.empty:
    best_season = seasonal_avg.loc[seasonal_avg['total_count'].idxmax(), 'season']
    worst_season = seasonal_avg.loc[seasonal_avg['total_count'].idxmin(), 'season']
else:
    best_season = "N/A"
    worst_season = "N/A"

with tab1:
    st.markdown("### Seasonal Rental Patterns")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Seasonal bar chart
        seasonal_avg = filtered_df.groupby('season')['total_count'].mean().reset_index()
        
        fig = px.bar(
            seasonal_avg, 
            x='season', 
            y='total_count',
            title="Average Daily Rentals by Season",
            color='season',
            color_discrete_map={
                'Spring': '#90EE90',
                'Summer': '#FFD700', 
                'Fall': '#FF8C00',
                'Winter': '#87CEEB'
            }
        )
        fig.update_layout(
            showlegend=False,
            xaxis_title="Season",
            yaxis_title="Average Daily Rentals",
            title_x=0.5
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔍 Key Insights")
        
        if not seasonal_avg.empty:
            st.markdown(f"""
            <div class="insight-box">
            <strong>Best Season:</strong> {best_season}<br>
            <strong>Worst Season:</strong> {worst_season}<br><br>
            <strong>Business Impact:</strong><br>
            • Fall shows optimal demand<br>
            • Spring requires promotional strategies<br>
            • Seasonal inventory planning needed
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No seasonal data available for the selected filters.")


    # Seasonal trend over time
    st.markdown("#### Seasonal Trends Over Time")
    monthly_trend = filtered_df.groupby([filtered_df['date'].dt.to_period('M'), 'season'])['total_count'].mean().reset_index()
    monthly_trend['date'] = monthly_trend['date'].astype(str)
    
    fig = px.line(
        monthly_trend, 
        x='date', 
        y='total_count', 
        color='season',
        title="Monthly Rental Trends by Season"
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Average Daily Rentals",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Weather Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather condition impact
        weather_avg = filtered_df.groupby('weather_situation')['total_count'].mean().reset_index()
        
        fig = px.bar(
            weather_avg,
            x='weather_situation',
            y='total_count', 
            title="Average Rentals by Weather Condition",
            color='total_count',
            color_continuous_scale='RdYlBu_r'
        )
        fig.update_layout(
            xaxis_title="Weather Condition",
            yaxis_title="Average Daily Rentals",
            title_x=0.5,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Temperature vs Rentals scatter
        fig = px.scatter(
            filtered_df,
            x='temperature',
            y='total_count',
            color='weather_situation',
            title="Temperature vs Rentals",
            opacity=0.7,
            trendline="ols"
        )
        fig.update_layout(
            xaxis_title="Temperature (Normalized)",
            yaxis_title="Daily Rentals",
            title_x=0.5
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Weather correlation heatmap
    st.markdown("#### Weather Variables Correlation")
    weather_corr = filtered_df[['temperature', 'humidity', 'wind_speed', 'total_count']].corr()
    
    fig = px.imshow(
        weather_corr,
        text_auto=True,
        aspect="auto",
        title="Weather Factors Correlation Matrix",
        color_continuous_scale='RdBu'
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### User Behavior Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # User type ratio by workday
        user_ratio = filtered_df.groupby('is_workingday')[['casual_ratio', 'registered_ratio']].mean().reset_index()
        user_ratio_melted = pd.melt(user_ratio, id_vars=['is_workingday'], 
                                   value_vars=['casual_ratio', 'registered_ratio'],
                                   var_name='user_type', value_name='percentage')
        
        fig = px.bar(
            user_ratio_melted,
            x='is_workingday',
            y='percentage',
            color='user_type',
            title="User Type Distribution: Workday vs Weekend",
            color_discrete_map={'casual_ratio': '#FF7F50', 'registered_ratio': '#4169E1'}
        )
        fig.update_layout(
            xaxis_title="Working Day",
            yaxis_title="Percentage (%)",
            title_x=0.5,
            legend_title="User Type"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Demand clusters pie chart
        cluster_counts = filtered_df['demand_cluster'].value_counts()
        
        fig = px.pie(
            values=cluster_counts.values,
            names=cluster_counts.index,
            title="Demand Cluster Distribution",
            color_discrete_map={
                'High Demand': '#CD5C5C',
                'Medium Demand': '#4682B4', 
                'Low Demand': '#2E8B57'
            }
        )
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    
    # User comparison by season
    st.markdown("#### User Types by Season")
    seasonal_users = filtered_df.groupby('season')[['casual_users', 'registered_users']].mean().reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Casual Users',
        x=seasonal_users['season'],
        y=seasonal_users['casual_users'],
        marker_color='#FF7F50'
    ))
    fig.add_trace(go.Bar(
        name='Registered Users', 
        x=seasonal_users['season'],
        y=seasonal_users['registered_users'],
        marker_color='#4169E1'
    ))
    
    fig.update_layout(
        barmode='stack',
        title="Average Users by Season",
        xaxis_title="Season",
        yaxis_title="Average Users",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Peak Hours Analysis")
    
    # Peak hours comparison
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hour_df['hour'],
        y=hour_df['workday_avg'],
        mode='lines+markers',
        name='Workday',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=hour_df['hour'], 
        y=hour_df['weekend_avg'],
        mode='lines+markers',
        name='Weekend',
        line=dict(color='#ff7f0e', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Hourly Rental Patterns: Workday vs Weekend",
        xaxis_title="Hour of Day",
        yaxis_title="Average Rentals",
        title_x=0.5,
        hovermode='x unified',
        xaxis=dict(tickmode='linear', dtick=2)
    )
    
    # Add peak hour annotations
    workday_peak = hour_df.loc[hour_df['workday_avg'].idxmax()]
    weekend_peak = hour_df.loc[hour_df['weekend_avg'].idxmax()]
    
    fig.add_annotation(
        x=workday_peak['hour'], y=workday_peak['workday_avg'],
        text=f"Peak: {workday_peak['hour']}:00",
        showarrow=True, arrowhead=2, arrowcolor='#1f77b4'
    )
    
    fig.add_annotation(
        x=weekend_peak['hour'], y=weekend_peak['weekend_avg'],
        text=f"Peak: {weekend_peak['hour']}:00", 
        showarrow=True, arrowhead=2, arrowcolor='#ff7f0e'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Peak hours summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🕐 Workday Peaks")
        workday_peaks = hour_df.nlargest(3, 'workday_avg')[['hour', 'workday_avg']]
        for _, row in workday_peaks.iterrows():
            st.markdown(f"**{int(row['hour'])}:00** - {int(row['workday_avg'])} rentals")
    
    with col2:
        st.markdown("#### 🕐 Weekend Peaks") 
        weekend_peaks = hour_df.nlargest(3, 'weekend_avg')[['hour', 'weekend_avg']]
        for _, row in weekend_peaks.iterrows():
            st.markdown(f"**{int(row['hour'])}:00** - {int(row['weekend_avg'])} rentals")

# Advanced Analytics Section
st.markdown("---")
st.markdown("### 🎯 Advanced Analytics")

col1, col2 = st.columns(2)

with col1:
    # Demand cluster characteristics
    st.markdown("#### Demand Cluster Characteristics")
    cluster_stats = filtered_df.groupby('demand_cluster').agg({
        'total_count': ['mean', 'count'],
        'temperature': 'mean',
        'casual_ratio': 'mean'
    }).round(2)
    
    cluster_stats.columns = ['Avg Rentals', 'Days Count', 'Avg Temp', 'Casual %']
    st.dataframe(cluster_stats, use_container_width=True)

with col2:
    # Weather impact summary
    st.markdown("#### Weather Impact Summary")
    weather_impact = filtered_df.groupby('weather_situation').agg({
        'total_count': 'mean',
        'temperature': 'mean', 
        'humidity': 'mean'
    }).round(2)
    
    weather_impact.columns = ['Avg Rentals', 'Avg Temp', 'Avg Humidity']
    st.dataframe(weather_impact, use_container_width=True)

# Business Insights Section
st.markdown("---")
st.markdown("### 💡 Business Insights & Recommendations")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    st.markdown("""
    <div class="insight-box">
    <h4>🎯 Key Findings</h4>
    <ul>
    <li><strong>Fall is the peak season</strong> with highest average rentals</li>
    <li><strong>Clear weather</strong> significantly boosts demand (+50% vs rainy days)</li>
    <li><strong>Registered users</strong> dominate workdays (87.7%)</li>
    <li><strong>Casual users</strong> prefer weekends for recreational rides</li>
    <li><strong>Bimodal pattern</strong> on workdays (7-9 AM, 5-7 PM peaks)</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with insights_col2:
    st.markdown("""
    <div class="insight-box">
    <h4>🚀 Business Recommendations</h4>
    <ul>
    <li><strong>Seasonal Pricing:</strong> Premium rates during Fall/Summer</li>
    <li><strong>Weather-based Alerts:</strong> Dynamic pricing on clear days</li>
    <li><strong>Target Marketing:</strong> Commuter packages for registered users</li>
    <li><strong>Weekend Promotions:</strong> Family/leisure packages for casual users</li>
    <li><strong>Fleet Management:</strong> Rebalance bikes during peak hours</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Interactive Analysis Section
st.markdown("---")
st.markdown("### 🔍 Interactive Analysis")

analysis_option = st.selectbox(
    "Choose Analysis Type:",
    ["Temperature vs Demand", "Seasonal Weather Patterns", "User Type Trends"]
)

if analysis_option == "Temperature vs Demand":
    if not filtered_df.empty:
        # Temperature analysis
        temp_bins = pd.cut(
            filtered_df['temperature'], 
            bins=5, 
            labels=['Very Cold', 'Cold', 'Moderate', 'Warm', 'Hot']
        )
        temp_analysis = filtered_df.groupby(temp_bins)['total_count'].mean().reset_index()
        
        fig = px.bar(
            temp_analysis,
            x='temperature',
            y='total_count',
            title="Rentals by Temperature Range",
            color='total_count',
            color_continuous_scale='thermal'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data available for Temperature vs Demand analysis.")


elif analysis_option == "Seasonal Weather Patterns":
    # Seasonal weather analysis
    season_weather = pd.crosstab(filtered_df['season'], filtered_df['weather_situation'], normalize='index') * 100
    
    fig = px.imshow(
        season_weather,
        text_auto=True,
        aspect="auto", 
        title="Weather Patterns by Season (%)",
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

else:  # User Type Trends
    # Monthly user trends
    monthly_users = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))[['casual_users', 'registered_users']].mean().reset_index()
    monthly_users['date'] = monthly_users['date'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_users['date'],
        y=monthly_users['casual_users'],
        mode='lines+markers',
        name='Casual Users',
        line=dict(color='#FF7F50', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=monthly_users['date'],
        y=monthly_users['registered_users'], 
        mode='lines+markers',
        name='Registered Users',
        line=dict(color='#4169E1', width=2)
    ))
    
    fig.update_layout(
        title="Monthly User Type Trends",
        xaxis_title="Month",
        yaxis_title="Average Daily Users",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <strong>🚴‍♂️ Bike Sharing Analytics Dashboard</strong><br>
    Muhammad Irfan Abidin | Dicoding | 2025
</div>
""", unsafe_allow_html=True)