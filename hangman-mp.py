import random
import time
import pygame,os
import requests
import json

### SCREEN SIZE
WIDTH = 1024
HEIGHT = 683

### COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY  = (192,192,192)
DGREY  = (50,50,50)
RED  = (207,0,0)
BLUE  = (70,70,207)
GREEN  = (70,207,70)

### INITIALIZE PYGAME
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0 ,32)
systemExit=False
buffer = 50
alphabet=['a','b','c','d','e','f','g','h','i','j',
          'k','l','m','n','o','p','q','r','s','t',
          'u','v','w','x','y','z','-']
letters=['a','b','c','d','e','f','g','h','i','j',
    'k','l','m','n','o','p','q','r','s','t',
    'u','v','w','x','y','z','A','B','C','D',
     'E','F','G','H','I','J','K','L','M','N',
     'O','P','Q','R','S','T','U','V','W','X','Y','Z']

### BACKGROUND IMAGE
background = pygame.image.load('./bg.jpg').convert_alpha()
trophy = pygame.image.load('./hi.png').convert_alpha()

### INITIALIZE FONTS
tin50 = pygame.font.Font('font/CoffeeTin.ttf', 50)
tin100 = pygame.font.Font('font/CoffeeTin.ttf',100)
chalkFont = pygame.font.Font('font/Chalkduster.ttf', 50)
chalkFont2 = pygame.font.Font('font/Chalkduster.ttf', 22)
chalkFont3 = pygame.font.Font('font/Chalkduster.ttf', 35)
WARNING = pygame.font.Font('font/blzee.ttf', 30)
indianFont = pygame.font.Font('font/IndianPoker.ttf', 40)
indianFont.set_bold(True)

loadText = tin50.render("Loading...", 1, BLACK)
loadSize = tin50.size("Loading...")
loadLoc = (WIDTH/2 - loadSize[0]/2, HEIGHT/2 - loadSize[1]/2)

### SHOW LOADING FOR 1 SEC
screen.blit(background, (0,0))
screen.blit(loadText, loadLoc)
pygame.display.flip()
time.sleep(1)

### START SCREEN
startText = chalkFont.render("Welcome to Hangman!", 1, GREY)
startSize = chalkFont.size("Welcome to Hangman!")
startLoc = (WIDTH/2 - startSize[0]/2, buffer)

### SINGLEPLAYER TEXT
spText = chalkFont3.render(" Single Player", 1, pygame.Color('lightskyblue3'))
spSize = chalkFont3.size(" Single Player")
spLoc = (100, buffer + 100)

sp_rect = pygame.Rect(WIDTH/2,buffer+100,WIDTH/2-100,spSize[1])
sp_labelrect = pygame.Rect(spLoc[0] - 30, spLoc[1], spSize[0] + 30, spSize[1])

### MULTIPLAYER TEXT
mpText = chalkFont3.render(" Multi Player", 1, pygame.Color('lightskyblue3'))
mpSize = chalkFont3.size(" Multi Player")
mpLoc = (100, buffer + 200)

mp_rect1 = pygame.Rect(WIDTH/2,buffer+200,(WIDTH/2-100)/2-5,mpSize[1])
mp_rect2 = pygame.Rect(WIDTH/2+(WIDTH/2-100)/2+5,buffer+200,(WIDTH/2-100)/2-5,mpSize[1])
mp_labelrect = pygame.Rect(mpLoc[0] - 30, mpLoc[1], mpSize[0] + 30, mpSize[1])

active_mp_1 = False
active_mp_2 = False
active_sp = False

p1name = ''
p2name = ''
mpStats = {}
active_player=1

### START BUTTON
startButton = tin100.render(" Start ", 1, BLACK)
buttonSize = tin100.size(" Start ")
buttonLoc = (WIDTH/2 - buttonSize[0]/2, HEIGHT/2 + buttonSize[1])
buttonRect = pygame.Rect(buttonLoc, buttonSize)
buttonRectOutline = pygame.Rect(buttonLoc, buttonSize)

### NEW GAME BUTTON
ngButton = tin50.render(" New Game ", 1, BLUE)
ngButtonSize = tin50.size(" New Game ")
ngButtonLoc = (WIDTH - ngButtonSize[0] - 10, HEIGHT - ngButtonSize[1] - 10)
ngButtonRect = pygame.Rect(ngButtonLoc, ngButtonSize)
# ngButtonRectOutline = pygame.Rect(ngButtonLoc, ngButtonSize)

### EXIT BUTTON
eButton = indianFont.render(" EXIT ", 1, RED)
eButtonSize = indianFont.size(" EXIT ")
eButtonLoc = (10, HEIGHT - eButtonSize[1] - 10)
eButtonRect = pygame.Rect(eButtonLoc, eButtonSize)

### NEXT BUTTON
nextButton = tin100.render(" Next ", 1, BLACK)
nextSize = tin100.size(" Next ")
nextLoc = (WIDTH/2 - nextSize[0]/2, HEIGHT/2 + nextSize[1])
nextRect = pygame.Rect(nextLoc, nextSize)
nextRectOutline = pygame.Rect(nextLoc, nextSize)

### STARTING STATE
state = 0
gamesWon = 0
gamesLost = 0
active_sp = True

### Guess Word
wordToGuess = ''
wordDefinition = ''
answer = []
invalidTries = []
inputword_rect = pygame.Rect(WIDTH/2,buffer+200,WIDTH/2-100, spSize[1])

show_error=False
#######################################################

#Welcome Screen - Select Single vs Multi Player
def welcome():
    global systemExit, state, active_mp_1, active_mp_2, active_sp, p1name, p2name, mpStats
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            systemExit=True
            return

        #when the user clicks the start button, change to the playing state
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseRect = pygame.Rect(event.pos, (1,1))
                if mouseRect.colliderect(buttonRect):
                    if p1name.strip() == "":
                        p1name = "Player 1"
                    if p2name.strip() == "":
                        p2name = "Player 2"
                    mpStats[p1name] = 0
                    mpStats[p2name] = 0
                    state += 1
                    return
                elif mp_rect1.collidepoint(event.pos) or mp_labelrect.collidepoint(event.pos):
                    if active_sp == True:
                        p1name = ""
                    active_mp_1 = True
                    active_mp_2 = False
                    active_sp = False
                elif mp_rect2.collidepoint(event.pos) or mp_labelrect.collidepoint(event.pos):
                    if active_sp == True:
                        p1name = ""
                        p2name = ""
                    active_mp_1 = False
                    active_mp_2 = True
                    active_sp = False
                elif sp_rect.collidepoint(event.pos) or sp_labelrect.collidepoint(event.pos):
                    active_sp = True
                    active_mp_1 = False
                    active_mp_2 = False
                    
        if event.type == pygame.KEYDOWN:
            #print("event=",event.key)
            if active_mp_1 == True:
                #print("active_mp_1 is True")
                if event.key == pygame.K_BACKSPACE:
                    p1name = p1name[:-1]
                elif event.key == pygame.K_RETURN:
                    active_mp_1 = False
                    active_mp_2 = True
                else:
                    if len(p1name)<=8:
                        p1name += event.unicode
                    #print("P1 Name:",p1name)
            elif active_mp_2 == True:
                if event.key == pygame.K_BACKSPACE:
                    p2name = p2name[:-1]
                elif event.key == pygame.K_RETURN:
                    active_mp_1 = True
                    active_mp_2 = False
                else:
                    if len(p2name)<=8:
                        p2name += event.unicode
                    #print("P2 Name:",p2name)
                        
            elif active_sp == True:
                if event.key == pygame.K_BACKSPACE:
                    p1name = p1name[:-1]
                else:
                    if len(p1name)<=12:
                        p1name += event.unicode
                    #print("P1 Name:",p1name)
               

    #draw background
    screen.blit(background, (0,0))

    #draw welcome text
    screen.blit(startText, startLoc)
    pygame.draw.circle(screen, GREY, (spLoc[0] - 20, spLoc[1] + 22), 16, 2)
    pygame.draw.circle(screen, GREY, (mpLoc[0] - 20, mpLoc[1] + 22), 16, 2)
    screen.blit(spText, spLoc)
    screen.blit(mpText, mpLoc)
    pygame.draw.rect(screen,pygame.Color('lightskyblue3'),sp_rect,2)
    pygame.draw.rect(screen,pygame.Color('lightskyblue3'),mp_rect1,2)
    pygame.draw.rect(screen,pygame.Color('lightskyblue3'),mp_rect2,2)
    
    if active_mp_1:
        pygame.draw.circle(screen, GREY, (mpLoc[0] - 20, mpLoc[1] + 22), 8)
        pygame.draw.rect(screen,pygame.Color('lightskyblue3'),mp_rect1,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),mp_rect2,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),sp_rect,2)
    elif active_mp_2:
        pygame.draw.circle(screen, GREY, (mpLoc[0] - 20, mpLoc[1] + 22), 8)
        pygame.draw.rect(screen,pygame.Color('gray15'),mp_rect1,2)
        pygame.draw.rect(screen,pygame.Color('lightskyblue3'),mp_rect2,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),sp_rect,2)
    elif active_sp:
        pygame.draw.circle(screen, GREY, (spLoc[0] - 20, spLoc[1] + 22), 8)
        pygame.draw.rect(screen,pygame.Color('lightskyblue3'),sp_rect,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),mp_rect1,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),mp_rect2,2)
    else:
        pygame.draw.rect(screen,pygame.Color('gray15'),mp_rect1,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),mp_rect2,2)
        pygame.draw.rect(screen,pygame.Color('gray15'),sp_rect,2)
        
    text_mp1 = chalkFont3.render(p1name,True,WHITE)
    text_mp2 = chalkFont3.render(p2name,True,WHITE)
    text_sp = chalkFont3.render(p1name,True,WHITE)
    if active_sp == False:
        screen.blit(text_mp1, (mp_rect1.x+5,mp_rect1.y+5))
        screen.blit(text_mp2, (mp_rect2.x+5,mp_rect2.y+5)) 
    else:
        screen.blit(text_sp, (sp_rect.x+5,sp_rect.y+5))
    
    #draw the start button
    pygame.draw.rect(screen, BLUE, buttonRect)
    pygame.draw.rect(screen, BLACK, buttonRectOutline, 2)
    screen.blit(startButton, buttonLoc)
    
    #Flip Display
    pygame.display.flip()
    
#Ask Player to enter a word (multi-player only)
def enter_a_word():
    global systemExit, state, active_mp_1, active_mp_2, active_sp, p1name, p2name, active_player
    global wordToGuess, inputword_rect, event, show_error
    #Return if Single Player
    if active_sp == True:
        initialize_game()
        state = 2
        return
    
    #Loop - event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            systemExit=True
            return
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseRect = pygame.Rect(event.pos, (1,1))
                if mouseRect.colliderect(nextRect):
                    if is_word_valid(wordToGuess):
                        initialize_game()
                        state += 1
                        return
                    else:
                        show_error=True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                wordToGuess = wordToGuess[:-1]
                show_error=False
            else:
                if len(wordToGuess)<=20:
                    if event.unicode in letters:
                        wordToGuess += event.unicode
                    show_error=False
    
    #Clear background
    screen.blit(background, (0,0))
    
    #Top Two Lines of Text
    if active_player == 1:
        wordtext1=p1name+", Please Enter a Word."
        wordtext2="("+p2name+", Please Look Away... NO PEEKING)"
    elif active_player == 2:
        wordtext1=p2name+", Please Enter a Word"
        wordtext2="("+p1name+", Please Look Away... NO PEEKING)"
    
    wordInputText = chalkFont3.render(wordtext1, 1, pygame.Color('lightskyblue3'))
    wordInputSize = chalkFont3.size(wordtext1)
    wordInputLoc = (WIDTH/2 - wordInputSize[0]/2, buffer)
    screen.blit(wordInputText, wordInputLoc)
    
    wordWarnText = WARNING.render(wordtext2, 1, pygame.Color('salmon'))
    wordWarnSize = WARNING.size(wordtext2)
    wordWarnLoc = (WIDTH/2 - wordWarnSize[0]/2, buffer + 100)
    screen.blit(wordWarnText, wordWarnLoc)
    
    #Input Rectangle
    inputword_rect = pygame.Rect(WIDTH/2-inputword_rect.w/2,buffer+200,inputword_rect.w, spSize[1])
    pygame.draw.rect(screen,pygame.Color('lightskyblue3'),inputword_rect,2)
    # Render Input Text
    text_surface = chalkFont3.render(wordToGuess,True,WHITE)
    # Show Text inside Rectangle
    screen.blit(text_surface, (inputword_rect.x+5,inputword_rect.y+5))
    # Make Rectangle grow with Text
    inputword_rect.w = max(100,text_surface.get_width() + 10)
    
    #Show Error (if applicable)
    if len(wordToGuess)>=19:
        error_text="Must be below 20 characters."
    elif show_error:
        error_text="Invalid Word. Please Try Again."
        
    if len(wordToGuess)>=19 or show_error:
        errorText = WARNING.render(error_text, 1, pygame.Color('salmon'))
        errorSize = WARNING.size(error_text)
        errorLoc = (WIDTH/2 - errorSize[0]/2, buffer + 300)
        screen.blit(errorText, errorLoc)

    # NEXT action button
    screen.blit(nextButton,nextLoc)
    
    #Flip Display
    pygame.display.flip()

# Get a new word from dictionary
def picklePicker():
    global wordToGuess
    word_file = "/usr/share/dict/words"
    WORDS = open(word_file).read().splitlines()
    if active_sp==True:
        randomWord = fix_word(random.choice(WORDS))
        randomWord = randomWord.replace("'","").strip()
        return randomWord.replace(" ", "-")
    else:
        return wordToGuess
    #randomWord="Word"    
    
def fix_word(word):
    response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + 
                            word + "?key=1d70c06e-168f-438c-b958-43e3c8e4e081")
    responseString = json.dumps(response.json())
    if "shortdef" in responseString:
        return word
    else:
        print("shortdef missing, got response:", responseString)
        return random.choice(response.json())
            
def is_word_valid(word):
    response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + 
                            word + "?key=1d70c06e-168f-438c-b958-43e3c8e4e081")
    responseString = json.dumps(response.json())
    if "shortdef" in responseString:
        return True
    else:
        return False
    
    
def initialize_game():
    global wordToGuess, answer, invalidTries, wordDefinition, gamesWon, gamesLost
    answer = []
    invalidTries = []
    wordToGuess=picklePicker().lower()
    wordDefinition = lookup_dictionary(wordToGuess)[0];
    
    for i in range(0,len(wordToGuess),1):
        answer.append("_")
    draw_background()
    pygame.display.flip()

def draw_background():
    Pi = 3.14
    #clear all
    screen.fill((0,0,0))
    
    #draw background
    screen.blit(background, (0,0))
       
    pygame.draw.line(screen, GREY, (80, 80), (80, 500),20)
    pygame.draw.line(screen, GREY, (71, 80), (300, 80),20)
    pygame.draw.line(screen, GREY, (300, 71), (300, 130),20)
    pygame.draw.line(screen, GREY, (80, 130), (130, 80),10)
    pygame.draw.circle(screen, DGREY, (300, 180), 50, 10)
    pygame.draw.line(screen, DGREY, (300, 230), (300, 380),10)
    pygame.draw.line(screen, DGREY, (300, 270), (380, 230),10)
    pygame.draw.line(screen, DGREY, (300, 270), (220, 230),10)
    pygame.draw.line(screen, DGREY, (300, 380), (340, 450),10)
    pygame.draw.line(screen, DGREY, (300, 380), (260, 450),10)
    pygame.draw.circle(screen, DGREY, (280, 165), 10, 5)
    pygame.draw.circle(screen, DGREY, (320, 165), 10, 5)
    pygame.draw.arc(screen, DGREY, [280,180,40,30], Pi, 2*Pi, 5)
    draw_alphabet()
    display_current_answer()

def display_current_answer():
    x = 100
    y = 570
    width = (WIDTH - 2*100)/len(answer)
    spacing = width/5
    width = width - spacing
    
    for ch in answer:
        if ch == '_':
            pygame.draw.line(screen, GREY, (x, y), (x + width, y), 2)
            x = x + width + spacing
        else:
            pygame.draw.line(screen, GREY, (x, y), (x + width, y), 2)
            char = chalkFont.render(ch, 1, GREY)
            charSize = chalkFont.size(ch)
            screen.blit(char, (x + width/2 - charSize[0]/2,y - charSize[1]))
            x = x + width + spacing
            
def find(s, ch):
    Indexes=list()
    i=0
    for char in s:
        if char==ch:
            Indexes.append(i)
        i+=1
    return Indexes

            
def draw_alphabet():
    x = 500
    y = 150
    spacing = 20    
    for ch in alphabet:
        char = chalkFont.render(ch, 1, GREY)
        charSize = chalkFont.size(ch)
        screen.blit(char, (x,y - charSize[1]))
        if ch in invalidTries:
            pygame.draw.line(screen, GREY, (x, y), (x + charSize[0], y - charSize[1]), 2)
        elif ch in answer:
            char = chalkFont.render(ch, 1, DGREY)
            charSize = chalkFont.size(ch)
            screen.blit(char, (x,y - charSize[1]))
        x = x + 40 + spacing
        if x > WIDTH - 124: #900
            x = 500
            y = y + 100

def draw_hangman(count):
    Pi=3.14
    global state, gamesLost, invalidTries
    if count > 0: ##Head
        pygame.draw.circle(screen, GREY, (300, 180), 50, 10)
    if count > 1: ##Eyes
        pygame.draw.circle(screen, GREY, (280, 165), 10, 5)
        pygame.draw.circle(screen, GREY, (320, 165), 10, 5)
    if count > 2: ##Mouth
        if len(invalidTries) == 3:
            pygame.draw.arc(screen, GREY, [280,180,40,30], Pi, 2*Pi, 4) #Smile
        elif len(invalidTries) == 4:
            pygame.draw.arc(screen, GREY, [280,184,40,20], Pi, 2*Pi, 4) #Smile
        elif len(invalidTries) == 5:
            pygame.draw.arc(screen, GREY, [280,188,40,10], Pi, 2*Pi, 4) #Smile
        elif len(invalidTries) == 6:
            pygame.draw.arc(screen, GREY, [280,188,40,20], 2*Pi, Pi, 4) #Frown            
        elif len(invalidTries) == 7:
            pygame.draw.arc(screen, GREY, [280,188,40,30], 2*Pi, Pi, 4) #Frown            
    if count > 3:
        pygame.draw.line(screen, GREY, (300, 230), (300, 380),10)
    if count > 4:
        pygame.draw.line(screen, GREY, (300, 270), (380, 230),10)
    if count > 5:
        pygame.draw.line(screen, GREY, (300, 270), (220, 230),10)
    if count > 6:
        pygame.draw.line(screen, GREY, (300, 380), (340, 450),10)
        showWordDefinition(610)
    if count > 7:
        pygame.draw.line(screen, GREY, (300, 380), (260, 450),10)
        state+=1
        gamesLost+=1
        
            
def play():
    global systemExit, state, invalidTries, wordToGuess, answer, gamesWon, p1name, p2name, active_player, mpStats
    letter_clicked = ''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            systemExit=True
            return

        #when the user clicks the start button, change to the playing state
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
#                 print("Pos:", event.pos)
                if ((event.pos[0] - 495)%60 <= 30) and ((event.pos[1] - 100)%100 <= 30):
                    xIndex= int((event.pos[0] - 495)/60)
                    yIndex= int((event.pos[1] - 100)/100)
                    if xIndex >= 0 and yIndex >= 0:
                        letter_clicked = alphabet[xIndex + yIndex*7]
#                         print("Letter Clicked",letter_clicked)
                        if letter_clicked in wordToGuess:
                            found_indexes=find(wordToGuess, letter_clicked)
                            for i in found_indexes:
                                answer[i]=letter_clicked
                        else:
                            if letter_clicked not in invalidTries:
                                invalidTries.append(letter_clicked)
#                     else:
#                         print("X-Index:", xIndex, "Offset:", (event.pos[0] - 495)%60)
#                         print("Y-Index:", yIndex, "Offset:", (event.pos[1] - 100)%100)

    draw_background()
#     draw_alphabet()
#     display_current_answer()
    if active_sp==True:
        showGameNumber()
    else:
        showMpStats()
    draw_hangman(len(invalidTries))
    if list(wordToGuess)==answer:
        state+=1
        if active_sp == True:
            gamesWon+=1
        else:
            if active_player == 1:
                mpStats[p1name]+=1
            else:
                mpStats[p2name]+=1
    pygame.display.flip()

def lookup_dictionary(word):
    #School dictionary 8aec5760-79cb-41cb-a876-62a3b22515e5
    #https://www.dictionaryapi.com/api/v3/references/sd4/json/baseball?key=your-api-key

    #College dictionary 1d70c06e-168f-438c-b958-43e3c8e4e081
    #https://www.dictionaryapi.com/api/v3/references/collegiate/json/voluminous?key=your-api-key

    response = requests.get("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + 
                            word + "?key=1d70c06e-168f-438c-b958-43e3c8e4e081")
    if response.status_code != 200:
        # This means something went wrong.
        print("Error in dictionary lookup:", response.json())
        return ""
    else:
        short_def = response.json()[0]['shortdef']
        print("short_def:",short_def)
        return short_def
    
def showHintLine(wordDef, ypos):
    wordDescText = chalkFont2.render(wordDef, 1, GREY)
    wordDescSize = chalkFont2.size(wordDef)
    wordDescLoc = (WIDTH/2 - wordDescSize[0]/2, ypos)
    screen.blit(wordDescText, wordDescLoc)

def showWordDefinition(ypos):
    wordDescText = chalkFont2.render("\"" + wordDefinition + "\"", 1, GREY)
    wordDescSize = chalkFont2.size("\"" + wordDefinition + "\"")
    rows = int(wordDescSize[0] / (WIDTH - 20)) + 1 # 10 margin on both sides
    startingYos = ypos if rows == 1 else (ypos - wordDescSize[1]/2 if rows == 2 else ypos - wordDescSize[1]);
    words = wordDefinition.split()
    for row in range(0,rows,1):
        partText = ""
        for i in range(int(row*len(words)/rows),int(((row+1)*len(words))/rows),1):
            partText += words[i] + " "
        partText = "\"" + partText if row == 0 else (partText.strip() + "\"" if row == (rows-1) else partText)
        partText = partText.strip() + "\"" if rows == 1 else partText
        showHintLine(partText, startingYos + (row)*wordDescSize[1])

def showGameNumber():
    gameText = chalkFont2.render("Game "+ str(gamesWon+gamesLost+1), 1, pygame.Color('lightskyblue3'))
    gameTextSize = chalkFont2.size("Game "+ str(gamesWon+gamesLost+1))
    gameTextLoc = (10, 10)
    screen.blit(gameText, gameTextLoc)

    wonText = chalkFont2.render("Games Won: "+ str(gamesWon), 1, pygame.Color('lightgreen'))
    wonTextSize = chalkFont2.size("Games Won: "+ str(gamesWon) + " ")
    gameTextLoc = (WIDTH - wonTextSize[0] - 10, 10)
    screen.blit(wonText, gameTextLoc)

    lostText = chalkFont2.render("Games Lost: "+ str(gamesLost), 1, pygame.Color('salmon'))
    lostTextSize = chalkFont2.size("Games Lost: "+ str(gamesLost))
    gameTextLoc = (WIDTH - lostTextSize[0] - 10, wonTextSize[1] + 10)
    screen.blit(lostText, gameTextLoc)

def showMpStats():
    global p1name, p2name, mpStats
    gameText = chalkFont2.render("Game "+ str(gamesWon+gamesLost+1), 1, pygame.Color('lightskyblue3'))
    gameTextSize = chalkFont2.size("Game "+ str(gamesWon+gamesLost+1))
    gameTextLoc = (10, 10)
    screen.blit(gameText, gameTextLoc)

    p1wonText = chalkFont2.render(p1name+"'s Games Won: "+ str(mpStats[p1name]), 1, pygame.Color('lightgreen'))
    p1wonTextSize = chalkFont2.size(p1name+"'s Games Won: "+ str(mpStats[p1name]) + " ")
    p1gameTextLoc = (WIDTH - p1wonTextSize[0] - 10, 10)
    screen.blit(p1wonText, p1gameTextLoc)

    p2wonText = chalkFont2.render(p2name+"'s Games Won: "+ str(mpStats[p2name]), 1, pygame.Color('lightgreen'))
    p2wonTextSize = chalkFont2.size(p2name+"'s Games Won: "+ str(mpStats[p2name]))
    p2gameTextLoc = (WIDTH - p2wonTextSize[0] - 10, p1wonTextSize[1] + 10)
    screen.blit(p2wonText, p2gameTextLoc)

    
def results():
    global systemExit, wordToGuess, answer, state, wordDefinition, active_player, mpStats, p1name, p2name
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            systemExit=True
            return

        #when the user clicks the start button, change to the playing state
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouseRect = pygame.Rect(event.pos, (1,1))
                if mouseRect.colliderect(ngButtonRect):
                    state = 1
                    wordToGuess = ""
                    if active_player == 1:
                        active_player=2
                    else:
                        active_player=1
                    if active_sp == True:
                        initialize_game()
                    else:
                        enter_a_word()
                    return
                elif mouseRect.colliderect(eButtonRect):
                    systemExit=True
                    return
    #clear all
    screen.fill((0,0,0))
    #draw background
    screen.blit(background, (0,0))
    

    if list(wordToGuess)==answer:
        restext="You Won!"
        reveal_answer="You guessed "
        resultText = chalkFont.render(restext, 1, pygame.Color('lightgreen'))
        screen.blit(trophy, (WIDTH/2-140,(HEIGHT/2-243)/2+HEIGHT/2))
    else:
        restext="You Lost!"
        reveal_answer="The answer was "
        resultText = chalkFont.render(restext, 1, pygame.Color('salmon'))

    revealText = chalkFont.render(reveal_answer, 1, GREY)
    revealSize = chalkFont.size(reveal_answer)
    wtgText = chalkFont.render(wordToGuess, 1, pygame.Color('lightskyblue3'))
    wtgSize = chalkFont.size(wordToGuess)
    
    revealLoc = (WIDTH/2 - (revealSize[0] + wtgSize[0])/2, buffer)
    screen.blit(revealText, revealLoc)
    
    wtgLoc = (WIDTH/2 + revealSize[0]-(revealSize[0] + wtgSize[0])/2, buffer)
    screen.blit(wtgText, wtgLoc)
    
    showWordDefinition(HEIGHT/4)

    resultSize = chalkFont.size(restext)
    resultLoc = (WIDTH/2 - resultSize[0]/2, HEIGHT/2 - resultSize[1]/2)
    screen.blit(resultText, resultLoc)
    
#     pygame.draw.rect(screen, BLUE, ngButtonRect)
#     pygame.draw.rect(screen, BLACK, ngButtonRectOutline, 2)
    screen.blit(ngButton, ngButtonLoc)
    
    screen.blit(eButton, eButtonLoc)
#     lookup_dictionary(wordToGuess)
    
    pygame.display.flip()
    
    
#############################################################
if __name__ == "__main__":
	os.environ['SDL_VIDEO_CENTERED'] = '1' #center screen
	pygame.init()
	pygame.display.set_caption("Hangman")
	screen = pygame.display.set_mode((WIDTH, HEIGHT), 0 ,32)
	
	Myclock = pygame.time.Clock()
	while True:
		if systemExit==True:
			pygame.quit()
			break;
		if state == 0:
			welcome()
		elif state == 1:
			enter_a_word()
		elif state == 2:
			play()
		elif state == 3:
			results()
		Myclock.tick(64)    
	exit()
