import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import streamlit as st

def run_dashboard():  # <-- make sure this is defined
    st.set_page_config(page_title="Emotional Dashboard", layout="wide")

    # Load
    def load_entries(file_path="entries.csv"):
        try:
            df = pd.read_csv(file_path)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except FileNotFoundError:
            st.error("entries.csv not found!")
            return pd.DataFrame()

    # Clean
    def clean_text(text):
        text = re.sub(r"[^\w\s]", "", text.lower())
        return text

    # Plot mood
    def plot_mood_over_time(df):
        df = df.copy()
        df['Mood'] = pd.to_numeric(df['Mood'], errors='coerce')
        df = df.dropna(subset=['Mood'])
        df = df.sort_values('Date')
        plt.figure(figsize=(10, 4))
        plt.plot(df['Date'], df['Mood'], marker='o')
        plt.title("Mood Over Time")
        plt.xlabel("Date")
        plt.ylabel("Mood (1–10)")
        st.pyplot(plt)

    # Plot energy
    def plot_energy_over_time(df):
        df = df.copy()
        df['Energy'] = pd.to_numeric(df['Energy'], errors='coerce')
        df = df.dropna(subset=['Energy'])
        df = df.sort_values('Date')
        plt.figure(figsize=(10, 4))
        plt.plot(df['Date'], df['Energy'], color='orange', marker='s')
        plt.title("Energy Over Time")
        plt.xlabel("Date")
        plt.ylabel("Energy (1–10)")
        st.pyplot(plt)

    # Word Cloud
    def generate_word_cloud(df):
        if 'Text' not in df.columns:
            st.warning("No text found.")
            return
        text = " ".join(df['Text'].dropna().astype(str))
        wc = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 4))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud")
        st.pyplot(plt)

    # Streamlit App
    df = load_entries()

    if df.empty:
        st.warning("No data loaded.")
    else:
        st.title("📊 Emotional Dashboard")
        st.subheader("🔁 Mood & Energy Trends")
        plot_mood_over_time(df)
        plot_energy_over_time(df)

        st.divider()
        st.subheader("☁️ Word Cloud from Entries")
        generate_word_cloud(df)

        st.divider()
        st.subheader("📜 Raw Data")
        st.dataframe(df, use_container_width=True)
