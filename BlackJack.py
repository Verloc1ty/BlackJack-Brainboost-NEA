import pygame
import random
import sqlite3


pygame.init()
connection = sqlite3.connect("Data.db")
cursor = connection.cursor()  


clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((1920, 1080))
font = pygame.font.SysFont('Arial', 55, bold=True)
run = True
active = False
Initial = False
PlayerHand = []
DealerHand = []

PlayerScore = 0
DealerScore = 0
QuestionsRight = 0
QuestionsWrong = 0
QuestionMode = False

from Main_Menu import Button

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.name = f"{value} of {suit}"
        self.image_filename = f'{value}_of_{suit}.png'

    def __repr__(self):
        return self.name

    def card_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)


class Deck:
    def __init__(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(value, suit) for suit in suits for value in values]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def DealCard(self):
        return self.cards.pop() if self.cards else None

    def __len__(self):
        return len(self.cards)


class CardImage():
    def __init__(self, image, pos):
        self.image = pygame.transform.scale(image, (175, 225))
        self.XCord = pos[0]
        self.YCord = pos[1]
        self.rect = self.image.get_rect(center=(self.XCord, self.YCord))

    def Update(self):
        if self.image is not None:
            screen.blit(self.image, self.rect)


def DrawCard(active, QuestionsRight, QuestionsWrong):
    ButtonList = []
    if not active:
        DealHand = pygame.draw.rect(screen, 'white', (800, 375, 300, 100), 0, 5)
        DealText = font.render('Deal Hand', True, 'black')
        screen.blit(DealText, (830, 390))


        QuestionsRightText = font.render(f'Questions Right: {QuestionsRight}', True, 'black')
        QuestionsWrongText = font.render(f'Questions Wrong: {QuestionsWrong}', True, 'black')
        screen.blit(QuestionsRightText, (50, 50))  
        screen.blit(QuestionsWrongText, (50, 100)) 

        ButtonList.append(DealHand)
    else:
        Hit = pygame.draw.rect(screen, 'white', (400, 875, 300, 100), 0, 5)
        HitText = font.render('Hit', True, 'black')
        screen.blit(HitText, (515, 895))

        Stand = pygame.draw.rect(screen, 'white', (1200, 875, 300, 100), 0, 5)
        StandText = font.render('Stand', True, 'black')
        screen.blit(StandText, (1290, 895))

        ReplayButton = pygame.draw.rect(screen, 'white', (1650, 40, 200, 54), 0, 5)
        ReplayText = font.render('Replay', True, 'black')
        screen.blit(ReplayText, (1678, 30))

        ButtonList.append(Stand)
        ButtonList.append(Hit)
        ButtonList.append(ReplayButton)

        active = True

    return ButtonList



def DealHand(deck):
    global PlayerHand, DealerHand, PlayerScore, DealerScore
    PlayerHand.append(deck.DealCard())
    PlayerHand.append(deck.DealCard())

    DealerHand.append(deck.DealCard())
    DealerHand.append(deck.DealCard())

    PlayerScore = CalculateScore(PlayerHand)
    DealerScore = CalculateScore(DealerHand)

    return PlayerHand, DealerHand, PlayerScore, DealerScore


def CalculateScore(hand):
    score = 0
    ace_count = 0

    for card in hand:
        score += card.card_value()
        if card.value == 'A':
            ace_count += 1

    while score > 21 and ace_count:
        score -= 10
        ace_count -= 1

    return score if score <= 21 else None


def CardDrawing(PlayerHand, DealerHand, PlayerScore, DealerScore, QuestionsRight, QuestionsWrong):
    PlayerCards = []
    DealerCards = []

    for i in range(len(DealerHand)):
        DealerCards.append(CardImage(pygame.image.load(DealerHand[i].image_filename), (850 + (i * 185), 200)))

    for i in range(len(PlayerHand)):
        PlayerCards.append(CardImage(pygame.image.load(PlayerHand[i].image_filename), (850 + (i * 185), 700)))

    for card in DealerCards:
        card.Update()

    for card in PlayerCards:
        card.Update()

    if PlayerScore == None:
        PlayerScoreText = font.render("Player: Busted", True, 'Black')
    elif PlayerScore == 21:
        PlayerScoreText = font.render("Player: BlackJack", True, 'Black')
    else:
        PlayerScoreText = font.render(f"Player Score: {PlayerScore}", True, 'Black')
    screen.blit(PlayerScoreText, (50, 50))

    if DealerScore == None:
        DealerScoreText = font.render("Dealer: Busted", True, 'Black')
    elif DealerScore == 21:
        DealerScoreText = font.render("Dealer: BlackJack", True, 'Black')
    else:
        DealerScoreText = font.render(f"Dealer Score: {DealerScore}", True, 'Black')
    screen.blit(DealerScoreText, (50, 150))


    CorrectAnswersText = font.render(f"Correct Answers: {QuestionsRight}", True, 'Black')
    IncorrectAnswersText = font.render(f"Incorrect Answers: {QuestionsWrong}", True, 'Black')

    screen.blit(CorrectAnswersText, (50, 250))
    screen.blit(IncorrectAnswersText, (50, 320)) 

    return PlayerCards, DealerCards, PlayerScore, DealerScore



def DetermineWinner(PlayerScore, DealerScore):
    if PlayerScore is None:
        return "Dealer Wins! Player Busted"
    elif DealerScore is None:
        return "Player Wins! Dealer Busted"
    
    if PlayerScore > 21:
        return "Dealer Wins! Player Busted"
    elif DealerScore > 21:
        return "Player Wins! Dealer Busted"
    
    if PlayerScore > DealerScore:
        return "Player Wins!"
    elif DealerScore > PlayerScore:
        return "Dealer Wins!"
    else:
        return "It's a Tie!"



def GameOverScreen(winner, screen):
    screen.fill('#35654d')

    font = pygame.font.SysFont('Arial', 55, bold=True)
    ResultText = font.render(winner, True, 'white')
    ReplayText = font.render('Click to Replay', True, 'white')

    screen.blit(ResultText, (850, 400))
    screen.blit(ReplayText, (850, 500))

    ScoreText = font.render(f"Correct Answers: {QuestionsRight} | Incorrect Answers: {QuestionsWrong}", True, 'white')
    screen.blit(ScoreText, (850, 600))

    pygame.display.update()

    WaitingForClick = True
    while WaitingForClick:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                WaitingForClick = False
                return True


def DrawExitButton(screen):
    font = pygame.font.SysFont('Arial', 36)
    exit_text = font.render('Exit', True, (255, 255, 255))  
    button_width = 150
    button_height = 50
    button_x = 1770 
    button_y = 950  
    pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))  # Red button
    screen.blit(exit_text, (button_x + 40, button_y + 10))  # Position the text inside the button
    return pygame.Rect(button_x, button_y, button_width, button_height)  # Return the button rectangle for collision detection



# /////////////////////////////////////////Question Mode/////////////////////////////////////////


def WrapText(text, font, MaxWidth):
    words = text.split(' ')
    lines = []
    CurrentLine = ""
    
    for word in words:
        test_line = CurrentLine + " " + word if CurrentLine else word
        if font.size(test_line)[0] <= MaxWidth:
            CurrentLine = test_line
        else:
            if CurrentLine:
                lines.append(CurrentLine)
            CurrentLine = word

    if CurrentLine:
        lines.append(CurrentLine)
    
    return lines


def Question(QuestionsRight, QuestionsWrong, screen, cursor):
    global inQuestionScreen

    if inQuestionScreen:  
        return

    inQuestionScreen = True  

    RandomQuestion = cursor.execute("SELECT Question, Answer1, Answer2, Answer3, Answer4, CorrectAnswer FROM Questions ORDER BY RANDOM() LIMIT 1").fetchone()

    if RandomQuestion:
        QuestionText, answer1, answer2, answer3, answer4, correct_answer = RandomQuestion

        screen.fill('#35654d')

        pygame.draw.rect(screen, 'White', (0, 0, 1920, 540), 0, 5)

        font = pygame.font.SysFont('Arial', 48)
        QuestionSurface = font.render(QuestionText, True, (0, 0, 0))
        screen.blit(QuestionSurface, (20, 20))  

        box_width = 960
        box_height = 270
        margin = 20  

        WrappedAnswer1 = WrapText(answer1, font, box_width - 40)  
        WrappedAnswer2 = WrapText(answer2, font, box_width - 40)
        WrappedAnswer3 = WrapText(answer3, font, box_width - 40)
        WrappedAnswer4 = WrapText(answer4, font, box_width - 40)

        def RenderAnswer(AnswerLines, x, y):
            line_height = font.get_height() + margin  
            for i, line in enumerate(AnswerLines):
                AnswerSurface = font.render(line, True, (0, 0, 0))
                screen.blit(AnswerSurface, (x + 20, y + i * line_height))  

        Answer1 = pygame.draw.rect(screen, 'Red', (0, 540, box_width, box_height), 0, 5)
        Answer2 = pygame.draw.rect(screen, 'Blue', (0, 810, box_width, box_height), 0, 5)
        Answer3 = pygame.draw.rect(screen, 'Yellow', (960, 540, box_width, box_height), 0, 5)
        Answer4 = pygame.draw.rect(screen, 'Green', (960, 810, box_width, box_height), 0, 5)

        RenderAnswer(WrappedAnswer1, 0, 540)
        RenderAnswer(WrappedAnswer2, 0, 810)
        RenderAnswer(WrappedAnswer3, 960, 540)
        RenderAnswer(WrappedAnswer4, 960, 810)

        pygame.display.update()

        QuestionAnswered = False  

        while not QuestionAnswered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Answer1.collidepoint(event.pos):
                        if answer1 == correct_answer:
                            QuestionsRight += 1
                            Correct(screen)
                        else:
                            QuestionsWrong += 1
                            Incorrect(screen, correct_answer)
                        QuestionAnswered = True

                    elif Answer2.collidepoint(event.pos):
                        if answer2 == correct_answer:
                            QuestionsRight += 1
                            Correct(screen)
                        else:
                            QuestionsWrong += 1
                            Incorrect(screen, correct_answer)
                        QuestionAnswered = True

                    elif Answer3.collidepoint(event.pos):
                        if answer3 == correct_answer:
                            QuestionsRight += 1
                            Correct(screen)
                        else:
                            QuestionsWrong += 1
                            Incorrect(screen, correct_answer)
                        QuestionAnswered = True

                    elif Answer4.collidepoint(event.pos):
                        if answer4 == correct_answer:
                            QuestionsRight += 1
                            Correct(screen)
                        else:
                            QuestionsWrong += 1
                            Incorrect(screen, correct_answer)
                        QuestionAnswered = True

            pygame.display.update()


def Correct(screen):
    global QuestionsRight, inQuestionScreen 
    screen.fill('#00c121')

    CorrectText = font.render('Correct', True, 'white')
    ClickText = font.render('Click to Continue', True, 'White')

    screen.blit(CorrectText, (920, 250))
    screen.blit(ClickText, (920, 980))
    pygame.display.update()

    WaitingForClick = True
    while WaitingForClick:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                QuestionsRight += 1 
                WaitingForClick = False 
                inQuestionScreen = False  # Reset flag so we can go back to Blackjack screen
                return 


def Incorrect(screen, CorrectAnswer):
    global QuestionsWrong, inQuestionScreen  
    screen.fill('#f40000')

    IncorrectText = font.render('Incorrect', True, 'white')
    ClickText = font.render('Click to Continue', True, 'White')
    CorrectAnswerText = font.render(f'Correct Answer: {CorrectAnswer}', True, 'white')

    screen.blit(IncorrectText, (860, 250))
    screen.blit(CorrectAnswerText, (100, 350))
    screen.blit(ClickText, (880, 900))
    pygame.display.update()

    WaitingForClick = True
    while WaitingForClick:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                QuestionsWrong += 1  
                WaitingForClick = False  
                inQuestionScreen = False  # Reset flag so we can go back to Blackjack screen
                return
  




# /////////////////////////////////////////Main Game////////////////////////////////////////

inQuestionScreen = False  

while run:
    screen.fill('#35654d')
    clock.tick(fps)
    MousePos = pygame.mouse.get_pos()
    button = DrawCard(active, QuestionsRight, QuestionsWrong)

    # Add the Exit Button
    exit_button_rect = DrawExitButton(screen)

    if inQuestionScreen:
        continue  # Skip the rest of the loop while in question screen

    if Initial:
        CardDrawing(PlayerHand, DealerHand, PlayerScore, DealerScore, QuestionsRight, QuestionsWrong)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button_rect.collidepoint(event.pos):  # Check if the Exit button is clicked
                run = False  # Exit the game

            if not active:
                if button[0].collidepoint(event.pos):
                    active = True
                    Initial = True
                    deck = Deck()
                    PlayerHand = []
                    DealerHand = []
                    PlayerScore = 0
                    DealerScore = 0
                    QuestionsRight = 0
                    QuestionsWrong = 0
                    DealHand(deck)
                    CardDrawing(PlayerHand, DealerHand, PlayerScore, DealerScore, QuestionsRight, QuestionsWrong)
                    clock.tick(fps)

            if active:
                if len(button) > 1 and button[1].collidepoint(event.pos):
                    if PlayerScore is not None and PlayerScore < 21:
                        PlayerHand.append(deck.DealCard())
                        PlayerScore = CalculateScore(PlayerHand)
                        CardDrawing(PlayerHand, DealerHand, PlayerScore, DealerScore, QuestionsRight, QuestionsWrong)
                        clock.tick(fps)

                    QuestionMode = True  
                    Question(QuestionsRight, QuestionsWrong, screen, cursor)
                    clock.tick(fps)

                elif len(button) >= 2 and button[0].collidepoint(event.pos):
                    PlayerScore = CalculateScore(PlayerHand)

                    while DealerScore is not None and DealerScore < 17:
                        DealerHand.append(deck.DealCard())
                        DealerScore = CalculateScore(DealerHand)
                        CardDrawing(PlayerHand, DealerHand, PlayerScore, DealerScore, QuestionsRight, QuestionsWrong)
                        clock.tick(fps)

                    QuestionMode = True
                    Question(QuestionsRight, QuestionsWrong, screen, cursor)
                    clock.tick(fps)

                    winner = DetermineWinner(PlayerScore, DealerScore)
                    GameOver = GameOverScreen(winner, screen)

                    if GameOver:
                        active = False
                        Initial = False
                        PlayerHand = []
                        DealerHand = []
                        PlayerScore = 0
                        DealerScore = 0
                        QuestionsRight = 0
                        QuestionsWrong = 0
                        clock.tick(fps)

                elif len(button) >= 3 and button[2].collidepoint(event.pos):
                    active = False
                    Initial = False
                    PlayerHand = []
                    DealerHand = []
                    PlayerScore = 0
                    DealerScore = 0
                    QuestionsRight = 0
                    QuestionsWrong = 0
                    clock.tick(fps)

    pygame.display.update()



    