# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 21:52:30 2024

@author: andrew.clark
"""

import streamlit as st
import pandas as pd

# Load the data from Google Sheets
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS4tpaKnM4S2MEro74GTkw0kAewYjeofL1qMkebfTnIBa3ktZwpAmNfLnOTHYI7Hykygwp6ggkRAcub/pub?gid=598831182&single=true&output=csv'

df = pd.read_csv(url, dtype={'date': str})

# Convert date_long column to datetime if needed
df['date_long'] = pd.to_datetime(df['date_long'])

# Reformat the 'date' column to include the weekday
df['date'] = df['date_long'].dt.strftime('%A, %d %B %Y')

# Set up the Streamlit app title and subtitle
st.title("BLCC Junior Home Matches")
st.subheader("Most Recent Home Game By Oval")

# Create a dropdown for selecting the location
location = st.selectbox("Select a location", sorted(df['location'].unique()))

# Filter the DataFrame for the selected location
df_location = df[df['location'] == location]

# Get the most recent game played at the selected location (before or on today's date)
today = pd.Timestamp.today()
recent_game = df_location[df_location['date_long'] <= today].sort_values('date_long', ascending=False).head(1)

# Display the most recent game, if available
if not recent_game.empty:
    st.write("Most Recent Game at Selected Location:")
    st.table(recent_game.drop(columns=['date_long']))
else:
    st.write("No games found for the selected location.")

# Add subtitle for all games at the selected location
st.subheader("All Games")

# Display all games at the selected location
st.write("All games at selected location:")
st.table(df_location.drop(columns=['date_long']))

