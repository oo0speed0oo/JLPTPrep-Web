import random
import os
from question_loader import load_questions

class QuizLogic:
    def __init__(self, csv_file, selected_units=None, selected_chapters=None, limit=None):
        # We ensure the path is correct for the server environment
        # CSV_FILE should be the full path (e.g., 'data/quiz.csv')
        all_questions = load_questions(csv_file)

        units = selected_units if selected_units else []
        chapters = selected_chapters if selected_chapters else []

        filtered_questions = []
        for q in all_questions:
            unit_val = q.get("unit_number", "").strip()
            unit_match = not units or unit_val in units

            chap_val = q.get("chapter_number", "").strip()
            chap_match = not chapters or chap_val in chapters

            if unit_match and chap_match:
                filtered_questions.append(q)

        random.shuffle(filtered_questions)

        if limit and limit < len(filtered_questions):
            filtered_questions = filtered_questions[:limit]

        self.all_questions = filtered_questions
        self.total_questions = len(filtered_questions)
        self.current_index = 0
        self.score = 0

    def get_current_question(self):
        if 0 <= self.current_index < self.total_questions:
            return self.all_questions[self.current_index]
        return None

    def check_answer(self, user_choice):
        current = self.get_current_question()
        if not current:
            return False, None

        correct_letter = current["answer"].strip().upper()
        # Web browsers sometimes send extra whitespace, so we strip() carefully
        is_correct = user_choice.strip().upper() == correct_letter

        if is_correct:
            self.score += 1

        return is_correct, correct_letter

    def next_question(self):
        if self.current_index < self.total_questions - 1:
            self.current_index += 1
            return True
        return False

    def restart_quiz(self):
        random.shuffle(self.all_questions)
        self.current_index = 0
        self.score = 0