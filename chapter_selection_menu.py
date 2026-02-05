import csv
import os
import remi.gui as gui


class ChapterSelectionMenu:
    def __init__(self, app_instance, data_folder, filename, selected_units, open_next_menu_callback,
                 show_main_menu_callback):
        # In Remi, 'app_instance' refers to the main App class running the server
        self.app = app_instance
        self.data_folder = data_folder
        self.filename = filename
        self.selected_units = selected_units
        self.open_next_menu = open_next_menu_callback
        self.show_main_menu = show_main_menu_callback
        self.full_path = os.path.join(self.data_folder, self.filename)

        # We store the checkbox widgets themselves to check their values later
        self.chapter_checkboxes = {}

        self.unique_chapters = self.get_unique_chapters()

        if not self.unique_chapters:
            # Simple print for error handling; in a real app, you'd show a gui.GenericDialog
            print("Error: No chapters found.")
            self.show_main_menu()
            return

    def get_unique_chapters(self):
        chapters = set()
        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    unit = row.get("unit_number", "").strip()
                    chapter = row.get("chapter_number", "").strip()
                    if not self.selected_units or unit in self.selected_units:
                        if chapter:
                            chapters.add(chapter)
        except Exception as e:
            print(f"Error reading chapters: {e}")
        return sorted(chapters)

    def build_ui(self):
        """Returns a container widget that Remi can display"""
        # Main Vertical Container (like your root frame)
        main_container = gui.VBox(width='100%', height='100%',
                                  style={'margin': '0px auto', 'background-color': 'white'})

        # 1. Title
        lbl_title = gui.Label("Select Chapters", style={'font-size': '18px', 'font-weight': 'bold', 'margin': '20px'})
        main_container.append(lbl_title)

        # 2. Grid for Chapters (mimicking your 2-column grid)
        # We use a GridBox for easy column control
        grid = gui.GridBox(width='90%', style={'margin': '10px auto'})
        grid.set_column_sizes(['50%', '50%'])

        for chapter in self.unique_chapters:
            # Create a horizontal box for each checkbox + label pair
            item = gui.HBox(width='100%', style={'justify-content': 'flex-start', 'padding': '5px'})

            check = gui.CheckBox(True)  # Default to checked (value=1)
            lbl = gui.Label(f"Chapter {chapter}")

            item.append(check)
            item.append(lbl)

            self.chapter_checkboxes[chapter] = check
            grid.append(item)

        main_container.append(grid)

        # 3. Buttons
        btn_continue = gui.Button("Continue", width=200,
                                  style={'margin': '20px', 'background-color': '#4CAF50', 'color': 'white'})
        btn_continue.onclick.do(self.continue_forward)

        btn_back = gui.Button("Back", width=200)
        btn_back.onclick.do(lambda widget: self.show_main_menu())

        main_container.append(btn_continue)
        main_container.append(btn_back)

        return main_container

    def continue_forward(self, widget):
        # Check which checkboxes are ticked
        selected = [c for c, cb in self.chapter_checkboxes.items() if cb.get_value() == True]

        if not selected:
            # In Remi, we don't have messagebox.showwarning, so we just alert the console
            # or you could update a 'status_label' in the UI.
            print("Warning: Select at least one chapter.")
            return

        self.open_next_menu(self.filename, self.selected_units, selected)