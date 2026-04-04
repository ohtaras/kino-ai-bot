import streamlit as st
import pandas as pd
import os

st.title("🎰 Kino AI Live")

if os.path.exists('kino_data.csv'):
    df = pd.read_csv('kino_data.csv')
    st.success(f"✅ Δεδομένα Ενεργά! Σύνολο κληρώσεων: {len(df)}")
    st.write("Τελευταία νούμερα:")
    st.dataframe(df.head())
else:
    st.warning("⏳ Περιμένουμε τον αυτόματο εργάτη του GitHub να φτιάξει το αρχείο...")
    st.info("Πήγαινε στα Actions και πάτα 'Run workflow' για να ξεκινήσει τώρα.")
