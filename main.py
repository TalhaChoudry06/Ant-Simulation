import pygame
from env.Grid import Grid
from env.Ant import Ant
from env.PheromoneMap import PheromoneMap

# initializing imported module
pygame.init()

# displaying a window of height
# 500 and width 400
screen = pygame.display.set_mode((500, 500))

# Setting name for window
pygame.display.set_caption('GeeksforGeeks')

# creating a bool value which checks 
# if game is running and starts clock
running = True
clock = pygame.time.Clock()
fps = 10

# set up pheromone map
pheromone_map = PheromoneMap(rows=50, cols=50, cell_size=10)

# set up grid and ants
grid = Grid(rows=50, cols=50, cell_size=10)
ants = [
    Ant(pheromone_map=pheromone_map, row=20, col=3),
    Ant(pheromone_map=pheromone_map, row=7, col=7),
    Ant(pheromone_map=pheromone_map, row=0, col=0)
]

# place food 
grid.place_food(3, 5)
grid.place_food(4, 6)
grid.place_food(2, 8)


# Game loop
# keep game running till running is true
while running:

    # Clear screen
    screen.fill((0, 0, 0))

    # Check for event if user has pushed 
    # any event in queue
    for event in pygame.event.get():
      


        # if event is of type quit then set
        # running bool to false
        if event.type == pygame.QUIT:
            running = False
    
    # Draw and update Grid and ants to buffer
    grid.draw(screen)
    for ant in ants:
        ant.update(grid)
        ant.vision(grid, screen, grid.cell_size, grid.offset_x, grid.offset_y, draw=True)
        ant.draw(screen, grid.cell_size)

    # update and decay pheromone map
    pheromone_map.decay(0.1)
    pheromone_map.draw(screen)
    
    # Update entire screen
    pygame.display.flip()
    clock.tick(fps)