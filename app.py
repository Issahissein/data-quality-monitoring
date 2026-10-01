import duckdb
import plotly.express as px
import streamlit as st


# Open Parquet data with DuckDB
data = duckdb.sql("""
    SELECT *
    FROM 'data/processed/filtered.parquet'
""").df()


# Sidebar
st.sidebar.title("Filtres")


# Get all existing stores
stores = duckdb.sql("""
    SELECT DISTINCT store_id
    FROM 'data/processed/filtered.parquet'
    ORDER BY store_id
""").df()


# Store dropdown
selected_store = st.sidebar.selectbox(
    "Choisir un lieu",
    stores["store_id"],
)


# Get sensors for selected store
sensors = duckdb.sql(f"""
    SELECT DISTINCT sensor_id
    FROM 'data/processed/filtered.parquet'
    WHERE store_id = {selected_store}
    ORDER BY sensor_id
""").df()


# Sensor dropdown
selected_sensor = st.sidebar.selectbox(
    "Choisir un capteur",
    sensors["sensor_id"],
)


# Week or month selection
selected_period = st.sidebar.selectbox(
    "Choisir une période",
    ["Semaine", "Mois"],
)


# Filter data for selected store and sensor
sensor_data = data[
    (data["store_id"] == selected_store)
    & (data["sensor_id"] == selected_sensor)
].copy()


# Sort by date
sensor_data = sensor_data.sort_values("date")


# Filter week or month
if selected_period == "Semaine":
    sensor_data = sensor_data.tail(7)

elif selected_period == "Mois":
    sensor_data = sensor_data.tail(30)


# Title
st.title("Data Quality Monitoring")

st.write(
    f"Lieu {selected_store} - "
    f"Capteur {selected_sensor} - "
    f"{selected_period}"
)


# Display dataframe
st.dataframe(sensor_data)


# Daily values chart
fig_daily = px.line(
    sensor_data,
    x="date",
    y="visitors",
    title="Valeurs journalières",
)

st.plotly_chart(fig_daily)


# Average of the last 4 similar days chart
fig_average = px.line(
    sensor_data,
    x="date",
    y="average_last_4",
    title="Moyenne des 4 derniers jours similaires",
)

st.plotly_chart(fig_average)