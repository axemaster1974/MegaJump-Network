import pygame, socket, ipaddress, time, sys
from pygame.locals import *

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (240, 240, 20)

font = 'arialbd.ttf'

SOCKET_TIMEOUT = 10

socket.setdefaulttimeout(SOCKET_TIMEOUT)
serverHost = socket.gethostname()
serverPort = 50107

######## Generic functions ##########

# display text left justified with x co-ordinate as left of text rectangle
def displayTextLJ(surface, fontSize, x, y, text, colour):

    fontObj = pygame.font.Font(font, fontSize)

    textObj = fontObj.render(text, 0, colour)
    textRect = textObj.get_rect()
    textRect.left = x
    textRect.centery = y

    surface.blit(textObj, textRect)

# Return key pressed
def get_key():
  while True:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

######## Network base methods ##########

def createServerSocket(windowSurface):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # Create a socket object
        s.bind((serverHost, serverPort))                            # Bind to the port
        s.listen(5)                                                 # Now listen for client connection.
        return s
    except socket.error as err:
        if s:
            s.close()
        displayTextLJ(windowSurface, 12, 50, 500, "Socket Error: " + str(err), RED)
        pygame.display.flip()
        time.sleep(3)
        return

def acceptClientConn(s, windowSurface): # Establish connection with client.

    cs = None

    # socket set to non blocking required so window doesn't hang and become unresponsive awaiting server
    # instruction. Instead a loop checks each iteration for network data from client, and try / except clause means if
    # no data received, game doesn't not crash with "non blocking socket received no data error". Instead loop continues
    # and event pump prevents window hanging

    s.setblocking(0)

    while not cs:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.event.pump()

        if pygame.key.get_pressed()[K_ESCAPE]:
            return '', ''

        try:
            cs, addr = s.accept()
        except socket.error as err:
            pass

    return cs, addr

def receiveData(s):
    data = s.recv(1024).decode('utf-8')
    return data

def sendData(s, data):
    s.send(bytes(data,'utf-8'))

def getServerHost(windowSurface, background_image, background_position):

    ipArray = []
    ip = ""

    windowSurface.blit(background_image, background_position)
    displayTextLJ(windowSurface, 24, 50, 50, "Enter IP Address of Host Server: ", GREEN)
    displayTextLJ(windowSurface, 20, 50, 600, 'Escape to return to previous screen', RED)
    pygame.display.flip()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        ikey = get_key()

        if ikey == K_BACKSPACE:
            ipArray = ipArray[0:-1]
        elif ikey == K_PERIOD:
            ipArray.append(".")
        elif ikey >= 48 and ikey <= 57:
            ipArray.append(chr(ikey))
        elif ikey == K_RETURN:
            try:
                ipaddress.ip_address(ip)
                displayTextLJ(windowSurface, 24, 50, 150, "Trying to connect to host... (waiting " + str(SOCKET_TIMEOUT) + " seconds)", GREEN)
                pygame.display.flip()
                return ip
            except ValueError as err:
                displayTextLJ(windowSurface, 24, 50, 500, "Invalid IP Address", RED)
                pygame.display.flip()
                time.sleep(2)
                continue

        if pygame.key.get_pressed()[K_ESCAPE]:
            return

        ip = ''.join(ipArray)

        windowSurface.blit(background_image, background_position)
        displayTextLJ(windowSurface, 24, 50, 50, "Enter IP Address of Host Server: ", GREEN)
        displayTextLJ(windowSurface, 20, 50, 600, 'Escape to return to previous screen', RED)
        displayTextLJ(windowSurface, 24, 50, 100, ip, GOLD)
        pygame.display.flip()

def connectToServer(ip, serverPort, windowSurface):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        s.connect((ip, serverPort))
        return s
    except socket.error as err:
        if s:
            s.close()
        displayTextLJ(windowSurface, 12, 50, 500, "Socket Error: " + str(err), RED)
        pygame.display.flip()
        time.sleep(3)
        return

######## Network wrapper methods ##########

def setupServer(windowSurface, background_image, background_position):

    windowSurface.blit(background_image, background_position)

    listenerSocket = createServerSocket(windowSurface)

    displayTextLJ(windowSurface, 24, 50, 50, "Waiting for client connection...", GREEN)
    displayTextLJ(windowSurface, 20, 50, 600, 'Escape to return to previous screen', RED)
    pygame.display.flip()

    clientSocket, clientAddress = acceptClientConn(listenerSocket, windowSurface)
    if clientSocket:
        displayTextLJ(windowSurface, 24, 50, 100, "Connection received from: " + str(clientAddress), GREEN)
        pygame.display.flip()
        time.sleep(3)
        return clientSocket
    else:
        return

def setupClient(windowSurface, background_image, background_position):

    serverIP = getServerHost(windowSurface, background_image, background_position)

    if not serverIP:
        return

    serverSocket = connectToServer(serverIP, serverPort, windowSurface)
    if serverSocket:
        return serverSocket
    else:
        return