import argparse
from Service import saveAndRead
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Listbox
from datetime import datetime

BOARDS = ['debug', 'n00b', 'l33t', 'error']  # Available crossword boards
MARGIN = 20  # Pixels around the board
SIDE = 80  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 5  # Width and height of the whole board


class CrosswordError(Exception):
    """
    An application specific error.
    """
    pass


def parse_arguments():
    """
    Parses arguments of the form:
        crossGUI.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help="Desired board name",
                            type=str,
                            choices=BOARDS,
                            required=True)

    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())
    return args['board']


class CrosswordUI(Frame):
    """
     Drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.puzzle = saveAndRead.readFromFile(datetime.today().strftime("%B-%d-%Y"))

        self.__initUI()

    def __initUI(self):
        self.parent.title("COGITO")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)


        date_picker_button = Button(self,
                                    text="Old Puzzles",
                                    command=self.__display_old_puzzles)
        date_picker_button.pack(side=BOTTOM)


        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(side=BOTTOM)


        clear_button = Button(self,
                              text="Show Solutions",
                              command=self.__show_solutions)
        clear_button.pack(side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()
        self.__write_clues()
        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):

        for i in range(6):
            color = "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)


    def __write_clues(self):
        count = 0
        for i, question in enumerate(self.puzzle["questions"]):
            if i == 0:
                self.canvas.create_text(620, 30 * count + 30, text='ACCROSS', font="Purisa")
                count += 1
            if i == 5:
                self.canvas.create_text(620, 30 * count + 30, text='DOWN', font="Purisa", )
                count += 1
            self.canvas.create_text(460, 30 * count + 30, text=question, anchor="nw")
            count += 1

    def __draw_puzzle(self):
        self.canvas.delete("letters")
        labelcount = 0
        row = [0, 0, 0, 0, 0]
        col = [0, 0, 0, 0, 0]
        for i in range(5):
            for j in range(5):
                answer = self.game.puzzle[i][j]

                # printing numbers

                if self.puzzle['rects'][j + i*5] is None and (row[j] == i or col[i] == j):
                    if row[j] == i:
                        row[j] = i + 1
                    if col[i] == j:
                        col[i] = j + 1
                elif self.puzzle['rects'][j + i*5] is not None and row[j] == i:
                    x = j * SIDE + SIDE / 2 - 10
                    y = i * SIDE + SIDE / 2 - 10
                    labelcount += 1
                    row[j] = -1
                    self.canvas.create_text(x, y, text=labelcount)
                elif self.puzzle['rects'][j + i*5] is not None and col[i] == j:
                    x = j * SIDE + SIDE / 2 - 10
                    y = i * SIDE + SIDE / 2 - 10
                    labelcount += 1
                    col[i] = -1
                    self.canvas.create_text(x, y, text=labelcount)
                # end of printing numbers
                # printing black areas
                if self.puzzle['rects'] [j + i*5] is None:
                    x = j * SIDE + SIDE / 2 -20
                    y = i * SIDE + SIDE / 2 -20
                    self.canvas.create_rectangle(x,y,x + 80, y + 80, fill='black')

                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="letters", fill=color, font="Purisa"
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        self.canvas.delete("letters_clicked")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            keep_text = self.game.puzzle[self.row][self.col]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="yellow", tags="cursor", )
            if keep_text != 0:
                self.canvas.create_text((x1 + x0) // 2, (y0 + y1) // 2, text=keep_text, tags="letters_clicked",
                                        fill="black")

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if the cell is balck then not clickable
            if self.puzzle['rects'][col + row*5] is None:
                pass
            # if cell was selected already - deselect it
            elif (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ":
            if event.char in "abcdefghijklmnopqrstuvwxyz":
                event.char = event.char.upper()
            self.game.puzzle[self.row][self.col] = (event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()

    def __clear_answers(self):
        self.game.start()
        self.__draw_puzzle()

    def __show_solutions(self):
        for i in range (0,5):
            for j in range(0,5):
                self.game.puzzle[i][j] = self.puzzle['solutions'][j + i*5]
        self.__draw_puzzle()
        self.__draw_cursor()


    def __display_old_puzzles(self):

        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            self.puzzle = saveAndRead.readFromFile(value)
            top.destroy()
            self.canvas.destroy()
            self.canvas = Canvas(self,
                                 width=WIDTH,
                                 height=HEIGHT)
            self.canvas.pack(fill=BOTH, side=TOP)
            self.__draw_grid()
            self.__draw_puzzle()
            self.__write_clues()
            self.canvas.bind("<Button-1>", self.__cell_clicked)
            self.canvas.bind("<Key>", self.__key_pressed)

        top = Tk()
        top.title('Old Puzzles')
        l1 = Listbox(top)
        # Old puzzles and their solutions are displayed in pop-up
        for i,puzzle in enumerate(saveAndRead.getAllPuzzleLabels()):
            l1.insert(i,puzzle)
        l1.pack()
        l1.bind('<<ListboxSelect>>', onselect)




class CrosswordBoard(object):
    """
    Crossword Board representation
    """
    def __init__(self, board_file):
        self.board = self.__create_empty_board()
        self.fullboard= self.__create_board(board_file)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 5:
                raise CrosswordError(
                    "Each line in the crossword puzzle must be 5 letters long."
                )
            board.append([])

            for c in line:
                if not c.isalpha():
                    raise CrosswordError(
                        "Valid characters for a crossword puzzle must be in A-Z"
                    )
                board[-1].append(c)

        if len(board) != 5:
            raise CrosswordError("Each crossword puzzle must be 5 lines long")
        return board

    def __create_empty_board(self):
        board = []
        for i in range(5):
            board.append([])
            for j in range(5):
                board[-1].append(0)
        return board

class CrosswordGame(object):

    def __init__(self, board_file):
        self.board_file = board_file
        board = CrosswordBoard(board_file)
        self.start_puzzle = board.board
        self.answer_key = board.fullboard

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(5):
            self.puzzle.append([])
            for j in range(5):
                self.puzzle[i].append(self.start_puzzle[i][j])


if __name__ == '__main__':
    board_name = parse_arguments()

    with open('%s.crossword' % board_name, 'r') as boards_file:
        game = CrosswordGame(boards_file)
        game.start()

        root = Tk()
        CrosswordUI(root, game)
        root.geometry("%dx%d" % (WIDTH + 500, HEIGHT + 100))
        root.mainloop()
