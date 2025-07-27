# create_csv.py
import csv

with open("entries.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Type", "Text", "Mood", "Energy", "Tags", "GPT_Summary"])

print("✅ CSV file initialized!")