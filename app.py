import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Kino AI Engine", layout="wide")

st.title("🤖 Kino AI: Automated System")

try:
    # Διαβάζει το αρχείο που φτιάχνει το GitHub Action
    df = pd.read_csv('kino_data.csv')
    st.success(f"✅ Η μηχανή είναι online! (Δείγμα: {len(df)} κληρώσεις)")
    
    # Ανάλυση
    draws = df.values.tolist()
    all_numbers = [int(n) for sub in draws for n in sub]
    counts = Counter(all_numbers)
    
    # Πρόβλεψη
    st.subheader("🎯 AI Πρόταση")
    top_picks = [item[0] for item in counts.most_common(5)]
    st.success(f"Προτεινόμενα: {sorted(top_picks)}")
    
    # Γράφημα
    st.bar_chart(df.melt()['value'].value_counts().head(20))

except:
    st.info("⏳ Ο 'εργάτης' του GitHub ετοιμάζει τα δεδομένα... Περίμενε 1-2 λεπτά και κάνε ανανέωση.")
