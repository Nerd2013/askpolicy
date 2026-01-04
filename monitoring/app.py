import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="AskPolicy Monitor", layout="wide")
st.title("AskPolicy — Monitoring UI")

query = st.text_input("Question", value="How long do refunds take?")

if st.button("Ask"):
    with st.spinner("Querying AskPolicy..."):
        resp = requests.post(
            API_URL,
            params={"q": query},
        )

    if resp.status_code != 200:
        st.error(f"API error: {resp.text}")
    else:
        data = resp.json()

        # Answer
        st.subheader("Answer")
        st.write(data["answer"])

        explanation = data.get("explanation", {})

        # Stats
        st.subheader("Context Stats")
        st.json(explanation.get("stats", {}))

        # Approved chunks
        st.subheader("Approved Chunks")
        for i, chunk in enumerate(explanation.get("approved", []), start=1):
            with st.expander(f"Chunk {i} — {chunk['doc_id']}"):
                st.write(f"Distance: {chunk['distance']}")
                st.write(f"Reason: {chunk['reason']}")

        # Dropped chunks
        if explanation.get("dropped"):
            st.subheader("Dropped Chunks")
            for chunk in explanation["dropped"]:
                with st.expander(f"Dropped — {chunk['doc_id']}"):
                    st.write(chunk)