import pygame, sys, math, random, time
from pygame.locals import *

def h(pos1, pos2):
    #Euclidean distance
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    #dijkstra
    #return 0
    #manhattan
    #return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def astar(player, targ, obsts, windRect, moveSpeed):
    width = player.right - player.left
    start = player.center
    end = targ.center
    print(end)
    openList = [start]
    
    cameFrom = {}
    gScore = {}
    fScore = {}
    gScore[start] = 0
    fScore[start] = gScore[start] + h(start, end)
    
    while len(openList) > 0:
        bestInd = 0
        for i in range(len(openList)):
            if fScore[openList[i]] < fScore[openList[bestInd]]:
                bestInd = i
        currentPos = openList[bestInd]
        openList.pop(bestInd)
        #print(currentPos)
        testRect = pygame.Rect(currentPos[0] - width/2, currentPos[1] - width/2, width, width)
        if testRect.colliderect(targ):
            current = currentPos
            path = [current]
            while current in list(cameFrom.keys()):
                current = cameFrom[current]
                path.append(current)
            return path[::-1]
        for direction in [(moveSpeed, 0), (-moveSpeed, 0), (0, moveSpeed), (0, -moveSpeed)]:
            newPos = (currentPos[0] + direction[0], currentPos[1] + direction[1])
            testRect = pygame.Rect(newPos[0] - width/2, newPos[1] - width/2, width, width)
            if not windRect.contains(testRect):
                continue
            collision = False
            for obst in obsts:
                if obst.colliderect(testRect):
                    collision = True
            if collision:
                continue
            
            possG = gScore[currentPos] + 10
            if newPos in list(gScore.keys()):
                if possG < gScore[newPos]:
                    cameFrom[newPos] = currentPos
                    gScore[newPos] = possG
                    fScore[newPos] = gScore[newPos] + h(newPos, end)
                else:
                    continue
            else:
                openList.append(newPos)
                cameFrom[newPos] = currentPos
                gScore[newPos] = possG
                fScore[newPos] = gScore[newPos] + h(newPos, end)
            
    return -1
   

def main():
    pygame.init()
    myWindow = pygame.display.set_mode((600, 600), 0, 32)
    pygame.display.set_caption("Track Drawer")
    
    clock = pygame.time.Clock()
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BACK = (255, 255, 204)

    player = pygame.Rect(0, 0, 20, 20)
    targ = pygame.Rect(600 - 20, 600 - 20, 20, 20)
    obsts = [pygame.Rect(300, 300, 100, 100), pygame.Rect(400, 500, 50, 150), pygame.Rect(500, 400, 150, 50)]
    
    path = astar(player, targ, obsts, myWindow)
    #print(path)
    

    for i in range(len(path)):
        myWindow.fill(WHITE)
        player.centerx = path[i][0]
        player.centery = path[i][1]
        pygame.draw.rect(myWindow, BLUE, player)
        pygame.draw.rect(myWindow, GREEN, targ)
        for obst in obsts:
            pygame.draw.rect(myWindow, RED, obst)
        pygame.display.update()
        clock.tick(100)


if __name__ == '__main__':
    main()