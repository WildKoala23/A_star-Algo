import pygame
from node import Node
from colors import *
import math
from time import sleep


WIDTH = 800
pygame.init()
screen = pygame.display.set_mode((WIDTH,WIDTH))
clock = pygame.time.Clock()


screen.fill((WHITE))

class Grid:
    def __init__(self, blocksize=40):
        self.listNodes = []
        self.columns = 0
        self.rows = 0    
        self.startNode = None
        self.endNode = None
        self.blocksize = blocksize

    def initGrid(self):
        global listNodes
        for x in range(0, WIDTH, self.blocksize):
            for y in range(0, WIDTH, self.blocksize):
                node = Node(x, y, self.blocksize, screen,0,0)
                if (node.y == 0 or node.y == WIDTH - self.blocksize) or (node.x == 0 or node.x == WIDTH - self.blocksize):
                    node.color = BLACK
                    node.border = True
                    node.walkable = False

                self.listNodes.append(node)

    def drawGrid(self):
        for node in self.listNodes:
            if node.color == GREY:
                node.draw()
            else:
                node.draw()

    def cleanGrid(self):
        self.startNode = None
        self.endNode = None
        counter = 0
        for node in self.listNodes:
            if node.border == False:
                node.cleanNode()  


    def findNode(self, x, y):
        for node in self.listNodes:
            if node.isNode(x, y):
                return node
        print("\n\nNothing found")
    def changeCell(self, pos, color):
        x = int(pos[0]/self.blocksize)
        y = int(pos[1]/self.blocksize)
        node = self.findNode(x, y)
        if node.border == False:
            node.color = color
            # If it's the start node
            if color == CYAN:
                if self.startNode:
                    old_start = self.findNode(int(self.startNode.x / self.blocksize), int(self.startNode.y / self.blocksize))
                    old_start.cleanNode()
                node.draw()
                self.startNode = node
                #print(f"Start node: {self.startNode.getCoords()}")
            # If it's the end node
            if color == ORANGE:
                if self.endNode:
                    old_end = self.findNode(int(self.endNode.x / self.blocksize), int(self.endNode.y / self.blocksize))
                    old_end.cleanNode()
                node.draw()
                self.endNode = node 
                #print(f"Start node: {self.endNode.getCoords()}")
            elif color == BLACK:
                node.draw()
                node.walkable = False

        else:
            pass
    
    def getNeighbours(self, node):
        neighbours = []
        x = int(node.x / self.blocksize)
        y = int(node.y / self.blocksize)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                neighbour = self.findNode(i, j)
                if neighbour.isNode(int(node.x / self.blocksize), int(node.y / self.blocksize)) == True:
                    continue
                else:
                    neighbours.append(neighbour)
        return neighbours
    
    # Get the distance between two node (Sebastian Lague method)
    def getDistance(self, nodeA, nodeB):
        dstX = abs(nodeA.x - nodeB.x)
        dstY = abs(nodeA.y - nodeB.y)

        if dstX > dstY:
            return 14*dstY + 10 * (dstX - dstY)    
        return 14*dstX + 10 * (dstY - dstX) 

    def createPath(self,startNode, endNode):
        path = []
        currentNode = endNode

        startNode.show()
        endNode.show()

        while currentNode is not startNode:
            path.append(currentNode)
            currentNode = currentNode.parent  
        print("Inside create path")
        path.reverse()
        endNode.color = ORANGE
        for node in path[:-1]:
            node.color = GREEN
        return path



def main():
    running = True
    grid = Grid(40)
    grid.initGrid()

    while running:
        grid.drawGrid()

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
                    print("Grid cleaned")
                if event.key == pygame.K_a:
                    grid.getNeighbours(grid.startNode)


        clock.tick(60)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
