from Scraper import scraper
import pickle
import os
import json
from datetime import datetime

def saveToFile(file, label):
    jsondata = json.dumps(file)
    with open('../data/' + label, 'w') as outfile:
        json.dump(file, outfile, indent=4)


def readFromFile(label):
    with open('../data/' + label, 'r') as f:
        data = json.load(f)

    return data


def saveTodaysPuzzle():
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
    dirs = os.listdir('../data')
    return dirs
