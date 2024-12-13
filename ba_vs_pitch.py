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
def get_data():
    try:
        data = pd.read_csv("statcast_2024.csv")
    except:
        data = statcast(start_dt="2024-03-20",end_dt="2024-09-30",parallel=True)
        data.to_csv("statcast_2024.csv",index=False)
    return data



data = get_data()

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
            filtered[filtered['events'] == "home_run"].shape[0],

        atbats = filtered['abs'].sum(),

        ba = hits/atbats if atbats > 0 else 0
        st.write(f"Batting Average: {ba:.3f}")
else:
      st.write("No data available")
