import random
import pygame
from env.PheromoneMap import PheromoneMap
from behavior.AntState import SearchingState

class Ant():
    def __init__(self, pheromone_map, row, col, nest, vision_radius=3, draw=False):
        self.pheromone_map = pheromone_map
        self.row = row
        self.col = col
        self.nest = nest  
        self.vision_radius = vision_radius
        self.carrying_food = False
        self.state = SearchingState()  

    def set_state(self, new_state):
        self.state = new_state


    def update(self, grid):
        self.state.update(self, grid)

    def move(self, dr, dc, grid):        
        new_row = self.row + dr
        new_col = self.col + dc

        # Check boundaries
        if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:
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
        visible_cells = []

        for r in range(self.row - 1, self.row + 2):
            for c in range(self.col - 1, self.col + 2):
                # Skip out-of-bound cells
                if r < 0 or c < 0 or r >= grid.rows or c >= grid.cols:
                    continue

                visible_cells.append((r, c))

                # draw vision cells
                if draw and screen and cell_size > 0:
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill((0, 255, 0, 50))  # translucent green
                    screen.blit(s, (c * cell_size + offset_x, r * cell_size + offset_y))

        return visible_cells
