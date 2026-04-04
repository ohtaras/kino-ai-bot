import streamlit as st
import pandas as pd
from collections import Counter
import time
import os

st.set_page_config(page_title="Kino AI Live", layout="wide")

st.title("🎰 Kino AI: Automated System")

# Έλεγχος αν υπάρχει το αρχείο
if os.path.exists('kino_data.csv'):
    try:
        df = pd.read_csv('kino_data.csv')
        st.success(f"✅ Δεδομένα Online. Τελευταία ενημέρωση: {time.strftime('%H:%M:%S')}")

        draws = df.values.tolist()
        all_numbers = [int(n) for sub in draws for n in sub]
        counts = Counter(all_numbers)

        st.subheader("🎯 AI Πρόταση (Top 5)")
        top_5 = [item[0] for item in counts.most_common(5)]
        st.success(f"Προτεινόμενη 5άδα: {sorted(top_5)}")
        
        st.bar_chart(df.melt()['value'].value_counts().head(20))

        # Αυτόματο Refresh κάθε 1 λεπτό
        time.sleep(60)
        st.rerun()

    except Exception as e:
        st.error(f"Σφάλμα ανάγνωσης δεδομένων: {e}")
else:
    st.warning("⏳ Το αρχείο 'kino_data.csv' δεν έχει δημιουργηθεί ακόμα.")
    st.info("Πήγαινε στα Actions του GitHub, πάτα 'Ultra Fast Kino Update' και μετά το κουμπί 'Run workflow'.")
