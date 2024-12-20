import pandas as pd
import streamlit as st
from pybaseball import statcast

pitch_type_mapping = {
    "FF": "Four-Seam Fastball",
    "SL": "Slider",
    "CU": "Curveball",
    "CH": "Changeup",
    "FS": "Splitter",
    "SI": "Sinker",
    "FC": "Cutter",
    "KC": "Knuckle Curve",
    "KN": "Knuckleball",
    "SV": "Sweeper",
    "ST": "Sweeping Curve",
    "CS": "Slow Curve",
}

@st.cache_data
def get_filtered_data(start_date, end_date):
    data = statcast(start_dt=start_date, end_dt=end_date, parallel=True)
    return data.dropna(subset=["events"])

start_date = st.date_input("Start Date", value=pd.to_datetime("2024-06-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2024-06-30"))

if start_date > end_date:
    st.error("Start date must be before or equal to the end date.")
else:
    # Fetch data based on user inputs
    with st.spinner("Fetching data..."):
        data = get_filtered_data(start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"))
        data = data.dropna(subset=["events"])
    
    # Display success message
    st.success(f"Data loaded successfully for the range {start_date} to {end_date}.")

    # Debug or display data as needed
    st.write(data.head())

st.title("Batting average against pitches MLB 2024")

pitch_type = st.selectbox(
    "Select Pitch Type",
    options = data['pitch_type'].dropna().unique(),
    index=0
)

pitcher_hand = st.selectbox(
    "Select Pitcher Handedness",
    options = data['p_throws'].dropna().unique(),
    index=0
)

batter_stance = st.selectbox(
    "Select Batter Handedness",
    options = data['stand'].dropna().unique(),
    index=0
)

filtered = data[
    (data["pitch_type"] == pitch_type) &
    (data['p_throws']== pitcher_hand) &
    (data['stand'] == batter_stance)
    ]

if not filtered.empty:
    
        hits = filtered[filtered['events'] == "single"].shape[0] + \
            filtered[filtered['events'] == "double"].shape[0] + \
            filtered[filtered['events'] == "triple"].shape[0] + \
            filtered[filtered['events'] == "home_run"].shape[0]

        atbats = filtered[filtered['events'] == "single"].shape[0] + \
            filtered[filtered['events'] == "double"].shape[0] + \
            filtered[filtered['events'] == "triple"].shape[0] + \
            filtered[filtered['events'] == "home_run"].shape[0] + \
            filtered[filtered['events'] == "field_out"].shape[0] + \
            filtered[filtered['events'] == "strikeout"].shape[0] + \
            filtered[filtered['events'] == "grounded_into_double_play"].shape[0]

        

        ba = hits/atbats if atbats > 0 else 0
        st.write(f"Batting Average: {ba:.3f}")
else:
      st.write("No data available")


