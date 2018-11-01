from selenium import webdriver

driver = webdriver.Firefox(executable_path="./geckodriverUnix")

def init():
    driver.get("https://www.nytimes.com/crosswords/game/mini")
    elem = driver.find_element_by_css_selector('.buttons-modalButton--1REsR')
    if elem is not None:
        elem.click()


def close():
    driver.close()

'''
Return String array questions are in the format of 
 "<number>/questiontext"
'''
def getQuestions():
    questions = []
    raw = driver.find_elements_by_css_selector('.Clue-li--1JoPu')
    for question in raw:
        questions.append(question.text)
    return questions

'''
Return String array if cell is black block is None else the text in the cell by default ""
'''
def getCells():
    cells = []
    for i in range(0, 25):
        cell = driver.find_element_by_id('cell-id-' + str(i))
        if cell.get_attribute('class') is "Cell-block--1oNaD":
            cells.append(None)
        else:
            cells.append('')
    return cells


def getTodaysSolutions():
    pass

init()
print(getQuestions())
close()