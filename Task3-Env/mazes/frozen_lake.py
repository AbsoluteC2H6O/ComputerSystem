"""
Frozen Lake environment as a maze
"""
import maze_generators
import kruskal2
from colorama import init
from colorama import Fore, Back, Style
height = 11
width = 27
class FrozenLake:
    def __init__(self, **kwargs):
        self._rows = kwargs.get("rows", 4)
        self._cols = kwargs.get("cols", 4)
        maze_generator = kwargs.get(
            "maze_generator_class", maze_generators.KruskalMazeGenerator
        )(self._rows, self._cols)
        self.walls = maze_generator.generate()
       
    # def printMaze(self):
    #     # Initialize colorama
    #     init()
    #     for i in range(0, height):
    #         for j in range(0, width):
    #             if (self.walls[i][j] == 'u'):
    #                 print(Fore.WHITE + str(self.walls[i][j]), end=" ")
    #             elif (self.walls[i][j] == ' '):
    #                 print(Fore.GREEN + str(self.walls[i][j]), end=" ")
    #             else:
    #                 print(Fore.RED + str(self.walls[i][j]), end=" ")
    #         print('\n')
            
    def render(self):
        # render the top wall
        # print('maze', self.walls)
        print("-" * int(self._cols * 2 + 1))

        for i in range(self._rows):
            for j in range(self._cols):
                # evaluate if there is a left wall
                current_index = i * self._cols + j
                left_index = i * self._cols + j - 1
                has_left_wall = (
                    j == 0
                    or (current_index, left_index) in self.walls
                    or (left_index, current_index) in self.walls
                )

                # render the left wall if exists
                if has_left_wall:
                    # every left cell has a left wall
                    print("|", end="")
                else:
                    # space if there is no a left wall
                    print(" ", end="")

                # render the cell
                print(" ", end="")

            # render the right wall for the current row
            print("|")

            # render the bottom wall when if exists
            for j in range(self._cols * 2 + 1):
                current_index = i * self._cols + j
                bottom_index = (i + 1) * self._cols + j
                has_bottom_wall = (
                    i == self._rows - 1
                    or j % 2 == 0
                    or (current_index, bottom_index) in self.walls
                    or (bottom_index, current_index) in self.walls
                )
                if has_bottom_wall:
                    print("-", end="")
                else:
                    # space if there is not a bottom wall
                    print(" ", end="")

            # finally, end of line
            print("")
