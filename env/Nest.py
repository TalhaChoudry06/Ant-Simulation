import pygame
from env.Food import Food

class Nest:
    def __init__(self, row, col, inventory=None):
        if inventory is None:
            inventory = []
        self.inventory = inventory
        self.row = row
        self.col = col
    
    def draw(self, screen, cell_size, offset_x=0, offset_y=0):
        red = (255, 0, 0)
        x = self.col * cell_size + offset_x
        y = self.row * cell_size + offset_y
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, red, rect)


    # add ant interaction
    def receive_ant(self, ant):
        return
    
    # deploys ant from nest 
    def deploy_ant(self, ant):
        return