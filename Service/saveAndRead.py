from Scraper import scraper
import pickle
from datetime import datetime

def saveToFile(file, label):
    pickle_out = open(label, "wb")
    pickle.dump(file, pickle_out)
    pickle_out.close()


def readFromFile(label):
    pickle_in = open(label, "rb")
    return pickle.load(pickle_in)


def saveTodaysPuzzle():
    dict = {}
    dict['questions'] = []
    for question in scraper.getQuestions():
        question = question.repalece('/n', ' ')
        dict['questions'].append(question)

    dict['rects'] = []
    for rect in scraper.getRects():
        dict['rects'].append(question)

    dict['solutions'] = []
    for solution in scraper.getQuestions():
        dict['solutions'].append(question)
    saveToFile(dict, datetime.today().strftime("%B %d, %Y") )

