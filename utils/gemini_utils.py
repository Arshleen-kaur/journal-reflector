"""import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def get_tags_and_summary(text):
    prompt = f
    Analyze the following journal/dream entry:
    If it is a dream, apply freudian analysis of dream and form a result as to what this dream may have been related to
    Text: {text}
    1. Mood (e.g., happy, anxious, sad, frustrated, neutral)
    2. Energy Level (e.g., high, moderate, low)
    3. Summarize the entry in one line.
    4. List key themes/tags: emotions, activities, people, dream motifs if present.

    Format:
    Mood: ...
    Energy: ...
    Summary: <summary here>
    Tags: <comma-separated tags>
    

    try:
        response = model.generate_content(prompt)
        content = response.text

        # Very basic parsing
        lines = content.strip().split("\n")
        summary = lines[0].replace("Summary:", "").strip()
        tags = lines[1].replace("Tags:", "").strip()

        return summary, tags
    except Exception as e:
        print("Gemini error:", e)
        return "Error", ""
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_with_gemini(text):
    prompt = f"""
    Text: {text}
    Analyze the following journal/dream entry:
    If it is a dream, apply Freudian analysis and infer what the dream may be related to.

    Provide the following in the response:

    1. Mood (e.g., happy, anxious, sad, frustrated, neutral)
    2. Energy Level (e.g., high, moderate, low)
    3. Summarize the entry in one line.
    4. List key themes/tags: emotions, activities, people, dream motifs if present.

    Format:
    Mood: ...
    Energy: ...
    Summary: <summary here>
    Tags: <comma-separated tags>
    """

    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split("\n")

        mood = energy = summary = tags = ""

        for line in lines:
            if "Mood:" in line:
                mood = line.replace("Mood:", "").strip().lower()
            elif "Energy:" in line:
                energy = line.replace("Energy:", "").strip().lower()
            elif "Summary:" in line:
                summary = line.replace("Summary:", "").strip()
            elif "Tags:" in line:
                tags = line.replace("Tags:", "").strip()

        # === Mood mapping (scale 1–10) ===
        mood_scale = {
            "very depressed": 1, "scared": 2, "sad": 3, "anxious": 4,
            "neutral": 5, "calm": 6, "content": 7, "happy": 8,
            "excited": 9, "euphoric": 10
        }
        mood_score = next((v for k, v in mood_scale.items() if k in mood), 5)  # default = 5

        # === Energy mapping (scale 1–10) ===
        energy_scale = {
            "exhausted": 1, "very low": 2, "low": 3, "tired": 4,
            "moderate": 5, "okay": 6, "normal": 6, "good": 7,
            "high": 8, "very high": 9, "energetic": 10
        }
        energy_score = next((v for k, v in energy_scale.items() if k in energy), 5)  # default = 5

        return mood_score, energy_score, summary, tags

    except Exception as e:
        print("Gemini error:", e)
        return 5, 5, "Error", ""
