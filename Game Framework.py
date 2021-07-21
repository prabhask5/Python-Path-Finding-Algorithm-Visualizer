import pygame, sys, math, random, time
from pygame.locals import *
from AStarPathfinder import astar
from GeneticPopulation import GeneticPopulation

pygame.init()
width = 1000
height = 600
myWindow = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Ultimate Pathfinder")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACK = (255, 255, 204)
MOVESPEED = 10

myWindow.fill(WHITE)
PIXSIZE = 5
BUTTONSIZE = 50
PLAYERSIZE = 30
#PIXES = pygame.PixelArray(myWindow)
obsts = []

clock = pygame.time.Clock()

#BUTTONS
backRect = pygame.Rect(0, 0, 200, height)
pygame.draw.rect(myWindow, BACK, backRect)

playButton = pygame.Rect(20, 50, 160, 50)
pygame.draw.rect(myWindow, GREEN, playButton)

astarButton = pygame.Rect(20, 150, 160, 50)
pygame.draw.rect(myWindow, GREEN, astarButton)

setButton = pygame.Rect(20, 250, 160, 50)
pygame.draw.rect(myWindow, GREEN, setButton)

probButton = pygame.Rect(20, 350, 160, 50)
pygame.draw.rect(myWindow, GREEN, probButton)

player = pygame.Rect(200, 0, PLAYERSIZE, PLAYERSIZE)
pygame.draw.rect(myWindow, BLUE, player)

targ = pygame.Rect(width - PLAYERSIZE, height - PLAYERSIZE, PLAYERSIZE, PLAYERSIZE)
pygame.draw.rect(myWindow, GREEN, targ)

# startButton = pygame.Rect(20, 150, 160, 50)
# pygame.draw.rect(myWindow, RED, startButton)
# 
# endButton = pygame.Rect(20, 250, 160, 50)
# pygame.draw.rect(myWindow, BLUE, endButton)
# 
# drawButton = pygame.Rect(20, 350, 160, 50)
# pygame.draw.rect(myWindow, BLACK, drawButton)

#TEXT
basicFont = pygame.font.SysFont(None, 48)
text = basicFont.render("PLAY", True, BLACK, GREEN)
textRect = text.get_rect()
textRect.center = playButton.center
#print(myWindow.get_rect())
myWindow.blit(text, textRect)

text = basicFont.render("A*", True, BLACK, GREEN)
textRect = text.get_rect()
textRect.center = astarButton.center
#print(myWindow.get_rect())
myWindow.blit(text, textRect)

text = basicFont.render("G-SET", True, BLACK, GREEN)
textRect = text.get_rect()
textRect.center = setButton.center
#print(myWindow.get_rect())
myWindow.blit(text, textRect)

text = basicFont.render("G-PROB", True, BLACK, GREEN)
textRect = text.get_rect()
textRect.center = probButton.center
#print(myWindow.get_rect())
myWindow.blit(text, textRect)


def isIn(pos, rect):
    return pos[0] < rect.right and pos[0] > rect.left and pos[1] < rect.bottom and pos[1] > rect.top

moveLeft = False
moveRight = False
moveUp = False
moveDown = False

windRect = pygame.Rect(200, 0, width - 200, height)

mode = 'plan'
color = BLACK
last = -1
draw = False
plan = True
won = False
path = []
astarCounter = 0
while won == False:
    if plan:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and event.key == K_t:
                mode = "setTarget"
            elif event.type == KEYUP and event.key == K_o:
                mode = "plan"
            if mode == "plan":
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if not isIn(event.pos, backRect):
                        draw = True
                        obst = pygame.Rect(event.pos[0] - PIXSIZE/2, event.pos[1] - PIXSIZE/2, PIXSIZE, PIXSIZE)
                        if not player.colliderect(obst) and not targ.colliderect(obst):
                            obsts.append(obst)
                            pygame.draw.rect(myWindow, color, obst)
                if event.type == MOUSEMOTION and draw == True and event.pos[0] - PIXSIZE > 200:
                    #pygame.draw.line(myWindow, color, last, event.pos, PIXSIZE)
                    last = event.pos
                    obst = pygame.Rect(event.pos[0] - PIXSIZE/2, event.pos[1] - PIXSIZE/2, PIXSIZE, PIXSIZE)
                    obsts.append(obst)
                    pygame.draw.rect(myWindow, color, obst)
                if event.type == MOUSEBUTTONUP and event.button == 1 and draw == True:
                    draw = False
            elif mode == "setTarget":
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if not isIn(event.pos, backRect):
                        last = event.pos
                        pygame.draw.rect(myWindow, WHITE, targ)
                        targ = pygame.Rect(event.pos[0] - PLAYERSIZE/2, event.pos[1] - PLAYERSIZE/2, PLAYERSIZE, PLAYERSIZE)
                        pygame.draw.rect(myWindow, GREEN, targ)
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if isIn(event.pos, playButton):
                    startTime = time.time()
                    mode = 'PLAY'
                    plan = False
                    runStartTime = time.time()
                    print(mode)
                
                elif isIn(event.pos, astarButton):
                    startTime = time.time()
                    mode = 'A*'
                    plan = False
                    path = astar(player, targ, obsts, windRect, MOVESPEED)
                    runStartTime = time.time()
                    print(mode)
                    if path == -1:
                        print('Impossible!')
                        won = True
                elif isIn(event.pos, setButton):
                    startTime = time.time()
                    mode = 'G-SET'
                    plan = False
                    print(mode)
                    mode = 'G'
                    pop = GeneticPopulation(100, MOVESPEED, PLAYERSIZE, (player.left, player.top), windRect, targ, obsts)
                    genBeginTime = time.time()
                
                elif isIn(event.pos, probButton):
                    startTime = time.time()
                    mode = 'G-PROB'
                    plan = False
                    print(mode)
                    mode = 'G'
                    pop = GeneticPopulation(100, MOVESPEED, PLAYERSIZE, (player.left, player.top), windRect, targ, obsts, 'prob')
                    genBeginTime = time.time()
    elif mode == 'PLAY':
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = True
                    moveLeft = False
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True
                if event.key == K_UP or event.key == K_w:
                    moveUp = True
                    moveDown = False
                if event.key == K_SPACE:
                    slow = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False
                if event.key == K_SPACE:
                    slow = False
                    
        pygame.draw.rect(myWindow, WHITE, player)
        if moveLeft == True and player.left > 200:
            player.left -= MOVESPEED
        if moveRight == True and player.right < width:
            player.right += MOVESPEED
        if moveUp == True and player.top > 0:
            player.top -= MOVESPEED
        if moveDown == True and player.bottom < height:
            player.bottom += MOVESPEED
        
        collision = False
        for obst in obsts:
            if player.colliderect(obst):
                collision = True
                pygame.draw.rect(myWindow, color, obst)
        if collision:
            runStartTime = time.time()
            player.left = 200
            player.top = 0
        
        pygame.draw.rect(myWindow, BLUE, player)
        if player.colliderect(targ):
            won = True
            print("Run Time: " + str(time.time() - runStartTime))


    elif mode == 'A*':
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.draw.rect(myWindow, WHITE, player)
        player.center = path[astarCounter]
        astarCounter += 1
        pygame.draw.rect(myWindow, BLUE, player)
        if astarCounter == len(path):
            print("Run Time: " + str(time.time() - runStartTime))
            won = True
    
    elif mode == 'G':
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        
        for p in pop.players:
            if not p.dead and not p.reachedGoal:
                pygame.draw.rect(myWindow, WHITE, p.player)
            
        pop.update()
        for p in pop.players:
            if not p.dead and not p.reachedGoal:
                if p.isBest:
                    pygame.draw.rect(myWindow, RED, p.player)
                else:
                    pygame.draw.rect(myWindow, BLUE, p.player)
        

        if pop.allPlayersDead():
            genTime = time.time() - genBeginTime
            pop.naturalSelection()
            pop.mutateChildren()
            print("Gen: " + str(pop.gen) + " | Time: " + str(genTime))
            genBeginTime = time.time()

        
    pygame.display.update()
    clock.tick(550)
    #print(PIXES[0][0])

myStr = "Course Complete"
print(myStr)
print("Total Time: " + str(time.time() - startTime))
text = basicFont.render(myStr, True, WHITE, BLACK)
textRect = text.get_rect()
textRect.centerx = myWindow.get_rect().centerx
textRect.centery = myWindow.get_rect().centery
myWindow.blit(text, textRect)
pygame.display.update()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
            
    
    

        
    
    
    
    
    
    
    
    
    
