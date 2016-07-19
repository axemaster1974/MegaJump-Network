# MegaJump game functions

import pygame, time, os, sys
from pygame.locals import *
from pyglet import clock

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (240, 240, 20)

saveFile="gameSaves.txt"
font = 'arialbd.ttf'

# display text with x co-ordinate as center
def displayText(surface, fontSize, x, y, text, colour):
    
    fontObj = pygame.font.Font(font, fontSize)

    textObj = fontObj.render(text, 0, colour)
    textRect = textObj.get_rect()
    textRect.center = (x, y)

    surface.blit(textObj, textRect)

# display text left justified with x co-ordinate as left of text rectangle
def displayTextLJ(surface, fontSize, x, y, text, colour):

    fontObj = pygame.font.Font(font, fontSize)

    textObj = fontObj.render(text, 0, colour)
    textRect = textObj.get_rect()
    textRect.left = x
    textRect.centery = y

    surface.blit(textObj, textRect)

# display time in user friendly format    
def displayTime(windowSurface, timeElapsed, x, y, COLOUR, textSize, justify):
        
    minutes = timeElapsed // 1000 // 60
    seconds = timeElapsed // 1000 % 60
    hundrethSecs = timeElapsed % 1000 // 10

    if minutes < 10:
        minStr = '0' + str(minutes)
    else:
        minStr = str(minutes)

    if seconds < 10:
        secStr = '0' + str(seconds)
    else:
        secStr = str(seconds)

    if hundrethSecs < 10:
        hundrethStr = '0' + str(hundrethSecs)
    else:
        hundrethStr = str(hundrethSecs)

    if justify:
        displayTextLJ(windowSurface, textSize, x, y, minStr + ' : ' + secStr + ' : ' + hundrethStr, COLOUR)
    else:
        displayText(windowSurface, textSize, x, y, minStr + ' : ' + secStr + ' : ' + hundrethStr, COLOUR)

# display countdown
def countdown(windowSurface, WWIDTH, WHEIGHT):
    COUNTDOWN = ['3', '.', '.', '2', '.', '.', '1', '.', '.']
    count = 0
    shift = 30
    
    for i in COUNTDOWN:
        displayText(windowSurface, 64, (WWIDTH / 2 - 150) + (shift * count) , WHEIGHT / 2, i, GREEN)
        pygame.display.update()
        time.sleep(0.2)
        count+=1

    displayText(windowSurface, 64, (WWIDTH / 2 - 150) + (shift * count) + 40 , WHEIGHT / 2, "GO!", GREEN)
    pygame.display.update()
    time.sleep(0.2)

# Load saved games from save file into array of dictionary entries
def loadGames(windowSurface, WWIDTH):

    try:
        file = open(saveFile, 'r')
    except FileNotFoundError:
        displayText(windowSurface, 24, WWIDTH / 2, 400, 'No save file found', RED)
        return

    if os.stat(file.name).st_size == 0:
        displayText(windowSurface, 24, WWIDTH / 2, 400, 'No saved games found', RED)
        return

    savedGames = []

    for line in file:
        line = line.rstrip('\n')
        (name, record, score, wwidth, wheight, pwidth, pheight, radius, pnumber, difficulty, coords) = line.split(',')
        d = {'name': name, 'record': record, 'score': score, 'wwidth': wwidth, 'wheight': wheight, 'pwidth': pwidth, 'pheight': pheight, 'radius': radius, 'pnumber': pnumber, 'difficulty': difficulty, 'coords': coords}
        savedGames.append(d)

    file.close()

    return savedGames

# Take saved game, update savedGames array, then write to gamesSaves file
def saveGames(windowSurface, WWIDTH, WHEIGHT, savedGame, savedGames, gameSlot, mode):
    
    try:
        file = open(saveFile, 'w+')
    except FileNotFoundError:
        displayText(windowSurface, 24, WWIDTH / 2, WHEIGHT - 100, 'No save file found', RED)
        return "Save Failed"

    if savedGames:
        numberSavedGames = len(savedGames)
        if numberSavedGames >= 9:
            mode = "Maxed"
    else:
        numberSavedGames = 0
        savedGames = []

    if mode == "Save":
        if gameSlot == None:
            savedGame.update({'name': "Game" + str(numberSavedGames + 1)})
            savedGames.append(dict(savedGame))
        else:
            savedGame.update({'name': "Game" + str(gameSlot + 1)})
            savedGames[gameSlot] = dict(savedGame)

    count = 1    
    for game in savedGames:
        savedGameStr = "Game" + str(count) + "," + str(game['record']) + "," + str(game['score']) + "," + str(game['wwidth']) + "," + str(game['wheight']) + "," + str(game['pwidth']) + "," + str(game['pheight']) + "," + str(game['radius']) + "," + str(game['pnumber']) + "," + game['difficulty'] + "," + str(game['coords']) + "\n"
        file.write(savedGameStr)
        count += 1
               
    file.close()

    if mode == "Save":
        return "Game Saved"   

    if mode == "Delete":
        return "Game Deleted"

    if mode == "Maxed":
        return "Save Failed: No more save slots free"

# Take game data and convert to dictionary format    
def convertGameForSave(bestTime, score, WWIDTH, WHEIGHT, PWIDTH, PHEIGHT, RADIUS, PNUMBER, DIFFICULTY, rects):

    # Convert rects co-ordinates into co-ordinate string for save
    coordsStr = ""
    for rect in rects:
        coordsStr = coordsStr + str(rect['rect'].x) + ":" + str(rect['rect'].y) + "-"
    coordsStr = coordsStr[:-1]

    savedGameDict = {'record': bestTime, 'score': score, 'wwidth': WWIDTH, 'wheight': WHEIGHT, 'pwidth': PWIDTH, 'pheight': PHEIGHT, 'radius': RADIUS, 'pnumber': PNUMBER, 'difficulty': DIFFICULTY, 'coords': coordsStr}

    return savedGameDict

# Perform basic window setup
def windowSetup(WWIDTH, WHEIGHT, BACKGROUND):
    
    windowSurface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)
    pygame.display.set_caption('MegaJump')
    background_position = [0, 0]
    background_image = pygame.image.load(BACKGROUND).convert()
    background_image = pygame.transform.scale(background_image, (WWIDTH, WHEIGHT))

    return windowSurface, background_position, background_image


######### Game Screen Functions ##########

def titleScreen(windowSurface, WWIDTH):
    
    displayText(windowSurface, 128, WWIDTH / 2, 125, 'MEGA', RED)
    displayText(windowSurface, 128, WWIDTH / 2, 275, 'JUMP!', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 450, '1 = NEW GAME', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 500, '2 = SAVED GAMES', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 550, '3 = INSTRUCTIONS', GREEN)
    
def instructionScreen(windowSurface, WWIDTH, FRAMES, background_image, background_position):

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.blit(background_image, background_position)
        
        displayText(windowSurface, 128, WWIDTH / 2, 125, 'MEGA', RED)
        displayText(windowSurface, 128, WWIDTH / 2, 275, 'JUMP!', GREEN)
        displayText(windowSurface, 20, WWIDTH / 2, 400, 'Space to jump (+ down arrow for small jump, M for MegaJump)', GREEN)
        displayText(windowSurface, 20, WWIDTH / 2, 450, 'Left & Right arrows to move (+ up arrow to move faster)', GREEN)
        displayText(windowSurface, 20, WWIDTH / 2, 500, 'Q to quit, R to reset', GREEN)
        displayText(windowSurface, 20, WWIDTH / 2, 550, 'Only 1 MegaJump per game!', RED)
        displayText(windowSurface, 20, WWIDTH / 2, 600, 'Press ESC to return to main screen', GREEN)

        pygame.draw.circle(windowSurface, GOLD, (510, 550), 10, 0)

        if pygame.key.get_pressed()[K_ESCAPE]:
            return

        pygame.display.flip()

        clock.set_fps_limit(FRAMES)
        clock.tick()
        
def introScreen1(windowSurface, WWIDTH):

    displayText(windowSurface, 128, WWIDTH / 2, 125, 'MEGA', RED)
    displayText(windowSurface, 128, WWIDTH / 2, 275, 'JUMP!', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 400, 'Select Platform Size:', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 450, '1 = EASY', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 500, '2 = MEDIUM', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 550, '3 = HARD', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 620, '4 = INSANE (Only your score matters here!)', RED)

def introScreen2(windowSurface, WWIDTH):

    displayText(windowSurface, 128, WWIDTH / 2, 125, 'MEGA', RED)
    displayText(windowSurface, 128, WWIDTH / 2, 275, 'JUMP!', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 400, 'Select Game Size:', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 450, '1 = SMALL', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 500, '2 = MEDIUM', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 550, '3 = LARGE', GREEN)
    displayText(windowSurface, 24, WWIDTH / 2, 600, '4 = MEGA', RED)

def savedGameScreen(savedGames, windowSurface, WWIDTH, WHEIGHT, FRAMES, background_image, background_position):        

    time.sleep(0.3)
    
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.blit(background_image, background_position)
        displayTextLJ(windowSurface, 36, 50, 50, 'Saved Games List', RED)
        displayTextLJ(windowSurface, 24, 50, 100, "Name", RED)
        displayTextLJ(windowSurface, 24, 200, 100, "Difficulty", RED)
        displayTextLJ(windowSurface, 24, 350, 100, "Platforms", RED)
        displayTextLJ(windowSurface, 24, 500, 100, "Record", RED)
        
        displayTextLJ(windowSurface, 20, 50, 550, 'Press number to select game or D plus number to delete game', RED)
        displayTextLJ(windowSurface, 20, 50, 600, 'Escape to return to previous screen', RED)
        
        count = 1
        for game in savedGames:
            displayTextLJ(windowSurface, 20, 50, 100 + (count * 30), str(count) + ". " + game['name'], GREEN)
            displayTextLJ(windowSurface, 20, 200, 100 + (count * 30), game['difficulty'], GREEN)
            displayTextLJ(windowSurface, 20, 350, 100 + (count * 30), game['pnumber'], GREEN)
            if game['difficulty'] == "INSANE":
                displayTextLJ(windowSurface, 20, 500, 100 + (count * 30), "Score: " + game['score'], GREEN)
            else:
                displayTime(windowSurface, int(game['record']), 500, 100 + (count * 30), GREEN, 20, "True")
            count += 1

        if not pygame.key.get_pressed()[ord('d')]:
            for i in range(len(savedGames)):
                if pygame.key.get_pressed()[ord(str(i+1))]:
                    return savedGames[i], i

        if pygame.key.get_pressed()[ord('d')]:
            for i in range(len(savedGames)):
                if pygame.key.get_pressed()[ord(str(i+1))]:
                     del savedGames[i]
                     saveGames(windowSurface, WWIDTH, WHEIGHT, None, savedGames, None, "Delete")
                     time.sleep(0.5)
                     break
                       
        if pygame.key.get_pressed()[K_ESCAPE]:
            return None, None

        pygame.display.flip()

        clock.set_fps_limit(FRAMES)
        clock.tick()
       
