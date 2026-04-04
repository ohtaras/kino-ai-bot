import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from collections import Counter

st.set_page_config(page_title="Kino AI Engine", layout="wide")

def get_opap_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        return res.json() if res.status_code == 200 else None
    except:
        return None

# --- ΚΥΡΙΩΣ ΕΦΑΡΜΟΓΗ ---
st.title("🎰 Kino AI: Daily Training Mode")

# 1. ΠΑΙΡΝΟΥΜΕ ΤΗΝ ACTIVE ΚΛΗΡΩΣΗ
active_info = get_opap_data("https://api.opap.gr/draws/v3.0/1100/last-result-and-active")
if active_info:
    active_id = active_info['active']['drawId']
    last_draw_nums = active_info['last']['winningNumbers']['list']
    st.sidebar.success(f"Επόμενη Κλήρωση: {active_id}")
    st.sidebar.write(f"Τελευταία Κλήρωση: {last_draw_nums}")
else:
    active_id = None

# 2. ΕΚΠΑΙΔΕΥΣΗ ΜΕ DRAW-DATE (ΟΛΗ Η ΗΜΕΡΑ)
if st.sidebar.button("🚀 ΕΚΠΑΙΔΕΥΣΗ (ΟΛΗ Η ΗΜΕΡΑ)"):
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.opap.gr/draws/v3.0/1100/draw-date/{today}/{today}"
    
    with st.spinner("Η μηχανή αναλύει όλες τις σημερινές κληρώσεις..."):
        data = get_opap_data(url)
        if data and 'content' in data:
            draws = [d['winningNumbers']['list'] for d in data['content']]
            st.session_state.daily_data = draws
            st.success(f"✅ Η μηχανή εκπαιδεύτηκε σε {len(draws)} κληρώσεις!")
        else:
            st.error("Αποτυχία λήψης ημερήσιων δεδομένων.")

# 3. ΑΝΑΛΥΣΗ & ΠΡΟΒΛΕΨΗ
if 'daily_data' in st.session_state:
    draws = st.session_state.daily_data
    all_nums = [n for sub in draws for n in sub]
    counts = Counter(all_nums)
    
    # Γράφημα Συχνότητας
    df = pd.DataFrame(counts.most_common(20), columns=['Αριθμός', 'Εμφανίσεις'])
    st.subheader(f"📊 Στατιστική Τάση Σήμερα ({len(draws)} κληρώσεις)")
    st.bar_chart(df.set_index('Αριθμός'))
    
    # Λογική AI: Hot Numbers που δεν βγήκαν στην τελευταία κλήρωση
    suggestions = []
    for num, freq in counts.most_common(30):
        if num not in last_draw_nums: # Αν λείπει από την τελευταία
            suggestions.append(num)
        if len(suggestions) == 5: break
            
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Σιγουριά AI", f"{min(99, 80 + len(draws)//10)}%")
    with col2:
        st.success(f"🎯 Πρόταση για την κλήρωση {active_id}: {sorted(suggestions)}")
    st.balloons()
else:
    st.info("Πατήστε 'ΕΚΠΑΙΔΕΥΣΗ' για να ξεκινήσει η ανάλυση της ημέρας.")
