import pygame
from time import sleep
from aStar import Finder
from grid import Grid
from colors import *
import threading
import math
import numpy as np

grid = Grid()
finder = Finder(grid)

WIDTH = 800
pygame.init()
screen = pygame.display.set_mode((WIDTH,WIDTH))
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

running = True
grid.initGrid()
foundPath = False

while running:
    screen.fill((WHITE))
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
                    finder.grid.changeCell(pos, BLACK)
                if event.key == pygame.K_q:
                    finder.openSet.append(grid.startNode)
                    t1 = threading.Thread(target=finder.findPath, args=(True,), daemon=True)
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
