import re
import string
from copy import deepcopy

from datamuse import datamuse
from Service import saveAndRead
from _datetime import datetime
import numpy as np

class Node(object):
    def __init__(self, board, point, parent):
        self.board = board
        self.parent = parent
        self.point = point
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def set_point(self, obj):
        self.point = obj

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

def initialize_env_variables(puzzle, board):
    # create board
    for i,rect in enumerate(puzzle['rects']):
        if rect is None:
            board[i//5][i%5] = None
        else:
            board[i // 5][i%5] = ""


def get_possible_answers(board, questions, squares, num_of_word):
    possibilities = []
    for i, question in enumerate(questions):
        incomplete = False
        sp = ''
        words = []
        for j, square in enumerate(squares[i]):
            sp += board[square[0]][square[1]]
            if board[square[0]][square[1]] == '':
                incomplete = True
                sp += '?'
        if incomplete:
            question = question[3:]
            regex = re.compile('[^a-zA-Z ]')
            # First parameter is the replacement, second parameter is your input string
            question = regex.sub(' ', question)

            print(datetime.today().strftime(question))
            print(datetime.today().strftime("%H:%M:%S.%f  acquiring words on the pattern of:" + sp))
            words = api.words(ml=question, max=num_of_word, sp=sp)
            for word in words:
                print(word['word'], end=' ')
            print()

            if len(words) == 0:
                words = api.words(max=num_of_word, sp=sp)
        possibilities.append(words)
    return possibilities


def put_in_board(word, squares, board, ui):
    points = [5,5,5]
    newboard = deepcopy(board)
    point = 0
    for i,square in enumerate(squares):
        if board[square[0]][square[1]] is word['word'][i]:
            newboard[square[0]][square[1]] = word['word'][i]
            point += points[ui]
        elif board[square[0]][square[1]] is '':
            newboard[square[0]][square[1]] = word['word'][i]
            point += 0
        else:
            return False , board, -1
    return True, newboard, point


def create_tree_of_possibilities(root, possibilities, squares, leaf, ui):
    if len(possibilities) == 0:
        leaf.append(root)
        return
    if len(possibilities[0]) > 0:
        for i in range(0,len(possibilities[0]) + 1):
            if i == len(possibilities[0]):
                child = Node(root.board, root.point + 1, root)
                root.add_child(child)
                create_tree_of_possibilities(child,possibilities[1:],squares[1:], leaf, ui)
            else:
                put, board, point = put_in_board(possibilities[0][i], squares[0], root.board, ui)
                if put:
                    child = Node(board, root.point + point, root)
                    root.add_child(child)
                    create_tree_of_possibilities(child, possibilities[1:], squares[1:], leaf, ui)
    else:
        child = Node(root.board, root.point + 1, root)
        root.add_child(child)
        create_tree_of_possibilities(child, possibilities[1:], squares[1:], leaf, ui)

'''
def check_truuthness(board,solution, squares):
    point = 0
    for word in squares:
        for letter in word:
            if solution[letter[0] * 5 + letter[1]] is not None and solution[letter[0] * 5 + letter[1]] != board.board[letter[0]][letter[1]].upper():
                point -= 5
                break
        point += 5
    board.point += point
'''

def run_pipeline(puzzle, squares, root, num_of_words, top_n_possinle, ui):
    possibilities = get_possible_answers(root.board,puzzle['questions'], squares, num_of_words)
    leaf = []
    create_tree_of_possibilities(root, possibilities, squares, leaf, ui)

    #idk if we can
    '''
    if ui == -1:
        for node in leaf:
            check_truuthness(node, puzzle['solutions'], squares)
    '''

    leaf = sorted(leaf, key=lambda x: x.point, reverse=True)
    return leaf[:top_n_possinle]


def solve(puzzle, ui):
    board = [[[] for x in range(5)] for y in range(5)]
    sqaures = preprocess(puzzle)
    initialize_env_variables(puzzle, board)

    root = Node(board,0,None)

    results = []
    for i in range(2):

        print(datetime.today().strftime("%H:%M:%S.%f  cretae tree of possible answers with the root of:"))
        for row in root.board:
            print(row)

        results = run_pipeline(puzzle, sqaures, root, 3, 3, i)
        root = results[0]

    trace_node = results[0]

    print(datetime.today().strftime("%H:%M:%S.%f  Trace from resulting leaf node to root Node: "))
    while trace_node is not None:
        for i in range(5):
            for j, children in enumerate(trace_node.children):
                print(children.board[i], end='\t')
            print('\n', end='')
        print()

        trace_node = trace_node.parent
    print(datetime.today().strftime("%H:%M:%S.%f  End of Trace"))

    return results[0].board


'''
#Acquire words

for i in range(len(puzzle['questions'])):
    question = puzzle['questions'][i][3:]
    regex = re.compile('[^a-zA-Z ]')
    # First parameter is the replacement, second parameter is your input string
    question = regex.sub(' ', question)
    words = api.words(ml=question , max = 3, sp='?'*len(squares[i]))
    possibilities.append(words)
    
def check_truuthness(board,solution):
    point = 0
    for i, letter in enumerate(solution):
        if letter is not None and board[0][i // 5][i % 5].upper() == letter:
            point += 1
    board[1] = point

for board in leaf:
    check_truuthness(board,puzzle['solutions'])

leaf = sorted(leaf, key=lambda x: x[1], reverse=True)


def find_incomplete_results(board, questions, squares):
    for i, question in enumerate(questions):
        incomplete = False
        sp = ''
        for j, square in enumerate(squares[i]):
            sp += board[square[0]][square[1]]
            if board[square[0]][square[1]] == '':
                incomplete = True
                sp += '?'
        if incomplete:
            question = puzzle['questions'][i][3:]
            word = api.words(ml=question, max=1, sp=sp) #[0]['word']
            if len(word) > 0 :
                word = word[0]['word']
                for j, square in enumerate(squares[i]):
                    board[square[0]][square[1]] = word[j]


for board in leaf:
    find_incomplete_results(board[0],puzzle['questions'], squares)
'''



