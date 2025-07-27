import streamlit as st
import csv
from datetime import datetime
from collections import deque
from utils.gemini_utils import analyze_with_gemini
import pandas as pd
import subprocess
from dashboard import run_dashboard 

CSV_FILE = "entries.csv"

st.set_page_config(page_title="Emotion Agent", layout="centered")

# ======= Add Entry =======
def add_entry_ui():
    st.subheader("✏️ Add a New Entry")

    entry_type = st.selectbox("Type of entry", ["journal", "dream"])
    entry_text = st.text_area("Write your entry below", height=200)

    if st.button("Submit Entry"):
        if not entry_text.strip():
            st.warning("Entry cannot be empty.")
            return

        mood, energy, summary, tags = analyze_with_gemini(entry_text)
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(CSV_FILE, "a", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([today, entry_type, entry_text, mood, energy, tags, summary])

        st.success("✅ Entry saved!")
        st.markdown(f"**Mood:** {mood} | **Energy:** {energy}")
        st.markdown(f"**Summary:** {summary}")
        st.markdown(f"**Tags:** {tags}")

if st.button("Clear all entries"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

# ======= Search Entries =======
def search_entries_ui():
    st.subheader("🔍 Search Entries")

    date_filter = st.text_input("Filter by date (YYYY-MM-DD)", "")
    type_filter = st.selectbox("Filter by type", ["", "journal", "dream"])
    mood_min = st.slider("Minimum mood", 1, 10, 1)
    keyword = st.text_input("Search keyword", "")

    results = []
    try:
        with open(CSV_FILE, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                date, e_type, text, mood, energy, tags, summary = row
                if date_filter and not date.startswith(date_filter):
                    continue
                if type_filter and e_type.lower() != type_filter:
                    continue
                try:
                    if int(mood) < int(mood_min):
                        continue
                except:
                    continue
                if keyword and keyword.lower() not in text.lower() and keyword.lower() not in summary.lower():
                    continue
                results.append(row)
    except FileNotFoundError:
        st.warning("entries.csv not found.")
        return

    if not results:
        st.warning("❌ No matching entries found.")
    else:
        st.success(f"📋 Found {len(results)} result(s):")
        for r in results:
            st.markdown(f"**🗓 {r[0]}** | Type: *{r[1]}* | Mood: *{r[3]}*")
            st.markdown(f"→ {r[2][:150]}...")
            st.markdown("---")


# ======= Emotional Red Flags =======
def emotional_red_flags_ui():
    st.subheader("🚨 Emotional Red Flag Scan")
    mood_deque = deque(maxlen=5)
    overwhelmed_count = 0
    red_flags = []

    try:
        with open(CSV_FILE, newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                date, e_type, text, mood, energy, tags, summary = row
                try:
                    mood = int(mood)
                    mood_deque.append(mood)
                    if all(m <= 4 for m in mood_deque) and len(mood_deque) == 5:
                        red_flags.append(f"⚠️ 5 low mood entries ending on {date}")
                except:
                    continue

                if "overwhelmed" in text.lower() or "overwhelmed" in summary.lower():
                    overwhelmed_count += 1
    except FileNotFoundError:
        st.warning("entries.csv not found.")
        return

    if red_flags:
        for flag in red_flags:
            st.error(flag)
    else:
        st.success("✅ No 5-day low mood streaks.")

    if overwhelmed_count >= 3:
        st.warning(f"⚠️ 'Overwhelmed' mentioned {overwhelmed_count} times — consider journaling stressors.")
    else:
        st.success("✅ No repeated 'overwhelmed' mentions.")



# ======= Launch Dashboard =======
def launch_dashboard():
    st.subheader("📊 Mood Trend Dashboard")
    if st.button("Show Me My Mood Trend"):
        run_dashboard() 

# ======= Sidebar Navigation =======
st.title("📘 Emotion Agent")

page = st.sidebar.radio("Navigate", ["Add Entry", "Search", "Red Flags", "Dashboard"])

if page == "Add Entry":
    add_entry_ui()
elif page == "Search":
    search_entries_ui()
elif page == "Red Flags":
    emotional_red_flags_ui()
elif page == "Dashboard":
    launch_dashboard()
