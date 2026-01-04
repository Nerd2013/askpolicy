import streamlit as st
import requests
import re

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="AskPolicy Monitor", layout="wide")
st.title("AskPolicy — Monitoring UI")

# ----------------------------
# Helpers
# ----------------------------

def extract_citation_numbers(answer_text: str) -> set[int]:
    return {
        int(n)
        for n in re.findall(r"\[(\d+)\]", answer_text)
    }


# ----------------------------
# UI
# ----------------------------

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

        # ----------------------------
        # Answer
        # ----------------------------
        answer_text = data["answer"]
        citations = extract_citation_numbers(answer_text)

        st.subheader("Answer")
        st.markdown(answer_text)
        st.caption(f"Citations used: {sorted(citations) if citations else 'None'}")

        explanation = data.get("explanation", {})

        # ----------------------------
        # Stats
        # ----------------------------
        st.subheader("Context Stats")
        st.json(explanation.get("stats", {}))

        # ----------------------------
        # Approved Chunks (Enhanced)
        # ----------------------------
        approved = explanation.get("approved", [])

        if approved:
            # Sort by distance
            approved_sorted = sorted(
                approved,
                key=lambda c: c.get("distance", float("inf"))
            )

            # Filter by doc_id
            doc_ids = sorted({c["doc_id"] for c in approved_sorted})
            selected_doc = st.selectbox(
                "Filter by document",
                options=["ALL"] + doc_ids,
                index=0,
            )

            if selected_doc != "ALL":
                approved_sorted = [
                    c for c in approved_sorted
                    if c["doc_id"] == selected_doc
                ]

            st.subheader("Approved Chunks")

            for i, chunk in enumerate(approved_sorted, start=1):
                header = f"Chunk {i} — {chunk['doc_id']}"

                if i in citations:
                    header += " ⭐ (cited)"

                with st.expander(header):
                    st.write(f"**Distance:** {chunk['distance']}")
                    st.write(f"**Reason:** {chunk['reason']}")

                    if "text" in chunk:
                        st.markdown("**Raw Text:**")
                        st.code(chunk["text"])

        # ----------------------------
        # Dropped Chunks
        # ----------------------------
        if explanation.get("dropped"):
            st.subheader("Dropped Chunks")
            for chunk in explanation["dropped"]:
                with st.expander(f"Dropped — {chunk['doc_id']}"):
                    st.json(chunk)