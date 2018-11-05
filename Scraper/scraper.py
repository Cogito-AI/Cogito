from selenium import webdriver
from datetime import datetime

driver = None

def init():
    print(datetime.today().strftime("%B-%d-%Y   Initializing scraper"))
    global driver
    driver = webdriver.Firefox(executable_path="../Scraper/geckodriverUnix")
    driver.get("https://www.nytimes.com/crosswords/game/mini")
    elem = driver.find_element_by_css_selector('.buttons-modalButton--1REsR')
    if elem is not None:
        elem.click()


def close():
    print(datetime.today().strftime("%B-%d-%Y   Disconnecting from Webpage"))
    driver.close()

'''
Return String array questions are in the format of 
 "<number>/questiontext"
'''
def getQuestions():
    print(datetime.today().strftime("%B-%d-%Y   Fething questions via scraper"))

    questions = []
    raw = driver.find_elements_by_css_selector('.Clue-li--1JoPu')
    for question in raw:
        questions.append(question.text)
    return questions

'''
Return String array if rect is black block is None else the text in the cell by default ""
'''
def getRects():
    print(datetime.today().strftime("%H:%M:%S.%f   Fething rectangles via scraper"))

    rects = []
    for i in range(0, 25):
        rect = driver.find_element_by_id('cell-id-' + str(i))
        if rect.get_attribute('class') == "Cell-block--1oNaD":
            rects.append(None)
        else:
            rects.append('')
    return rects

'''
Return String array if rect is black block is None else the letter in the rect
'''
def getTodaysSolutions():
    print(datetime.today().strftime("%H:%M:%S.%f   Fething solutions via scraper"))

    revealbutton = driver.find_element_by_xpath('/html/body/div/div/div/div[4]/div/main/div[2]/div/div/ul/div[1]/li[2]')
    revealbutton.click()
    puzzlereveal = driver.find_element_by_xpath(
        '/html/body/div/div/div[1]/div[4]/div/main/div[2]/div/div/ul/div[1]/li[2]/ul/li[3]')
    puzzlereveal.click()
    reveal = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[2]/article/div[2]/button[2]')
    reveal.click()

    solutions = []
    for i in range(1, 26):
        cell = driver.find_element_by_css_selector("#xwd-board > g:nth-child(3) > g:nth-child(" +str(i)+ ")")
        if len(cell.text) == 0:
            solutions.append(None)
        else:
            solutions.append(cell.text[len(cell.text) -1 ])
    return solutions

#init()
#print(getTodaysSolutions())
#close()