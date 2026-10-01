import duckdb
import streamlit as st


data = duckdb.sql("""
    SELECT *
    FROM 'data/processed/filtered.parquet'
""").df()

sensors = duckdb.sql("""
    SELECT DISTINCT sensor_id
    FROM 'data/processed/filtered.parquet'
    ORDER BY sensor_id
""").df()

selected_sensor = st.selectbox(
    "Choisir un capteur",
    sensors["sensor_id"],
)

filtered_data = duckdb.sql(f"""
    SELECT *
    FROM 'data/processed/filtered.parquet'
    WHERE sensor_id = {selected_sensor}
""").df()

st.dataframe(filtered_data)