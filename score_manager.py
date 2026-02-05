import csv
from datetime import datetime
import os

# Ensure the scores folder exists so the server doesn't crash
DATA_FOLDER = "data/test_scores"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

SCORE_FILENAME = os.path.join(DATA_FOLDER, "quiz_scores.csv")
current_quiz_file = None


def start_quiz(file):
    """Sets the active filename for the session."""
    global current_quiz_file
    current_quiz_file = file

    # Ensure the CSV file has headers if it's being created for the first time
    if not os.path.exists(SCORE_FILENAME):
        with open(SCORE_FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Quiz Name", "Score", "Total"])


def end_quiz(score, total):
    """Saves the final score to the CSV file."""
    global current_quiz_file

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(SCORE_FILENAME, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, current_quiz_file, score, total])
        print(f"✅ Score saved to {SCORE_FILENAME}: {score}/{total}")
    except Exception as e:
        print(f"❌ Error saving score: {e}")