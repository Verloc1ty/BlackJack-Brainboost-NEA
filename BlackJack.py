import pygame
import random
import sqlite3


pygame.init()
connection = sqlite3.connect("Data.db")
cursor = connection.cursor()  

# Variable Set up
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((1920, 1080))
font = pygame.font.SysFont('Arial', 55, bold=True)
run = True
active = False
Initial = False
PlayerHand = []
DealerHand = []

# Setting up both scores for Questions and the BlackJack Game
PlayerScore = 0
DealerScore = 0
QuestionsRight = 0
QuestionsWrong = 0
QuestionMode = False

from Main_Menu import Button

class Card:
    # Function that initilises the Card class with the Value and Suit of each card. Furthermore, Set up each name of the card and grabs each PNG related to that name.
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.name = f"{value} of {suit}"
        self.image_filename = f'{value}_of_{suit}.png'

    
    def __repr__(self):
        return self.name

    # Function that gets the Value of the Card, returns the Value as the corresponding Value of the card. But returns 10 if Jack, King or Queen is pulled and 11 if an Ace is pulled.
    def card_value(self):
        if self.value in ['J', 'Q', 'K']:
            return 10
        elif self.value == 'A':
            return 11
        else:
            return int(self.value)


class Deck:
    # Function that sets up what a normal deck of cards should be. With 4 suits and 13 cards per suit.
    # Furthermore, creates a cards array that has each Card that has a Suit and a value corresponding to it. Then calls the Shuffle function to shuffle the cards in each index of the array so the card order is random.
    def __init__(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(value, suit) for suit in suits for value in values]
        self.shuffle()

    # Function that shuffes the order of cards in the card array
    def shuffle(self):
        random.shuffle(self.cards)

    # Function that Removes (pops) an item from the array of cards for each card in the Array and stops when there is no more cards in the array.
    def DealCard(self):
        return self.cards.pop() if self.cards else None

    # Calculates how many cards are in the card array at any given time.
    def __len__(self):
        return len(self.cards)


class CardImage():
    # Function that Initialises the class.
    # It also transforms the size of the Image using pygame to specified pixel height and widths
    # Assigns X and Y cordinates to to be chosen where the Rectangle is wanted to be placed
    # Sets up a rectangle around the Image from a center of the X and Y cords, this allows it to function as a button in future
    def __init__(self, image, pos):
        self.image = pygame.transform.scale(image, (175, 225))
        self.XCord = pos[0]
        self.YCord = pos[1]
        self.rect = self.image.get_rect(center=(self.XCord, self.YCord))

    # Function that updates the screen with the Images, using blit fro pygame to put the Image of the card and its rectangle that allows for future processing around it
    def Update(self):
        if self.image is not None:
            screen.blit(self.image, self.rect)


# ----------------------------------------------Main Functions----------------------------------------------------------------


# Function that Sets up a array of Buttons that are to be pressed in the BlackJackGame
# First if the Active flag is not active (meaning it is false) then it will draw the Deal Hand button on the screen as well as the Amount of Questions the Player gets right or wrong. It will also Draw a Rectangle and Put Deal Hand text inside that Rectangle button
# Then if the Active flag is active, it will Draw the Hit, Stand and Replay retangles on the screen. Also appends the Hit, Stand and Replay buttons into the Button array.
# Finally returns the List of Buttons / Rectangles that there is.
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


# Function that Deals the cards to the Player's and Dealer's hand via using the DealCard function to Pop cards off the Card array randomly and putting it into the Player's and Dealer's Hand respectively
# Also uses CalculateScore Function to assign the Player and Dealer a hand score depending on what cards they have
# Finally Returns all these values
def DealHand(deck):
    global PlayerHand, DealerHand, PlayerScore, DealerScore
    PlayerHand.append(deck.DealCard())
    PlayerHand.append(deck.DealCard())

    DealerHand.append(deck.DealCard())
    DealerHand.append(deck.DealCard())

    PlayerScore = CalculateScore(PlayerHand)
    DealerScore = CalculateScore(DealerHand)

    return PlayerHand, DealerHand, PlayerScore, DealerScore

# Function that Calculates the Scores for every hand that can be given in BlackJack
# Does this by first taking every card in the hand and looping through it, adding the cards value (Calculated via the card_value function) to the score. But if the card is an Ace it increments the Ace count by 1.
# Then if the Hand has an Ace in it, and the score is less that 21 is subtracts 10 from the score to indicate the Hand has chosen the Ace to be a 1 instead of a 11 just like in BlackJack
# Then Returns the Score if it is less than 21, because there is something else that is displayed later for when they Bust in Blackjack.
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



# Function that draws the cards on the screen for each of the Cards removed previously from the card array and put into the Player and Dealer card array
# Loops through Player and Dealers hand, and displays each card that is in the Respective hands next to each other (Uses .Update() to update the screen). Each new card goes to the right of the last one
# Then it calculates whether or not the Player has Busted (Indicated by if CalculateScore returns none), Hit BlackJack (If the PlayersScore is 21) or just a score (if the PlayerScore < 21)
# Then it calculates whether or not the Dealer has Busted (Indicated by if CalculateScore returns none), Hit BlackJack (If the DealersScore is 21) or just a score (if the DealerScore < 21)
# With it Updating the screen using .blit to upload the scores to the screen for the User to see

# Also Uses the QuestionsRight and QuestionsWrong variables to indicate / display how many questions the User has answered correct or incorrectly
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


# Function that Chooses who wins the Game
# Does this by taking the PlayerScore and DealerScore and comparing them in Different ways to determine who wins
# Follows Main BlackJack logic, of if Player busted then dealer wins etc...
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


# Function that displays who won the BlackJack Game
# Does this by creating a new screen that displays how many questiosn they have gotten Right and or Wrong
# Then also waits for the User to click the screen so it doesnt automatically go away. Also if you quit / press the close button the Python program stops
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

# Function that Draws the Exit button that stops the Game of BlackJack / Dealing of Cards and takes the User back to the Main menu parts of the Program
# Does this by setting a bunch of Pixel Measurements / Cordinates and then using them to draw a Rectanlge at thoses cordinates of a specific size
# Then .blits it to the screen so that the screen is updated and then returns it so that it can be tested for whether or not a User has pressed it
def DrawExitButton(screen):
    font = pygame.font.SysFont('Arial', 36)
    exit_text = font.render('Exit', True, (255, 255, 255))  
    button_width = 150
    button_height = 50
    button_x = 1770 
    button_y = 950  
    pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
    screen.blit(exit_text, (button_x + 40, button_y + 10)) 
    return pygame.Rect(button_x, button_y, button_width, button_height)



# /////////////////////////////////////////Question Mode/////////////////////////////////////////


# Function that is used to Make the Questions text doesnt Overspill into the Other boxes
# Does this by splitting each answers text into seperate words and looping through all of these words and test their width to see if they can fit on the same line
# Then it appends the words into the Currentline Text and then Returns lines
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


# Function to Ask questions during the Game of BlackJack
# Uses the inQuestionScreen for debugging to make sure the screen only pops up upon pressing a blackjack action button
# Gets the Relavent things from the Data.db database's Questions table
# For these different answers it is wrapping then using Wraptext() to make sure they fit into the Rectangle and also creating the Question box at the top of the screen
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

        # Function that Uses the Amount of Lines each answer texts up to Render each Answer on a seperate line inside of Rectanlge and then Displays it on the screen.
        def RenderAnswer(AnswerLines, x, y):
            line_height = font.get_height() + margin  
            for i, line in enumerate(AnswerLines):
                AnswerSurface = font.render(line, True, (0, 0, 0))
                screen.blit(AnswerSurface, (x + 20, y + i * line_height))  

        # Displays the 4 different answer's boxes and then Blits the text for the answers inside of those boxes.
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

        # This is the logic of whether or not the User has clicked the correct answer or a wrong answer. Uses Question answered to make sure the question screen stays up until the User has answered the Prompted Question
        # Uses simple Comparisons between the Answers to correct_answer and displays the appropriate Correct or Incorrect screen when answered.
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

# Function that is used to display the Correct Screen when the User presses the correct answer out of all the Answers given
# Does this by setting up a new screen that says Correct and Click to continue on it and waits for the User to click the screen again to get rid of it.
def Correct(screen):
    global QuestionsRight, inQuestionScreen 
    screen.fill('#00c121')

    CorrectText = font.render('Correct', True, 'white')
    ClickText = font.render('Click to Continue', True, 'White')

    screen.blit(CorrectText, (920, 250))
    screen.blit(ClickText, (920, 980))
    pygame.display.update()

    # Input Handling to test whether or not the User is still on that screen and so it doenst automatically go away.
    # Resets the flags also so it can go back to the Main BlackJackg game
    WaitingForClick = True
    while WaitingForClick:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                QuestionsRight += 1 
                WaitingForClick = False 
                inQuestionScreen = False
                return 

# Function to display Whether or not the User has gotten an Asnwer that is displayed Wrong
# Does this by Displaying a Red screen that says Incorrect as well as the Correct Answer so the User knows what the correct answer actually is
# Uses Pygame to update the screen with the relavent variables / things created
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

    # Input handling to check whether or not the User has clicked the Incorrect screen so that it can go away and bring them back to the Main BlackJack Game
    # Resets the flags also so it can go back to the Main BlackJackg game
    WaitingForClick = True
    while WaitingForClick:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                QuestionsWrong += 1  
                WaitingForClick = False  
                inQuestionScreen = False 
                return
  




# /////////////////////////////////////////Main Game////////////////////////////////////////



# Sets thiis to false as to make it so the question screens dont pop up
inQuestionScreen = False  

# Main Game loop
# Sets the screen to the Deal Hand screen, so that the User can press it to start the BlackJack game
while run:
    screen.fill('#35654d')
    clock.tick(fps)
    MousePos = pygame.mouse.get_pos()
    button = DrawCard(active, QuestionsRight, QuestionsWrong)

    exit_button_rect = DrawExitButton(screen)

    # Uses this to skip the whole rest of the loop (The BlackJack game) when the Question screen pops up. This allows them to not clash with each other and happen one after another instead of simultaneously which would cause errors
    if inQuestionScreen:
        continue
    # Initial Used to Initiate the Deal Hand Button as the Blackjack hands havent been dealt yet so the Deal Hand button is required as to deal them out
    if Initial:
        CardDrawing(PlayerHand, DealerHand, PlayerScore, DealerScore, QuestionsRight, QuestionsWrong)


    # Event Handling
    # Has a Generic Pygame quit event check, to check if someone closes the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        # Checks for when and if someone presses the Exit button at any time so that it can bring them back to the main menu of the program
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button_rect.collidepoint(event.pos): 
                run = False

            # Uses active to tell the program that the BlackJack game hasnt started and the cards need to be dealt out, so it displays the Deal Hand button for the User to press to Deal out the Cards to the Player and Dealer
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

            # When the Game is Active (Active = True), then it checks to whether or not the Mouse has clicked on the rectangle with "Hit", "Stand" or "Replay" and does the specific things
            # Upon pressing Hit the Player is Dealt a card (Popped out of the Card array) and the value of the card is added to the PlayerScore and then a Question is displayed for the User to answer due to QuestionMode being flagged as True
            # Upon Pressing Stand it Deals the Dealer a card if the Dealers hand total is less than 17 (standard blackjack rules), also adding the value of the card to the DealerScore and then asks the User a question.
            # Upon pressing Replay, it changes the Active flag to false and clears all variables for the Game to start again, as it brings you back to the Deal hand screen
            # After Pressing stand it also Determines who won the game and displays the Gameover screen depending on whether or not the Player or Dealerhas won
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



    
