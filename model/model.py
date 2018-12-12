from copy import deepcopy

from datamuse import datamuse
from Service import saveAndRead
from _datetime import datetime
import numpy as np

class Node(object):
    def __init__(self, board, point):
        self.board = board
        self.point = point
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


def preprocess(puzzle):
    squares = [[] for y in range(10)]

    # preprocessdata
    que_pixels = np.zeros((5, 5))
    labelcount = 0
    row = [0, 0, 0, 0, 0]
    col = [0, 0, 0, 0, 0]
    for i in range(5):
        for j in range(5):
            if puzzle['rects'][j + i * 5] is None and (row[j] == i or col[i] == j):
                if row[j] == i:
                    row[j] = i + 1
                if col[i] == j:
                    col[i] = j + 1
            elif puzzle['rects'][j + i * 5] is not None and row[j] == i:
                labelcount += 1
                row[j] = -1
                que_pixels[i, j] = labelcount
            elif puzzle['rects'][j + i * 5] is not None and col[i] == j:
                labelcount += 1
                col[i] = -1
                que_pixels[i, j] = labelcount

    sqrs = [[] for y in range(10)]
    for i in range(5):
        for j in range(5):
            num = int(que_pixels[i][j])
            if num != 0:
                sqrs[num] = [j, i]

    for i in range(5):
        q = puzzle['questions'][i]
        num = int(q[:1])
        for j in range(sqrs[num][0], 5):
            if puzzle['rects'][i * 5 + j] is not None:
                squares[i].append([i, j])
    for i in range(5, 10):
        q = puzzle['questions'][i]
        num = int(q[:1])
        for j in range(sqrs[num][1], 5):
            if puzzle['rects'][sqrs[num][0] + j * 5] is not None:
                squares[i].append([j, sqrs[num][0]])
    return squares
# end of preporcess

# connect to apı
api = datamuse.Datamuse()
puzzle = saveAndRead.readFromFile(datetime.today().strftime("%B-%d-%Y"))

# create board
board = [[[]for x in range(5)] for y in range(5)]
for i,rect in enumerate(puzzle['rects']):
    if rect is None:
        board[i//5][i%5] = None
    else:
        board[i // 5][i%5] = " "

squares = preprocess(puzzle)


#Acquire words
possibilities = []
for i in range(len(puzzle['questions'])):
    words = api.words(ml=puzzle['questions'][i][3:], max = 5, sp='?'*len(squares[i]))
    possibilities.append(words)

def put_in_board(word, squares, board):
    newboard = deepcopy(board)
    point = 0
    for i,square in enumerate(squares):
        if board[square[0]][square[1]] is word['word'][i]:
            newboard[square[0]][square[1]] = word['word'][i]
            point = 2
        elif board[square[0]][square[1]] is ' ':
            newboard[square[0]][square[1]] = word['word'][i]
            point = 0
        else:
            return False , board, -1
    return True, newboard, point

## create tree from possibilities

#list of leaf nodes with number of solved
leaf = []
#root Node with empy board
root = Node(board,0)
def create_tree_of_possibilities(root, possibilities, squares):
    if len(possibilities) == 0:
        leaf.append([root.board, root.point])
        return
    if len(possibilities[0]) > 0:
        for i in range(0,len(possibilities[0]) + 1):
            if i == len(possibilities[0]) :
                 child = Node(root.board, root.point)
                 root.add_child(child)
                 create_tree_of_possibilities(child,possibilities[1:],squares[1:])
            else:
                put, board, point = put_in_board(possibilities[0][i], squares[0], root.board)
                if put:
                    child = Node(board, root.point + point)
                    root.add_child(child)
                    create_tree_of_possibilities(child, possibilities[1:], squares[1:])
    else:
        child = Node(root.board, root.point)
        root.add_child(child)
        create_tree_of_possibilities(child, possibilities[1:], squares[1:])



create_tree_of_possibilities(root,possibilities,squares)
leaf = sorted(leaf, key=lambda x: x[1], reverse=True)
pass


