"""
Maze generator based on depth first search algorithm
"""
from typing import List, Any, Tuple, Set

import random

from .MazeGenerator import MazeGenerator


class KruskalMazeGenerator(MazeGenerator):
    def __init__(
        self,
        num_rows: int,
        num_cols: int,
        neighborhood: List[Tuple[int, int]] = [(0, -1), (1, 0), (0, 1), (-1, 0)],
    ) -> None:
        super().__init__(num_rows, num_cols, neighborhood)

    def _init_walls(self) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                current_index = i * self.num_cols + j
                for offset_i, offset_j in self.neighborhood:
                    n_i, n_j = i + offset_i, j + offset_j

                    neighbor_index = n_i * self.num_cols + n_j
                    self.walls.add((current_index, neighbor_index))

    def generate(self, start: int = 0) -> Set[Tuple[int, int]]:
        self._init_walls()

        stack: List[int] = [start]
        visited: Set[int] = {start}
        arrayVisted=[]
        # print('unvis', self.walls)
        list_walls: List[int] = []
        
        # 1. Created a list of walls
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                current_index = i * self.num_cols + j
                list_walls.insert(current_index, current_index)

        # 1.1 Create a set for each cell, each containning just that one cell
        
        # 2 For each wall, in some random order:
        # randomCell =  random.randint(0, len(list_walls))
        # while randomCell in visited:
        #     randomCell =  random.randint(0, len(list_walls))
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                unvisited_neighbors: List[int] = []
                current_index = i * self.num_cols + j
                
                # Saber si tiene vecinos no visitados o con muros
                i, j = current_index // self.num_cols, current_index % self.num_cols

                for offset_i, offset_j in self.neighborhood:
                    n_i, n_j = i + offset_i, j + offset_j
                    if not ((0 <= n_i < self.num_rows) and (0 <= n_j < self.num_cols)):
                        continue
                    neighbor_index = n_i * self.num_cols + n_j
                    if neighbor_index not in visited:
                        unvisited_neighbors.append(neighbor_index)

                if len(unvisited_neighbors) == 0:
                    continue

                neighbor = random.choice(unvisited_neighbors)
                # Remove the wall
                if (current_index, neighbor) in self.walls:
                    self.walls.remove((current_index, neighbor))
                if (neighbor, current_index) in self.walls:
                    self.walls.remove((neighbor, current_index))

                visited.add(neighbor)
            # while len(list_walls)
            
        return self.walls
                # list_walls.insert(current_index, current_index)
        # 2.1 If the cells divided by this wall belong to distinct sets:
           


