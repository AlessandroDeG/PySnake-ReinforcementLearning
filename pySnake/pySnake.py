import pygame
import random
import os.path
import inspect
import threading
import time
import sys
pygame.init()
pygame.font.init()

##############################################################

class AskForInput(threading.Thread):
    # active = True
    yn = ""
    def run(self):
        #print("started")
        # while(AskForInput.active):
        AskForInput.yn=""
        AskForInput.yn = input()
        while(AskForInput.yn != "y" and AskForInput.yn != "n"):
            print("y = yes , n = no")
            AskForInput.yn = input()
        #print("closed")

############################################################

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

print(path)
print(filename)

print("\nCOMMANDS:")
print(" W,A,S,D or KEYPAD ARROWS to move")
print(" KEYPAD +,- or p,m to change speed\n")

FONTSIZE = 15
myfont = pygame.font.SysFont('Comic Sans MS', FONTSIZE)
gameoverfont = pygame.font.SysFont('Comic Sans MS', FONTSIZE * 2)
# pygame.font.Font.set_bold(True)

screenX = 600
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))

PLAYER_SIZE = 20
playerSizeX = PLAYER_SIZE
playerSizeY = PLAYER_SIZE
playerPosX = screenX // 2
playerPosY = screenY // 2
playerColor = pygame.Color(255, 0, 0)

PLAYER_SPEED = PLAYER_SIZE

playerDirectionX = 0
playerDirectionY = 0

resources =''
print("SYS= "+ sys.platform)
if(sys.platform =='Windows' or sys.platform =='windows'):
    resources = '\\pySnakeResources\\'
if(sys.platform =='Darwin' or sys.platform =='darwin' ):#mac
    resources='/pySnakeResources/'

player = pygame.transform.scale(
    pygame.image.load(path + resources+"pythonlogob.jpg"),
    (playerSizeX + playerSizeX // 4,
     playerSizeY + playerSizeY // 4))

bodyPart = pygame.transform.scale(
    pygame.image.load(path +  resources+"pythonlogobody.jpg"),
    (playerSizeX,
     playerSizeY))

mela = pygame.transform.scale(
    pygame.image.load(path +  resources+"mela.png"),
    (playerSizeX,
     playerSizeY))

gameover = False

MOVEINCREMENT = 50
MOVETIME_MAX = 500
MOVETIME_MIN = 0
MOVETIME = 500
timeToMove = 0
delay = 15

bodyList = []
bodyList.append((playerPosX, playerPosY + PLAYER_SIZE * 3))
bodyList.append((playerPosX, playerPosY + PLAYER_SIZE * 2))
bodyList.append((playerPosX, playerPosY + PLAYER_SIZE))

MAX_FOOD = 5
foodList = []
eat = False
playerMoved = True

score = 0
scoreText = myfont.render("Score : " + str(score), False, (255, 255, 255))
speedText = myfont.render(
    "Speed" + str((MOVETIME_MAX - MOVETIME) // MOVEINCREMENT), False, (255, 255, 255))
gameoverString = "GAMEOVER!"
gameoverText = gameoverfont.render(gameoverString, False, (255, 255, 255))

playAgain = True

while(playAgain):

    while(not gameover):
        screen.fill(0)

        scoreText = myfont.render(
            "Score : " + str(score), False, (255, 255, 255))
        speedText = myfont.render(
            "Speed : " + str((MOVETIME_MAX - MOVETIME) // MOVEINCREMENT), False, (255, 255, 255))

        if(len(foodList) < MAX_FOOD):
            foodList.append(
                (random.randint(0, (screenX // PLAYER_SIZE) - 1) * PLAYER_SIZE, random.randint(0, (screenX // PLAYER_SIZE) - 1) * PLAYER_SIZE))
            #print(foodList)
        for food in foodList:
            if(not(food == (playerPosX, playerPosY))):
                screen.blit(mela, food)
            else:
                foodList.remove(food)

        for body in bodyList:
            screen.blit(bodyPart, body)

        screen.blit(
            player,
            (playerPosX -
             playerSizeX //
             8,
             playerPosY -
             playerSizeY //
             8))

        screen.blit(scoreText, (0, 0))
        screen.blit(speedText, (0, FONTSIZE + 10))

        # refresh
        for event in pygame.event.get():
            # print(event)
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP or event.key == pygame.K_w):
                    if(playerDirectionY == 0 and playerMoved):
                        playerDirectionY = -PLAYER_SPEED
                        playerDirectionX = 0
                        playerMoved = False
                if(event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    if(playerDirectionY == 0 and playerMoved):
                        playerDirectionY = PLAYER_SPEED
                        playerDirectionX = 0
                        playerMoved = False
                if(event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    if(playerDirectionX == 0 and playerMoved):
                        playerDirectionX = -PLAYER_SPEED
                        playerDirectionY = 0
                        playerMoved = False
                if(event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    if(playerDirectionX == 0 and playerMoved):
                        playerDirectionX = PLAYER_SPEED
                        playerDirectionY = 0
                        playerMoved = False

                if(event.key == pygame.K_KP_PLUS or event.key == pygame.K_p):
                    if(MOVETIME > MOVETIME_MIN):
                        MOVETIME -= MOVEINCREMENT
                if(event.key == pygame.K_KP_MINUS or event.key == pygame.K_m):
                    if(MOVETIME < MOVETIME_MAX):
                        MOVETIME += MOVEINCREMENT

            if(event.type == pygame.QUIT):
                blablamerda.pitononculo = esci  # lol

        if(playerDirectionX < -69):
            merdablablablab = stringintnonsenseblablapitonculo

        if(playerDirectionX != 0 or playerDirectionY != 0):
            if(timeToMove >= MOVETIME):
                bodyList.append((playerPosX, playerPosY))
                if(not eat):
                    bodyList.pop(0)
                else:
                    eat = False
                playerPosX += playerDirectionX
                playerPosY += playerDirectionY
                playerMoved = True
                timeToMove = 0
                for body in bodyList:
                    if(body == (playerPosX, playerPosY)):
                        gameover = True
                        break
                for food in foodList:
                    if(food == (playerPosX, playerPosY)):
                        eat = True
                        score += 1
                        foodList.remove(food)
                        break

            if(playerPosX < 0):
                playerPosX = screenX - PLAYER_SIZE
            if(playerPosY < 0):
                playerPosY = screenY - PLAYER_SIZE
            if(playerPosX >= screenX):
                playerPosX = 0
            if(playerPosY >= screenY):
                playerPosY = 0

        if(gameover):
            screen.blit(gameoverText, (screenX //
                                       2 -
                                       (gameoverfont.size(gameoverString))[0] //
                                       2, screenY //
                                       2 -
                                       (gameoverfont.size("GAMEOVER!"))[1] //
                                       2))

        pygame.display.flip()
        # pygame.display.update()
        pygame.time.delay(delay)
        timeToMove += delay

    print("\n****GAMEOVER****\n")

    # highScoreFile=open(path+"\\highscore.txt","+")
    try:
        highScoreFileReader = open(path + resources+ "highscore.txt", "r+")
        shighscore = highScoreFileReader.read().strip().replace(
            "\n", "").replace(
            "\t", "").replace(
            "\r", "")
        highScoreFileReader.close()
        highscore = int(shighscore)
    except BaseException:
        highScoreFileWriter = open(path + resources+ "highscore.txt", "w+")
        highscore = 0
        highScoreFileWriter.write("0")
        highScoreFileWriter.close()

    if(score > highscore):
        highScoreFileWriter = open(path + resources+ "highscore.txt", "w")
        highScoreFileWriter.write(str(score))
        highScoreFileWriter.close()
        print("NEW HIGH-SCORE!  : " + str(score))

    print("Play again? y/n")
    askforinput = AskForInput()
    askforinput.daemon=True
    askforinput.start()
    yn = askforinput.yn
    while(yn != "y" and yn != "n"):  ##waiting for input and prevent stupid pygame event to crash
        yn = askforinput.yn
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                pitononculo = pitonculooexit  # lol
                   
    if(yn == "n"):
        playAgain = False
    else:
        score = 0
        playerPosX = screenX // 2
        playerPosY = screenY // 2
        playerDirectionX = 0
        playerDirectionY = 0
        timeToMove = 0
        bodyList = []
        bodyList.append((playerPosX, playerPosY + PLAYER_SIZE * 3))
        bodyList.append((playerPosX, playerPosY + PLAYER_SIZE * 2))
        bodyList.append((playerPosX, playerPosY + PLAYER_SIZE))
        foodList = []
        eat = False
        playerMoved = True
        gameover = False
        print("NEW GAME STARTED ...")
