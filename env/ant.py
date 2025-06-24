import random
import pygame

class Ant():
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def move(self, grid_row, grid_col):
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
