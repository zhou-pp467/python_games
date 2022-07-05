# by zhou_pp

import tkinter
import pickle

from logic import Matrix2048


class Window2048():

    def __init__(self, column=4):
        # init the matrix
        self.data = Matrix2048(column)

        # import top 3 scores
        self.best_score = self.load_score()

        # size of the board
        self.column = column

        # space between grids
        self.space_size = 18

        # size of grids
        self.cell_size = 120

        # style of the elements
        self.style = {
            'page': {'bg': '#d6dee0', },
            # 0 ~ 4 background-color font-color font-size
            0: {'bg': '#EEEEEE', 'fg': '#EEEEEE', 'fz': 30},
            2 ** 1: {'bg': '#E5E5E5', 'fg': '#707070', 'fz': 30},
            2 ** 2: {'bg': '#D4D4D4', 'fg': '#707070', 'fz': 30},
            # 8 ～ 16 background-color font-color font-size
            2 ** 3: {'bg': '#FFCC80', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 4: {'bg': '#FFB74D', 'fg': '#FAFAFA', 'fz': 30},
            # 32 ～ 64 background-color font-color font-size
            2 ** 5: {'bg': '#FF7043', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 6: {'bg': '#FF5722', 'fg': '#FAFAFA', 'fz': 30},
            # 128～2048 background-color font-color font-size
            2 ** 7: {'bg': '#FFEE58', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 8: {'bg': '#FFEB3B', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 9: {'bg': '#FDD835', 'fg': '#FAFAFA', 'fz': 30},
            # 1024~2048 background-color font-color font-size
            2 ** 10: {'bg': '#FF9800', 'fg': '#FAFAFA', 'fz': 30},
            2 ** 11: {'bg': '#FB8C00', 'fg': '#FAFAFA', 'fz': 28},
            # 4096 +  background-color font-color font-size
            2 ** 12: {'bg': '#fb3030', 'fg': '#FAFAFA', 'fz': 28},
            2 ** 13: {'bg': '#e92e2e', 'fg': '#FAFAFA', 'fz': 28},
            2 ** 14: {'bg': '#da1e1e', 'fg': '#FAFAFA', 'fz': 24},
            # 2**15 +  background-color font-color font-size
            2 ** 15: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 22},
            2 ** 16: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2 ** 17: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2 ** 18: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 20},
            2 ** 19: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 18},
            2 ** 20: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 17},
            2 ** 21: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 16},
            2 ** 22: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 15},
            2 ** 23: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 14},
            2 ** 24: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 13},
            2 ** 25: {'bg': '#3a3a3a', 'fg': '#E0E0E0', 'fz': 12},
        }

    # init the window
    def init_window(self):
        column = self.column
        space_size = self.space_size
        cell_size = self.cell_size

        # generate the window
        root = tkinter.TK()
        root.title('肥肥的2048')

        # set window size
        window_w = column * (space_size + cell_size) + space_size
        window_h = window_w + cell_size + 2 * space_size

        # header section
        header_h = cell_size + space_size * 2
        header = tkinter.Frame(root, height=header_h, width=window_w)

        # init header section
        def init_header(master):
            master['bg'] = self.style['page']['bg']

            # current score
            emt_score = tkinter.Label(master, bd=0)
            emt_score['fg'] = '#707070'
            emt_score['bg'] = self.style['page']['bg']
            emt_score['font'] = ("黑体", 30, "bold")
            img = Image.new('RGB', (self.cell_size, self.cell_size),
                            self.style['page']['bg'])
            img = ImageTk.PhotoImage(img)
            emt_score.configure(image=img)
            emt_score['image'] = img

            emt_score['text'] = 'SCORE:' + str(self.data.score)
            emt_score['compound'] = 'center'
            self.emt_score = emt_score
            emt_score.place(x=15, y=15)

            # best score
            top_score = tkinter.Label(master, bd=0)
            top_score['fg'] = '#707070'
            top_score['bg'] = self.style['page']['bg']
            top_score['font'] = ("黑体", 30, "bold")
            img = Image.new('RGB', (self.cell_size, self.cell_size),
                            self.style['page']['bg'])
            img = ImageTk.PhotoImage(img)
            top_score.configure(image=img)
            top_score['image'] = img

            top_score['text'] = 'BEST:' + str(self.best_score)
            top_score['compound'] = 'center'
            self.emt_score = emt_score
            top_score.place(x=300, y=15)

            master.pack()

        init_header(header)

    # save best score
    def save_score(self):
        self.best_score = max(self.best_score, self.data.score)
        with open("high_score.pkl", 'wb') as f:
            pickle.dump(str(self.best_score), f, 0)

    # load best score
    def load_score(self):
        try:
            with open("high_score.pkl", "rb") as f:
                best_score = pickle.load(f)
                return best_score
        except FileNotFoundError:
            return 0

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
