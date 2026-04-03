import streamlit as st
import requests
import pandas as pd
from collections import Counter
import time

st.set_page_config(page_title="Kino AI Predictor", layout="wide")

def get_data_safely(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def fetch_history(active_id):
    all_draws = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Προσπαθούμε να πάρουμε 5 πακέτα των 100 (500 κληρώσεις) για να μην φάμε block
    current_end = active_id - 1
    for i in range(5):
        current_start = current_end - 99
        url = f"https://api.opap.gr/draws/v3.0/1100/draw-id/{current_start}/{current_end}"
        
        status_text.text(f"📥 Συλλογή δεδομένων: Πακέτο {i+1}/5...")
        data = get_data_safely(url)
        
        if data:
            for draw in data:
                if 'winningNumbers' in draw:
                    all_draws.append(draw['winningNumbers']['list'])
        
        current_end = current_start - 1
        progress_bar.progress((i + 1) / 5)
        time.sleep(1.2) # Χρόνος αναμονής για να μην μας μπλοκάρει ο ΟΠΑΠ
        
    return all_draws

st.title("🎰 Kino AI Predictor: Deep Analysis")

if 'big_data' not in st.session_state:
    st.session_state.big_data = None

# Λήψη Active ID με ασφάλεια
active_data = get_data_safely("https://api.opap.gr/draws/v3.0/1100/active")
active_id = active_data['drawId'] if active_data else None

if st.sidebar.button("🚀 ΕΝΑΡΞΗ ΕΚΠΑΙΔΕΥΣΗΣ"):
    if active_id:
        with st.spinner("Η μηχανή αναλύει το ιστορικό..."):
            st.session_state.big_data = fetch_history(active_id)
            if not st.session_state.big_data:
                st.error("⚠️ Ο ΟΠΑΠ περιόρισε την πρόσβαση. Δοκιμάστε ξανά σε λίγα λεπτά.")
    else:
        st.error("⚠️ Αδυναμία σύνδεσης με τον διακομιστή του ΟΠΑΠ.")

if st.session_state.big_data:
    draws = st.session_state.big_data
    st.success(f"✅ Η εκπαίδευση ολοκληρώθηκε σε {len(draws)} κληρώσεις!")
    
    # Στατιστική Ανάλυση
    all_nums = [n for sub in draws for n in sub]
    counts = Counter(all_nums)
    
    # Εμφάνιση Top 15
    df = pd.DataFrame(counts.most_common(15), columns=['Αριθμός', 'Συχνότητα'])
    st.subheader("🔥 Hot Numbers (Τρέχουσα Τάση)")
    st.bar_chart(df.set_index('Αριθμός'))
    
    # Πρόβλεψη
    top_picks = df['Αριθμός'].head(5).tolist()
    st.divider()
    st.header(f"🎯 Προτεινόμενη 5άδα: {sorted(top_picks)}")
    st.balloons()
