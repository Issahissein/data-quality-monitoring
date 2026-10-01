import duckdb
import plotly.express as px
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

sensor_data = duckdb.sql(f"""
    SELECT date, visitors
    FROM 'data/processed/filtered.parquet'
    WHERE sensor_id = {selected_sensor}
    ORDER BY date
""").df()

fig = px.line(
    sensor_data,
    x="date",
    y="visitors",
    title=f"Valeurs journalières du capteur {selected_sensor}",
)

st.plotly_chart(fig)