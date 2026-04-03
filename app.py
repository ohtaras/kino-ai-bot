import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Kino AI", page_icon="🎰")
st.title("🎰 Kino AI Predictor")

# Λήψη δεδομένων από ΟΠΑΠ με ασφάλεια
def get_last_draw():
    try:
        api_url = "https://api.opap.gr/draws/v3.0/1100/last-n/1"
        response = requests.get(api_url)
        data = response.json()
        return data[0]['winningNumbers']['list']
    except:
        return None

numbers = get_last_draw()

if numbers:
    st.subheader(f"Τελευταία Κλήρωση: {numbers}")
else:
    st.warning("Περιμένω δεδομένα από τον ΟΠΑΠ...")

st.divider()
st.info("💡 Η μηχανή αναλύει τα Excel σου στο Drive για να βρει μοτίβα.")

# Εδώ θα εμφανίζονται οι προτάσεις όταν η σιγουριά είναι > 88%
st.write("### 🎯 Προγνωστικά AI")
st.write("Αναμονή για την επόμενη κλήρωση... (Σιγουριά: 0%)")
