# utils/analyzer.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

def analyze_entry(text):
    # Mood analysis
    sentiment_scores = sid.polarity_scores(text)
    compound = sentiment_scores['compound']

    if compound >= 0.5:
        mood = "happy"
    elif compound >= 0.1:
        mood = "calm"
    elif compound <= -0.5:
        mood = "angry/sad"
    elif compound <= -0.1:
        mood = "anxious"
    else:
        mood = "neutral"

    # Energy analysis (basic keyword spotting)
    text_lower = text.lower()
    if any(word in text_lower for word in ["tired", "drained", "exhausted", "sleepy"]):
        energy = "low"
    elif any(word in text_lower for word in ["energized", "active", "pumped", "excited"]):
        energy = "high"
    else:
        energy = "moderate"

    return mood, energy
