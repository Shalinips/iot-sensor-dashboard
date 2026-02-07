# dashboard.py

import streamlit as st
import pandas as pd
import os
import datetime
import plotly.express as px

st.set_page_config(page_title="IoT Live Dashboard", layout="wide")

# --- Function to read and clean data ---
def load_data(file_name):
    if not os.path.exists(file_name):
        return pd.DataFrame()

    df = pd.read_csv(file_name)

    if df.empty:
        return df

    # Preprocessing
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df[(df['temperature'] >= 15) & (df['temperature'] <= 60)]
    df = df[(df['humidity'] >= 30) & (df['humidity'] <= 90)]

    return df

# --- Main Dashboard UI ---
st.title("🌐 IoT Sensor Data Dashboard")
st.markdown("Real-time analysis of temperature and humidity using Python and Streamlit")

data_file = "live_sensor_data.csv"
df = load_data(data_file)

if df.empty:
    st.warning("Waiting for sensor data...")
else:
    latest_time = df['timestamp'].max()
    st.write(f"📅 Last updated: {latest_time}")

    # ALERTS
    alert_df = df[(df['temperature'] > 50) | (df['temperature'] < 20) |
                  (df['humidity'] > 80) | (df['humidity'] < 40)]

    if not alert_df.empty:
        st.error(f"🚨 {len(alert_df)} Alert(s) detected!")
        st.dataframe(alert_df.tail(5))

    # Averages
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Temperature (°C)", round(df['temperature'].mean(), 2))
    with col2:
        st.metric("Average Humidity (%)", round(df['humidity'].mean(), 2))

    # Line Charts
    fig_temp = px.line(df, x="timestamp", y="temperature", color="sensor_id", title="Temperature Over Time")
    fig_hum = px.line(df, x="timestamp", y="humidity", color="sensor_id", title="Humidity Over Time")
    st.plotly_chart(fig_temp, use_container_width=True)
    st.plotly_chart(fig_hum, use_container_width=True)

# --- Auto-refresh every 5 seconds ---
st.markdown(
    "<meta http-equiv='refresh' content='5'>",
    unsafe_allow_html=True
)
