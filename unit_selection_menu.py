import csv
import os
import remi.gui as gui


class UnitSelectionMenu:
    def __init__(self, app_instance, data_folder, filename, open_next_menu_callback, show_main_menu_callback):
        self.app = app_instance
        self.data_folder = data_folder
        self.filename = filename
        self.open_next_menu = open_next_menu_callback
        self.show_main_menu = show_main_menu_callback

        self.full_path = os.path.join(self.data_folder, self.filename)
        self.unit_checkboxes = {}  # Store widgets directly
        self.units = self.get_unique_units()

    def get_unique_units(self):
        units = set()
        try:
            with open(self.full_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    u = row.get("unit_number", "").strip()
                    if u:
                        units.add(u)
        except Exception as e:
            print(f"Error reading units: {e}")
        return sorted(units)

    def build_ui(self):
        # Main Vertical Container
        container = gui.VBox(width='100%', style={'margin': '0px auto', 'background-color': 'white'})

        # Title
        lbl_title = gui.Label("Select Unit", style={'font-size': '20px', 'font-weight': 'bold', 'margin': '20px'})
        container.append(lbl_title)

        # Selection Frame (Vertical list of units)
        list_container = gui.VBox(width='80%', style={'margin': '0px auto', 'align-items': 'flex-start'})

        for unit in self.units:
            # Create a row for each checkbox + label
            row = gui.HBox(width='100%', style={'justify-content': 'flex-start', 'padding': '5px'})

            check = gui.CheckBox(True)  # Default to checked
            lbl = gui.Label(f"Unit {unit}", style={'margin-left': '10px'})

            row.append(check)
            row.append(lbl)

            # Save the checkbox widget to check its state later
            self.unit_checkboxes[unit] = check
            list_container.append(row)

        container.append(list_container)

        # Buttons
        btn_continue = gui.Button("Continue to Chapter Selection", width='90%', height='50px',
                                  style={'margin': '20px auto', 'background-color': '#2196F3', 'color': 'white'})
        btn_continue.onclick.do(self.continue_forward)

        btn_back = gui.Button("Back to Main Menu", width='90%')
        btn_back.onclick.do(lambda w: self.show_main_menu())

        container.append(btn_continue)
        container.append(btn_back)

        return container

    def continue_forward(self, widget):
        # Filter units where the checkbox is checked (get_value() returns True/False)
        selected_units = [u for u, cb in self.unit_checkboxes.items() if cb.get_value() == True]

        # In Remi, we pass self.filename and the list to the callback
        self.open_next_menu(self.filename, selected_units)