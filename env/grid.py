import pygame

class Grid:
    def __init__(self, rows, cols, cell_size, offset=(0,0)):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.offset_x, self.offset_y = offset
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.cell_size + self.offset_x,
                    row * self.cell_size + self.offset_y,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # draw cell borders

    def update_cell(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = value

    def get_cell(self, x, y):
        col = (x - self.offset_x) // self.cell_size
        row = (y - self.offset_y) // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None
