import pygame, socket, ipaddress, time, sys
from pygame.locals import *

# Constants
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (240, 240, 20)

font = 'arialbd.ttf'

SOCKET_TIMEOUT = 60

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
        displayTextLJ(windowSurface, 24, 50, 500, "Socket Error: " + str(err), RED)
        pygame.display.flip()
        time.sleep(3)
        return

def acceptClientConn(s, windowSurface):
    try:
        cs, addr = s.accept()     # Establish connection with client.
        return cs, addr
    except socket.error as err:
        if s:
            s.close()
        displayTextLJ(windowSurface, 24, 50, 500, "Socket Error: " + str(err), RED)
        pygame.display.flip()
        time.sleep(3)
        return None, None

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
                return ip
            except ValueError as err:
                displayTextLJ(windowSurface, 24, 50, 500, "Invalid IP Address", RED)
                pygame.display.flip()
                time.sleep(2)
                continue

        ip = ''.join(ipArray)

        windowSurface.blit(background_image, background_position)
        displayTextLJ(windowSurface, 24, 50, 50, "Enter IP Address of Host Server: ", GREEN)
        displayTextLJ(windowSurface, 24, 50, 100, ip, GREEN)
        pygame.display.flip()

def connectToServer(ip, serverPort, windowSurface):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        s.connect((ip, serverPort))
        return s
    except socket.error as err:
        if s:
            s.close()
        displayTextLJ(windowSurface, 24, 50, 500, "Socket Error: " + str(err), RED)
        pygame.display.flip()
        time.sleep(3)
        return

######## Network wrapper methods ##########

def setupServer(windowSurface, background_image, background_position):

    windowSurface.blit(background_image, background_position)

    listenerSocket = createServerSocket(windowSurface)

    if not listenerSocket:
        return

    displayTextLJ(windowSurface, 24, 50, 50, "Waiting for client connection...", GREEN)
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

    serverSocket = connectToServer(serverIP, serverPort, windowSurface)
    if serverSocket:
        return serverSocket
    else:
        return



