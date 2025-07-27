import streamlit as st
import pandas as pd
from dream_analyzer import load_dream_entries, analyze_dreams, generate_gpt_style_insight

# Page config
st.set_page_config(page_title="Dream Dashboard", page_icon="🌙", layout="wide")

st.title("🌙 Dream Insight Dashboard")
st.markdown("Welcome! This dashboard analyzes your dream entries and uncovers hidden patterns.")

# Load data
dreams = load_dream_entries()

if not dreams:
    st.warning("No dream entries found in `entries.csv`. Try adding some!")
else:
    motifs, people = analyze_dreams(dreams)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔁 Motif Frequency")
        motif_df = pd.DataFrame(motifs.most_common(), columns=["Motif", "Count"])
        st.dataframe(motif_df, use_container_width=True)

    with col2:
        st.subheader("🧑‍🤝‍🧑 Recurring People / Symbols")
        people_df = pd.DataFrame(people.most_common(), columns=["Name", "Count"])
        st.dataframe(people_df, use_container_width=True)

    st.divider()
    st.subheader("🤖 GPT-style Insight")
    insight = generate_gpt_style_insight(motifs, people)
    st.markdown(insight)

    st.divider()
    st.subheader("📝 All Dream Entries")
    for i, d in enumerate(dreams, 1):
        with st.expander(f"Dream #{i}"):
            st.write(d)
