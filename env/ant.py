import random
import pygame
from env.EntityLayer import EntityLayer
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
        
    def draw(self, screen, cell_size):
        yellow = (255, 255, 0)
        x = self.col * cell_size
        y = self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, yellow, rect)

    def move(self, dr, dc, grid):
        new_row = self.row + dr
        new_col = self.col + dc

        # Check boundaries
        if 0 <= new_row < grid.rows and 0 <= new_col < grid.cols:
            # Remove from old position in entity layer
            grid.entity_layer.remove(self, self.row, self.col)

            # Update internal position
            self.row = new_row
            self.col = new_col

            # Add to new position in entity layer
            grid.entity_layer.add(self.row, self.col, self)

    def vision(self, grid, screen=None, cell_size=0, offset_x=0, offset_y=0, draw=False):
        visible_cells = []

        for r in range(self.row - self.vision_radius, self.row + self.vision_radius + 1):
            for c in range(self.col - self.vision_radius, self.col + self.vision_radius + 1):
                # Skip out-of-bound cells
                if r < 0 or c < 0 or r >= grid.rows or c >= grid.cols:
                    continue

                visible_cells.append((r, c))

                # draw vision cells
                if not draw and screen and cell_size > 0:
                    s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    s.fill((0, 255, 0, 50))  # translucent green
                    screen.blit(s, (c * cell_size + offset_x, r * cell_size + offset_y))

        return visible_cells

    def perception(self, grid, screen=None, cell_size=0, offset_x=0, offset_y=0, draw=False):
        observation_vector = []

        for r in range(self.row - self.vision_radius, self.row + self.vision_radius + 1):
            for c in range(self.col - self.vision_radius, self.col + self.vision_radius + 1):
                if r < 0 or c < 0 or r >= grid.rows or c >= grid.cols:
                    continue
                
                # pheormone data
                cell = self.pheromone_map.map[r][c]
                search_level = cell.get("search", 0.0)
                return_level = cell.get("return", 0.0)
                food_smell_level = cell.get("food_smell", 0.0)

                ant_present = 0
                ant_carrying_food = 0
                entities = grid.entity_layer.get(r, c)
                
                for entity in entities:
                    if isinstance(entity, Ant) and entity is not self:
                        ant_present += 1
                        if entity.carrying_food:
                            ant_carrying_food += 1

                observation_vector.extend([search_level, return_level, food_smell_level, ant_present, ant_carrying_food])
                # Print line by line
                # print(f"Cell ({r}, {c}): search={search_level:.3f}, return={return_level:.3f}, food_smell={food_smell_level:.3f}, ants_present={ant_present}")

        return observation_vector
