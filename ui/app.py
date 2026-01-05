import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="AskPolicy",
    layout="centered",
)

st.title("AskPolicy")
st.caption("Ask questions about company policies")

query = st.text_input(
    "Your question",
    placeholder="e.g. How long do refunds take?",
)

if st.button("Ask") and query.strip():
    with st.spinner("Thinking..."):
        resp = requests.post(
            API_URL,
            params={"q": query},
        )

    if resp.status_code != 200:
        st.error("Something went wrong. Please try again.")
    else:
        data = resp.json()

        st.markdown("### Answer")
        st.write(data["answer"])