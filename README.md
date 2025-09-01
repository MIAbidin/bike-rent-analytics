# 🚴‍♂️ Bike Sharing Analytics

A fully interactive **Streamlit dashboard** for analyzing bike sharing data. This dashboard provides insights into seasonal trends, weather impact, user behavior, and peak hours, helping businesses optimize bike rental operations.

---

## 📝 Features

- **Seasonal Patterns Analysis**  
  Explore average daily rentals by season, identify the best and worst seasons, and visualize seasonal trends over time.

- **Weather Impact Analysis**  
  Analyze the effect of temperature, humidity, and weather conditions on bike rentals with bar charts, scatter plots, and correlation heatmaps.

- **User Behavior Analysis**  
  Compare casual vs registered users, visualize demand clusters, and see user patterns by season and workdays/weekends.

- **Peak Hours Analysis**  
  Identify peak rental hours for workdays and weekends with line charts and annotations.

- **Advanced Analytics**  
  Explore demand clusters characteristics and weather impact summaries in table format.

- **Business Insights & Recommendations**  
  Key findings and actionable strategies for seasonal pricing, marketing, and fleet management.

- **Interactive Analysis Section**  
  Analyze rentals by temperature ranges, seasonal weather patterns, or user type trends.

---

## 📂 Dataset

The dashboard uses the **Bike Sharing Dataset**:

- `day.csv`: Daily bike rentals data  
- `hour.csv`: Hourly bike rentals data  

---

## 🛠️ Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MIAbidin/bike-rent-analytics.git
    cd bike-rent-analytics
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3. Activate the virtual environment:
    ```bash
    venv\Scripts\activate
    ```
4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run the dashboard using Streamlit:
    ```bash
    cd dashboard
    streamlit run dashboard.py
    ```
Open the URL provided by Streamlit (usually http://localhost:8501) in your browser to interact with the dashboard.
---

## 🌐 Live Demo

The dashboard is deployed on **Streamlit Community Cloud** and can be accessed at:

[🚴‍♂️ Bike Sharing Analytics Dashboard](https://muham-bike-share.streamlit.app)