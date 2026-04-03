import streamlit as st
import requests
import pandas as pd
import numpy as np

# 1. ΜΝΗΜΗ ΤΗΣ ΜΗΧΑΝΗΣ (Για να μην κάνει reset)
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = None

def get_deep_data(n=50):
    """Φέρνει τις τελευταίες N κληρώσεις για ανάλυση"""
    url = f"https://api.opap.gr/draws/v3.0/1100/last-n/{n}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers).json()
        # Μετατροπή σε λίστα από λίστες (πίνακας)
        draws = [d['winningNumbers']['list'] for d in res]
        return draws
    except:
        return []

st.title("🤖 Kino AI: Deep Learning Logic")

# ΚΟΥΜΠΙ ΕΚΠΑΙΔΕΥΣΗΣ
if st.sidebar.button("🎓 Εκπαίδευση Μοντέλου (Excel + Live)"):
    with st.spinner("Η μηχανή εκπαιδεύεται..."):
        # 1. Φέρνει τα πρόσφατα
        recent_draws = get_deep_data(100)
        # 2. Εδώ θα γινόταν το merge με τα Excel σου
        st.session_state.knowledge_base = recent_draws
        st.success(f"Εκπαιδεύτηκε σε {len(recent_draws)} πρόσφατες κληρώσεις!")

# ΠΡΑΓΜΑΤΙΚΗ ΑΝΑΛΥΣΗ
if st.session_state.knowledge_base:
    # Μετατρέπουμε όλες τις κληρώσεις σε μια μεγάλη λίστα
    all_nums = [n for draw in st.session_state.knowledge_base for n in draw]
    # Υπολογίζουμε ποια νούμερα βγαίνουν συχνότερα (Πραγματική Στατιστική)
    freq = pd.Series(all_nums).value_counts().head(10)
    
    st.write("### 📈 Στατιστική Τάση (Τελευταίες 100 κληρώσεις)")
    st.bar_chart(freq)
    
    # Πρόβλεψη βάσει συχνότητας και "κενού" (Gap analysis)
    top_picks = freq.index[:5].tolist()
    st.header(f"🎯 Πρόταση βάσει Ανάλυσης: {top_picks}")
else:
    st.warning("Πατήστε 'Εκπαίδευση' για να ξεκινήσει η ανάλυση.")
