import streamlit as st
import requests
import pandas as pd
import numpy as np

st.title("🎰 Kino AI Predictor")
st.write("Η μηχανή μελετάει τα Excel σου και προτείνει...")

# Εδώ θα συνδεθεί ο φάκελος Drive σου στο επόμενο βήμα
folder_url = "https://drive.google.com/drive/folders/1QHxCd74c5D9U7TvLdyt-GRArbSRuLsZn"

def get_last_draw():
    # Παίρνει την τελευταία κλήρωση από τον ΟΠΑΠ
    api_url = "https://api.opap.gr/draws/v3.0/1100/last-n/1"
    res = requests.get(api_url).json()
    return res[0]['winningNumbers']['list']

last_numbers = get_last_draw()
st.subheader(f"Τελευταία Κλήρωση: {last_numbers}")

# Εδώ θα μπει το Neural Network (LSTM) μόλις συνδέσουμε τα δεδομένα
st.success("Η μηχανή είναι Online και περιμένει σήμα σιγουριάς > 88%")
