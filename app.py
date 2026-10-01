import duckdb
import plotly.express as px
import streamlit as st


# Open Parquet data with DuckDB
data = duckdb.sql("""
    SELECT *
    FROM 'data/processed/filtered.parquet'
""").df()


# Get all existing sensors
sensors = duckdb.sql("""
    SELECT DISTINCT sensor_id
    FROM 'data/processed/filtered.parquet'
    ORDER BY sensor_id
""").df()


# Sensor dropdown
selected_sensor = st.selectbox(
    "Choisir un capteur",
    sensors["sensor_id"],
)


# Filter data for selected sensor
sensor_data = data[
    data["sensor_id"] == selected_sensor
]


# Plot average of the last 4 similar days
fig = px.line(
    sensor_data,
    x="date",
    y="average_last_4",
    title="Moyenne des 4 derniers jours similaires",
)

st.plotly_chart(fig)