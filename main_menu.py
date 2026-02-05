import os
import csv
import remi.gui as gui
# Note: You will eventually need to convert these imported classes to Remi too!
from unit_selection_menu import UnitSelectionMenu
from chapter_selection_menu import ChapterSelectionMenu
from question_count_menu import QuestionCountMenu
from quiz_ui import start_quiz

DATA_FOLDER = "data"


class MainMenu:
    def __init__(self, app_instance):
        self.app = app_instance  # This is our reference to the main web app
        self.data_folder = DATA_FOLDER

    def get_quiz_files(self):
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        return [f for f in os.listdir(self.data_folder) if f.endswith(".csv")]

    def build_ui(self):
        """Creates and returns the Main Menu visual layout"""
        # Main Vertical Container
        container = gui.VBox(width='100%', style={'margin': '0px auto', 'background-color': 'white'})

        # Title (Label)
        title = gui.Label("Select a Quiz", style={
            'font-size': '22px',
            'font-weight': 'bold',
            'margin': '30px auto',
            'display': 'block'
        })
        container.append(title)

        # File Buttons
        for file in self.get_quiz_files():
            button_label = file.replace(".csv", "").replace("_", " ").title()

            # Create button
            btn = gui.Button(button_label, width='80%', height='50px', style={'margin': '8px auto'})

            # Setup click event (Remi passes widget first, then our custom args)
            btn.onclick.do(self.handle_quiz_selection, file)

            container.append(btn)

        return container

    def handle_quiz_selection(self, widget, filename):
        """Logic for determining which menu to show next"""
        full_path = os.path.join(self.data_folder, filename)
        unique_units = set()
        unique_chapters = set()

        try:
            with open(full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    u = row.get("unit_number", "").strip()
                    c = row.get("chapter_number", "").strip()
                    if u: unique_units.add(u)
                    if c: unique_chapters.add(c)
        except Exception as e:
            print(f"Error reading file: {e}")

        sorted_units = sorted(list(unique_units))
        sorted_chapters = sorted(list(unique_chapters))

        # NAVIGATION LOGIC
        if len(sorted_units) <= 1:
            self.open_question_amount_menu(filename, sorted_units, sorted_chapters)
        else:
            # Switch screen to Unit Selection
            menu = UnitSelectionMenu(
                app_instance=self.app,
                data_folder=self.data_folder,
                filename=filename,
                open_next_menu_callback=self.open_chapter_selection,
                show_main_menu_callback=self.show_self
            )
            self.app.set_root_widget(menu.build_ui())

    def show_self(self):
        """Helper to return to this main menu"""
        self.app.set_root_widget(self.build_ui())

    def open_chapter_selection(self, filename, selected_units):
        menu = ChapterSelectionMenu(
            app_instance=self.app,
            data_folder=self.data_folder,
            filename=filename,
            selected_units=selected_units,
            open_next_menu_callback=self.open_question_amount_menu,
            show_main_menu_callback=self.show_self
        )
        self.app.set_root_widget(menu.build_ui())

    def open_question_amount_menu(self, filename, selected_units, selected_chapters):
        menu = QuestionCountMenu(
            app_instance=self.app,
            data_folder=self.data_folder,
            filename=filename,
            selected_units=selected_units,
            selected_chapters=selected_chapters,
            start_quiz_callback=start_quiz,
            show_main_menu_callback=self.show_self
        )
        self.app.set_root_widget(menu.build_ui())