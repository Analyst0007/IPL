# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 07:24:07 2025

@author: Hemal
"""
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os
from datetime import datetime

# URL to fetch data
url = "https://www.cricbuzz.com/cricket-series/9237/indian-premier-league-2025/stats"

# Function to fetch and save data
def fetch_and_save_data(url, file_path):
    data = requests.get(url)
    data = data.content
    data = pd.read_html(data)
    data = pd.DataFrame(data[0])
    data.to_csv(file_path, index=False)

# File path to store the data
data_file = "cricket_stats.csv"

# Check if data needs to be updated
if not os.path.exists(data_file) or (datetime.now() - datetime.fromtimestamp(os.path.getmtime(data_file))).days >= 1:
    fetch_and_save_data(url, data_file)

# Load data from file
data = pd.read_csv(data_file)

# Streamlit application
st.title("IPL Player Statistics")

# Sidebar for player selection
player = st.sidebar.selectbox("Select a Player", data["Player"])

# Filter data for the selected player
player_data = data[data["Player"] == player]

# Ensure player_data is not empty
if not player_data.empty:
    # Display player statistics
    st.write(f"### Statistics for {player}")
    st.write(player_data)

    # Plotting the data
    st.write(f"### Graphical Representation for {player}")

    # Plot Matches vs Runs
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(player_data.index, player_data["Runs"], color='skyblue', alpha=0.7)
    ax.set_title('Total Runs', fontsize=14)
    ax.set_ylabel('Runs', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Plot Matches vs Average
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(player_data.index, player_data["Avg"], color='lightgreen', alpha=0.7)
    ax.set_title('Batting Average', fontsize=14)
    ax.set_ylabel('Average', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Plot Matches vs Strike Rate
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(player_data.index, player_data["Sr"], color='salmon', alpha=0.7)
    ax.set_title('Strike Rate', fontsize=14)
    ax.set_ylabel('Strike Rate', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Plot 4s and 6s
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(player_data.index, player_data["4s"], color='lightcoral', label='Fours', alpha=0.7)
    ax.bar(player_data.index, player_data["6s"], color='lightblue', label='Sixes', bottom=player_data["4s"], alpha=0.7)
    ax.set_title('Fours and Sixes', fontsize=14)
    ax.set_ylabel('Count', fontsize=12)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)
else:
    st.write("No data available for the selected player.")
