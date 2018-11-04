from Scraper import scraper
import pickle
import os
from datetime import datetime

def saveToFile(file, label):
    pickle_out = open('../data/' + label, "wb")
    pickle.dump(file, pickle_out)
    pickle_out.close()


def readFromFile(label):
    pickle_in = open('../data/' + label , "rb")
    return pickle.load(pickle_in)


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
    saveToFile(dict, datetime.today().strftime("%B %d, %Y"))
    scraper.close()

def getAllPuzzleLabels():
    dirs = os.listdir('../data')
    return dirs

#saveTodaysPuzzle()
