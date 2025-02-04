import pygame
from colors import *

class Node:
    def __init__(self, x, y, blocksize, screen, gCost, hCost, border = False,  color=GREY, walkable=True, parent=None):
        self.x = x
        self.y = y
        self.color = color
        self.blocksize = blocksize
        self.screen = screen
        self.border = border
        self.gCost = gCost
        self.hCost = hCost
        self.walkable = walkable
        self.parent = parent

    def resetValues(self):
        self.gCost = 0
        self.hCost = 0
        self.walkable = True
        self.parent = None


    def draw(self):
            rect = pygame.Rect(self.x, self.y, self.blocksize, self.blocksize)
            pygame.draw.rect(self.screen, self.color, rect, 0)
            rect = pygame.Rect(self.x, self.y, self.blocksize, self.blocksize)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

    def show(self):
        print(f"Coords: [{int(self.x / self.blocksize), int(self.y / self.blocksize)}]")
        print(f"Color: [{self.color}]")
        if self.parent:
            print(f"Parent: [{self.parent.x, self.parent.y}]")

    def isNode(self, x, y):
        if x == int(self.x / self.blocksize) and y == int(self.y / self.blocksize):
              return True
        return False

    def fCost(self):
         return self.gCost + self.hCost
    
    def cleanNode(self):
            self.color = WHITE 
            self.draw()    
            self.color = GREY 
            self.draw()  
            self.resetValues()

    def getCoords(self):
        return (int(self.x / self.blocksize), int(self.y / self.blocksize))