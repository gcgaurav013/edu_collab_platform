import datetime
import pandas as pd
import streamlit as st

# This mimics a database. For a production-ready version, connect to Firebase.
# We use a session-state-based mock that persists during the session.
class CollabHub:
    def __init__(self):
        if 'global_db' not in st.session_state:
            # Mock data to make it look realistic immediately
            st.session_state.global_db = [
                {
                    "author": "Dr. Aris (Oxford)",
                    "title": "Quantum Computing Basics",
                    "model": "GPT-4o",
                    "score": 98,
                    "timestamp": "2023-10-24 14:00",
                    "content": "Quantum bits or qubits represent...",
                    "language": "English"
                },
                {
                    "author": "Global_Learner_88",
                    "title": "Photosynthesis Deep Dive",
                    "model": "Llama-3.3",
                    "score": 92,
                    "timestamp": "2023-10-25 09:30",
                    "content": "Process where light energy is converted...",
                    "language": "English"
                }
            ]

    def publish_resource(self, title, content, author, model, score, lang):
        entry = {
            "author": author,
            "title": title,
            "model": model,
            "score": score,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "content": content,
            "language": lang
        }
        st.session_state.global_db.insert(0, entry) # Add to top

    def get_all(self):
        return st.session_state.global_db