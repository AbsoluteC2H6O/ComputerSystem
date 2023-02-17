## Kruskal's Algorithm for Maze Generation
## Neil Thistlethwaite

# from PIL import Image
import random
import numpy as np
from typing import Tuple, Set

GRAPH_SIZE = 100

cels = [(i,j) for j in range(GRAPH_SIZE) for i in range(GRAPH_SIZE)]
neighbors = lambda n : [(n[0]+dx,n[1]+dy) for dx,dy in ((-1,0),(1,0),(0,-1),(0,1))
                       if n[0]+dx >= 0 and n[0]+dx < GRAPH_SIZE and n[1]+dy >= 0 and n[1]+dy < GRAPH_SIZE]
## Somewhat naive implementation, as it doesn't do rank balancing,
## but this could easily be replaced with something more efficient.
class KruskalMazeGenerator:
    def __init__(self, cels):
        self.cel_map = {}
        for i,val in enumerate(cels):
            n = self.NodeGraph(val, i)
            self.cel_map[val] = n

    def find(self, cel):
        return self.find_cel(cel).cel

    def find_cel(self, cel):
        if type(self.cel_map[cel].cel) is int:
            return self.cel_map[cel]
        else:
            parent_cel = self.find_cel(self.cel_map[cel].cel.val)
            self.cel_map[cel].cel = parent_cel
            return parent_cel

    def union(self, node1, node2):
        cel1 = self.find_cel(node1)
        cel2 = self.find_cel(node2)
        if cel1.cel != cel2.cel:
            cel1.cel = cel2

    class NodeGraph:
        def __init__(self, val, cel):
            self.val = val
            self.cel = cel

## Kruskal's Algorithm
walls = [(cel, nbor) for cel in cels for nbor in neighbors(cel)]
maze: Set[Tuple[int, int]] = set()
maze_kruskal = KruskalMazeGenerator(cels)
while len(maze) < len(cels)-1:
    wall = walls.pop(random.randint(0, len(walls)-1))
    if maze_kruskal.find(wall[0]) != maze_kruskal.find(wall[1]):
        maze_kruskal.union(wall[0], wall[1])
        maze.add((wall[0][0],wall[0][1]))
        maze.add((wall[1][0],wall[1][1]))

def graph():
    return maze
# print(maze)