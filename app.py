import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kino AI Bot", layout="centered")

st.title("🎰 Kino AI: Live System")

# Έλεγχος αν υπάρχει το αρχείο
if os.path.exists('kino_data.csv'):
    try:
        df = pd.read_csv('kino_data.csv')
        st.success(f"✅ Τα δεδομένα φορτώθηκαν! (Σύνολο: {len(df)} κληρώσεις)")
        st.subheader("Τελευταία Κλήρωση:")
        st.write(df.iloc[0].tolist())
    except Exception as e:
        st.error(f"Πρόβλημα στο αρχείο: {e}")
else:
    st.error("❌ Το αρχείο δεδομένων (kino_data.csv) λείπει!")
    st.info("Πήγαινε στο GitHub -> Actions -> Update Kino Data -> Run Workflow.")
