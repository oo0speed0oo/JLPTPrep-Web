import remi.gui as gui
from remi import start, App
from main_menu import MainMenu  # Make sure this class is now using Remi!


class QuizMarkerApp(App):
    def __init__(self, *args):
        # This replaces the geometry and title setup
        super(QuizMarkerApp, self).__init__(*args)

    def main(self):
        """ This function acts as your 'main_window' setup """

        # 1. Create the root container (fills the browser screen)
        # Instead of geometry("800x800"), we use percentages for mobile responsiveness
        self.main_container = gui.VBox(width='100%', height='100%',
                                       style={'margin': '0px auto', 'background-color': 'white'})

        # 2. Initialize the Main Menu class.
        # We pass 'self' (the app instance) so the menu can talk back to the server
        self.menu_manager = MainMenu(self)

        # 3. Add the Menu UI to our main container
        # (Assuming your MainMenu has a build_ui method like we did before)
        self.main_container.append(self.menu_manager.build_ui())

        # 4. Return the container to show it in the browser
        return self.main_container


if __name__ == "__main__":
    # start() replaces main_window.mainloop()
    # address='0.0.0.0' allows your phone to connect via your computer's IP
    # port=8081 is the 'room number' on your computer your phone will visit
    start(QuizMarkerApp,
          address='0.0.0.0',
          port=8081,
          start_browser=True,
          username=None,
          password=None)

    