import pygame
from env.Food import Food

class PheromoneMap:
    def __init__(self, rows, cols, cell_size, offset=(0,0)):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.offset_x, self.offset_y = offset
        self.map = [[{} for _ in range(cols)] for _ in range(rows)]

    def draw(self, screen):
        # Define colors for pheromone types
        pheromone_colors = {
            "search": (0, 0, 255),    # Blue
            "return": (255, 0, 0),  # red
            "food": (0, 0, 255) # green
            # Add more types/colors here if needed
        }

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.map[row][col]
                # cell is a dict with pheromone_type -> level
                for pheromone_type, level in cell.items():
                    if level > 0.01:  # Skip very weak pheromones
                        alpha = min(int(level * 255), 150)  # Clamp alpha
                        base_color = pheromone_colors.get(pheromone_type, (255, 255, 255))  # Default white

                        color = (*base_color, alpha)  # Add alpha channel

                        s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                        s.fill(color)
                        x = col * self.cell_size + self.offset_x
                        y = row * self.cell_size + self.offset_y
                        screen.blit(s, (x, y))

    def deposit(self, row, col, amount, pheromone_type="search"):
        cell = self.map[row][col]
        if pheromone_type not in cell:
            cell[pheromone_type] = 0.0
        cell[pheromone_type] += amount
        
    def get_level(self, x, y):
        return
    
    def decay(self, decay_rate):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.map[row][col]
                for p_type in list(cell.keys()):
                    cell[p_type] *= (1 - decay_rate)

                    # Optionally clean up tiny values
                    if cell[p_type] < 0.01:
                        del cell[p_type]
