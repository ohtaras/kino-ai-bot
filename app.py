import streamlit as st
import pandas as pd
from collections import Counter

st.set_page_config(page_title="Kino AI: Live", layout="wide")

st.title("🎰 Kino AI: Automated System")

try:
    # Διαβάζει το αρχείο που φτιάχνει το GitHub αυτόματα
    df = pd.read_csv('kino_data.csv')
    st.success(f"✅ Δεδομένα ενεργά! (Τελευταίες {len(df)} κληρώσεις)")
    
    # Στατιστική ανάλυση
    draws = df.values.tolist()
    flat = [int(n) for sub in draws for n in sub]
    counts = Counter(flat)
    
    st.subheader("🎯 AI Πρόταση")
    # Παίρνουμε τους 5 πιο συχνούς
    top_5 = [item[0] for item in counts.most_common(5)]
    st.success(f"Προτεινόμενη 5άδα: {sorted(top_5)}")
    
    # Εμφάνιση γραφήματος
    st.bar_chart(df.melt()['value'].value_counts().head(20))
    
except Exception as e:
    st.info("⏳ Ο εργάτης του GitHub ετοιμάζει το αρχείο 'kino_data.csv'... Περίμενε λίγο και κάνε Refresh.")
    st.write("Αν βλέπεις αυτό το μήνυμα, σημαίνει ότι το αρχείο δεν έχει δημιουργηθεί ακόμα στο GitHub σου.")
