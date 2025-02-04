from node import Node
from grid import Grid
from colors import *
import pygame
from time import sleep
import threading



class Finder:
    def __init__(self, grid):
        self.openSet = []# List of explorable nodes
        self.closedSet = []# List of nodes explored allready
        self.grid = grid

    def isTargetNode(self, nodeA, nodeB):
        if nodeA.x == nodeB.x and nodeA.y == nodeB.y:
            return True
        return False

    def getLowerCostNode(self, list):
        current = list[0]
        for node in list[1: ]:
            if node.fCost() < current.fCost() or node.fCost == current.fCost and node.hCost < current.hCost:
                current = node
        return current

    def reset(self):
        self.openSet.clear()
        self.closedSet.clear()
        self.grid.cleanGrid()

    def findPath(self):
        while self.openSet:
            #print(f"OPEN SET = [{len(openSet)}]")
            currentNode = self.getLowerCostNode(self.openSet) #Node with lowest fCost
            # currentNode.show()
            self.openSet.remove(currentNode)
            self.closedSet.append(currentNode)

            if self.isTargetNode(currentNode, self.grid.endNode):
                self.grid.createPath(self.grid.startNode, self.grid.endNode)
                print("GREAT SUCCESS")
                return
            
            neighbours = self.grid.getNeighbours(currentNode)

            for neighbour in neighbours:
                if not neighbour.walkable or neighbour in self.closedSet:
                    continue
                    
                newDstToNeighbour = currentNode.gCost +  self.grid.getDistance(currentNode, neighbour)
                if newDstToNeighbour < neighbour.gCost or neighbour not in self.openSet:
                    neighbour.gCost = newDstToNeighbour
                    neighbour.hCost = self.grid.getDistance(neighbour, self.grid.endNode)
                    neighbour.parent = currentNode
                    if neighbour not in self.openSet:
                        self.openSet.append(neighbour)
                neighbour.color = RED
                sleep(0.01)
        print("PATH NOT FOUND")
        return
            

def main():
    WIDTH = 800
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,WIDTH))
    clock = pygame.time.Clock()
    screen.fill((WHITE))
    grid = Grid(40)
    finder = Finder(grid)

    running = True
    grid.initGrid()
    findingPath = True
    foundPath = False
    while running:
        finder.grid.drawGrid()
        if not foundPath:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        finder.grid.changeCell(pos, CYAN)
                    elif event.button == 2:
                        finder.grid.changeCell(pos, BLACK)
                    elif event.button == 3:
                        finder.grid.changeCell(pos, ORANGE)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        finder.reset()
                        print("Grid cleaned")
                    if event.key == pygame.K_a:
                        finder.grid.getNeighbours(grid.startNode)
                    if event.key == pygame.K_q:
                        finder.openSet.append(grid.startNode)
                        # print("\nSTART NODE")
                        # print(grid.startNode.show())
                        # print("\nEND NODE")
                        # print(grid.endNode.show())
                        t1 = threading.Thread(target=finder.findPath, daemon=True)
                        t1.start()
                        foundPath = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        finder.reset()
                        print("Grid cleaned")
                        foundPath = False

        clock.tick(60)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
