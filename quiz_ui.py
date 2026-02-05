import os
import remi.gui as gui
from quiz_logic import QuizLogic
# Keep these managers as is, assuming they don't use Tkinter
from score_manager import start_quiz as start_quiz_tracking, end_quiz
from wrong_answer_manager import WrongAnswerManager

DATA_FOLDER = "data"


class QuizUI:
    def __init__(self, app_instance, filename, limit, show_main_menu_callback, selected_units, selected_chapters):
        self.app = app_instance
        self.filename = filename
        self.limit = limit
        self.show_main_menu = show_main_menu_callback
        self.units = selected_units
        self.chapters = selected_chapters
        self.wrong_manager = WrongAnswerManager()

        # State
        self.current_question_number = 0
        self.full_path = os.path.join(DATA_FOLDER, filename)

        # Initialize Logic
        self.quiz = QuizLogic(
            self.full_path,
            selected_units=selected_units,
            selected_chapters=selected_chapters,
            limit=limit
        )

        start_quiz_tracking(filename)

    def build_ui(self):
        # Main Scrollable Container for Mobile
        self.container = gui.VBox(width='100%',
                                  style={'margin': '0px auto', 'background-color': 'white', 'padding': '10px'})

        # Question Display
        self.lbl_question = gui.Label("", style={'font-size': '18px', 'margin': '15px', 'text-align': 'center'})

        # Metadata Labels
        self.lbl_meta = gui.Label("", style={'font-size': '14px', 'color': 'gray'})
        self.lbl_progress = gui.Label("", style={'font-size': '14px', 'font-weight': 'bold', 'margin': '5px'})

        self.container.append(self.lbl_question)
        self.container.append(self.lbl_meta)
        self.container.append(self.lbl_progress)

        # Answer Buttons
        self.buttons = {}
        for letter in ["A", "B", "C", "D"]:
            btn = gui.Button("", width='90%', height='50px', style={'margin': '5px auto'})
            btn.onclick.do(self.handle_answer, letter)
            self.buttons[letter] = btn
            self.container.append(btn)

        # Result display
        self.lbl_result = gui.Label("", style={'font-size': '16px', 'margin': '15px'})
        self.container.append(self.lbl_result)

        # Navigation
        self.btn_next = gui.Button("Next Question", width='90%', height='50px',
                                   style={'background-color': '#2196F3', 'color': 'white'})
        self.btn_next.onclick.do(self.next_question)
        self.btn_next.set_enabled(False)  # Start disabled

        btn_back = gui.Button("Back to Main Menu", width='90%', style={'margin-top': '20px'})
        btn_back.onclick.do(lambda w: self.show_main_menu())

        self.container.append(self.btn_next)
        self.container.append(btn_back)

        # Load the first question
        self.load_question()

        return self.container

    def load_question(self):
        question = self.quiz.get_current_question()

        if not question:
            self.show_final_score()
            return

        self.current_question_number += 1

        # Update Text
        self.lbl_question.set_text(question["question"])

        qn = question.get("question_number", "").strip()
        ch = question.get("chapter_number", "").strip()
        self.lbl_meta.set_text(f"Q#: {qn} | Chapter: {ch}")

        self.lbl_progress.set_text(f"Progress: {self.current_question_number} / {self.quiz.total_questions}")

        # Update Buttons
        for letter in ["A", "B", "C", "D"]:
            choice_text = question.get(f"choice_{letter.lower()}", "")
            self.buttons[letter].set_text(f"{letter}) {choice_text}")
            self.buttons[letter].set_enabled(True)
            self.buttons[letter].style['background-color'] = 'lightgray'  # Reset color

        self.lbl_result.set_text("")
        self.btn_next.set_enabled(False)

    def handle_answer(self, widget, letter):
        is_correct, correct_letter = self.quiz.check_answer(letter)
        question = self.quiz.get_current_question()
        correct_text = question[f"choice_{correct_letter.lower()}"]

        if is_correct:
            self.lbl_result.set_text(f"✅ Correct!")
            widget.style['background-color'] = 'green'
        else:
            self.lbl_result.set_text(f"❌ Correct: {correct_letter}")
            widget.style['background-color'] = 'red'
            self.wrong_manager.add_wrong_answer(question)

        # Disable choices until 'Next' is clicked
        for btn in self.buttons.values():
            btn.set_enabled(False)
        self.btn_next.set_enabled(True)

    def next_question(self, widget):
        if self.quiz.next_question():
            self.load_question()
        else:
            self.show_final_score()

    def show_final_score(self):
        end_quiz(self.quiz.score, self.quiz.total_questions)

        # Clear container and show results
        self.container.empty()

        score_lbl = gui.Label(f"Final Score: {self.quiz.score} / {self.quiz.total_questions}",
                              style={'font-size': '26px', 'margin': '40px auto'})

        btn_restart = gui.Button("Restart Quiz", width='80%', height='50px')
        btn_restart.onclick.do(self.restart_quiz)

        btn_menu = gui.Button("Back to Menu", width='80%', style={'margin-top': '10px'})
        btn_menu.onclick.do(lambda w: self.show_main_menu())

        self.container.append(score_lbl)
        self.container.append(btn_restart)
        self.container.append(btn_menu)

    def restart_quiz(self, widget):
        # Just create a new UI instance and swap
        new_quiz = QuizUI(self.app, self.filename, self.limit, self.show_main_menu, self.units, self.chapters)
        self.app.set_root_widget(new_quiz.build_ui())


# To bridge this to your previous menu:
def start_quiz(app_instance, filename, limit, show_main_menu_callback, units, chapters):
    ui = QuizUI(app_instance, filename, limit, show_main_menu_callback, units, chapters)
    app_instance.set_root_widget(ui.build_ui())