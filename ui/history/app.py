import sys
from pathlib import Path

# Add askpolicy-app/app to PYTHONPATH
APP_ROOT = Path(__file__).resolve().parents[2] / "app"
sys.path.insert(0, str(APP_ROOT))

import streamlit as st
from persistence.store import list_interactions

st.set_page_config(
    page_title="AskPolicy History",
    layout="wide",
)

st.title("AskPolicy — History & Audit Log")

limit = st.slider("Number of recent interactions", 5, 100, 20)

records = list_interactions(limit=limit)

if not records:
    st.info("No interactions found.")
else:
    for r in records:
        with st.expander(
            f"[{r['id']}] {r['timestamp']} — {r['question']}"
        ):
            st.markdown("### Answer")
            st.write(r["answer"])

            st.markdown("### Explanation")
            st.json(r["explanation"])