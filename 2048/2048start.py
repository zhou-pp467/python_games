# by zhou_pp

from 2048logic import Matrix


class Window2048():

    def __init__(self, column=4):
        self.init_setting(column)
        self.data = Matrix2048(column)

    # init the settings
    def init_setting(self, column):
        pass

    # init the window
    def init_window(self):
        pass

    # update UI data
    def update_ui(self):
        pass

    # accept keyboard input
    def key_event(self):
        pass

    # reset the game
    def reset_game(self):
        pass

    # main function
    def main(self):
        pass


Window2048(4)