########## MEGAJUMP! #############

import pygame, sys, time, random
from pygame.locals import *
from pyglet import clock
from gameFunc import *
from networking import *

# set up pygame
pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (240, 240, 20)

EWWIDTH = 700                   # Easy Window width
EWHEIGHT = 650                  # Easy Window height
MWWIDTH = 1000                  # Medium Window width
MWHEIGHT = 650                  # Medium Window width
HWWIDTH = 1300                  # Hard Window width
HWHEIGHT = 650                  # Hard window height
EPWIDTH = 80                    # Easy platform width
MPWIDTH = 60                    # Medium platform width
HPWIDTH = 40                    # Hard platform width
IPWIDTH = 20                    # Insane platforn width
EPNUMBER = 10                   # Easy platform number
MPNUMBER = 15                   # Medium platform number
HPNUMBER = 20                   # Hard platform number
GPNUMBER = 50                   # Mega platform number
IPNUMBER = 100                  # Insane platform number
SPHEIGHT = 20                   # Standard platform height
IPHEIGHT = 10                   # Insane platform height2
SRADIUS = 16                    # Standard ball radius
IRADIUS = 8                     # Insane ball radius
ACC = 1200                      # y axis downward acceleration rate (to mimic gravity)
FRAMES = 60                     # Frame rate
RATE = 1 / FRAMES               # Time for each frame, hence loop iteration
FASTMOVE = 4                    # Fast x-axis movement
SLOWMOVE = 2                    # Slow x-axis movement
MEGAJUMPVEL = 1200              # y axis upward velocity on MEGA jump
HIGHJUMPVEL = 800               # y axis upward velocity on high jump
LOWJUMPVEL = 600                # y axis upward velocity on low jump
BALLCOLOUR = RED
SCOREPLAT = 1                   # Score for landing on platform
BACKGROUND = "background1.jpg"  # Background Image
iball = {'x': 50, 'y': 50, 'dir': "RIGHT", 'vel': 50} # Introduction ball data structure
role = "solo"                   # Initial game role
insane = "False"

# Ensure loadedGame and savedGames defined even if Saved Games option not selected:
loadedGame = {} # Empty dictionary
savedGames = [] # Empty array
savedMessage = ""

#Sounds
WIN = "Win.ogg"
LAND = "Land.ogg"
FAIL = "Ground.ogg"
JUMP = "Jump1.ogg"
MEGAJUMP = "MegaJump.ogg"
BGMUSIC = "Two Finger Johnny.ogg"
INSANEWIN = "Tada.ogg"
LOSE = "Lose1.ogg"

# set up music
pygame.mixer.music.load(BGMUSIC)
pygame.mixer.music.set_volume(0.3)
failSound = pygame.mixer.Sound(FAIL)
landSound = pygame.mixer.Sound(LAND)
winSound = pygame.mixer.Sound(WIN)
jumpSound = pygame.mixer.Sound(JUMP)
megaSound = pygame.mixer.Sound(MEGAJUMP)
insaneWinSound = pygame.mixer.Sound(INSANEWIN)
loseSound = pygame.mixer.Sound(LOSE)

# Main Loop
while True:

    WWIDTH = 700                   # Default Window Width (can be modified by user selected options)
    WHEIGHT = 650                  # Default Window Height (can be modified by user selected options)
    
    # set up the initial window
    (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)

    # Play music
    pygame.mixer.music.play(-1, 0.0)
    
    ################## Start Screen #######################

    while True:

        if role == "client":
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.blit(background_image, background_position)
        titleScreen(windowSurface, WWIDTH, role)

        # Intro ball
        
        if iball['dir'] == "RIGHT":
            iball['x'] += 3
        else:
            iball['x'] -= 3

        if iball['x'] > (WWIDTH - SRADIUS):
            iball['dir'] = "LEFT"

        if iball['x'] < SRADIUS:
            iball['dir'] = "RIGHT"
        
        iball['vel'] += ACC * RATE
        iball['y'] += int((iball['vel'] * RATE))

        if iball['y'] > (WHEIGHT - SRADIUS):
            iball['vel'] = -MEGAJUMPVEL

        pygame.draw.circle(windowSurface, GOLD, (iball['x'], iball['y']), SRADIUS, 0)

        # Option selection
        
        if pygame.key.get_pressed()[ord('1')]:
            loadedGame = False
            gameSlot = None
            break
        if pygame.key.get_pressed()[ord('2')]:
            savedGames = loadGames(windowSurface, WWIDTH)
            if savedGames:
                (loadedGame, gameSlot) = savedGameScreen(savedGames, windowSurface, WWIDTH, WHEIGHT, FRAMES, background_image, background_position)
                if loadedGame:
                    break
        if pygame.key.get_pressed()[ord('3')]:
            (role, socket) = networkScreen1(windowSurface, WWIDTH, FRAMES, background_image, background_position, role)
            if role == "solo":
                if socket:
                    socket.close()
        if pygame.key.get_pressed()[ord('4')]:
            instructionScreen(windowSurface, WWIDTH, FRAMES, background_image, background_position)

        # Background change options
        if pygame.key.get_pressed()[pygame.K_F1]:
            BACKGROUND = "background1.jpg"
            (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)
            continue
        if pygame.key.get_pressed()[pygame.K_F2]:
            BACKGROUND = "background2.jpg"
            (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)
            continue
        if pygame.key.get_pressed()[pygame.K_F3]:
            BACKGROUND = "background3.jpg"
            (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)
            continue
        if pygame.key.get_pressed()[pygame.K_F4]:
            BACKGROUND = "background4.jpg"
            (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)
            continue

        if role == "client":
            break

        if savedMessage:
            displayText(windowSurface, 24, WWIDTH / 2, 400, savedMessage, RED)

        pygame.display.flip()

        clock.set_fps_limit(FRAMES)
        clock.tick()
           
    time.sleep(0.3)
    
    ################## Intro Screen 1 #####################
    
    while True:
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if loadedGame:
            break

        if role == "client":
            break
        
        windowSurface.blit(background_image, background_position)
        introScreen1(windowSurface, WWIDTH, role)
        
        insane = False
        
        if pygame.key.get_pressed()[ord('1')]:
            DIFFICULTY = 'EASY'
            PWIDTH = EPWIDTH
            PHEIGHT = SPHEIGHT
            RADIUS = SRADIUS
            break
        if pygame.key.get_pressed()[ord('2')]:
            DIFFICULTY = 'MEDIUM'
            PWIDTH = MPWIDTH
            PHEIGHT = SPHEIGHT
            RADIUS = SRADIUS
            break
        if pygame.key.get_pressed()[ord('3')]:
            DIFFICULTY = 'HARD'
            PWIDTH = HPWIDTH
            PHEIGHT = SPHEIGHT
            RADIUS = SRADIUS
            break
        if pygame.key.get_pressed()[ord('4')]:
            DIFFICULTY = 'INSANE'
            PWIDTH = IPWIDTH
            PHEIGHT = IPHEIGHT
            RADIUS = IRADIUS
            PNUMBER = IPNUMBER
            WWIDTH = HWWIDTH
            WHEIGHT = HWHEIGHT
            insane = True
            break
        
        pygame.display.flip()

        clock.set_fps_limit(FRAMES)
        clock.tick()

    time.sleep(0.3)
    
    ################## Intro Screen 2 #####################

    while True:

        if loadedGame:
            break
        
        if insane:
            break

        if role == "client":
            break
                            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        windowSurface.blit(background_image, background_position)
        introScreen2(windowSurface, WWIDTH, role)
                
        if pygame.key.get_pressed()[ord('1')]:
            PNUMBER = EPNUMBER
            WWIDTH = EWWIDTH
            WHEIGHT = EWHEIGHT
            break
        if pygame.key.get_pressed()[ord('2')]:
            PNUMBER = MPNUMBER
            WWIDTH = MWWIDTH
            WHEIGHT = MWHEIGHT
            break
        if pygame.key.get_pressed()[ord('3')]:
            PNUMBER = HPNUMBER
            WWIDTH = HWWIDTH
            WHEIGHT = HWHEIGHT
            break
        if pygame.key.get_pressed()[ord('4')]:
            PNUMBER = GPNUMBER
            WWIDTH = HWWIDTH
            WHEIGHT = HWHEIGHT
            break
                        
        pygame.display.flip()

        clock.set_fps_limit(FRAMES)
        clock.tick()

    time.sleep(0.3)

    ################# Client Wait Screen ###########################

    if role == "client":
        role = clientScreen(socket, windowSurface, WWIDTH, FRAMES, background_image, background_position)
        if role == "solo":
            socket.close()
            continue
    if role == "server":
        sendData(socket, "Starting")
        while receiveData(socket) != "Received":
            continue

    ################## Pre-Game Initialization #####################

    bestTime = 0
    rects = []
    won = True  # Set to true intially so game variables are initialized on first run

    # Populate game variables from loaded game
    if loadedGame:
        bestTime = int(loadedGame['record'])
        WWIDTH = int(loadedGame['wwidth'])
        WHEIGHT = int(loadedGame['wheight'])
        PWIDTH = int(loadedGame['pwidth'])
        PHEIGHT = int(loadedGame['pheight'])
        RADIUS = int(loadedGame['radius'])
        PNUMBER = int(loadedGame['pnumber'])
        DIFFICULTY = loadedGame['difficulty']
        COORDS = loadedGame['coords']
        coordsList = COORDS.split('-')
        for n in range(PNUMBER):
            rects.append({'rect': pygame.Rect(int(coordsList[n-1].split(':')[0]), int(coordsList[n-1].split(':')[1]), PWIDTH, PHEIGHT), 'visited': False, 'colour': BLUE})

    # Create platform data structures if new game
    if not role == "client":
        if not loadedGame:
            for n in range(PNUMBER):
                rects.append({'rect': pygame.Rect(random.randint(0, (WWIDTH - PWIDTH)), random.randint(0, (WHEIGHT - PHEIGHT)), PWIDTH, PHEIGHT), 'visited': False, 'colour': BLUE})

    ##### Level data exchange if network play ######

    # Send level data to client if server
    if role == "server":
        game = convertGameForSave(bestTime, "0", WWIDTH, WHEIGHT, PWIDTH, PHEIGHT, RADIUS, PNUMBER, DIFFICULTY, rects)
        clientGameStr = str(game['record']) + "," + str(game['score']) + "," + str(game['wwidth']) + "," + str(game['wheight']) + "," + str(game['pwidth']) + "," + str(game['pheight']) + "," + str(game['radius']) + "," + str(game['pnumber']) + "," + game['difficulty'] + "," + str(game['coords'])
        sendData(socket, clientGameStr)

    # Receive level data from server if client
    if role == "client":
        loadedGameStr = receiveData(socket)
        (record, score, wwidth, wheight, pwidth, pheight, radius, pnumber, difficulty, coords) = loadedGameStr.split(',')
        loadedGame = {'record': record, 'score': score, 'wwidth': wwidth, 'wheight': wheight, 'pwidth': pwidth,
                      'pheight': pheight, 'radius': radius, 'pnumber': pnumber, 'difficulty': difficulty,
                      'coords': coords}

        bestTime = int(loadedGame['record'])
        WWIDTH = int(loadedGame['wwidth'])
        WHEIGHT = int(loadedGame['wheight'])
        PWIDTH = int(loadedGame['pwidth'])
        PHEIGHT = int(loadedGame['pheight'])
        RADIUS = int(loadedGame['radius'])
        PNUMBER = int(loadedGame['pnumber'])
        DIFFICULTY = loadedGame['difficulty']
        COORDS = loadedGame['coords']
        coordsList = COORDS.split('-')
        rects = []                          # Empty rects array before client creates rects array from server data
        for n in range(PNUMBER):
            rects.append({'rect': pygame.Rect(int(coordsList[n - 1].split(':')[0]),
                                              int(coordsList[n - 1].split(':')[1]), PWIDTH, PHEIGHT), 'visited': False,
                          'colour': BLUE})

    # set up the window again depending on selected options
    (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)

    # Calculate y coordinate where ball should stop so rests on ground
    GROUND = WHEIGHT - RADIUS

    pygame.mixer.music.stop()

    #Verify remote server ready and ensure data exchange is synced before proceeding
    if role != "solo":
        if role == "server":
            sendData(socket, "READY")
            while receiveData(socket) != "READY":
                continue

        if role == "client":
            while receiveData(socket) != "READY":
                continue
            sendData(socket, "READY")


    ################### Main Game Loop #####################
    
    while True:
        
        # Define / Reset game variables
        if won:
            finish = False                  # Has player quit?
            score = 0                       # No. of platforms landed on
            bestScore = 0                   # Best score so far (only for Insane Mode)
            megaused = False                # Has MEGA jump been used?
            onsurface = True                # Is ball resting on surface?
            previous_onsurface = onsurface  # Variable for previous surface state to determine if landed
            landed = False                  # Has ball changed state from in the air to landed?
            moveLeft = False                # Should ball move left?
            moveRight = False               # Should ball move right?
            won = False                     # Winning Flag
            count = 0                       # Loop iterations
            timeElapsed = 0                 # Time in seconds
            startTime = int(time.time() * 1000) # Game start time
            restart = True                  # Game restarted? Display countdown
            record = False                  # Has a record time been set for this run?
            savedMessage = ""               # Reset message advising if last save was successful
            status = "playing"              # Game status for network play

            # If loaded game, define insane accordingly and set bestScore to loaded game best score
            if loadedGame:
                if loadedGame['difficulty'] == "INSANE":
                    insane = True
                    bestScore = int(loadedGame['score'])
                else:
                    insane = False

            # Ball data structure
            ball = {'x': int(WWIDTH / 2), 'y': int(GROUND), 'xvel': 0, 'yvel': 0}
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT and onsurface:
                    moveLeft = True
                    moveRight = False
                if event.key == K_RIGHT and onsurface:
                    moveRight = True
                    moveLeft = False
                if event.key == K_SPACE and pygame.key.get_pressed()[pygame.K_DOWN]:
                    if onsurface:
                        ball['yvel'] = -LOWJUMPVEL
                        jumpSound.play()
                        landed = False
                if event.key == K_SPACE and not pygame.key.get_pressed()[pygame.K_DOWN]:
                    if onsurface:
                        ball['yvel'] = -HIGHJUMPVEL
                        jumpSound.play()
                        landed = False
                if event.key == K_SPACE and pygame.key.get_pressed()[ord('m')] and not megaused:
                    if onsurface:
                        ball['yvel'] = -MEGAJUMPVEL
                        megaSound.play()
                        megaused = True
                        BALLCOLOUR = GOLD
                        landed = False
                                
            if event.type == KEYUP:
                if event.key == K_LEFT and onsurface:
                    moveLeft = False
                if event.key == K_RIGHT and onsurface:
                    moveRight = False
        
        # Stop ball moving if it lands and no keys pressed. other wise keep moving
        if landed:
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                moveLeft = True
                moveRight = False
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                moveLeft = False
                moveRight = True
            else:
                moveLeft = False
                moveRight = False
                landed = False

        # Game exit/reset options
        if pygame.key.get_pressed()[ord('q')] and role != "client":
            if insane:
                displayText(windowSurface, 32, WWIDTH / 2, WHEIGHT / 2, 'Do you wish to save level? (y/n)', GREEN)
                pygame.display.flip()
                
                while True:
                    
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                
                    if pygame.key.get_pressed()[ord('y')]:
                        savedGame = convertGameForSave(bestTime, bestScore, WWIDTH, WHEIGHT, PWIDTH, PHEIGHT, RADIUS, PNUMBER, DIFFICULTY, rects)
                        if not savedGames:
                            savedGames = loadGames(windowSurface, WWIDTH)
                        savedMessage = saveGames(windowSurface, WWIDTH, WHEIGHT, savedGame, savedGames, gameSlot, "Save")        
                        break
                    if pygame.key.get_pressed()[ord('n')]:
                        break
                                                   
                clock.set_fps_limit(FRAMES)  
                clock.tick()

            status = "quit"
            finish = True

        if role == "solo":
            if pygame.key.get_pressed()[ord('r')]:
                count = 0
                score = 0
                restart = True
                ball = {'x': int(WWIDTH / 2), 'y': int(GROUND), 'xvel': 0, 'yvel': 0}
                for rect in rects:
                    rect['visited'] = False
                    rect['colour'] = BLUE
                
        # Determine move speed
        if pygame.key.get_pressed()[pygame.K_UP]:
            MOVESPEED = FASTMOVE
        else:
            MOVESPEED = SLOWMOVE
           
        # Move ball along x-axis and stop ball going off edge of screen
        if moveLeft and ball['x'] > RADIUS:
            ball['x'] -= MOVESPEED
        if moveRight and ball['x'] < WWIDTH - RADIUS:
            ball['x'] += MOVESPEED

        # Apply gravity to y-axis
        ball['yvel'] += (ACC * RATE)
        ball['y'] += int((ball['yvel'] * RATE))

        # Ensure ball doesn't go below window and record if on ground
        if ball['y'] > GROUND:
            ball['y'] = GROUND
        
        # Check if ball landed on platform
        for rect in rects:
            if (ball['x'] > rect['rect'].left and ball['x'] < rect['rect'].right):
                if ((ball['y'] + RADIUS) >= rect['rect'].top and (ball['y'] + RADIUS) <= rect['rect'].bottom and ball['yvel'] > 0):
                    onsurface = True
                    ball ['y'] = rect['rect'].top - RADIUS
                    ball ['yvel'] = 0
                    if rect['visited'] == False:
                        rect['visited'] = True
                        rect['colour'] = RED
                        landSound.play()
                        score += SCOREPLAT
                    break
                else:
                    onsurface = False
            else:
                onsurface = False

        # Is ball on the ground? If so, reset score and platform colours
        if ball['y'] == GROUND:
            onsurface = True
            if score > bestScore:
                bestScore = score
            score = 0
            for rect in rects:
                rect['visited'] = False
                rect['colour'] = BLUE
    
        # Detect if ball has changed state from being in the air to now being on the ground
        if previous_onsurface == False and onsurface == True:
            landed = True
            if ball['y'] == GROUND:
                failSound.play()
            
        previous_onsurface = onsurface

        # Change ball colour back to normal once ball landed after a MegaJump 
        if BALLCOLOUR == GOLD and onsurface:
            BALLCOLOUR = RED

        # Exchange and parse runtime player data if network play
        if role != "solo":
            sendData(socket, str(ball['x']) + ',' + str(ball['y']) + ',' + str(score) + ',' + status)
            otherPlayerData = receiveData(socket)

            otherPlayerX = int(otherPlayerData.split(',')[0])
            otherPlayerY = int(otherPlayerData.split(',')[1])
            otherPlayerScore = int(otherPlayerData.split(',')[2])
            otherPlayerStatus = otherPlayerData.split(',')[3]

        # Draw window
        windowSurface.blit(background_image, background_position)
        if role != "solo":
            pygame.draw.circle(windowSurface, GREEN, (otherPlayerX, otherPlayerY), RADIUS, 0)
            displayText(windowSurface, 16, WWIDTH - 75, 25, 'Network Mode', GOLD)
        pygame.draw.circle(windowSurface, BALLCOLOUR, (ball['x'], ball['y']), RADIUS, 0)

        for rect in rects:
            pygame.draw.rect(windowSurface, rect['colour'], rect['rect'])
        if role == "solo":
            displayText(windowSurface, 30, WWIDTH - 120, 50, 'Score: ' + str(score), GREEN)
        else:
            displayText(windowSurface, 24, WWIDTH - 120, 50, 'Player 1 Score: ' + str(score), GREEN)
            displayText(windowSurface, 24, WWIDTH - 120, 90, 'Player 2 Score: ' + str(otherPlayerScore), GREEN)

        if not insane:
            displayText(windowSurface, 30, 90, 50, 'Time: ', GREEN)
            displayTime(windowSurface, timeElapsed, 220, 50, GREEN, 30, None)
        if insane:
            displayTextLJ(windowSurface, 30, 50, 50, 'Best Score: ' + str(bestScore), GOLD)
        timeElapsedSaved = timeElapsed
        if not megaused:
                pygame.draw.circle(windowSurface, GOLD, (20, 20), 10, 0)
        if restart:
            countdown(windowSurface, WWIDTH, WHEIGHT)
            restart = False
            megaused = False
            timeElapsed = 0                 
            startTime = int(time.time() * 1000)

        if score == PNUMBER * SCOREPLAT:
            won = True
            if insane:
                displayText(windowSurface, 32, WWIDTH / 2, (WHEIGHT / 2), 'MegaJump Champion!!!', GOLD)
                insaneWinSound.play()
            else:
                if role == "solo":
                    displayText(windowSurface, 32, WWIDTH / 2, (WHEIGHT / 2), 'You Finished!', GREEN)
                else:
                    displayText(windowSurface, 32, WWIDTH / 2, (WHEIGHT / 2), 'You Won!', GREEN)
                winSound.play()

        if role != "solo":
            if otherPlayerScore == PNUMBER * SCOREPLAT:
                won = True
                displayText(windowSurface, 32, WWIDTH / 2, (WHEIGHT / 2), 'You got beat!', GREEN)
                loseSound.play()
                                        
        pygame.display.flip()

        timeElapsed = int(time.time() * 1000) - startTime
    
        clock.set_fps_limit(FRAMES)
        clock.tick()
        
        # Win rountine for single player
        
        if won and role == "solo":
            if bestTime == 0 or timeElapsedSaved < bestTime:
                bestTime = timeElapsedSaved
                record = True

            # Convert game data into format for save file
            savedGame = convertGameForSave(bestTime, score, WWIDTH, WHEIGHT, PWIDTH, PHEIGHT, RADIUS, PNUMBER, DIFFICULTY, rects)
            
            time.sleep(1)   

            if record:
                displayText(windowSurface, 32, (WWIDTH / 2) - 90, (WHEIGHT / 2) + 50, 'Record Set : ', GOLD)
                displayTime(windowSurface, bestTime, (WWIDTH / 2) + 105, (WHEIGHT / 2) + 50, GOLD, 30, None)
            else:
                displayText(windowSurface, 32, (WWIDTH / 2) - 85, (WHEIGHT / 2) + 50, 'Current Record: ', GREEN)
                displayTime(windowSurface, bestTime, (WWIDTH / 2) + 125, (WHEIGHT / 2) + 50, GREEN, 30, None)
            
            displayText(windowSurface, 32, WWIDTH / 2, (WHEIGHT / 2) + 100, 'Play Level Again or Save? (y/n/s)', GREEN)

            pygame.display.flip()

            # Sub loop to get user response to "Play Level Again?"
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                
                if pygame.key.get_pressed()[ord('y')]:
                    again = True
                    break
                if pygame.key.get_pressed()[ord('n')]:
                    again = False
                    break
                if pygame.key.get_pressed()[ord('s')]:
                    (WWIDTH, WHEIGHT) = (EWWIDTH, EWHEIGHT)
                    (windowSurface, background_position, background_image) = windowSetup(WWIDTH, WHEIGHT, BACKGROUND)
                    if not savedGames:
                        savedGames = loadGames(windowSurface, WWIDTH)
                    savedMessage = saveGames(windowSurface, WWIDTH, WHEIGHT, savedGame, savedGames, gameSlot, "Save")
                    again = False
                    break
                                   
                clock.set_fps_limit(FRAMES)  
                clock.tick()
                
            if again:
                continue
            else:
                break

        if won and role != "solo":

            time.sleep(1)

            if role == "server":
                displayText(windowSurface, 32, WWIDTH / 2, (WHEIGHT / 2) + 100, 'Play Level Again? (y/n)',
                            GREEN)

                pygame.display.flip()

                # Sub loop to get user response to "Play Level Again?"
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                    if pygame.key.get_pressed()[ord('y')]:
                        sendData(socket, "Restart")
                        again = True
                        break
                    if pygame.key.get_pressed()[ord('n')]:
                        sendData(socket, "NewGame")
                        again = False
                        break

                    clock.set_fps_limit(FRAMES)
                    clock.tick()

            if role == "client":
                serverChoice = receiveData(socket)
                if serverChoice == "Restart":
                    again = True
                else:
                    again = False

            if again:
                continue
            else:
                break

        # If player quits mid game

        if finish:
            break

        if role == "client":
            if otherPlayerStatus == "quit":
                break


