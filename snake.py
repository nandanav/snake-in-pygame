import pygame
from random import randrange
from pathlib import Path

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 155, 0)
BLUE = (0, 0, 255)
PURPLE = (138, 43, 226)

displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight), pygame.RESIZABLE)
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
blockSize = 10
FPS = 30
font = pygame.font.SysFont(None, 25)


def snake(blockSize, snakeList):
    for XnY in snakeList:
        pygame.draw.rect(gameDisplay, PURPLE, [XnY[0], XnY[1], blockSize, blockSize])


def messageToScreen(msg, color, x, y):
    screenText = font.render(msg, True, color)
    gameDisplay.blit(screenText, [x, y])



def gameLoop():
    gameExit = False
    gameOver = False
    gameSave = False
    gameStart = True
    leadX = displayHeight/2
    leadY = displayWidth/2
    leadXChange = 0
    leadYChange = 0
    randAppleX = round(randrange(0, displayWidth-blockSize)/10.0)*10.0
    randAppleY = round(randrange(0, displayHeight-blockSize)/10.0)*10.0
    snakeList = []
    snakeLength = 1
    score = 0
    name = []

    while not gameExit:
        while gameStart:
            gameDisplay.fill(WHITE)
            try:
                with open(str(Path.home()) + '/Documents/slither_save.txt') as f:
                    temporaryMovement = 300
                    for line in f:
                        messageToScreen(line, GREEN, displayWidth/2, temporaryMovement)
                        temporaryMovement += 20
                        pygame.display.update()
            except FileNotFoundError:
                with open(str(Path.home()) + '/Documents/slither_save.txt', 'a') as f:
                    continue
            messageToScreen("Press 'P' to play the game", BLACK, 200, 200)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gameStart = False
                        break
                        gameLoop()
                elif event.type == pygame.QUIT:
                    gameExit = True
                    gameStart = False
        while gameOver:
            gameDisplay.fill(WHITE)
            messageToScreen("Game Over !!, press P to play again or S to save your progress or Q to quit.", RED, 100, 300)
            messageToScreen("Your score was: {0}".format(score), RED, 100, 320)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_p:
                        gameStart = False
                        gameLoop()
                    elif event.key == pygame.K_s:
                        gameOver = False
                        gameSave = True
                        break
                elif event.type == pygame.QUIT:
                    gameExit = True
        while gameSave:
            gameDisplay.fill(WHITE)
            messageToScreen("Start typing your name and it will appear. Press Enter to submit.", PURPLE, 200, 100)
            messageToScreen("This will create a file in the Documents folder called: slither_save.txt", PURPLE, 200, 120)
            messageToScreen(''.join(name), BLACK, displayWidth/2, displayHeight/2)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        with open(str(Path.home()) + "/Documents/slither_save.txt", 'a') as f:
                            f.write(''.join(name) + " - " + str(score) + " \n")
                        gameSave = False
                        gameLoop()
                elif event.type == pygame.QUIT:
                    gameSave = False
                    gameExit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    leadXChange -= blockSize
                    leadYChange = 0
                elif event.key == pygame.K_RIGHT:
                    leadXChange += blockSize
                    leadYChange = 0
                elif event.key == pygame.K_UP:
                    leadYChange -= blockSize
                    leadXChange = 0
                elif event.key == pygame.K_DOWN:
                    leadYChange += blockSize
                    leadXChange = 0
        if leadX >= displayWidth or leadX <= 0 or leadY >= displayHeight or leadY <= 0:
            gameOver = True

        leadX += leadXChange
        leadY += leadYChange

        gameDisplay.fill(WHITE)
        pygame.draw.rect(gameDisplay, RED, [randAppleX, randAppleY, blockSize, blockSize])
        snakeHead = []
        snakeHead.append(leadX)
        snakeHead.append(leadY)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(blockSize, snakeList)
        pygame.display.update()

        if leadX == randAppleX and leadY == randAppleY:
            randAppleX = round(randrange(0, displayWidth-blockSize)/10.0)*10.0
            randAppleY = round(randrange(0, displayHeight-blockSize)/10.0)*10.0
            snakeLength += 1
            score += 1

        messageToScreen("Score: {0}".format(score), GREEN, 30, 30)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()


gameLoop()
