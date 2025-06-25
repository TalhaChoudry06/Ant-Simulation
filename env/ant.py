import random
import pygame
from env.PheromoneMap import PheromoneMap
class Ant():
    def __init__(self, pheromone_map, row, col, vision_radius=3, draw=False):
        self.pheromone_map = pheromone_map
        self.row = row
        self.col = col
        self.vision_radius = vision_radius
        self.is_stopped = False

    def move(self, grid_row, grid_col):
        if self.is_stopped:
            return
        
        # random directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        dr, dc = random.choice(directions)
        new_row = self.row + dr
        new_col = self.col + dc

        # Check boundaries
        if 0 <= new_row < grid_row and 0 <= new_col < grid_col:
            self.row = new_row
            self.col = new_col
        # else: do nothing (ant stays in place)

    def draw(self, screen, cell_size):
        yellow = (255, 255, 0)
        x = self.col * cell_size
        y = self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, yellow, rect)

    def vision(self, grid, screen=None, cell_size=0, offset_x=0, offset_y=0, draw=False):
        # Scan all cells in 1-block radius around ant (including diagonals)
        for r in range(self.row - 1, self.row + 2):
            for c in range(self.col - 1, self.col + 2):
                # Skip out-of-bound cells
                if r < 0 or c < 0 or r >= grid.rows or c >= grid.cols:
                    continue
                
                # If drawing is enabled, draw the vision cell
                if draw and screen and cell_size > 0:
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill((0, 255, 0, 50))  # translucent green
                    screen.blit(s, (c * cell_size + offset_x, r * cell_size + offset_y))

                # Check for food
                if (r, c) in grid.food_cells:
                    self.is_stopped = False
                    self.pheromone_map.deposit(self.row, self.col-1, .5)
                    return  # stop scanning once food is found
                
                # If you want to check enemies too, add similar logic here:
                # if (r, c) in grid.enemy_cells:
                #     do something

        # If no food found nearby, allow movement
        self.is_stopped = False

    def update(self, grid):
        self.vision(grid)       # Check surroundings first      
        self.move(grid.rows, grid.cols)  # Move if allowed
