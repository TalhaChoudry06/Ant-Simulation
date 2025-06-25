import pygame

class Food:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def draw(self, screen, cell_size, offset_x=0, offset_y=0):
        Green = (0, 255, 0)
        x = self.col * cell_size + offset_x
        y = self.row * cell_size + offset_y
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, Green, rect)
