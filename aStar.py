from node import Node
from grid import Grid
from colors import *
import pygame
from time import sleep
import threading

WIDTH = 800
pygame.init()
screen = pygame.display.set_mode((WIDTH,WIDTH))
clock = pygame.time.Clock()
screen.fill((WHITE))
grid = Grid(40)



running = True
grid.initGrid()
openSet = [] # List of explorable nodes
closedSet = [] # List of nodes explored allready
findingPath = True
foundPath = False


def isTargetNode(nodeA, nodeB):
    if nodeA.x == nodeB.x and nodeA.y == nodeB.y:
        return True
    return False

def getLowerCostNode(list):
    current = list[0]
    for node in list[1: ]:
        if node.fCost() < current.fCost() or node.fCost == current.fCost and node.hCost < current.hCost:
            current = node
    return current



def findPath(findingPath, openSet, closedSet, targetNode):
    while openSet:
        print(f"OPEN SET = [{len(openSet)}]")
        currentNode = getLowerCostNode(openSet) #Node with lowest fCost
        # currentNode.show()
        openSet.remove(currentNode)
        closedSet.append(currentNode)

        if isTargetNode(currentNode, targetNode):
            grid.createPath(grid.startNode, targetNode)
            print("GREAT SUCCESS")
            return
        
        neighbours = grid.getNeighbours(currentNode)

        for neighbour in neighbours:
            if not neighbour.walkable or neighbour in closedSet:
                continue
                
            newDstToNeighbour = currentNode.gCost +  grid.getDistance(currentNode, neighbour)
            if newDstToNeighbour < neighbour.gCost or neighbour not in openSet:
                neighbour.gCost = newDstToNeighbour
                neighbour.hCost = grid.getDistance(neighbour, targetNode)
                neighbour.parent = currentNode
                if neighbour not in openSet:
                    openSet.append(neighbour)
            neighbour.color = RED
            sleep(0.01)
    print("PATH NOT FOUND")
    return
            


while running:
    grid.drawGrid()
    if not foundPath:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    grid.changeCell(pos, CYAN)
                elif event.button == 2:
                    grid.changeCell(pos, BLACK)
                elif event.button == 3:
                    grid.changeCell(pos, ORANGE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.cleanGrid()
                    openSet.clear()
                    closedSet.clear()
                    print("Grid cleaned")
                if event.key == pygame.K_a:
                    grid.getNeighbours(grid.startNode)
                if event.key == pygame.K_q:
                    openSet.append(grid.startNode)
                    # print("\nSTART NODE")
                    # print(grid.startNode.show())
                    # print("\nEND NODE")
                    # print(grid.endNode.show())
                    t1 = threading.Thread(target=findPath, args=(findingPath, openSet, closedSet, grid.endNode), daemon=True)
                    t1.start()
                    foundPath = True
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.cleanGrid()
                    openSet.clear()
                    closedSet.clear()
                    print("Grid cleaned")
                    foundPath = False

    clock.tick(60)

    pygame.display.update()

pygame.quit()
