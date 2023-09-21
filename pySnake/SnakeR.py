
import pygame
import random
import os.path
import inspect
import threading
import time
import sys

##RL
import numpy as np
np.set_printoptions(linewidth=np.inf)

pygame.init()
pygame.font.init()

##############################################################
#Arrow Keys or press R for auto
###############################################################

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

######RL


class Rl:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    currentState=0

    gamma = 0.8 #discount factor
    foodReward = +10
    bodyReward = -100
    aliveReward = +1
    maxIter=100
    #gamma=1
    def __init__(self,side,food,body): 
        #print("GRID SIZE = "+str(side))
        self.terminals_food=food
        self.terminals_body=body
        self.side=side
        self.states = np.arange(side*side)
        self.stateValues = np.zeros(side*side) #stateValuefunction
        self.actions = np.array([self.UP, self.DOWN, self.LEFT, self.RIGHT])
        self.policy = np.array([np.random.choice(self.actions) for s in self.states]) ##random initial policy

        self.upSide=range(0,side)
        self.downSide=range((side*side)-side,side*side)
        self.rightSide=range(side-1,side*side,side)
        self.leftSide= range(0,side*side,side)

        self.actions_repr = np.array(['↑', '↓', '←', '→'])

        niters=self.train()
        print(f"ITERATIONS={niters}")

    ##get action from optimal policy
    def getAction(self,s):        
        self.print_debug(s)
        return self.policy[s]

    def print_debug(self,currentState):
        count=0
        print("CURRENT STATE =" + str(currentState))
        
        ##states
        #for i in range(0,self.side*self.side):
        #    if(i%self.side==0):
        #        print()
        #    else:
        #        print(self.states[i],end=" ")
        
        #values
        for i in range(0,self.side*self.side): 
            if(i%self.side==0):
                print("")
            print(np.round(self.stateValues[i],2),end=" ")
        print()       

        #policy
        for a in self.policy:
            if(count%self.side==0):
                print()
            print(self.actions_repr[int(a)], end="")
            count+=1

        print()
        for i in range(0,self.side*self.side):
            if(i%self.side==0):
                print("")
            if(i == currentState):
                print("O",end="")
            elif(i in self.terminals_food):
                print("F",end="")   
            elif(i in self.terminals_body):
                print("S",end="")  
            else:
                print("•",end="")
        print()

    def reset(self):
        self.policy = np.array([np.random.choice(self.actions) for s in self.states])
        self.stateValues = np.zeros(self.side*self.side)

    def updatePolicy(self,s):
        #print("POLICY UPDATE")
        bestAction=0
        max = sys.float_info.min
        for a in self.actions:
        #    for i in range(0,self.side*self.side):
        #            if(i%self.side==0):
        #                print()
        #            print(self.states[i],end=" ")
                    
            #print()
            #print("STATE="+str(s))
            #print("ACTION="+self.actions_repr[a])
            next = self.nextState(s,a)
            #print("NEXT STATE="+str(next))
            #print()
            value = self.stateValues[next]
            #print(a)
            #print(next)
            #print(value)
            if(value > max):
                max = value
                bestAction = a
                #print("Best"+str(bestAction))
        #print("Best"+str(bestAction))
        #print("##")
        return bestAction

    def updateValue(self,s): #update state value function
            a = self.policy[s]
            next = self.nextState(s,a)
            #print(self.reward(next))
            #print(self.gamma)
            #print(self.stateValues[next])
            return self.reward(s)+self.gamma*self.stateValues[next]

    def train(self):
        newStateValues = np.zeros(self.side*self.side) #stateValuefunction
        improve=True
        iters=0
        
        while(improve and self.maxIter>0):
        #while(improve):
        #while(maxIter>0):
            ##evaluate policy, calc state action values
            for s in self.states:
                newStateValues[s]= self.updateValue(s)
       
            self.stateValues=newStateValues
            ##update policy
            newPolicy = np.zeros(self.side*self.side)
            for s in self.states:
                newPolicy[s]= self.updatePolicy(s)

            if(np.all(np.array_equal(newPolicy,self.policy))):
                improve=False
            self.policy = newPolicy

            #self.print_policy()
            #print("**")
            self.maxIter-=1
            iters+=1
        return iters

        
    def nextState(self,s,a):
        if(a==self.UP):
            if(s in self.upSide): #first row
                return s + (self.side*(self.side-1))             
            return s-self.side
               
        elif(a==self.DOWN):
            if(s in self.downSide):            
                return s - (self.side*(self.side-1)) 
            return s+self.side
            
        elif(a==self.LEFT):         
            if(s in self.leftSide): 
              return s + self.side-1 
            return s-1
               
        elif(a==self.RIGHT):
            if(s in self.rightSide):
              return s -self.side+1
            return s+1


    def reward(self,s):
        #print("checkReward")
        #print(s)
        #print(self.terminals_food)
        #print(self.terminals_body)
        if(s in self.terminals_food):
            #print("FOOD")
            #return +5.0
            return self.foodReward 
        elif(s in self.terminals_body):
            #print("BODY")
            return self.bodyReward
        else:
            return self.aliveReward

########################################

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))

print(path)
print(filename)

print("\nCOMMANDS:")
print(" W,A,S,D or KEYPAD ARROWS to move")
print(" KEYPAD +,- or p,m to change speed")
print(" R for SmallBrain MDP\n")
print(" Y for BigBrain MDP\n")

FONTSIZE = 15
myfont = pygame.font.SysFont('Comic Sans MS', FONTSIZE)
gameoverfont = pygame.font.SysFont('Comic Sans MS', FONTSIZE * 2)
# pygame.font.Font.set_bold(True)

#screenX = 600  #need square for ez Rl to work 
#screenY = 600
screenX = 400  #need square for ez Rl to work 
screenY = 400
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

#/Users/ale/Desktop/pySnake/pySnakeResources/pythonlogob.jpg
print(path + resources +"pythonlogob.jpg")
player = pygame.transform.scale(
    pygame.image.load(path + resources +"pythonlogob.jpg"),
    (playerSizeX + playerSizeX // 4,
     playerSizeY + playerSizeY // 4))

bodyPart = pygame.transform.scale(
    pygame.image.load(path + resources +"pythonlogobody.jpg"),
    (playerSizeX,
     playerSizeY))

mela = pygame.transform.scale(
    pygame.image.load(path + resources + "mela.png"),
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

MAX_FOOD = 10
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

rl_active=False
dumbWin = False
bigBrain = 0


while(playAgain):

    while(not gameover):
        screen.fill(0)

        scoreText = myfont.render(
            "Score : " + str(score), False, (255, 255, 255))
        speedText = myfont.render(
            "Speed : " + str((MOVETIME_MAX - MOVETIME) // MOVEINCREMENT), False, (255, 255, 255))

        spawnedFood=False
        if(len(foodList) < MAX_FOOD):
            while(not spawnedFood):

                newFood = (random.randint(0, (screenX // PLAYER_SIZE) - 1) * PLAYER_SIZE, random.randint(0, (screenX // PLAYER_SIZE) - 1) * PLAYER_SIZE)
                spawnedFood=True
                for body in bodyList:
                    #print(f"food({newFood[0]},{newFood[1]}) == player({body[0]},{body[1]})")
                    if(newFood == body):
                        spawnedFood=False
            foodList.append(newFood)
                    

        
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


                if(event.key == pygame.K_r): #Reinforcement learning auto
                    rl_active = not rl_active
                    print("**BIG BRAIN="+str(rl_active)+"**")
                
                if(event.key == pygame.K_y): #Reinforcement learning auto dumb win
                    rl_active = True
                    dumbWin= not dumbWin
                    print("**DUMB WIN="+str(rl_active)+"**")
                   
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
                ######RL 
                if(rl_active):
                    if(dumbWin and len(bodyList) > screenX//PLAYER_SIZE):
                        Rl.foodReward=Rl.aliveReward
                        Rl.maxIter=1
                    else:
                        Rl.gamma = 0.8 #discount factor
                        Rl.foodReward = +10
                        Rl.bodyReward = -100
                        Rl.aliveReward = +1
                        Rl.maxIter=100



                    side= screenX//PLAYER_SIZE
                    food = [(y//PLAYER_SIZE * side + x//PLAYER_SIZE) for (x,y) in foodList]
                    body = [(y//PLAYER_SIZE * side + x//PLAYER_SIZE) for (x,y) in bodyList] 
                    bigBrain = Rl(side,food,body)
                    #bigBrain.print_debug()
                    action = bigBrain.getAction((playerPosY//PLAYER_SIZE * side + playerPosX//PLAYER_SIZE))
                    print("ACTION = " +bigBrain.actions_repr[int(action)])
                    
                    #directions are fuked
                    if(action == bigBrain.UP):
                        playerDirectionY = -PLAYER_SPEED
                        playerDirectionX = 0

                    if(action == bigBrain.DOWN):
                        playerDirectionY = PLAYER_SPEED
                        playerDirectionX = 0

                    if(action == bigBrain.LEFT):
                        playerDirectionY = 0
                        playerDirectionX = -PLAYER_SPEED

                    if(action == bigBrain.RIGHT):
                        playerDirectionY = 0
                        playerDirectionX = PLAYER_SPEED


                #######
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
        highScoreFileReader = open(path +  resources +"highscore.txt", "r+")
        shighscore = highScoreFileReader.read().strip().replace(
            "\n", "").replace(
            "\t", "").replace(
            "\r", "")
        highScoreFileReader.close()
        highscore = int(shighscore)
    except BaseException:
        highScoreFileWriter = open(path + resources +"highscore.txt", "w+")
        highscore = 0
        highScoreFileWriter.write("0")
        highScoreFileWriter.close()

    if(score > highscore):
        highScoreFileWriter = open(path + resources+"highscore.txt", "w")
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
        ##RL
        Rl.gamma = 0.8 #discount factor
        Rl.foodReward = +10
        Rl.bodyReward = -100
        Rl.aliveReward = +1
        Rl.maxIter=100
        print("NEW GAME STARTED ...")
