import csv

def load_questions(filename):
    questions = []
    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # This logic remains perfect for the web
                questions.append({
                    "question_number": row.get("question_number", "").strip(),
                    "unit_number": row.get("unit_number", "").strip(),
                    "chapter_number": row.get("chapter_number", "").strip(),
                    "question": row.get("question", "").strip(),
                    "choice_a": row.get("choice_a", "").strip(),
                    "choice_b": row.get("choice_b", "").strip(),
                    "choice_c": row.get("choice_c", "").strip(),
                    "choice_d": row.get("choice_d", "").strip(),
                    "answer": row.get("answer", "").strip().upper()
                })
    except Exception as e:
        print(f"Error loading questions from {filename}: {e}")

    return questions