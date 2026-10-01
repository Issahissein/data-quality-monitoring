import duckdb
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


# Select a sensor
selected_sensor = st.selectbox(
    "Choisir un capteur",
    sensors["sensor_id"],
)


# Get data for the selected sensor
filtered_data = duckdb.sql(f"""
    SELECT *
    FROM 'data/processed/filtered.parquet'
    WHERE sensor_id = {selected_sensor}
    ORDER BY date
""").df()


# Display data for the selected sensor
st.write(filtered_data)