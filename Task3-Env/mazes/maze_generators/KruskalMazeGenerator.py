"""
Maze generator based on depth first search algorithm
"""
import sys
from collections import deque
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
        mat = []
        for row in range(self.num_rows):
            colMat = []
            for col in range(self.num_cols):
                components[self.maze_kruskal.find(
                    (row, col))].append((row, col))
                key = self.maze_kruskal.find((row, col))
                keyComp.insert(n, n)
                n += 1
                colMat.append(1)
            mat.append(colMat)

        # Generate init and finish character position
        initPosition = components[key][random.randint(
            0, len(components[key])-1)]
        endPosition = initPosition
        while endPosition == initPosition:
            endPosition = components[key][random.randint(
                0, len(components[key])-1)]

        stateInit = initPosition[0] * self.num_cols + initPosition[1]

        # Generate shortes path in the puzzle:
        D = self.findShortestPathLength(mat, initPosition, endPosition)
        if D[3] != -1:
            print("The shortest path from source to destination has length", D[3])
        else:
            print("Destination cannot be reached from source")
        # self.findShortestPathLength(mat,initPosition,endPosition)

        print('robotPositions', initPosition, endPosition, stateInit)
        # print('init state = ', stateDic[0]*self.num_cols + stateDic[1])
        dic1 = dict(zip([0, 1, 2, 3], [None]*4))
        dic2 = dict(zip(keyComp, [dic1]*(self.num_rows*self.num_cols)))
        # pos.append((1, 2, 0.0, False),(1, 2, 0.0, False),(1, 2, 0.0, False))

    def isValid(self, mat, visited, row, col, i, j):
        initState = i*self.num_rows + j
        endState = row*self.num_rows + col
        return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0])) and not visited[row][col] and (((endState, initState) not in self.walls) and ((initState, endState) not in self.walls)) and initState >= 0 and initState < self.num_cols*self.num_rows and endState >= 0 and endState < self.num_cols*self.num_rows

    def findShortestPathLength(self, mat, src, dest):
        # obtener celda fuente (i, j)
        row = [-1, 0, 0, 1]
        col = [0, -1, 1, 0]
        i, j = src
        # obtener celda de destino (x, y)
        x, y = dest
        # Caso base: entrada no válida
        if not mat or len(mat) == 0 or mat[i][j] == 0 or mat[x][y] == 0:
            return -1
        # Matriz `M × N`
        (M, N) = (len(mat), len(mat[0]))
        # construye una matriz para realizar un seguimiento de las celdas visitadas
        visited = [[False for x in range(N)] for y in range(M)]
        # crea una queue vacía
        q = deque()
        # marcar la celda de origen como visitada y poner en queue el nodo de origen
        visited[i][j] = True
        # (i, j, dist) representa las coordenadas de las celdas de la matriz y sus
        # distancia mínima de la fuente
        q.append((i, j, 0))
        # almacena la longitud de la ruta más larga desde el origen hasta el destino
        min_dist = sys.maxsize
        # Bucle # hasta que la queue esté vacía
        pasage = []
        nodePassages = []
        pasage.append((i, j, 0))
        parentsDic = {}
        parentPairs = []
        
        while q:
            # quitar la queue del nodo frontal y procesarlo
            (i, j, dist) = q.popleft()
            # (i, j) representa una celda actual, y `dist` almacena su
            # distancia mínima de la fuente
            # si se encuentra el destino, actualice `min_dist` y pare

            if i == x and j == y:
                min_dist = dist
                break
            # verifica los cuatro movimientos posibles desde la celda actual
            # y poner en queue cada movimiento válido
            for k in range(4):
                # comprobar si es posible ir a la posición
                # (i + row[k], j + col[k]) desde la posición actual
                condition = self.isValid(
                    mat, visited, i + row[k], j + col[k], i, j)
                if condition:
                    endState = (i + row[k])*self.num_rows + (j + col[k])
                    initState = i*self.num_rows + j
                    parentPairs.append((initState, endState))
                    # marca la siguiente celda como visitada y la pone en queue
                    visited[i + row[k]][j + col[k]] = True
                    q.append((i + row[k], j + col[k], dist + 1))
                    newDist = dist + 1
                    pasage.append((i + row[k], j + col[k]))
                    nodePassages.append(
                        ((i, j), (i + row[k], j + col[k], dist + 1)))

        for i in range(self.num_cols*self.num_rows):
            parentsDic[i] = []
            
        for l in range(len(parentPairs)):
            parentsDic[parentPairs[l][1]].append(parentPairs[l][0])
            
        actualNode = dest[0]*self.num_rows + dest[1]
        endNode = src[0]*self.num_rows + src[1]
        path = []
        path.append(endNode)
        while parentsDic[actualNode][0] != endNode:
            path.append(actualNode)
            actualNode = parentsDic[actualNode][0]
        path.append(actualNode)
        # Generate aleatory holes
        randomBombsStates = []
        while len(randomBombsStates) != self.num_cols:
            aleatoryState = random.randint(0, self.num_cols*self.num_rows)
            if (aleatoryState) not in path and (aleatoryState) not in randomBombsStates:
                randomBombsStates.append(aleatoryState)
        D = [
            randomBombsStates,
            dest[0]*self.num_rows + dest[1],
            endNode,
            min_dist,
            path
        ]
        if min_dist != sys.maxsize:
            return D
        else:
            return -1
