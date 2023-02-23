"""
Frozen Lake environment as a maze
"""
import maze_generators
import pygame
class FrozenLake:
    def __init__(self, **kwargs):
        self._rows = kwargs.get("rows", 4)
        self._cols = kwargs.get("cols", 4)
        maze_generator = kwargs.get(
            "maze_generator_class", maze_generators.KruskalMazeGenerator
        )(self._rows, self._cols)
        self.walls = maze_generator.generate()
        self.P = maze_generator.generatePMatrix()
        
    def render(self):
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
                    print("|", end="")
                else:
                    # space if there is no a left wall
                    print(" ", end="")

                # render the cell
                print(' ', end="")

            # render the right wall for the current row
            print("|")

            # render the first bottom wall
            print("-", end="")

            # render the bottom wall when if exists
            for j in range(self._cols):
                current_index = i * self._cols + j
                bottom_index = (i + 1) * self._cols + j
                has_bottom_wall = (
                    i == self._rows - 1
                    or (current_index, bottom_index) in self.walls
                    or (bottom_index, current_index) in self.walls
                )
                if has_bottom_wall:
                   print("-", end="")
                else:
                    # space if there is not a bottom wall
                    print(" ", end="")
                
                # render the next bottom wall
                print("-", end="")

            # finally, end of line
            print("")
            
    def renderPygame(self):
        pygame.init()
        