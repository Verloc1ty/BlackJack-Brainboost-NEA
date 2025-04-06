import sys
import pygame
import sqlite3
import os
from pygame.display import set_mode

pygame.init()
connection = sqlite3.connect("Data.db")
cursor = connection.cursor()  

screen = set_mode((1920, 1080))
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Arial', 55, bold=True)
running = True
userText = ''
inputRect = pygame.Rect(750, 490, 300, 75)
subjects = []
pageNum = 1
totalPages = len(subjects) // 9 + 1


# ----------------------------------------Classes----------------------------------------

class Button():
    def __init__(self, image, pos, width, height, buttonText, font, baseColour):
        self.image = pygame.transform.scale(image, (width, height))
        self.xCord = pos[0]
        self.yCord = pos[1]
        self.font = font
        self.buttonText = buttonText
        self.baseColour = baseColour
        self.text = font.render(self.buttonText, True, self.baseColour)

        self.rect = self.image.get_rect(center=(self.xCord, self.yCord))
        self.textRect = self.text.get_rect(center=(self.xCord, self.yCord))

    def update(self):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.textRect)

    def checkInput(self, position):
        if self.rect.left <= position[0] <= self.rect.right and self.rect.top <= position[1] <= self.rect.bottom:
            return True
        return False

class CardImage():
    def __init__(self, image, pos):
        self.image = pygame.transform.scale(image, (175, 275))
        self.xCord = pos[0]
        self.yCord = pos[1]

        self.rect = self.image.get_rect(center=(self.xCord, self.yCord))

    def Update(self):
        if self.image is not None:
            screen.blit(self.image, self.rect)




def BlackJack():
    BlackjackFilePath = os.path.join(os.path.dirname(__file__), 'BlackJack.py')
    exec(compile(open(BlackjackFilePath).read(), BlackjackFilePath, 'exec'), globals())


# ----------------------------------------Database Functions----------------------------------------


def fetchSubjectsFromDatabase():
    connection = sqlite3.connect('Data.db')  
    cursor = connection.cursor()
    
    cursor.execute("SELECT SubjectName FROM Subject")  
    subjects = cursor.fetchall()  

    connection.close()
    return [subject[0] for subject in subjects]  


def fetchTopicsFromDatabase(subjectName):
    connection = sqlite3.connect('Data.db')  
    cursor = connection.cursor()
    
    cursor.execute("SELECT SubjectID FROM Subject WHERE SubjectName=?", (subjectName,))
    subjectID = cursor.fetchone()

    if subjectID:
        cursor.execute("SELECT UnitID FROM Units WHERE SubjectID=?", (subjectID[0],))
        unitIDs = cursor.fetchall()
        
        topics = []
        for unitID in unitIDs:
            cursor.execute("SELECT TopicName FROM Topics WHERE UnitID=?", (unitID[0],))
            topics.extend([topic[0] for topic in cursor.fetchall()])
        
        connection.close()
        return topics
    else:
        connection.close()
        return []




def addSubjectToDatabase(subjectName, level):
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()
    
    cursor.execute("INSERT INTO Subject (SubjectName, Level) VALUES (?, ?)", (subjectName, level))
    
    connection.commit() 
    
    cursor.execute("SELECT * FROM Subject WHERE SubjectName=?", (subjectName,))
    result = cursor.fetchall()
    print(result) 
    
    connection.close() 


def addTopicToDatabase(subjectName, topicName):
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT SubjectID FROM Subject WHERE SubjectName=?", (subjectName,))
    subjectID = cursor.fetchone()

    if subjectID:
        cursor.execute("INSERT INTO Topics (SubjectID, TopicName) VALUES (?, ?)", (subjectID[0], topicName)) 
        connection.commit()

    connection.close()


def addQuestionToDatabase(topicName, questionText, answer1Text, answer2Text, answer3Text, answer4Text, correctAnswerText):
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT TopicID FROM Topics WHERE TopicName=?", (topicName,))
    topicID = cursor.fetchone()

    if topicID:
        cursor.execute("""
            INSERT INTO Questions (TopicID, Question, Answer1, Answer2, Answer3, Answer4, CorrectAnswer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (topicID[0], questionText, answer1Text, answer2Text, answer3Text, answer4Text, correctAnswerText))
        
        connection.commit()
    connection.close()


# ----------------------------------------Menu Functions----------------------------------------
def play(screen, font, subjects):
    pygame.display.set_caption('Play')

    subjects = fetchSubjectsFromDatabase()

    while True:
        screen.fill('#35654d')
        mousePos = pygame.mouse.get_pos()

        menuText = font.render('Choose a Subject to Revise', font, True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))

        yOffset = 250  

        buttonWidth = 300  
        buttonHeight = 100
        buttonsPerRow = 1  

        for i, subject in enumerate(subjects):
            buttonPosY = yOffset + i * (buttonHeight)  
            buttonPosX = 960

            button = Button(image=pygame.image.load('Button.jpg'), pos=(buttonPosX, buttonPosY), width=buttonWidth, height=buttonHeight, buttonText=subject, font=font, baseColour=pygame.Color('black'))
            button.update()

        screen.blit(menuText, menuRect)
        exitButton.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    mainMenu(screen, font)
                
                for i, subject in enumerate(subjects):
                    buttonPosY = yOffset + i * (buttonHeight)
                    buttonPos = pygame.Rect(buttonPosX - buttonWidth / 2, buttonPosY, buttonWidth, buttonHeight)
                    
                    if buttonPos.collidepoint(mousePos):
                        BlackJack()

        pygame.display.update()



# ----------------------------------------Subject List Functions----------------------------------------


def subjectList(screen, font, subjects, pageNum, totalPages):
    subjects = fetchSubjectsFromDatabase()  
    totalPages = len(subjects) // 9 + 1

    pygame.display.set_caption('Subject List')

    while True:
        screen.fill('#35654d')
        mousePos = pygame.mouse.get_pos()

        menuText = font.render('Subject List', True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))
        addButton = Button(image=pygame.image.load('Add Button.jpg'), pos=(1775, 75), width=100, height=100, buttonText='', font=font, baseColour=pygame.Color('black'))
        pageButton = Button(image=pygame.image.load('Button.jpg'), pos=(175, 1000), width=300, height=100, buttonText= 'Page ' + str(pageNum) + ' of ' + str(totalPages), font=font, baseColour=pygame.Color('black'))
        nextPage = Button(image=pygame.image.load('Arrow Right.jpg'), pos=(1800, 1000), width=75, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))
        previousPage = Button(image=pygame.image.load('Arrow Left.jpg'), pos=(1700, 1000), width=75, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))

        screen.blit(menuText, menuRect)
        exitButton.update()
        addButton.update()
        pageButton.update()
        nextPage.update()
        previousPage.update()

        xOffset = 450   
        yOffset = 375
        buttonWidth = 300
        buttonHeight = 100
        buttonsPerRow = 3 
        
        startIndex = (pageNum - 1) * 9
        endIndex = startIndex + 9

        subject_buttons = [] 

        for i, subject in enumerate(subjects[startIndex:endIndex]):
            row = i // buttonsPerRow
            col = i % buttonsPerRow
            
            buttonPosX = xOffset + col * (buttonWidth + 210)
            buttonPosY = yOffset + row * (buttonHeight + 100)

            button = Button(image=pygame.image.load('Button.jpg'), pos=(buttonPosX, buttonPosY), width=buttonWidth, height=buttonHeight, buttonText=subject, font=font, baseColour=pygame.Color('black'))
            button.update()

            subject_buttons.append((button, subject)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    mainMenu(screen, font)
                if addButton.checkInput(mousePos):
                    addSubject(screen, font, '', subjects)
                if nextPage.checkInput(mousePos):
                    pageNum += 1
                    if pageNum > totalPages:
                        pageNum = 1
                    subjectList(screen, font, subjects, pageNum, totalPages)
                if previousPage.checkInput(mousePos):
                    pageNum -= 1
                    if pageNum < 1:
                        pageNum = totalPages
                    subjectList(screen, font, subjects, pageNum, totalPages)


                for button, subject in subject_buttons:
                    if button.checkInput(mousePos):
                        topicList(screen, font, subject) 
                        return  

        pygame.display.update()




def addSubject(screen, font, userText, subjects):
    pygame.display.set_caption('Add a Subject')

    levelText = ''
    levelInputRect = pygame.Rect(750, 690, 300, 75) 
    activeField = 'subject' 

    totalPages = len(subjects) // 9 + 1

    while True:
        screen.fill('#35654d')

        menuText = font.render('Add a Subject', font, True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        subjectTitle = font.render('Subject', True, pygame.Color('white'))
        levelTitle = font.render('Level', True, pygame.Color('white'))

        subjectTitleRect = subjectTitle.get_rect(center=(960, 410))
        levelTitleRect = levelTitle.get_rect(center=(960, 590))  

        pygame.draw.rect(screen, (25, 25, 112), inputRect, 2)  
        pygame.draw.rect(screen, (25, 25, 112), levelInputRect, 2)  

        subjectSurface = font.render(userText, True, pygame.Color('white'))
        levelSurface = font.render(levelText, True, pygame.Color('white'))

        screen.blit(subjectTitle, subjectTitleRect) 
        screen.blit(levelTitle, levelTitleRect) 

        screen.blit(subjectSurface, (inputRect.x + 5, inputRect.y + 5))
        screen.blit(levelSurface, (levelInputRect.x + 5, levelInputRect.y + 5))

        inputRect.w = max(100, subjectSurface.get_width() + 10)
        levelInputRect.w = max(100, levelSurface.get_width() + 10)

        mousePos = pygame.mouse.get_pos()

        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))

        screen.blit(menuText, menuRect)
        exitButton.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    subjectList(screen, font, subjects, 1, totalPages)  

                if inputRect.collidepoint(mousePos):
                    activeField = 'subject'
                elif levelInputRect.collidepoint(mousePos):
                    activeField = 'level'

            if event.type == pygame.KEYDOWN:
                if activeField == 'subject':
                    if event.key == pygame.K_BACKSPACE:
                        userText = userText[:-1]
                    else:
                        userText += event.unicode
                elif activeField == 'level':
                    if event.key == pygame.K_BACKSPACE:
                        levelText = levelText[:-1]
                    else:
                        levelText += event.unicode

                if event.key == pygame.K_RETURN:
                    if userText and levelText:
                        addSubjectToDatabase(userText, levelText)  
                        subjects.append(userText) 
                        userText = ''  
                        levelText = ''  
                        totalPages = len(subjects) // 9 + 1  
                        subjectList(screen, font, subjects, 1, totalPages)  
                        return

        pygame.display.update()


def subjectPage(screen, font, subjects, pageNum, totalPages):
    pygame.display.set_caption('Subject Page')

    startIndex = (pageNum - 1) * 9 
    endIndex = startIndex + 9

    while True:
        screen.fill('#35654d')
        mousePos = pygame.mouse.get_pos()

        menuText = font.render('Subject Page', font, True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))
        addButton = Button(image=pygame.image.load('Add Button.jpg'), pos=(1775, 75), width=100, height=100, buttonText='', font=font, baseColour=pygame.Color('black'))
        page = Button(image=pygame.image.load('Button.jpg'), pos=(175, 1000), width=300, height=100, buttonText= 'Page ' + str(pageNum) + ' of ' + str(totalPages), font=font, baseColour=pygame.Color('black'))
        nextPage = Button(image=pygame.image.load('Arrow Right.jpg'), pos=(1800, 1000), width=75, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))
        previousPage = Button(image=pygame.image.load('Arrow Left.jpg'), pos=(1700, 1000), width=75, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))

        screen.blit(menuText, menuRect)
        exitButton.update()
        addButton.update()
        page.update()
        nextPage.update()
        previousPage.update()

        xOffset = 450   
        yOffset = 375
        buttonWidth = 300
        buttonHeight = 100
        buttonsPerRow = 3 
        
        for i, subject in enumerate(subjects[startIndex:endIndex]):
            if pageNum == 2 and i > 9:
                row = i // buttonsPerRow 
                col = i % buttonsPerRow  
            
                buttonPosX = xOffset + col * (buttonWidth + 210)  
                buttonPosY = yOffset + row * (buttonHeight + 100)  

                button = Button(image=pygame.image.load('Button.jpg'), pos=(buttonPosX, buttonPosY), width=buttonWidth, height=buttonHeight, buttonText=subject, font=font, baseColour=pygame.Color('black'))
                button.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    subjectList(screen, font, subjects, pageNum, totalPages)        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if addButton.checkInput(mousePos):
                    addSubject(screen, font, '', subjects) 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if previousPage.checkInput(mousePos):
                    pageNum -= 1
                    subjectList(screen, font, subjects, pageNum, totalPages)
                if nextPage.checkInput(mousePos):
                    pageNum += 1
                    if pageNum > totalPages:
                        pageNum = 1
                    subjectList(screen, font, subjects, pageNum, totalPages)
        pygame.display.update()




def topicList(screen, font, subjectName):
    pygame.display.set_caption('Topic List')

    topics = fetchTopicsFromDatabase(subjectName)
    
    while True:
        screen.fill('#35654d')
        mousePos = pygame.mouse.get_pos()

        menuText = font.render(f'Topics for {subjectName}', True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        addButton = Button(image=pygame.image.load('Add Button.jpg'), pos=(1775, 75), width=100, height=100, buttonText='', font=font, baseColour=pygame.Color('black'))
        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))

        screen.blit(menuText, menuRect)
        exitButton.update()
        addButton.update()

        yOffset = 250  
        buttonWidth = 300  
        buttonHeight = 100  
        buttonsPerRow = 2  
        
        xOffset = 450  
        xOffset2 = 1220  

        for i, topic in enumerate(topics):
            row = i // buttonsPerRow  
            col = i % buttonsPerRow 


            if col == 0:  
                buttonPosX = xOffset
            else:  
                buttonPosX = xOffset2

            buttonPosY = yOffset + row * (buttonHeight + 50)  
            
            button = Button(image=pygame.image.load('Button.jpg'), pos=(buttonPosX, buttonPosY), width=buttonWidth, height=buttonHeight, buttonText=topic, font=font, baseColour=pygame.Color('black'))
            button.update()

            if button.checkInput(mousePos):
                if pygame.mouse.get_pressed()[0]:  
                    addQuestion(screen, font, subjectName, topic)
                    return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    subjectList(screen, font, subjects, pageNum=1, totalPages=len(topics) // 9 + 1)  
                    return  

                if addButton.checkInput(mousePos):
                    addTopic(screen, font, subjectName)

        pygame.display.update()




def addTopic(screen, font, subjectName):
    pygame.display.set_caption('Add a Topic')

    topicText = ''  
    inputRect = pygame.Rect(750, 490, 300, 75) 
    activeField = 'topic'

    while True:
        screen.fill('#35654d')

        menuText = font.render('Add a Topic', font, True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        topicTitle = font.render('Topic Name', True, pygame.Color('white'))
        topicTitleRect = topicTitle.get_rect(center=(960, 410))  


        pygame.draw.rect(screen, (25, 25, 112), inputRect, 2) 


        topicSurface = font.render(topicText, True, pygame.Color('white'))

        screen.blit(menuText, menuRect)
        screen.blit(topicTitle, topicTitleRect) 
        screen.blit(topicSurface, (inputRect.x + 5, inputRect.y + 5))  

        inputRect.w = max(100, topicSurface.get_width() + 10)  

        mousePos = pygame.mouse.get_pos()

        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))
        screen.blit(exitButton.image, exitButton.rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    topicList(screen, font, subjectName)  

            if event.type == pygame.KEYDOWN:
                if activeField == 'topic':
                    if event.key == pygame.K_BACKSPACE:
                        topicText = topicText[:-1] 
                        topicText += event.unicode 

                if event.key == pygame.K_RETURN:
                    if topicText:  
                        addTopicToDatabase(subjectName, topicText) 
                        topicText = ''  
                        topicList(screen, font, subjectName)  
                        return

        pygame.display.update()


def addQuestion(screen, font, subjectName, topicName):
    pygame.display.set_caption('Add Question')

    questionText = ''
    answer1Text = ''
    answer2Text = ''
    answer3Text = ''
    answer4Text = ''
    correctAnswerText = ''

    questionRect = pygame.Rect(750, 290, 500, 50)
    answer1Rect = pygame.Rect(750, 390, 500, 50)
    answer2Rect = pygame.Rect(750, 490, 500, 50)
    answer3Rect = pygame.Rect(750, 590, 500, 50)
    answer4Rect = pygame.Rect(750, 690, 500, 50)
    correctAnswerRect = pygame.Rect(750, 790, 500, 50)

    activeField = 'question' 
    
    while True:
        screen.fill('#35654d')

        menuText = font.render(f'Add Question for {topicName} in {subjectName}', True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        questionTitle = font.render('Question', True, pygame.Color('white'))
        answer1Title = font.render('Answer 1', True, pygame.Color('white'))
        answer2Title = font.render('Answer 2', True, pygame.Color('white'))
        answer3Title = font.render('Answer 3', True, pygame.Color('white'))
        answer4Title = font.render('Answer 4', True, pygame.Color('white'))
        correctAnswerTitle = font.render('Correct Answer', True, pygame.Color('white'))

        pygame.draw.rect(screen, (25, 25, 112), questionRect, 2)
        pygame.draw.rect(screen, (25, 25, 112), answer1Rect, 2)
        pygame.draw.rect(screen, (25, 25, 112), answer2Rect, 2)
        pygame.draw.rect(screen, (25, 25, 112), answer3Rect, 2)
        pygame.draw.rect(screen, (25, 25, 112), answer4Rect, 2)
        pygame.draw.rect(screen, (25, 25, 112), correctAnswerRect, 2)


        questionSurface = font.render(questionText, True, pygame.Color('white'))
        answer1Surface = font.render(answer1Text, True, pygame.Color('white'))
        answer2Surface = font.render(answer2Text, True, pygame.Color('white'))
        answer3Surface = font.render(answer3Text, True, pygame.Color('white'))
        answer4Surface = font.render(answer4Text, True, pygame.Color('white'))
        correctAnswerSurface = font.render(correctAnswerText, True, pygame.Color('white'))

        screen.blit(menuText, menuRect)
        screen.blit(questionTitle, (questionRect.x - 200, questionRect.y + 5))
        screen.blit(answer1Title, (answer1Rect.x - 200, answer1Rect.y + 5))
        screen.blit(answer2Title, (answer2Rect.x - 200, answer2Rect.y + 5))
        screen.blit(answer3Title, (answer3Rect.x - 200, answer3Rect.y + 5))
        screen.blit(answer4Title, (answer4Rect.x - 200, answer4Rect.y + 5))
        screen.blit(correctAnswerTitle, (correctAnswerRect.x - 200, correctAnswerRect.y + 5))

        screen.blit(questionSurface, (questionRect.x + 5, questionRect.y + 5))
        screen.blit(answer1Surface, (answer1Rect.x + 5, answer1Rect.y + 5))
        screen.blit(answer2Surface, (answer2Rect.x + 5, answer2Rect.y + 5))
        screen.blit(answer3Surface, (answer3Rect.x + 5, answer3Rect.y + 5))
        screen.blit(answer4Surface, (answer4Rect.x + 5, answer4Rect.y + 5))
        screen.blit(correctAnswerSurface, (correctAnswerRect.x + 5, correctAnswerRect.y + 5))

        questionRect.w = max(100, questionSurface.get_width() + 10)
        answer1Rect.w = max(100, answer1Surface.get_width() + 10)
        answer2Rect.w = max(100, answer2Surface.get_width() + 10)
        answer3Rect.w = max(100, answer3Surface.get_width() + 10)
        answer4Rect.w = max(100, answer4Surface.get_width() + 10)
        correctAnswerRect.w = max(100, correctAnswerSurface.get_width() + 10)

        mousePos = pygame.mouse.get_pos()


        exitButton = Button(image=pygame.image.load('Exit Button.jpg'), pos=(150, 75), width=200, height=75, buttonText='', font=font, baseColour=pygame.Color('black'))
        exitButton.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitButton.checkInput(mousePos):
                    topicList(screen, font, subjectName)  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if questionRect.collidepoint(mousePos):
                    activeField = 'question'
                elif answer1Rect.collidepoint(mousePos):
                    activeField = 'answer1'
                elif answer2Rect.collidepoint(mousePos):
                    activeField = 'answer2'
                elif answer3Rect.collidepoint(mousePos):
                    activeField = 'answer3'
                elif answer4Rect.collidepoint(mousePos):
                    activeField = 'answer4'
                elif correctAnswerRect.collidepoint(mousePos):
                    activeField = 'correctAnswer'

            if event.type == pygame.KEYDOWN:
                if activeField == 'question':
                    if event.key == pygame.K_BACKSPACE:
                        questionText = questionText[:-1]
                    else:
                        questionText += event.unicode
                elif activeField == 'answer1':
                    if event.key == pygame.K_BACKSPACE:
                        answer1Text = answer1Text[:-1]
                    else:
                        answer1Text += event.unicode
                elif activeField == 'answer2':
                    if event.key == pygame.K_BACKSPACE:
                        answer2Text = answer2Text[:-1]
                    else:
                        answer2Text += event.unicode
                elif activeField == 'answer3':
                    if event.key == pygame.K_BACKSPACE:
                        answer3Text = answer3Text[:-1]
                    else:
                        answer3Text += event.unicode
                elif activeField == 'answer4':
                    if event.key == pygame.K_BACKSPACE:
                        answer4Text = answer4Text[:-1]
                    else:
                        answer4Text += event.unicode
                elif activeField == 'correctAnswer':
                    if event.key == pygame.K_BACKSPACE:
                        correctAnswerText = correctAnswerText[:-1]
                    else:
                        correctAnswerText += event.unicode


                if event.key == pygame.K_RETURN:
                    if all([questionText, answer1Text, answer2Text, answer3Text, answer4Text, correctAnswerText]):
                        addQuestionToDatabase(topicName, questionText, answer1Text, answer2Text, answer3Text, answer4Text, correctAnswerText)
                        questionText = ''
                        answer1Text = ''
                        answer2Text = ''
                        answer3Text = ''
                        answer4Text = ''
                        correctAnswerText = ''
                        topicList(screen, font, subjectName)
                        return

        pygame.display.update()



# ----------------------------------------Main Menu----------------------------------------


def mainMenu(screen, font):
    pygame.display.set_caption('Main Menu')

    while True:
        screen.fill('#35654d')
        mousePos = pygame.mouse.get_pos()

        menuText = font.render('Main Menu', font, True, pygame.Color('white'))
        menuRect = menuText.get_rect(center=(960, 150))

        playButton = Button(image=pygame.image.load("Button.jpg"), pos=(960, 550), width=300, height=150, buttonText='Play', font=font, baseColour=pygame.Color('black'))
        subjectListButton = Button(image=pygame.image.load("Button.jpg"), pos=(960, 720), width=300, height=150, buttonText='Subject List', font=font, baseColour=pygame.Color('black'))
        quitButton = Button(image=pygame.image.load("Button.jpg"), pos=(960, 890), width=300, height=150, buttonText='Quit', font=font, baseColour=pygame.Color('black'))

        card1 = CardImage(image=pygame.image.load("A_of_Spades.png"), pos=(500, 250))
        card2 = CardImage(image=pygame.image.load("A_of_Hearts.png"), pos=(250, 250))
        card3 = CardImage(image=pygame.image.load("A_of_Clubs.png"), pos=(1420, 250))
        card4 = CardImage(image=pygame.image.load("A_of_Diamonds.png"), pos=(1670, 250))

        screen.blit(menuText, menuRect)
        playButton.update()
        subjectListButton.update()
        quitButton.update()
        card1.Update()
        card2.Update()
        card3.Update()
        card4.Update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkInput(mousePos):
                    play(screen, font, subjects)
                elif subjectListButton.checkInput(mousePos):
                    subjectList(screen, font, subjects, pageNum, totalPages)
                elif quitButton.checkInput(mousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

mainMenu(screen, font)
