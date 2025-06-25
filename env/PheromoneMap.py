import pygame
from env.Food import Food

class PheromoneMap:
    def __init__(self, rows, cols, cell_size, offset=(0,0)):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.offset_x, self.offset_y = offset
        self.map = [[0.0 for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                level = self.map[row][col]
                if level > 0.01:  # Skip very weak pheromones
                    alpha = min(int(level * 255), 150)  # Clamp to avoid full opacity
                    color = (0, 0, 255, alpha)  # Blue with transparency

                    s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    s.fill(color)
                    x = col * self.cell_size + self.offset_x
                    y = row * self.cell_size + self.offset_y
                    screen.blit(s, (x, y))

    def deposit(self, row, col, amount):
        self.map[row][col] += amount
    
    def get_level(self, x, y):
        return
    
    def decay(self, decay_rate):
        for row in range(self.rows):
            for col in range(self.cols):
                self.map[row][col] *= (1 - decay_rate)
