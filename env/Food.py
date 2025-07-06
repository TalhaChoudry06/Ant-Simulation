import pygame

class Food:
    def __init__(self, row, col, amount=5):
        self.row = row
        self.col = col
        self.amount = amount

    def take(self, amount=1):
        self.amount -= amount
        print("food -1")
        if self.amount <= 0:
            self.amount = 0  # Just to be safe
        return self.amount <= 0
    
    def emit_scent(self, pheromone_map):
        max_radius = 3
        base_amount = 1

        for dr in range(-max_radius, max_radius + 1):
            for dc in range(-max_radius, max_radius + 1):
                r = self.row + dr
                c = self.col + dc

                # Calculate distance from food
                dist = abs(dr) + abs(dc)  # Manhattan distance, or use Euclidean

                if dist <= max_radius:
                    # Decay scent amount based on distance (linear decay example)
                    amount = base_amount * (max_radius - dist) / max_radius

                    pheromone_map.deposit(r, c, amount, pheromone_type="food_smell")



    def draw(self, screen, cell_size, offset_x=0, offset_y=0):
        Green = (0, 255, 0)
        x = self.col * cell_size + offset_x
        y = self.row * cell_size + offset_y
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, Green, rect)
