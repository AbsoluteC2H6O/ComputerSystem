"""
Maze generator based on depth first search algorithm
"""
from typing import List, Tuple, Set
import random
from .MazeGenerator import MazeGenerator

GRAPH_SIZE = 10
cels = [(i, j) for j in range(GRAPH_SIZE) for i in range(GRAPH_SIZE)]


def neighbors(n): return [(n[0]+dx, n[1]+dy) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))
                          if n[0]+dx >= 0 and n[0]+dx < GRAPH_SIZE and n[1]+dy >= 0 and n[1]+dy < GRAPH_SIZE]


class Kruskal:
    def __init__(self, cels):
        self.cel_map = {}
        for i, val in enumerate(cels):
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


class KruskalMazeGenerator(MazeGenerator):
    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        neighborhood: List[Tuple[int, int]] = [
            (0, -1), (1, 0), (0, 1), (-1, 0)],
    ) -> None:
        super().__init__(num_rows, num_cols, neighborhood)

    def _init_walls(self) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                current_index = i * self.num_cols + j
                for offset_i, offset_j in self.neighborhood:
                    n_i, n_j = i + offset_i, j + offset_j

                    if not ((0 <= n_i < self.num_rows) and (0 <= n_j < self.num_cols)):
                        continue

                    neighbor_index = n_i * self.num_cols + n_j

                    if (current_index, neighbor_index) in self.walls or (
                        neighbor_index,
                        current_index,
                    ) in self.walls:
                        continue

                    self.walls.add((current_index, neighbor_index))

    def generate(self, start: int = 0) -> Set[Tuple[int, int]]:
        self._init_walls()
        walls = [(cel, nbor) for cel in cels for nbor in neighbors(cel)]
        maze = []
        maze_kruskal = Kruskal(cels)
        while len(maze) < len(cels)-1:
            wall = walls.pop(random.randint(0, len(walls)-1))
            if maze_kruskal.find(wall[0]) != maze_kruskal.find(wall[1]):
                celZero = wall[0][0]
                celZeroAd = wall[0][1]
                celOne = wall[1][0]
                celOneAd = wall[1][1]
                maze_kruskal.union(wall[0], wall[1])
                maze.append(wall)
                if (celZero*self.num_cols + celZeroAd,celOne*self.num_cols + celOneAd) in self.walls:
                    self.walls.remove((celZero*self.num_cols +celZeroAd,celOne*self.num_cols +celOneAd))
                elif (celOne*self.num_cols + celOneAd,celZero*self.num_cols + celZeroAd) in self.walls:
                    self.walls.remove((celOne*self.num_cols +celOneAd,celZero*self.num_cols +celZeroAd))
        self.maze = maze
        self.maze_kruskal = maze_kruskal
        return self.walls

    def generatePMaztrix(self):
        print('Generating P matrix')
        components = {}
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                components[self.maze_kruskal.find((row, col))] = []

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                components[self.maze_kruskal.find((row, col))].append((row, col))
        print(len(components))
        print('components', components)
        self.generateInitEndPositions(components)
        
    def generateInitEndPositions(self, components):
        initialPosition = components[random.randint(0, len(components)-1)]
        endPosition =components[random.randint(0, len(components)-1)]
        
        return {initialPosition, endPosition}