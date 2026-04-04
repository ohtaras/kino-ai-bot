import streamlit as st
import pandas as pd
from collections import Counter
import time

st.set_page_config(page_title="Kino AI Live", layout="wide")

st.title("🎰 Kino AI: Real-Time Automated System")

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

    # ΑΥΤΟΜΑΤΟ REFRESH
    time.sleep(60)
    st.rerun()

except Exception:
    st.warning("⏳ Περιμένουμε το αρχείο 'kino_data.csv'...")
    st.info("Πήγαινε στα Actions, πάτα το 'Ultra Fast Kino Update' και μετά 'Run workflow'.")
