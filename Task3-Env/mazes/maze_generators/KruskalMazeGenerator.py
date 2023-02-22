"""
Maze generator based on depth first search algorithm
"""
from typing import List, Tuple, Set
import random
from .MazeGenerator import MazeGenerator

GRAPH_SIZE = 5
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
                if (celZero*self.num_cols + celZeroAd, celOne*self.num_cols + celOneAd) in self.walls:
                    self.walls.remove(
                        (celZero*self.num_cols + celZeroAd, celOne*self.num_cols + celOneAd))
                elif (celOne*self.num_cols + celOneAd, celZero*self.num_cols + celZeroAd) in self.walls:
                    self.walls.remove(
                        (celOne*self.num_cols + celOneAd, celZero*self.num_cols + celZeroAd))
        self.maze = maze
        self.maze_kruskal = maze_kruskal
        return self.walls

    def generatePMaztrix(self):
        components = {}
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                components[self.maze_kruskal.find((row, col))] = []
        key = 0
        keyComp = []
        n = 0
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                components[self.maze_kruskal.find(
                    (row, col))].append((row, col))
                key = self.maze_kruskal.find((row, col))
                keyComp.insert(n, n)
                n += 1
        # Generate init and finish character position
        initPosition = components[key][random.randint(
            0, len(components[key])-1)]
        endPosition = initPosition
        while endPosition == initPosition:
            endPosition = components[key][random.randint(
                0, len(components[key])-1)]

        stateInit = initPosition[0] * self.num_cols + initPosition[1]
        stateFinal = endPosition[0] * self.num_cols + endPosition[1]
        print('robotPositions',initPosition, endPosition,stateInit, stateFinal)
        dic1 = dict(zip([0, 1, 2, 3], [None]*4))
        # print(dic1)
        dic2 = dict(zip(keyComp, [dic1]*(self.num_rows*self.num_cols)))
        # pos.append((1, 2, 0.0, False),(1, 2, 0.0, False),(1, 2, 0.0, False))
        i = 0
        for rows in range(self.num_rows): # 0 1
            for cols in range(self.num_cols):
                current_index = rows * self.num_cols + cols
                left_index = rows * self.num_cols + cols - 1
                down_index = (rows+1) * self.num_cols + cols
                right_index = rows * self.num_cols + cols + 1
                up_index = (rows-1) * self.num_cols + cols
                #print('actual', current_index, left_index, down_index, right_index, up_index)
                for action in range(4):
                    if(current_index == stateFinal):
                        dic1[action] = (1, current_index, 0.0, True)
                        print('here')
                    # else:
                    #     print('')
                    #     if (action == 0):  # movimiento en izq
                    #         dic1[action] = (1, actual, 0.0, False), (1, 2, 0.0, False), (1, 2, 0.0, False)
                    #     if (action == 1):  # movimiento en abajo
                    #         dic1[action] = (1, actual, 0.0, False), (1, 2, 0.0, False), (1, 2, 0.0, False)
                    #     if (action == 2):  # movimiento en der
                    #         dic1[action] = (1, actual, 0.0, False), (1, 2, 0.0, False), (1, 2, 0.0, False)
                    #     if (action == 0):  # movimiento en arriba
                    #         dic1[action] = (1, actual, 0.0, False), (1, 2, 0.0, False), (1, 2, 0.0, False)
        print(dic2)