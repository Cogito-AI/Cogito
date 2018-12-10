from datamuse import datamuse
from Service import saveAndRead
from _datetime import datetime
import numpy as np

api = datamuse.Datamuse()
puzzle = saveAndRead.readFromFile(datetime.today().strftime("%B-%d-%Y"))
possibilities = []
squares = [[] for y in range(10)]


que_pixels = np.zeros((5,5))
labelcount = 0
row = [0, 0, 0, 0, 0]
col = [0, 0, 0, 0, 0]
for i in range(5):
    for j in range(5):
        if puzzle['rects'][j + i*5] is None and (row[j] == i or col[i] == j):
            if row[j] == i:
                row[j] = i + 1
            if col[i] == j:
                col[i] = j + 1
        elif puzzle['rects'][j + i*5] is not None and row[j] == i:
            labelcount += 1
            row[j] = -1
            que_pixels[i,j] = labelcount
        elif puzzle['rects'][j + i*5] is not None and col[i] == j:
            labelcount += 1
            col[i] = -1
            que_pixels[i, j] = labelcount

sqrs = [[] for y in range(10)]
for i in range(5):
    for j in range(5):
        num = int(que_pixels[i][j])
        if num != 0:
            sqrs[num] = [j,i]
for i in range(5):
    q = puzzle['questions'][i]
    num = int(q[:1])
    for j in range(sqrs[num][0],5):
        if puzzle['rects'][i*5 + j] is not None:
            squares[i].append([j,i])
for i in range(5,10):
    q = puzzle['questions'][i]
    num = int(q[:1])
    for j in range(sqrs[num][1],5):
        if puzzle['rects'][sqrs[num][0] + j*5] is not None:
            squares[i].append([sqrs[num][0],j])

for i in range(len(puzzle['questions'])):
    words = api.words(ml=puzzle['questions'][i][3:], max = 10, sp='?'*len(squares[i]))
