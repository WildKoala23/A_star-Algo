from node import Node
from grid import Grid
from colors import *
import pygame
from time import sleep
import threading
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

class Finder:
    def __init__(self, grid, path=None, waypoints = None):
        self.openSet = []# List of explorable nodes
        self.closedSet = []# List of nodes explored already
        self.grid = grid
        self.path = path
        self.waypoints = waypoints

    def isTargetNode(self, nodeA, nodeB):
        if nodeA.x == nodeB.x and nodeA.y == nodeB.y:
            return True
        return False

    def showPath(self):
        for node in self.path:
            print(f"{node.getCoords()} ->", end=" ")
        print("End")

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

    def drawLine(self, screen, startNode):
        norm_path = []
        norm_path.append((startNode.x + (int(startNode.blocksize / 2)), startNode.y + (int(startNode.blocksize / 2)) ))
        for node in self.path:
            cx = node.x + (int(node.blocksize / 2))
            cy = node.y + (int(node.blocksize / 2))
            norm_path.append((cx, cy))
        # pygame.draw.line(screen, WHITE, (cx_start, cy_start ), (cx_end, cy_end), 5)
        pygame.draw.lines(screen, WHITE, False, norm_path, 5)

        pygame.display.flip()

    def getWaypoints(self):
        waypoints = []
        # for node in self.path:
        #     waypoint = {"x": node.x, "y": node.y}
        #     waypoints.append(waypoint)
        for node in self.path:
            waypoints.append((node.x, node.y))
        return waypoints

    def findPath(self, animate=False):
        while self.openSet:
            #print(f"OPEN SET = [{len(openSet)}]")
            currentNode = self.getLowerCostNode(self.openSet) #Node with lowest fCost
            # currentNode.show()
            self.openSet.remove(currentNode)
            self.closedSet.append(currentNode)

            if self.isTargetNode(currentNode, self.grid.endNode):
                self.path = self.grid.createPath(self.grid.startNode, self.grid.endNode)
                self.waypoints =self.getWaypoints()
                self.showPath()
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
                if animate:
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
                        linePath = False
                        print("Grid cleaned")
                    if event.key == pygame.K_a:
                        finder.grid.getNeighbours(grid.startNode)
                    if event.key == pygame.K_q:
                        finder.openSet.append(grid.startNode)
                        # print("\nSTART NODE")
                        # print(grid.startNode.show())
                        # print("\nEND NODE")
                        # print(grid.endNode.show())
                        t1 = threading.Thread(target=finder.findPath, args=(True,), daemon=True)
                        t1.start()
                        foundPath = True
        else:
            if finder.path:
                finder.drawLine(screen, finder.grid.startNode)
                linePath = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        finder.reset()
                        print("Grid cleaned")
                        foundPath = False
                        linePath = False

        clock.tick(60)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
