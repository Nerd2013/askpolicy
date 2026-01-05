import sys
from pathlib import Path
import difflib

# Add askpolicy-app/app to PYTHONPATH
APP_ROOT = Path(__file__).resolve().parents[2] / "app"
sys.path.insert(0, str(APP_ROOT))

import streamlit as st
from persistence.store import list_interactions


def diff_text(old: str, new: str) -> str:
    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        lineterm="",
        fromfile="Original",
        tofile="Replay",
    )
    return "\n".join(diff)


def extract_chunk_ids(explanation):
    return {
        f"{c['doc_id']}#{c['chunk_index']}"
        for c in explanation.get("approved", [])
    }
    
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
            # --------------------
            # Original Answer
            # --------------------
            st.markdown("### 🕘 Original Answer")
            st.write(r["answer"])

            # --------------------
            # Replay button
            # --------------------
            if st.button(f"🔁 Replay #{r['id']}", key=f"replay_{r['id']}"):
                import requests

                resp = requests.post(
                    f"http://127.0.0.1:8000/replay/{r['id']}"
                )

                if resp.status_code != 200:
                    st.error("Replay failed")
                else:
                    replay_data = resp.json()

                    # --------------------
                    # Replay Answer
                    # --------------------
                    st.markdown("### 🔁 Replay Answer")
                    st.write(replay_data["replay"]["answer"])

                    # --------------------
                    # Answer Diff
                    # --------------------
                    st.markdown("### 🔍 Answer Diff")

                    answer_diff = diff_text(
                        r["answer"],
                        replay_data["replay"]["answer"],
                    )

                    if answer_diff.strip():
                        st.code(answer_diff)
                    else:
                        st.caption("No change in answer text.")

                    # --------------------
                    # Context Diff
                    # --------------------
                    st.markdown("### 📄 Context Diff")

                    old_chunks = extract_chunk_ids(r["explanation"])
                    new_chunks = extract_chunk_ids(
                        replay_data["replay"]["explanation"]
                    )

                    added = new_chunks - old_chunks
                    removed = old_chunks - new_chunks

                    if not added and not removed:
                        st.caption("No change in approved context chunks.")
                    else:
                        if added:
                            st.markdown("**Added chunks:**")
                            for c in sorted(added):
                                st.write(f"+ {c}")

                        if removed:
                            st.markdown("**Removed chunks:**")
                            for c in sorted(removed):
                                st.write(f"- {c}")

                    # --------------------
                    # Replay Explanation
                    # --------------------
                    with st.expander("🔍 Replay Explanation (details)"):
                        st.json(replay_data["replay"]["explanation"])

                    # --------------------
                    # Original Explanation
                    # --------------------
                    with st.expander("📘 Original Explanation (details)"):
                        st.json(r["explanation"])