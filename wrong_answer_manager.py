import csv
import os

# We define the data folder relative to where your main.py is running
DATA_FOLDER = "data"
WRONG_ANSWER_FILE = os.path.join(DATA_FOLDER, "wrong_answers.csv")

class WrongAnswerManager:

    def __init__(self, filename=WRONG_ANSWER_FILE):
        self.filename = filename
        # Ensure the directory exists so the open() command doesn't fail
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create the file with headers if it does not exist on the server."""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "question", "choice_a", "choice_b", "choice_c", "choice_d", "answer"
                ])

    def add_wrong_answer(self, question_dict):
        """Append wrong question to the server's CSV file."""
        try:
            with open(self.filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    question_dict.get("question", ""),
                    question_dict.get("choice_a", ""),
                    question_dict.get("choice_b", ""),
                    question_dict.get("choice_c", ""),
                    question_dict.get("choice_d", ""),
                    question_dict.get("answer", "")
                ])
        except Exception as e:
            print(f"Error saving wrong answer to CSV: {e}")