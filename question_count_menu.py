import os
import csv
import remi.gui as gui


class QuestionCountMenu:
    def __init__(self, app_instance, data_folder, filename, selected_units, selected_chapters, start_quiz_callback,
                 show_main_menu_callback):
        self.app = app_instance
        self.data_folder = data_folder
        self.filename = filename
        self.selected_units = selected_units
        self.selected_chapters = selected_chapters
        self.start_quiz = start_quiz_callback
        self.show_main_menu = show_main_menu_callback
        self.full_path = os.path.join(self.data_folder, self.filename)

        self.total_questions = self.count_questions()

    def count_questions(self):
        count = 0
        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    u = row.get("unit_number", "").strip()
                    c = row.get("chapter_number", "").strip()
                    unit_ok = not self.selected_units or u in self.selected_units
                    chap_ok = not self.selected_chapters or c in self.selected_chapters
                    if unit_ok and chap_ok:
                        count += 1
        except:
            return 0
        return count

    def build_ui(self):
        # 1. Main Container
        container = gui.VBox(width='100%', style={'margin': '0px auto', 'background-color': 'white'})

        # 2. Labels
        lbl_title = gui.Label("Quiz Setup", style={'font-size': '20px', 'font-weight': 'bold', 'margin': '20px'})
        lbl_count = gui.Label(f"Total Questions: {self.total_questions}", style={'font-size': '16px', 'margin': '10px'})

        container.append(lbl_title)
        container.append(lbl_count)

        # 3. SpinBox (Numeric Input)
        # In Remi, SpinBox arguments are: (default_value, min, max, step)
        self.spinbox = gui.SpinBox(self.total_questions, 1, max(1, self.total_questions), 1,
                                   width='150px', height='40px', style={'margin': '20px', 'font-size': '18px'})
        container.append(self.spinbox)

        # 4. Buttons
        btn_start = gui.Button("START QUIZ", width='80%', height='60px',
                               style={'background-color': '#4CAF50', 'color': 'white', 'font-weight': 'bold',
                                      'margin': '10px'})
        btn_start.onclick.do(self.start_selected_amount)

        btn_back = gui.Button("Back", width='80%', height='40px', style={'margin': '10px'})
        btn_back.onclick.do(lambda widget: self.show_main_menu())

        container.append(btn_start)
        container.append(btn_back)

        return container

    def start_selected_amount(self, widget):
        # In Remi, we use .get_value()
        try:
            amount = int(self.spinbox.get_value())
        except:
            amount = self.total_questions

        # Passing control to the quiz_ui
        self.start_quiz(self.app, self.filename, amount, self.show_main_menu,
                        self.selected_units, self.selected_chapters)