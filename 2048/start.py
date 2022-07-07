# by zhou_pp

import tkinter
from tkinter import messagebox
import pickle
from PIL import ImageTk, Image

from logic import Matrix2048

style = {
            'page': {'bg': '#d6dee0', },
            # 0 ~ 4 background-color font-color font-size
            0: {'bg': '#EEEEEE', 'fg': '#EEEEEE', 'fz': 30},
            2 ** 1: {'bg': '#D4D4D4', 'fg': '#707070', 'fz': 34},
            2 ** 2: {'bg': '#9F9F9F', 'fg': '#FAFAFA', 'fz': 34},
            # 8 ～ 16 background-color font-color font-size
            2 ** 3: {'bg': '#FFCC80', 'fg': '#FAFAFA', 'fz': 34},
            2 ** 4: {'bg': '#FFB74D', 'fg': '#FAFAFA', 'fz': 34},
            # 32 ～ 64 background-color font-color font-size
            2 ** 5: {'bg': '#FF7043', 'fg': '#FAFAFA', 'fz': 34},
            2 ** 6: {'bg': '#FF5722', 'fg': '#FAFAFA', 'fz': 34},
            # 128～2048 background-color font-color font-size
            2 ** 7: {'bg': '#FFEE58', 'fg': '#FAFAFA', 'fz': 34},
            2 ** 8: {'bg': '#FFEB3B', 'fg': '#FAFAFA', 'fz': 34},
            2 ** 9: {'bg': '#FDD835', 'fg': '#FAFAFA', 'fz': 34},
            # 1024~2048 background-color font-color font-size
            2 ** 10: {'bg': '#FF9800', 'fg': '#FAFAFA', 'fz': 32},
            2 ** 11: {'bg': '#FB8C00', 'fg': '#FAFAFA', 'fz': 30},
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


class Window2048():

    def __init__(self, column=4):
        # init the matrix
        self.data = Matrix2048(column)

        # import best score
        self.best_score = self.load_score()

        # to determine game over message
        self.best_before = self.load_score()

        # size of the board
        self.column = column

        # space between grids
        self.space_size = 18

        # size of grids
        self.cell_size = 120

        # style of the elements
        self.style = style

        # window
        self.root = self.init_window()

        # when game over if True end game
        self.flag = False

        # start the game
        self.main()

    # init the window
    def init_window(self):
        column = self.column
        space_size = self.space_size
        cell_size = self.cell_size

        # generate the window
        root = tkinter.Tk()
        root.title('肥肥的2048')

        # set window size
        window_w = column * (space_size + cell_size) + space_size
        window_h = window_w + cell_size + 2 * space_size
        root.geometry(f'{window_w}x{window_h}')

        # init header of the window
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
            self.top_score = top_score
            top_score.place(x=300, y=15)

            master.pack()

        # header section
        header_h = cell_size + space_size * 2
        header = tkinter.Frame(root, height=header_h, width=window_w)
        init_header(header)

        # board
        table = tkinter.Frame(root, height=window_w, width=window_w)
        self.init_table(table)

        return root

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
                return int(best_score)
        except FileNotFoundError:
            return 0

    # init board
    def init_table(self, master):
        column = self.column
        cell_size = self.cell_size
        space_size = self.space_size
        master['bg'] = self.style['page']['bg']

        # create grids
        emts = [[0 for x in range(column)] for y in range(column)]
        for row in range(column):
            for col in range(column):
                emt = tkinter.Label(master, bd=0)
                emt['width'] = self.cell_size
                emt['height'] = self.cell_size
                emt['text'] = ''
                emt['compound'] = 'center'

                x = space_size + col * (cell_size + space_size)
                y = space_size + row * (cell_size + space_size)
                emt.place(x=x, y=y)
                emts[row][col] = emt

        self.emts = emts
        master.pack()

    # update UI data
    def update_ui(self):
        def update_score():
            img = Image.new(
                'RGB', (self.cell_size, self.cell_size), self.style['page']['bg']
            )
            img = ImageTk.PhotoImage(img)
            self.emt_score.configure(image=img)
            self.emt_score['image'] = img
            self.emt_score['text'] = 'SCORE:' + str(self.data.score)

        def update_best():
            img = Image.new(
                'RGB', (self.cell_size, self.cell_size), self.style['page']['bg']
            )
            img = ImageTk.PhotoImage(img)
            self.top_score.configure(image=img)
            self.top_score['image'] = img
            self.top_score['text'] = 'BEST:' + str(self.best_score)
        update_score()
        update_best()
        matrix = self.data.matrix
        for row in range(self.column):
            for col in range(self.column):
                num = matrix[row][col]
                emt = self.emts[row][col]
                img = Image.new(
                    'RGB', (self.cell_size, self.cell_size), self.style[num]['bg']
                )
                img = ImageTk.PhotoImage(img)
                emt.configure(image=img)
                emt['fg'] = self.style[num]['fg']
                emt['bg'] = self.style[num]['bg']
                emt['image'] = img
                emt['font'] = ("黑体", self.style[num]['fz'], "bold")
                emt['text'] = str(num) if num != 0 else ''

    # get game over message
    def game_over_msg(self):
        if self.data.score < 4000:
            return '没有发挥好呀！'
        elif self.data.score < 13000:
            return 'emmmm......这局玩的还可以吧。'
        elif self.data.score > self.best_before:
            return '哇，创了新纪录哎，好厉害！'
        else:
            return '矮油，还不错哦~'

    # accept keyboard input
    def key_event(self, event):
        match event.keysym:
            case 'Up':
                self.data.matrix_move('U')
            case 'Down':
                self.data.matrix_move('D')
            case 'Left':
                self.data.matrix_move('L')
            case 'Right':
                self.data.matrix_move('R')
            case 'r' | 'R':
                res = messagebox.askyesno(
                    title='肥肥的2048', message='确定要重新开始游戏吗？'
                )
                if res is True:
                    self.reset_game()
                else:
                    pass
        self.save_score()
        self.load_score()
        self.update_ui()
        # print(self.data.game_over(), self.data.matrix)

        if self.data.game_over():
            # if end immediately UI not updated
            if self.flag:
                res = messagebox.askyesno(
                    title='肥肥的2048',
                    message=self.game_over_msg()+'\n'+'要再来一局吗？'
                )
                if res is True:
                    self.reset_game()
                else:
                    self.root.quit()
            else:
                self.flag = True

    # reset game
    def reset_game(self):
        self.data.init()
        self.update_ui()
        self.flag = False

    # main function
    def main(self):
        self.load_score()
        self.update_ui()

        # bind key event
        self.root.bind('<Key>', self.key_event)

        # main loop
        self.root.mainloop()


Window2048(4)
