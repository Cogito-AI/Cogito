from Scraper import scraper
import os
from pathlib import Path
import json
from datetime import datetime

def saveToFile(file, label):
    jsondata = json.dumps(file)
    print(datetime.today().strftime("%H:%M:%S.%f   Saving Todays Puzzle to File"))
    with open('../data/' + label, 'w') as outfile:
        json.dump(file, outfile, indent=4)


def readFromFile(label):
    print(datetime.today().strftime("%H:%M:%S.%f  Reading data from file"))
    my_file = Path('../data/' + label)
    if not my_file.exists():
        print(datetime.today().strftime("%H:%M:%S.%f   File not exist"))
        saveTodaysPuzzle()
    with open(my_file, 'r') as f:
        data = json.load(f)

    return data


def saveTodaysPuzzle():
    print(datetime.today().strftime("%H:%M:%S.%f   Acquiring data from webpage"))
    scraper.init()
    dict = {}
    dict['questions'] = []
    for question in scraper.getQuestions():
        question = question.replace('\n', '-  ')
        dict['questions'].append(question)

    dict['rects'] = []
    for rect in scraper.getRects():
        dict['rects'].append(rect)

    dict['solutions'] = []
    for solution in scraper.getTodaysSolutions():
        dict['solutions'].append(solution)
    saveToFile(dict, datetime.today().strftime("%B-%d-%Y"))
    scraper.close()

def getAllPuzzleLabels():
    print(datetime.today().strftime("%H:%M:%S.%f   Fetching filenames from os"))
    dirs = os.listdir('../data')
    return dirs
